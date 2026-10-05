"""Build complete editions and a reproducible example archive from canonical sources."""
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
(ROOT / 'editions').mkdir(exist_ok=True)
for lang, name in [('en', 'english'), ('zh', 'chinese')]:
    title = 'Pocket Framework — Complete edition' if lang == 'en' else 'Pocket Framework — 完整阅读版'
    text = f'''---
title: {json.dumps(title, ensure_ascii=False)}
lang: {'en' if lang == 'en' else 'zh'}
sidebar: {lang}
search: false
include-in-header:
  text: |
    <meta name="pocket-english" content="english.html">
    <meta name="pocket-chinese" content="chinese.html">
---

<!-- Generated from en/*.qmd and zh/*.qmd. Edit those source articles. -->

[English](english.qmd) · [中文](chinese.qmd)

'''
    for source in sorted((ROOT / lang).glob('*.qmd')):
        raw = source.read_text()
        title = json.loads(re.search(r'^title: (.+)$', raw, re.M).group(1))
        body = raw.split('<!-- article-body -->', 1)[1].strip()
        body = re.sub(r'\{#section-(\d+)\}', lambda m: '{#' + source.stem + '-section-' + m[1] + '}', body)
        body = re.sub(r'^## ', '### ', body, flags=re.M)
        text += f'## {source.stem[:2]} · {title} {{#{source.stem}}}\n\n{body}\n\n'
    (ROOT / 'editions' / (name + '.qmd')).write_text(text)

(ROOT / 'assets').mkdir(exist_ok=True)
with zipfile.ZipFile(ROOT / 'assets/pocket-notes-examples.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for source in sorted((ROOT / 'examples').rglob('*')):
        if source.is_file() and source.suffix in ('.go', '.mod', '.html', '.json'):
            info = zipfile.ZipInfo(source.relative_to(ROOT).as_posix(), (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, source.read_bytes())
print('Built both complete editions and the downloadable Go examples.')
