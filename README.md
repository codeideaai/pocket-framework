# Pocket Framework

An original, beginner-friendly series about building a small Go web framework through a personal notebook service. Fourteen complete articles, with English and Chinese versions of every article, exercise, and answer.

## Read

Open `index.html` directly in a browser. No installation or network connection is required for the reader. English is the default; the language buttons preserve the current chapter and approximate reading position.

For a localhost preview, run this from the repository root:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Visit `http://127.0.0.1:4173`. Search titles and article text with the sidebar. Press `/` to focus search and Escape to clear it. Mark completed articles to save progress in the current browser. Browser settings can prevent persistent storage; reading still works.

The `editions/english.html` and `editions/chinese.html` files contain the full series without JavaScript and are suitable for browser printing.

## Run the Go examples

Install Go 1.22 or later; use a currently supported release for development. Commands in the series use a macOS/Linux shell; Windows users can use WSL.

```sh
cd examples/hello
go run .
```

Stop the first example with Control+C before starting the notebook service:

```sh
cd ../notebook
go test ./...
go test -race ./...
go run .
```

The notebook listens on `127.0.0.1:8080`. Use `-addr` or the `NOTE_ADDR` environment variable to select another address. Flags take precedence over the environment.

- `GET /health`: process health.
- `GET /notes`: list notes.
- `POST /notes`: create a note with `Content-Type: application/json` and `{"title":"Learn Go"}`.

This is a local learning application. Notes exist only in memory and disappear when the process exits. Database, cache, and account features are extension designs in the articles, not implemented features of the example. The optional browser client is explained in article 12.

## Edit the series

The authoring source is `scripts/write_content.py`. Each article contains English and Chinese fields, a shared code example where appropriate, an exercise, an answer, and official documentation links.

After editing:

```sh
python3 scripts/write_content.py
python3 scripts/build_editions.py
node --check app.js
```

The first script writes `content/chapters.json` and its browser-compatible counterpart `content/chapters.js`. The second writes both complete printable HTML editions. Edit the authoring source rather than the generated files.

The reader uses plain HTML, CSS, and JavaScript with no external assets, package dependencies, or tracking. The Go examples use only the standard library.

## 中文说明

直接用浏览器打开 `index.html`，即可离线阅读。页面默认英文，右上角可切换完整中文版。支持正文搜索、章节导航、代码复制、阅读进度和打印。

共 14 篇原创文章，以个人笔记服务为贯穿项目；每篇都有解释、示例、练习与答案。`editions/chinese.html` 是不依赖 JavaScript 的中文完整版。

核心 Go 示例位于 `examples`；先安装 Go，再按文章运行。数据库、缓存和账户内容明确标记为后续扩展，不应误认为当前示例已经实现。
