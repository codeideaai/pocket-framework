#!/usr/bin/env python3
"""Build offline editions from the same chapter sources as the Quarto site."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote, unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
READER = "markdown+fenced_divs+auto_identifiers-raw_html-raw_tex-tex_math_dollars-citations"


SLUG = "pocket-framework"
REPOSITORY = "https://github.com/codeideaai/pocket-framework"
TITLES = {"en": "Pocket Framework", "zh": "从零写一个 Go Web 框架"}


def chapters(language):
    paths = sorted((ROOT / language).glob("[0-9][0-9]-*.qmd"))
    if [int(path.name[:2]) for path in paths] != list(range(14)):
        raise ValueError("Expected exactly one numbered chapter 00–13 in each edition")
    return paths


def source_text(path):
    raw = path.read_text(encoding="utf-8")
    frontmatter, body = raw.split("<!-- article-body -->", 1)
    title = next(line.removeprefix("title: ") for line in frontmatter.splitlines()
                 if line.startswith("title: "))
    return f"# {path.name[:2]} · {json.loads(title)}\n\n{body.strip()}\n"



def pandoc(*arguments, text=None, cwd=ROOT):
    return subprocess.run(
        ["pandoc", *arguments], input=text, text=True, encoding="utf-8",
        stdout=subprocess.PIPE, cwd=cwd, check=True,
    ).stdout


def nodes(value, kind):
    if isinstance(value, dict):
        if value.get("t") == kind:
            yield value["c"]
        for child in value.values():
            yield from nodes(child, kind)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child, kind)


def make_book(language, stage):
    paths = chapters(language)
    if not paths:
        raise ValueError(f"No chapter sources for {language}")
    combined = []
    all_headings = {}
    documents = {}
    chapter_ids = {path: f"chapter-{index:02d}" for index, path in enumerate(paths)}
    for path, prefix in chapter_ids.items():
        document = json.loads(pandoc("--from", READER, "--to", "json", text=source_text(path)))
        blocks = document["blocks"]
        if not blocks or blocks[0].get("t") != "Header" or blocks[0]["c"][0] != 1:
            raise ValueError(f"Expected a chapter title at the beginning of {path.relative_to(ROOT)}")
        headings = {}
        for index, (level, attrs, _) in enumerate(nodes(blocks, "Header")):
            original = attrs[0]
            attrs[0] = prefix if index == 0 else f"{prefix}-{original}"
            headings[original] = attrs[0]
        all_headings[path] = headings
        documents[path] = blocks

    for path, blocks in documents.items():
        for link in nodes(blocks, "Link"):
            address = urlsplit(link[2][0])
            if address.scheme or address.netloc:
                continue
            if not address.path:
                if address.fragment in all_headings[path]:
                    link[2][0] = "#" + all_headings[path][address.fragment]
                continue
            destination = (path.parent / unquote(address.path)).resolve()
            if destination in chapter_ids:
                target = all_headings[destination].get(unquote(address.fragment), chapter_ids[destination])
                link[2][0] = "#" + target
            elif destination.is_relative_to(ROOT):
                relative = destination.relative_to(ROOT)
                link[2][0] = f"{REPOSITORY}/blob/main/{quote(relative.as_posix())}"
                if address.fragment:
                    link[2][0] += "#" + address.fragment
        for image in nodes(blocks, "Image"):
            address = urlsplit(image[2][0])
            if address.path and not address.scheme and not address.netloc:
                file = (path.parent / unquote(address.path)).resolve()
                if not file.is_file() or not file.is_relative_to(ROOT):
                    raise ValueError(f"Unresolved image in {path.relative_to(ROOT)}: {image[2][0]}")
                asset = Path("assets") / file.relative_to(ROOT)
                copy = stage / asset
                copy.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(file, copy)
                image[2][0] = asset.as_posix()
        combined.extend(blocks)

    return json.dumps(
        {"pandoc-api-version": document["pandoc-api-version"], "meta": {}, "blocks": combined},
        ensure_ascii=False,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=("all", "en", "zh"), default="all")
    parser.add_argument("--format", choices=("all", "pdf", "epub"), default="all")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "_exports")
    args = parser.parse_args()
    languages = ("en", "zh") if args.language == "all" else (args.language,)
    formats = ("pdf", "epub") if args.format == "all" else (args.format,)
    for tool in ("pandoc", "typst") if "pdf" in formats else ("pandoc",):
        if not shutil.which(tool):
            parser.error(f"{tool} is required. See the repository README for dependencies.")

    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ebook-", dir=output) as directory:
        stage = Path(directory)
        book_header = stage / "book-header.typ"
        book_header.write_text(
            '#show raw: set text(font: ("DejaVu Sans Mono", "Noto Sans Mono CJK SC"), size: 8pt)\n',
            encoding="utf-8",
        )
        for language in languages:
            manuscript = make_book(language, stage)
            for format_name in formats:
                target = stage / f"{SLUG}-{language}.{format_name}"
                common = ["--from=json", "--standalone", "--toc", "--toc-depth=2",
                          "--metadata", f"title={TITLES[language]}"]
                if format_name == "epub":
                    pandoc(*common, "--to=epub3", "--split-level=1", "--metadata",
                           "lang=zh-CN" if language == "zh" else "lang=en",
                           "--output", target.name, text=manuscript, cwd=stage)
                else:
                    intermediate = stage / "book.typ"
                    pandoc(*common, "--to=typst", "--metadata", f"lang={language}",
                           "--include-in-header", book_header.name,
                           "--variable", "mainfont=Noto Serif CJK SC", "--variable", "papersize=a4",
                           "--output", intermediate.name, text=manuscript, cwd=stage)
                    subprocess.run(["typst", "compile", intermediate.name, target.name],
                                   cwd=stage, check=True)
        for target in sorted(stage.glob(f"{SLUG}-*")):
            destination = output / target.name
            target.replace(destination)
            print(destination)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Export failed: {error}", file=sys.stderr)
        sys.exit(1)
