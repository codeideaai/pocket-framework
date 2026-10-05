# Pocket Framework

[English website](https://codeideaai.github.io/pocket-framework/) · [中文网站](https://codeideaai.github.io/pocket-framework/zh.html)

Fourteen original, beginner-friendly articles about building a small Go web framework through a personal notebook service. Every article includes an English and Chinese edition, practical examples, an exercise, and an explanation.

## Read and edit

This is a **Quarto website**, using the same Quarto version and light/dark themes as Spring from Scratch.

- `index.qmd`: English landing page (default).
- `zh.qmd`: Chinese landing page.
- `en/*.qmd` and `zh/*.qmd`: the 28 editable article sources.
- `_quarto.yml`: navigation, search, theme, and publishing configuration.
- `examples/`: complete Go programs and tests.

Language links preserve the chapter. Quarto provides search, a table of contents, previous/next navigation, code copying, and light/dark mode. Read markers are saved locally in the browser. No JavaScript is required to read article text or follow the in-article language links.

Install [Quarto](https://quarto.org/docs/get-started/), then:

```sh
quarto preview
```

To produce the complete website:

```sh
quarto render
python3 scripts/check_site.py
```

The output is `_site/`. The pre-render script automatically assembles both complete printable editions and the downloadable example archive. Those generated files are ignored by Git; edit the `.qmd` articles directly. The original HTML reader remains recoverable in the initial Git commit.

For a static local preview of rendered output:

```sh
python3 -m http.server 4174 --bind 127.0.0.1 --directory _site
```

## Go examples

Use Go 1.22 or later; choose a currently supported Go release for development. Commands use a macOS/Linux shell; Windows users can use WSL.

```sh
cd examples/hello
go run .
```

Stop it with Control+C before starting the notebook:

```sh
cd ../notebook
go test -race ./...
go run .
```

The server defaults to `127.0.0.1:8080`. Set `NOTE_ADDR` or pass `-addr` to choose another address. Routes: `GET /health`, `GET /notes`, and `POST /notes` with JSON `{"title":"Learn Go"}`.

This is a local teaching application. Data is stored in memory and disappears at process exit. Database, cache, and accounts are extension designs, not implemented features of the example.

## GitHub Pages

`.github/workflows/publish.yml` tests the Go examples, renders with Quarto 1.10.18, validates output links, and uploads the Pages artifact. For a public repository, it also deploys through GitHub Actions. Choose **Settings → Pages → Source → GitHub Actions** to enable publishing. While the repository is private, the workflow builds and validates without deploying.

The intended site address is `https://codeideaai.github.io/pocket-framework/`. It becomes available after Pages is enabled and the deployment succeeds.

## 中文说明

本项目已迁移为 Quarto，与 Spring from Scratch 使用相同版本和明暗主题。默认英文，支持切换到当前章节的中文版。

直接编辑 `en/` 与 `zh/` 下的 `.qmd` 正文，运行 `quarto preview` 预览或 `quarto render` 构建。完整打印版和示例下载包会自动生成，不需要维护第二份正文。

GitHub Actions 会先验证 Go 示例，再构建和检查网站。仓库仍为私有时只构建、不部署；公开后可通过 GitHub Pages 发布。
