"""Build the bilingual article data. All prose and examples are authored for this series."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
chapters = []

def article(slug, en_title, zh_title, en_deck, zh_deck, part, minutes):
    a = dict(id=slug, title=dict(en=en_title,zh=zh_title), deck=dict(en=en_deck,zh=zh_deck), part=part, minutes=minutes, sections=[])
    chapters.append(a)
    return a

def section(a, en_title, zh_title, en, zh, code=None, language='go', filename=None):
    s = dict(title=dict(en=en_title,zh=zh_title), body=dict(en=en.strip(),zh=zh.strip()))
    if code: s.update(code=code.strip(),language=language,filename=filename or language)
    a['sections'].append(s)

def exercise(a, en, zh, en_answer, zh_answer):
    a['exercise'] = dict(question=dict(en=en,zh=zh),answer=dict(en=en_answer,zh=zh_answer))

def refs(a, *items):
    a['references'] = [dict(label=x[0],url=x[1]) for x in items]

a=article('00-start','A small project, a clear destination','从一个小项目开始','Set up your desk, learn just enough Go, and decide what we are building.','准备开发环境，认识必要的 Go 语法，明确我们要做什么。',0,10)
section(a,'Build something you can explain','做一个自己能解释清楚的东西',
'''Imagine a notebook with only two actions: save a short note and read your notes. A browser sends a message, a Go program decides what to do, and a response comes back. That tiny loop contains the central ideas of a web framework.

Our project is called Pocket Notes. We will first make the loop work, then extract the repeated parts into a package named mini. The application knows what a note is. The framework knows how to route a request and write a response. Keeping that boundary visible is the point of the series.

You do not need to know networking or a web framework already. You should be able to create a file and open a terminal. Every runnable command uses macOS/Linux shell syntax. Windows users can follow inside WSL. Each article names the file or function it discusses; short excerpts explain one idea, while the examples directory contains complete programs.''',
'''想象一个只有两项功能的笔记本：保存一句话，再读出已经保存的内容。浏览器发出消息，Go 程序决定怎么处理，然后返回结果。这个很小的过程，已经包含了 Web 框架的核心思想。

我们的项目叫 Pocket Notes。先让这个过程跑通，再把重复的工作提取到 mini 包中。应用知道什么是笔记，框架负责匹配请求和组织响应。整个系列最重要的事情，就是看清这条分工边界。

你不需要学过网络编程，也不需要用过框架，只要能创建文件、打开终端即可。文中的命令采用 macOS/Linux 的 shell 语法，Windows 可以在 WSL 中操作。每篇文章都会标明涉及的文件或函数；短代码用于解释一个概念，examples 目录则提供完整程序。''')
section(a,'Prepare one working directory','准备工作目录',
'''Install Go using the official installation guide, then open a new terminal and run go version. These examples require Go 1.22 or later because they use method-aware routing patterns. Use a currently supported Go release for your own work. An editor and a terminal are enough; there is no database to install for the core project.

From this series folder, enter examples/hello and run the commands below. A module is a group of Go packages that share a go.mod file. Its module path is the name used in imports; example.com/hello is a teaching name and does not require owning a domain. The supplied example already has go.mod, so do not run go mod init there again.

The last command stays running. That is expected: a server waits for requests. Open the address shown in the terminal. Press Control+C in that terminal when you want to stop it.''',
'''按照 Go 官方安装指南安装工具链，再打开一个新终端运行 go version。示例要求 Go 1.22 或更高版本，因为我们会使用带请求方法的路由规则。实际开发请选择仍受支持的 Go 版本。核心项目只需要编辑器和终端，不必先安装数据库。

在本系列的目录下，进入 examples/hello，运行下面的命令。模块是共享一个 go.mod 文件的一组 Go 包。模块路径用于 import 导入；example.com/hello 是教学名称，不需要购买域名。示例已提供 go.mod，因此不必再次运行 go mod init。

最后一条命令会一直运行，这是正常现象：服务器正在等待请求。打开终端提示的地址，就能看到结果。想停止时，在运行服务的终端按 Control+C。''',
'''cd examples/hello
go version
go run .
# Open http://127.0.0.1:8080 in your browser.''','sh','Terminal · examples/hello')
section(a,'Read Go without memorizing everything','先读懂眼前需要的 Go',
'''A package groups related code. package main plus a main function makes an executable program. import brings in another package. A function declares inputs inside parentheses and results after them. The := operator declares a variable and gives it an initial value.

A struct groups named fields. A method is a function attached to a type. An interface lists the methods a value must provide. We will meet each of these when it solves a real problem, rather than building an abstract vocabulary first.

When a function returns an error, check it. A missing error check turns a useful message such as “address already in use” into a mystery. If go is not found, finish the installation and reopen your terminal. If port 8080 is busy, stop the earlier example before starting another.''',
'''package 把相关代码放在一起。package main 配合 main 函数，构成可执行程序。import 用于导入其他包。函数在括号里声明输入参数，在括号后声明返回值。:= 表示声明变量并赋初值。

struct 把几个有名字的字段组合起来。方法是属于某个类型的函数。接口列出一个值需要提供哪些方法。我们会在真正用到的时候逐一认识它们，不必先背完术语。

如果函数返回 error，就要检查它。忽略错误会把“端口已被占用”这样清楚的提示，变成让人摸不着头脑的问题。如果终端找不到 go，请完成安装后重新打开终端。如果 8080 端口被占用，先停止之前启动的示例。''')
exercise(a,'Change the greeting, restart the program, and explain why refreshing the browser alone did not change it.','修改问候语，重启程序，并解释为什么只刷新浏览器不会更新内容。','go run compiles and starts a program. The running program does not automatically reload edited source files. Stop it and run go run . again.','go run 会编译并启动程序。正在运行的程序不会自动重新读取修改后的源码，需要停止后重新运行 go run .。')
refs(a,('Install Go','https://go.dev/doc/install'),('Go tutorial','https://go.dev/doc/tutorial/getting-started'))

a=article('01-request','Follow one request all the way home','跟着一次请求走完全程','Understand the conversation before adding abstractions.','先看懂浏览器与服务器的对话，再考虑抽象。',0,12)
section(a,'A request is a message','请求是一条有结构的消息',
'''Type http://127.0.0.1:8080 into a browser. The browser connects to a server on your own machine and asks for a resource. Here 127.0.0.1 means this computer, 8080 identifies the listening port, and / is the path. The browser normally uses GET when opening a page.

The response has a status code, headers, and usually a body. A 200 status says the request succeeded. A Content-Type header tells the reader how to interpret the body. The greeting itself is the body. HTTP bodies can contain bytes of many kinds, including images; HTTP is not limited to plain text.

Keep the roles separate: the server accepts connections, a router selects a handler, and the handler performs one piece of work. A framework helps organize these roles. It does not replace the HTTP protocol.''',
'''在浏览器里输入 http://127.0.0.1:8080，浏览器会连接本机的服务器，并请求一个资源。127.0.0.1 表示当前计算机，8080 是监听端口，/ 是路径。直接打开网页时，浏览器通常发送 GET 请求。

响应包含状态码、响应头，通常还有响应体。200 表示请求成功。Content-Type 告诉接收者如何解释响应体。页面上出现的问候语就是响应体。HTTP 的消息体可以携带图片等各种字节数据，并不局限于普通文本。

先分清三个角色：服务器接收连接，路由器选择处理函数，处理函数完成具体工作。框架帮助我们组织这些角色，而不是取代 HTTP 协议。''')
section(a,'Your first complete server','第一个完整服务器',
'''Read main.go in examples/hello from top to bottom. NewServeMux creates the router. HandleFunc connects a pattern to a function. The pattern GET /{$} means the root path for GET requests; the {$} marker keeps it from becoming a catch-all for deeper paths. Go also lets a GET pattern handle HEAD requests.

Inside the handler, r is the incoming request and w is where the response is written. Fprintln writes our greeting. Since the handler has not selected another status, writing the body sends the default success status. The Server value supplies the address, router, and a limit for reading request headers.

ListenAndServe blocks while the server runs. Its returned error matters: a port conflict prevents startup. The first example logs that error and exits. Later we will distinguish a normal shutdown from an unexpected failure.''',
'''从上到下阅读 examples/hello/main.go。NewServeMux 创建路由器；HandleFunc 把规则与函数关联起来。GET /{$} 匹配 GET 请求的根路径，{$} 让它不会顺便匹配更深层的路径。Go 也允许 GET 规则处理 HEAD 请求。

处理函数中的 r 是收到的请求，w 是写出响应的地方。Fprintln 输出问候语。因为此前没有指定其他状态码，首次写响应体时会发送默认的成功状态。Server 配置监听地址、路由器，以及读取请求头的时间限制。

ListenAndServe 会在服务器运行期间持续等待。它返回的错误很重要，例如端口冲突会导致启动失败。第一个示例会记录错误并退出；后面我们会进一步区分正常关闭和意外故障。''', (ROOT/'examples/hello/main.go').read_text(), 'go','examples/hello/main.go · complete file')
section(a,'Inspect what the browser hides','看看浏览器没有直接显示的内容',
'''Leave the server running and open a second terminal. curl is a command-line HTTP client. The -i option includes response headers. You should see a 200 status and Hello, framework! in the body. Header order, dates, and the displayed HTTP version can vary, so compare meaning rather than copying every line.

Now request /missing. The router should return 404. This is useful evidence: the server is reachable, but no route matched. “Connection refused” is different; it usually means nothing is listening at that address. Debug from the outside inward: connection, route, then handler.''',
'''保持服务器运行，再打开一个终端。curl 是命令行 HTTP 客户端，-i 选项让它同时显示响应头。你应该看到 200 状态，以及响应体中的 Hello, framework!。响应头顺序、日期和显示的 HTTP 版本可能不同，检查含义即可，不必逐行完全一致。

接着请求 /missing，路由器应该返回 404。这说明服务器能够连接，但没有匹配到路由。“Connection refused” 则是另一类问题，通常表示这个地址上没有程序监听。排错时由外向内检查：能否连接、能否匹配路由、处理函数是否正确。''',
'''curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/missing''','sh','Second terminal')
exercise(a,'What would change if the server listened on 127.0.0.1:9090?','如果服务器监听 127.0.0.1:9090，需要相应修改哪里？','Use port 9090 in the browser and curl URL too. A correct path on the wrong port still reaches the wrong destination.','浏览器和 curl 的地址也要改成 9090。路径正确但端口错误，仍然到不了目标服务器。')
refs(a,('HTTP server API','https://pkg.go.dev/net/http#Server'))

a=article('02-routing','Give each action an address','给每项操作一个地址','Design the notebook API and wrap the router in a tiny engine.','设计笔记接口，把路由器封装成一个小引擎。',0,12)
section(a,'Name resources, then choose actions','先确定资源，再确定操作',
'''A note is our resource. Reading the collection becomes GET /notes; creating one becomes POST /notes. The path identifies what we are working with, and the method tells us what kind of operation is intended. Keeping those choices predictable makes both clients and tests easier to write.

For now, we need three routes: GET /health to check that the process responds, GET /notes to list notes, and POST /notes to create a note. We deliberately postpone editing and deletion. A small working boundary is easier to reason about than a large collection of unfinished endpoints.

There is a meaningful distinction between 404 and 405. A missing path gets 404. A known path with an unsupported method gets 405. We let ServeMux handle that distinction, including the Allow header, instead of introducing a second, slightly different routing system.''',
'''笔记就是我们的资源。读取笔记集合使用 GET /notes，创建笔记使用 POST /notes。路径说明我们操作什么，请求方法说明准备做哪类操作。保持这些约定一致，客户端和测试代码都会更容易编写。

目前只需要三个路由：GET /health 检查进程能否响应，GET /notes 读取笔记，POST /notes 创建笔记。暂时不做修改和删除。一个小而完整的功能边界，比一堆尚未完成的接口更容易理解。

404 与 405 表达的含义不同。找不到路径时返回 404，路径存在但不支持这个方法时返回 405。我们让 ServeMux 负责区分这些情况，包括设置 Allow 响应头，不再另写一套行为略有不同的路由系统。''')
section(a,'An engine can start as a wrapper','引擎可以从简单封装开始',
'''The Engine type in mini owns a ServeMux. Its ServeHTTP method forwards the request to that router. This single method makes Engine satisfy http.Handler, so the standard server can use it directly. Go interfaces are satisfied by methods; there is no “implements” declaration to write.

Why add a wrapper at all? It gives our application one place to register framework handlers and gives us a home for future shared behavior. It is not a routing performance optimization. We gain a small API boundary while retaining the router’s existing behavior.

The excerpt below lives in mini.go. It is not a separate program: it needs package mini, the net/http import, and the Handle method shown with the request wrapper in the next article. The complete file is already supplied in the example.''',
'''mini 包中的 Engine 保存一个 ServeMux。它的 ServeHTTP 方法把请求交给这个路由器。只要提供这个方法，Engine 就满足 http.Handler 接口，标准服务器可以直接使用它。Go 通过方法判断是否满足接口，不需要声明 implements。

为什么还要加这一层？它让应用有一个统一的框架路由注册入口，也为后续公共行为提供位置。这不是路由性能优化，而是建立一个小型 API 边界，同时保留现有路由器的行为。

下面是 mini.go 中的片段，不是独立程序。它需要 package mini、net/http 导入，以及下一篇介绍的 Handle 方法。示例目录已经提供了完整文件。''',
'''type Engine struct { mux *http.ServeMux }

func New() *Engine {
    return &Engine{mux: http.NewServeMux()}
}

func (e *Engine) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    e.mux.ServeHTTP(w, r)
}''','go','examples/notebook/mini/mini.go · excerpt')
section(a,'Try the contract before growing it','扩展功能前，先验证约定',
'''Stop the hello server, then run go run . from examples/notebook. Run the requests below in another terminal. GET /notes returns an empty JSON array when the application has just started. DELETE /notes returns 405. GET /missing returns 404.

Register routes before starting the server. A duplicate or conflicting pattern can panic during registration, which is a startup error you should fix rather than hide. If you later add GET /notes/{id}, read r.PathValue("id") for the path value and validate it before using it as an integer. A route matching a string does not prove that the string is a valid record ID.''',
'''停止 hello 服务器，再从 examples/notebook 目录运行 go run .。在另一个终端执行下面的请求。应用刚启动时，GET /notes 返回空 JSON 数组，DELETE /notes 返回 405，GET /missing 返回 404。

应在服务器启动前注册路由。重复或冲突的规则可能在注册时触发 panic，这是应该修正的启动配置错误。如果以后增加 GET /notes/{id}，可以通过 r.PathValue("id") 读取路径参数，再验证它是不是合法整数。路由能匹配到字符串，并不代表它一定是有效的记录编号。''',
'''curl -i http://127.0.0.1:8080/notes
curl -i -X DELETE http://127.0.0.1:8080/notes
curl -i http://127.0.0.1:8080/missing''','sh','Second terminal')
exercise(a,'Should GET /notes create a new note as a side effect? Explain your choice.','GET /notes 是否应该顺便创建一条笔记？为什么？','No. Reading should not intentionally change application state. Browsers, crawlers, and clients may repeat reads; creation belongs to the POST route.','不应该。读取操作不应主动改变应用状态。浏览器、爬虫和客户端可能重复读取；创建应由 POST 路由承担。')
refs(a,('ServeMux patterns','https://pkg.go.dev/net/http#ServeMux'))

a=article('03-response','Make responses boring and consistent','让响应简单、一致','Build a request wrapper and a small JSON helper.','封装单次请求，写一个小巧的 JSON 响应方法。',0,13)
section(a,'Remove repetition you can already see','从已经出现的重复开始',
'''Our three handlers all need the request and the response writer. They also need to produce JSON. Copying header setup and serialization into every handler creates several places to make the same mistake. This is a good time for a small abstraction because we can name the repeated work precisely.

The framework Context groups Writer and Request for one request. It is allocated when the request enters the registered handler. It is not shared across requests and must not become a place to store global application state. A note repository belongs to the application, not to this temporary wrapper.

There are two different uses of the word context in this series. mini.Context is our convenience wrapper. context.Context from Go’s standard library carries cancellation and deadlines. You access the latter through c.Request.Context(). Keeping the names straight prevents a lot of confusion later.''',
'''三个处理函数都需要读取请求、写出响应，也都需要输出 JSON。如果每个函数都复制一遍响应头和序列化逻辑，就会增加重复出错的机会。现在适合做一个小抽象，因为我们已经能准确说出哪些工作在重复。

框架的 Context 把单次请求的 Writer 和 Request 放在一起，在进入注册的处理函数时创建。它不应在不同请求间共享，也不应变成保存全局应用状态的容器。笔记仓库属于应用，不属于这个临时包装对象。

本系列里有两个容易混淆的 context：mini.Context 是我们提供便利方法的包装类型；标准库的 context.Context 负责传递取消信号和截止时间。后者通过 c.Request.Context() 取得。先分清它们，后面就不容易绕晕。''')
section(a,'Serialize before sending the status','先序列化，再发送状态码',
'''The JSON method first turns the value into bytes. Only after serialization succeeds does it set Content-Type and send the status. That order matters: once the response has begun, you cannot replace an already sent success status with an error status.

Marshal can fail for unsupported values such as a channel. Writing can also fail when the client disconnects. The method returns an error instead of pretending either operation is infallible. The application’s reply helper logs that error. Our current response types contain only strings, integers, maps, and slices, so they are intentionally simple to serialize.

Do not call JSON twice for the same response. It would append another body rather than produce a clean replacement. After sending an error, return from the handler. That small habit prevents many accidental “error plus success” responses.''',
'''JSON 方法先把数据序列化成字节，成功后再设置 Content-Type 并发送状态码。顺序很重要：响应一旦开始发送，就无法把已经发出的成功状态替换成错误状态。

遇到 channel 之类不支持的值时，Marshal 会失败；客户端断开连接时，写出操作也可能失败。因此方法返回 error，而不是假定这些操作永远成功。应用中的 reply 辅助函数负责记录错误。当前响应只包含字符串、整数、映射和切片，刻意保持容易序列化。

同一条响应不要调用两次 JSON。第二次调用只会继续追加响应体，并不会干净地替换之前的内容。发送错误后立即 return，是避免“先报错、又成功”这种混乱响应的简单习惯。''',
'''type Context struct {
    Writer  http.ResponseWriter
    Request *http.Request
}

func (c *Context) JSON(status int, value any) error {
    data, err := json.Marshal(value)
    if err != nil { return err }
    c.Writer.Header().Set("Content-Type", "application/json; charset=utf-8")
    c.Writer.WriteHeader(status)
    _, err = c.Writer.Write(append(data, '\n'))
    return err
}''','go','examples/notebook/mini/mini.go · excerpt')
section(a,'Connect the wrapper to the router','把包装类型接到路由器上',
'''We define Handler as a function taking *Context. Engine.Handle adapts it to the function shape expected by ServeMux. An adapter is simply a small piece of code that connects two compatible ideas with different interfaces.

Notice that the framework still does not import Note. It can return a health response, a note list, or another application’s data. This is a useful test of the boundary: if changing the business object forces a change in mini, the framework probably knows too much.

In the completed app, GET /health returns {"status":"ok"}. Inspect it with curl -i and confirm both the content type and the body. A body that looks like JSON without the appropriate content type is an incomplete contract.''',
'''我们把 Handler 定义为接收 *Context 的函数。Engine.Handle 再把它转换成 ServeMux 所需要的函数形状。适配器并不神秘，就是一小段连接不同接口的代码。

注意，框架仍然不需要导入 Note。它可以输出健康检查结果、笔记列表，或其他应用的数据。这里有一个实用判断：如果业务对象一变，mini 就必须修改，通常说明框架知道的业务细节太多了。

完整应用中的 GET /health 返回 {"status":"ok"}。用 curl -i 检查响应体和内容类型。仅仅“看起来像 JSON”，却没有正确的 Content-Type，仍然不是完整的接口约定。''',
'''type Handler func(*Context)

func (e *Engine) Handle(pattern string, handler Handler) {
    e.mux.HandleFunc(pattern, func(w http.ResponseWriter, r *http.Request) {
        handler(&Context{Writer: w, Request: r})
    })
}''','go','examples/notebook/mini/mini.go · excerpt')
exercise(a,'Why does the JSON helper marshal before calling WriteHeader?','为什么 JSON 方法要在 WriteHeader 之前调用 Marshal？','Serialization can fail. Doing it first avoids committing a success response before knowing whether the value can be encoded.','序列化可能失败。先完成序列化，能避免在确认数据可编码之前，就已经发出了成功状态。')
refs(a,('JSON encoding','https://pkg.go.dev/encoding/json#Marshal'),('ResponseWriter','https://pkg.go.dev/net/http#ResponseWriter'))

a=article('04-input','Treat input as a question, not a fact','输入需要验证，不能直接相信','Accept one small JSON object and reject mistakes clearly.','只接收一个小 JSON 对象，清楚地处理错误。',1,15)
section(a,'Successful parsing is only the first check','解析成功只是第一关',
'''A client wants to create a note by sending {"title":"Learn Go"}. There are several independent questions to answer. Is the body JSON? Is it small enough? Does it contain exactly one value? Are its fields expected? Is the title useful? Solving only the first question is not input validation.

Our contract accepts application/json, limits the body to 4096 bytes, rejects unknown fields, and trims whitespace from the title. After trimming, the title must contain between 1 and 120 Unicode code points. Code points are not always the same as visible characters: an emoji sequence may contain several.

We use 415 for an unsupported media type, 413 when the decoder encounters the size limit, and 400 for invalid content. If the decoder finds an earlier syntax error before reaching the limit, a large malformed request can still get 400. The practical promise is that invalid input never becomes a saved note.''',
'''客户端希望发送 {"title":"Learn Go"} 来创建笔记。这里要分别回答几个问题：消息体是不是 JSON？有没有超出大小限制？是不是只有一个值？字段是否符合预期？标题是否有效？只解决第一个问题，还算不上输入校验。

我们的约定是：接收 application/json，消息体上限为 4096 字节，拒绝未知字段，去掉标题前后的空白。处理后的标题必须包含 1 到 120 个 Unicode 码点。码点不一定等于肉眼看到的字符，例如一个表情组合可能包含多个码点。

媒体类型不支持时返回 415，解码器遇到大小限制时返回 413，内容无效时返回 400。如果很大的畸形请求先触发语法错误，也可能返回 400。真正要保证的是：无效输入不会变成已保存的笔记。''')
section(a,'Decode once, then check for the end','读完一个值，再确认结束',
'''A JSON decoder reads one value at a time. A first successful Decode does not prove that the body contains nothing else. A second decode must reach io.EOF. Otherwise, a body like {"title":"a"} {} would silently include an extra value.

The implementation also uses MaxBytesReader before decoding. Checking Content-Length alone is insufficient because it can be absent, and the application must limit the bytes it actually reads. DisallowUnknownFields helps catch a typo such as titel instead of title.

After decoding, trim and validate the title before calling the store. Keep decoding, validation, and persistence in that order. The excerpt below shows the happy-path structure; app.go contains the full error branches and media-type check.''',
'''JSON 解码器一次读取一个值。第一次 Decode 成功，并不能证明后面没有其他内容。第二次解码必须得到 io.EOF，否则 {"title":"a"} {} 这种包含两个值的输入就会被悄悄放过。

实现中会在解码前使用 MaxBytesReader。只检查 Content-Length 不够，因为这个头可能不存在；应用需要限制实际读取的字节。DisallowUnknownFields 则能帮助发现把 title 写成 titel 这样的字段拼写错误。

解码完成后，先去掉空白、校验标题，再调用仓库。保持“解码、校验、保存”的顺序。下面是成功路径的结构，app.go 中包含完整的错误分支和媒体类型检查。''',
'''c.Request.Body = http.MaxBytesReader(c.Writer, c.Request.Body, 4096)
var input struct { Title string `json:"title"` }
dec := json.NewDecoder(c.Request.Body)
dec.DisallowUnknownFields()
// Check the first Decode error, then require io.EOF on the second.
// See app.go for all error branches.
''','go','examples/notebook/app.go · setup excerpt')
section(a,'Prove the failure cases too','错误分支也要亲自验证',
'''Run these requests against the notebook server. The first should return 201 and a note with an ID. The second should return 400 because spaces are not a meaningful title. GET /notes should show only the successful note, not an empty placeholder left behind by the rejected request.

Try a misspelled field and a second JSON object next. Both should fail. If a request unexpectedly returns 415, check the Content-Type header; curl does not infer application/json just because its data looks like JSON.

This exercise reveals a general design rule: validate before changing state. Error handling is much simpler when rejecting input does not require undoing a half-completed write.''',
'''向笔记服务发送下面的请求。第一条应返回 201，以及带编号的笔记；第二条应返回 400，因为纯空白不是有效标题。之后 GET /notes 应只出现成功创建的笔记，不应留下失败请求产生的空记录。

接着试试拼错字段名，或者在后面追加第二个 JSON 对象，两者都应被拒绝。如果意外得到 415，请检查 Content-Type。curl 不会因为数据看起来像 JSON，就自动推断它是 application/json。

这个练习揭示了一条通用原则：先校验，再改变状态。如果拒绝输入时不需要撤销半完成的写入，错误处理就会简单很多。''',
'''curl -i http://127.0.0.1:8080/notes \
  -H 'Content-Type: application/json' \
  -d '{"title":"Learn Go"}'
curl -i http://127.0.0.1:8080/notes \
  -H 'Content-Type: application/json' \
  -d '{"title":"   "}'
curl http://127.0.0.1:8080/notes''','sh','Second terminal')
exercise(a,'Why does len(title) give the wrong unit for our title rule?','为什么 len(title) 不适合直接实现这里的标题长度规则？','For a Go string, len counts bytes. utf8.RuneCountInString counts Unicode code points, which is the unit our contract explicitly chose.','Go 字符串的 len 计算字节数。utf8.RuneCountInString 计算 Unicode 码点数，符合这里明确选择的计量单位。')
refs(a,('Decoder','https://pkg.go.dev/encoding/json#Decoder'),('MaxBytesReader','https://pkg.go.dev/net/http#MaxBytesReader'))

a=article('05-middleware','Wrap a handler without changing its job','给处理函数增加公共行为','Use middleware for request timing and learn why order matters.','用中间件记录耗时，理解执行顺序。',1,12)
section(a,'One shared behavior, many routes','一份公共逻辑，作用于多个路由',
'''Suppose every request should produce a timing log. Adding the same clock code to all three handlers is possible, but the fourth handler might forget it. The shared behavior belongs around the application’s handler.

Middleware takes an http.Handler and returns another http.Handler. The returned handler can do work before and after calling the original one. Our access logger records a start time, calls next.ServeHTTP, then logs the elapsed duration. The note handlers remain focused on notes.

This middleware measures the duration of the downstream handler call. It does not measure when a user finishes receiving the response across the network, and it does not record a status code. Being precise about what a metric measures makes the log useful.''',
'''假设每次请求都需要记录耗时。可以把计时代码复制进三个处理函数，但新增第四个时很容易忘记。这样的公共行为应该放在整个应用处理函数的外围。

中间件接收一个 http.Handler，再返回另一个 http.Handler。新处理函数可以在调用原处理函数之前和之后做事。访问日志中间件记录开始时间，调用 next.ServeHTTP，再记录经过的时间。笔记处理函数仍只负责笔记业务。

这里测量的是下游处理函数调用的耗时，不是用户通过网络接收完整响应所花的时间，也没有记录状态码。明确指标到底测量什么，日志才有意义。''')
section(a,'Read the function from the inside out','从内到外理解函数嵌套',
'''The innermost function handles one request. The function around it receives next, the handler it should call. The outermost accessLog function receives the logger. This arrangement captures the logger once at startup and uses it for many requests.

Calling next passes control inward. Returning from next brings control back to the middleware. If middleware chooses to reject a request, it can write an error and return without calling next. Authentication often uses that shape.

Do not add a goroutine merely to make middleware “asynchronous.” ResponseWriter has a request lifetime, and concurrent writes create correctness problems. Synchronous wrapping is enough for this logger.''',
'''最里面的函数处理一次请求。包住它的函数接收 next，也就是它应该调用的下游处理函数。最外层 accessLog 接收日志对象。这种写法在启动时保存日志依赖，随后可以服务很多请求。

调用 next 会把控制权交给里面的处理逻辑，next 返回后又回到中间件。如果中间件决定拒绝请求，可以写出错误并直接返回，不再调用 next。身份认证经常采用这种结构。

不要仅仅为了“异步”就额外启动 goroutine。ResponseWriter 有请求生命周期，并发写响应会带来正确性问题。这里同步地包装处理函数已经足够。''',
'''func accessLog(logger *slog.Logger) mini.Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()
            next.ServeHTTP(w, r)
            logger.Info("request", "method", r.Method,
                "path", r.URL.Path, "duration", time.Since(start))
        })
    }
}''','go','examples/notebook/app.go · excerpt')
section(a,'Order is part of the behavior','顺序也是行为的一部分',
'''Chain(app, A, B) should execute A before B before app, then return through B and A. The chain builder therefore wraps from the end of the list toward the beginning. This is easier to verify by writing the nesting: A(B(app)).

Try adding temporary “before” and “after” logs to two middleware functions. Predict the output on paper first. If an authorization layer returns early, anything inside it does not run. A logger outside it can still record the rejected request.

Our logger records paths but avoids bodies and credentials. Extra detail is not always helpful: a log that contains a password is now a second place that password must be protected.''',
'''Chain(app, A, B) 应先进入 A，再进入 B，最后进入 app，然后依次返回 B 和 A。所以组合函数需要从列表末尾向前包装。把它写成 A(B(app))，就更容易看清。

可以临时给两个中间件增加 before 和 after 日志，先在纸上预测输出，再运行验证。如果授权层提前返回，它里面的逻辑不会执行；放在外层的日志中间件仍然可以记录被拒绝的请求。

我们的日志记录路径，但不记录请求体和凭据。更多细节不一定更好：日志里一旦出现密码，就多了一个需要保护密码的地方。''',
'''func Chain(handler http.Handler, middleware ...Middleware) http.Handler {
    for i := len(middleware)-1; i >= 0; i-- {
        handler = middleware[i](handler)
    }
    return handler
}''','go','examples/notebook/mini/mini.go · excerpt')
exercise(a,'For A(B(app)), what is the normal before/after order?','对于 A(B(app))，正常的 before/after 顺序是什么？','A before → B before → app → B after → A after. An early return can prevent the inner stages from running.','A before → B before → app → B after → A after。提前返回可能让内部阶段不再执行。')
refs(a,('Handler interface','https://pkg.go.dev/net/http#Handler'))

a=article('06-cancellation','Stop work nobody needs anymore','停止已经没有必要的工作','Use cooperative cancellation without racing the response writer.','通过协作式取消停止工作，避免并发写响应。',1,14)
section(a,'A deadline is a signal','截止时间发出的是信号',
'''Imagine that loading a note eventually requires a slow remote service. If the browser goes away, finishing that remote request may be wasted work. A context carries a cancellation signal through the call chain so each operation can notice when it should stop.

Cancellation is cooperative. It does not forcibly kill a goroutine or interrupt arbitrary code. An operation must check the context or call an API that understands it. Passing a context to a function that ignores it does not create a timeout.

Start from r.Context(), because it is tied to the incoming request. Derive a child with a shorter timeout when a particular operation needs a tighter budget. Always call the returned cancel function, usually with defer, so resources can be released promptly.''',
'''假设以后读取笔记需要调用一个很慢的远程服务。如果浏览器已经离开，继续完成那个请求可能只是浪费资源。context 可以沿着调用链传递取消信号，让每个操作知道何时应该停止。

取消是协作式的。它不会强行杀死 goroutine，也不会打断任意代码。操作必须主动检查 context，或调用支持 context 的 API。把 context 传给完全忽略它的函数，并不会自动产生超时能力。

从 r.Context() 开始，因为它与当前请求关联。如果某个操作需要更短的时间预算，再派生一个带超时的子 context。始终调用返回的 cancel，通常使用 defer，让相关资源及时释放。''')
section(a,'A complete cancellation experiment','做一个完整的取消实验',
'''Save the following program as main.go in a separate scratch directory and run go run main.go. It simulates work that would take 200 milliseconds but gives it a 50-millisecond budget. It should print context deadline exceeded.

select waits until one channel operation is ready. The timer channel becomes ready when the simulated work finishes. ctx.Done becomes ready when cancellation happens. Here the cancellation branch normally wins because its budget is shorter.

There is no HTTP response writer in this worker. That is deliberate. In an HTTP application, let work return a result or an error, and let the handler decide the response. Avoid designs where a timeout goroutine and a worker both write to the same response.''',
'''把下面的完整程序保存到独立实验目录的 main.go 中，执行 go run main.go。它模拟一项需要 200 毫秒的工作，但只给 50 毫秒预算，应该输出 context deadline exceeded。

select 会等待某个通道操作就绪。模拟工作结束时，定时器通道就绪；发生取消时，ctx.Done 就绪。这里通常会进入取消分支，因为时间预算更短。

这个工作函数没有接触 HTTP 响应写入器，这是刻意的设计。在 HTTP 应用中，让工作函数返回结果或错误，再由处理函数决定如何响应。避免超时 goroutine 和业务 goroutine 同时写同一个响应。''',
'''package main

import (
    "context"
    "fmt"
    "time"
)

func work(ctx context.Context) error {
    timer := time.NewTimer(200 * time.Millisecond)
    defer timer.Stop()
    select {
    case <-timer.C:
        return nil
    case <-ctx.Done():
        return ctx.Err()
    }
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
    defer cancel()
    fmt.Println(work(ctx))
}''','go','Standalone experiment · main.go')
section(a,'Follow cancellation through the application','把取消信号传到真正工作的地方',
'''Pocket Notes passes c.Request.Context() into its store. The memory store checks ctx.Err() before reading or changing its data. Its tiny operations finish quickly, so it does not need a timer of its own. A future SQL store can use QueryContext or ExecContext with that same context.

Network deadlines and application cancellation solve related but different problems. A server read timeout limits reading a request. A context budget tells downstream work when to stop. A write timeout does not magically cancel CPU work inside your handler.

When a client has disconnected, writing a beautifully formatted timeout response may itself fail. That is normal. The important part is releasing resources and avoiding unnecessary work. This is why our response helper reports write errors rather than promising every response will reach a user.''',
'''Pocket Notes 会把 c.Request.Context() 传给仓库。内存仓库在读取或修改数据之前检查 ctx.Err()。这些操作很短，所以不需要额外的定时器。以后换成 SQL 仓库时，可以把同一个 context 传给 QueryContext 或 ExecContext。

网络超时与应用取消相关，但解决的问题不同。服务器读取超时限制读取请求的时间；context 预算告诉下游工作何时停止。写超时不会自动取消处理函数内部正在执行的计算。

如果客户端已经断开，就算精心构造了超时响应，写出时也可能失败。这很正常。重要的是释放资源、避免无意义的工作。因此响应辅助函数会报告写入错误，而不会假定每条响应都能送达用户。''')
exercise(a,'Replace the select in work with time.Sleep(200*time.Millisecond). Does the 50-millisecond context interrupt the sleep?','把 work 中的 select 换成 time.Sleep(200*time.Millisecond)，50 毫秒的 context 会打断 Sleep 吗？','No. Sleep does not observe the context. The example demonstrates why cancellation must be supported by the operation doing the work.','不会。Sleep 不观察 context，这正说明取消需要执行工作的操作主动配合。')
refs(a,('Context cancellation','https://pkg.go.dev/context'))

a=article('07-storage','Give your data a home','给数据一个合适的位置','Separate note storage from HTTP and handle concurrent requests.','把笔记存储与 HTTP 分开，并处理并发请求。',1,15)
section(a,'Ask for capabilities, not a database','先声明需要的能力',
'''The handler needs two capabilities: list notes and create a note. It does not need to know whether the data is in memory, SQLite, or another database. A NoteStore interface expresses those capabilities with two methods.

newApp receives a NoteStore when the application starts. This is dependency injection in its simplest form: pass the thing a function needs as an argument. There is no service registry to search, and the compiler can check the required methods.

Our Note type uses JSON tags to give the API lowercase field names. ID is generated by the store; the client supplies only the title. Keeping those responsibilities separate prevents clients from choosing identifiers that collide with existing data.''',
'''处理函数需要两项能力：列出笔记、创建笔记。它不必知道数据保存在内存、SQLite，还是其他数据库。NoteStore 接口用两个方法表达这些能力。

应用启动时，把一个 NoteStore 传给 newApp。这就是最直接的依赖注入：把需要的东西通过参数传进去。没有需要查找的服务注册表，编译器也能检查方法是否满足要求。

Note 类型通过 JSON 标签，让 API 输出小写字段名。ID 由仓库生成，客户端只提供标题。分清这些职责，可以避免客户端随意选择编号而与已有数据冲突。''',
'''type Note struct {
    ID    int    `json:"id"`
    Title string `json:"title"`
}

type NoteStore interface {
    List(context.Context) ([]Note, error)
    Create(context.Context, string) (Note, error)
}''','go','examples/notebook/store.go · excerpt')
section(a,'Two requests can arrive together','两个请求可能同时到达',
'''A server can run handlers concurrently. If two requests both read the same nextID and then increment it without coordination, they may produce duplicate IDs or a data race. The shared slice also needs protection when one request writes while another reads.

MemoryStore uses one mutex around its state. Lock obtains exclusive access; defer Unlock releases it when the function returns. A single lock is easy to explain and sufficient for this small teaching application. Locking a Go mutex does not itself respond to context cancellation, so we check the context after acquiring it.

List copies the slice while holding the lock. Returning the internal slice would let callers retain access to storage that later changes. The copy gives the handler its own snapshot. We also create an empty, non-nil slice so an empty collection encodes as [] rather than null.''',
'''服务器可能同时执行多个处理函数。如果两个请求都在没有协调的情况下读取、增加 nextID，可能出现重复编号或数据竞争。一个请求写切片、另一个请求读切片时，也需要保护共享状态。

MemoryStore 使用一把互斥锁保护状态。Lock 获得独占访问权，defer Unlock 在函数返回时释放。对这个小型教学应用，一把锁容易理解，也足够使用。Go 互斥锁等待本身不会响应 context 取消，因此我们在获取锁之后检查 context。

List 在持锁期间复制切片。如果直接返回内部切片，调用者可能一直引用后续还会改变的存储。复制后，处理函数得到自己的快照。我们还会创建非 nil 的空切片，让空集合编码成 []，而不是 null。''',
'''func (s *MemoryStore) List(ctx context.Context) ([]Note, error) {
    s.mu.Lock()
    defer s.mu.Unlock()
    if err := ctx.Err(); err != nil { return nil, err }
    result := make([]Note, len(s.notes))
    copy(result, s.notes)
    return result, nil
}''','go','examples/notebook/store.go · excerpt')
section(a,'Know what memory does not promise','明确内存存储没有承诺什么',
'''Create a note, stop the server, restart it, and list notes again. The list is empty. That is the defined behavior of this implementation, not a mysterious persistence bug. Data exists only inside the running process.

A mutex protects requests inside that process. It does not coordinate two separate server processes. If you start two copies on different ports, each has its own notes and ID counter. Shared durable storage becomes necessary when you need restarts or multiple instances to see the same data.

The current store also grows without a limit. This is acceptable for a short local experiment, but not a long-running public service. The benefit of the interface is that we can replace this implementation while keeping the HTTP handlers almost unchanged.''',
'''创建一条笔记，停止服务器，重新启动，再读取列表，你会得到空数组。这是当前实现的明确行为，并不是神秘的持久化故障。数据只存在于正在运行的进程中。

互斥锁只能协调这个进程里的请求，不能协调两个独立进程。如果在不同端口启动两个实例，它们各自拥有笔记和编号计数器。当你需要重启后仍保留数据，或多个实例共享数据时，就需要共享的持久化存储。

当前仓库还会无限增长，适合短时间的本地实验，不适合长期公开运行。接口的好处是，我们可以更换存储实现，而基本不改 HTTP 处理函数。''')
exercise(a,'Why copy the notes slice if List already holds a lock?','List 已经加锁了，为什么还要复制笔记切片？','The lock is released when List returns. A copy prevents callers from sharing the underlying slice storage with later mutations.','List 返回时锁就释放了。复制可以避免调用者继续共享后续可能被修改的底层切片存储。')
refs(a,('Mutex','https://pkg.go.dev/sync#Mutex'),('Race detector','https://go.dev/doc/articles/race_detector'))

a=article('08-tests','Turn expectations into tests','把预期变成自动测试','Check the API without opening a port or clicking a browser.','不用监听端口，也不用点浏览器，就能检查接口。',2,14)
section(a,'Test the promise a client sees','测试客户端能看到的承诺',
'''We have been testing with curl. That is useful for exploration, but repeating ten requests by hand after every edit is easy to forget. A test should capture the behavior we intend to preserve.

For Pocket Notes, a useful test creates a note, rejects several invalid requests, then confirms that only the valid note was saved. This checks an observable promise across routing, decoding, validation, and storage. It is more valuable than a test that merely repeats the implementation line by line.

The supplied app_test.go also checks missing routes, unsupported methods, oversized input, and incorrect media types. A test table keeps these independent input/output cases readable. A failure should name the method and path so you know which promise changed.''',
'''前面一直用 curl 验证行为，这适合探索接口。但每次改代码后手动重试十种请求，很容易遗漏。自动测试应该保存我们希望长期保持的行为。

对于 Pocket Notes，一个有用的测试是：成功创建笔记，拒绝几种无效请求，最后确认只保存了那条有效笔记。它跨越路由、解码、校验和存储，检查客户端可以观察到的承诺，比逐行复述实现的测试更有价值。

提供的 app_test.go 还检查不存在的路径、不支持的方法、过大的输入和错误的媒体类型。测试表让这些独立的输入输出案例便于阅读。失败信息应带上请求方法和路径，方便判断哪个约定被破坏了。''')
section(a,'A recorder stands in for the connection','用记录器代替网络连接',
'''httptest.NewRequest constructs a request in memory. NewRecorder collects the status, headers, and body written by the handler. Calling handler.ServeHTTP directly exercises the HTTP boundary without reserving port 8080 or leaving a server process running.

The app receives a fresh MemoryStore and a logger that discards output. Fresh state prevents one test run from depending on another. The example below is a focused test you can add to app_test.go; its imports are already present there.

A recorder is not a complete network test. It does not prove that socket timeouts or operating-system signals work correctly. Use it for handler behavior, and separately test startup and shutdown with a real process.''',
'''httptest.NewRequest 在内存里构造请求，NewRecorder 收集处理函数写出的状态码、响应头和响应体。直接调用 handler.ServeHTTP，就能测试 HTTP 边界，不需要占用 8080 端口，也不会留下运行中的服务进程。

测试给应用传入新的 MemoryStore，以及丢弃输出的日志对象。独立状态避免不同测试运行互相依赖。下面这个聚焦的小测试可以添加到 app_test.go，所需导入已经在该文件里。

记录器不是完整的网络测试，它不能证明 socket 超时或操作系统信号的行为正确。用它验证处理函数，再用真实进程单独验证启动与关闭。''',
'''func TestHealth(t *testing.T) {
    app := newApp(&MemoryStore{}, slog.New(slog.NewTextHandler(io.Discard, nil)))
    response := httptest.NewRecorder()
    request := httptest.NewRequest(http.MethodGet, "/health", nil)
    app.ServeHTTP(response, request)
    if response.Code != http.StatusOK {
        t.Fatalf("got %d, want 200", response.Code)
    }
    var body map[string]string
    if err := json.Unmarshal(response.Body.Bytes(), &body); err != nil {
        t.Fatal(err)
    }
    if body["status"] != "ok" { t.Fatalf("unexpected body: %v", body) }
}''','go','Optional addition · examples/notebook/app_test.go')
section(a,'Use a failure to verify the test','故意制造失败，确认测试有效',
'''From examples/notebook, run go test ./.... Then temporarily change the expected creation status in the existing test from 201 to 200. Run the tests again: they should fail. Restore 201 and rerun. A test you have seen fail for the right reason is easier to trust.

Run go test -race ./... when your Go platform supports the race detector. This detects races only on paths actually exercised; a passing sequential test does not establish concurrency safety. To investigate the store under load, add concurrent Create calls and check that IDs are unique and the final count is correct.

Read failures as evidence, not interruptions. A 415 where you expected 201 often means the test forgot Content-Type. A 404 might mean the path is wrong. Tests need debugging too.''',
'''在 examples/notebook 中运行 go test ./...。然后临时把现有测试里创建成功的预期状态从 201 改成 200，再运行，应该失败。改回 201 后重新验证。亲眼见过测试因正确原因失败，更能确认它真的在检查行为。

如果当前 Go 平台支持竞争检测器，可以运行 go test -race ./...。它只能发现实际执行路径上的竞争，因此串行测试通过，并不能证明并发安全。要检查仓库并发行为，可以增加多个并发 Create 调用，确认编号不重复且最终数量正确。

把失败当作证据。例如，预期 201 却得到 415，往往是测试忘记设置 Content-Type；404 可能是路径写错。测试代码本身也需要调试。''',
'''go test ./...
go test -race ./...''','sh','Terminal · examples/notebook')
exercise(a,'Why give each test a fresh MemoryStore?','为什么要给每个测试新的 MemoryStore？','So its outcome depends on its own setup, not the order of previous tests or leftover notes.','让结果只依赖当前测试自己的准备过程，而不是之前测试的执行顺序或残留数据。')
refs(a,('httptest','https://pkg.go.dev/net/http/httptest'),('Go testing','https://pkg.go.dev/testing'))

a=article('09-lifecycle','Start clearly. Stop cleanly.','清楚地启动，妥善地停止','Make configuration, logs, and shutdown part of the application.','让配置、日志和关闭流程成为应用的一部分。',2,16)
section(a,'Configuration is input at startup','配置也是输入，只是发生在启动时',
'''Hardcoding port 8080 is fine until you want two local servers. The notebook program accepts an address in three levels of precedence: a default of 127.0.0.1:8080, then NOTE_ADDR from the environment, then the -addr command-line flag.

The program calls net.Listen before reporting that it is listening. That is a small but important truthfulness rule: a log should describe something that actually happened. An invalid address or occupied port fails immediately instead of leaving a half-started service.

Use configuration for things that vary between environments, not for every internal constant. The memory store’s title rule belongs to the API contract. A listen address belongs to the environment. Mixing those two kinds of choices makes configuration difficult to understand.''',
'''把端口写死为 8080，直到想同时启动两个服务时才显得不方便。笔记程序按三层优先级选择地址：默认值 127.0.0.1:8080，其次是环境变量 NOTE_ADDR，最后由命令行 -addr 覆盖。

程序先调用 net.Listen 成功，才记录“正在监听”。这是一条很实用的原则：日志应该描述确实发生的事情。无效地址或被占用的端口会立即导致启动失败，而不是留下一个半启动的服务。

配置用于不同环境间会变化的内容，不必把所有内部常量都变成配置。标题长度限制属于 API 约定，监听地址属于运行环境。混淆这两类选择，会让配置难以理解。''',
'''go run . -addr 127.0.0.1:9090
# Or set the environment for this one command:
NOTE_ADDR=127.0.0.1:9090 go run .''','sh','Terminal · examples/notebook · run one command at a time')
section(a,'Shutdown must finish before main returns','main 退出前，要等关闭流程完成',
'''When the process receives an interrupt or SIGTERM, it should stop accepting new work and give active requests a brief opportunity to finish. Server.Shutdown does that for ordinary HTTP connections. It does not automatically manage every background task or hijacked connection.

The shutdown budget must come from a fresh context. The signal context is already canceled, so using it directly would cancel the shutdown wait immediately. Our program creates a new five-second budget, waits for Shutdown, and closes remaining connections if that budget is exceeded.

The complete main.go also waits for the serving goroutine and treats http.ErrServerClosed as normal. Returning from main too early would terminate the process while shutdown was still running. Build a binary when testing signals so the process you interrupt is the server itself.''',
'''收到中断或 SIGTERM 后，进程应该停止接收新工作，并给正在处理的请求一点时间完成。Server.Shutdown 会为普通 HTTP 连接完成这些工作，但不会自动管理所有后台任务或被接管的连接。

关闭流程需要一个新的时间预算。信号 context 此时已经取消，如果直接使用它，等待关闭也会立即取消。程序会新建一个五秒预算，等待 Shutdown，若超时则关闭剩余连接。

完整 main.go 还会等待提供服务的 goroutine 结束，并把 http.ErrServerClosed 视作正常结果。如果 main 太早返回，进程会在关闭流程尚未完成时退出。测试信号时请先编译成二进制，让收到中断的进程就是服务器本身。''',
'''ctx, release := context.WithTimeout(context.Background(), 5*time.Second)
defer release()
if err := server.Shutdown(ctx); err != nil {
    _ = server.Close()
    return fmt.Errorf("shutdown: %w", err)
}''','go','examples/notebook/main.go · excerpt inside run')
section(a,'Make logs answer practical questions','让日志回答具体问题',
'''slog writes structured JSON logs containing a message and named fields. Our startup log records the actual address; request logs record method, path, and duration. Keeping fields separate lets a log viewer filter by path without parsing a sentence.

Build and run the program below. Make a request from another terminal, then press Control+C in the server terminal. A normal shutdown should exit without a “server stopped” error. Start two copies on the same address and the second should fail promptly with a bind error.

A health endpoint currently says only that the process can serve a response. If you add a database, decide whether you also need a separate readiness check. Being alive and being ready to serve useful traffic are different questions.''',
'''slog 输出结构化 JSON 日志，包含消息和具名字段。启动日志记录实际地址，请求日志记录方法、路径和耗时。字段独立后，日志工具可以直接按路径筛选，不必从一句话里重新解析信息。

按下面的方式编译并运行。在另一个终端发出请求，再回到服务终端按 Control+C。正常关闭不应该出现“server stopped”错误。如果在同一地址启动两个实例，第二个应立即因绑定失败退出。

当前健康检查只说明进程可以返回响应。添加数据库后，再决定是否需要独立的就绪检查。“进程还活着”和“已经可以处理有效业务”是两个不同的问题。''',
'''go build -o notebook .
./notebook -addr 127.0.0.1:8080
# Press Control+C to stop.''','sh','Terminal · examples/notebook')
exercise(a,'Why not call Shutdown with the context returned by signal.NotifyContext after its Done channel fires?','signal.NotifyContext 的 Done 已经触发后，为什么不直接把这个 context 传给 Shutdown？','It is already canceled. A fresh context gives shutdown its own bounded period to drain active requests.','它已经被取消。新的 context 才能给关闭流程一段独立、有限的等待时间。')
refs(a,('Server.Shutdown','https://pkg.go.dev/net/http#Server.Shutdown'),('Structured logging','https://pkg.go.dev/log/slog'),('Signal contexts','https://pkg.go.dev/os/signal#NotifyContext'))

a=article('10-persistence','Keep data after the process exits','让数据在重启之后仍然存在','Plan a database adapter, then decide whether a cache is worth adding.','设计数据库适配层，再判断是否需要缓存。',2,16)
section(a,'Replace the store, keep the contract','替换仓库，保留接口约定',
'''The memory store taught us the API without requiring infrastructure. Its next limitation is durability. A SQL implementation of NoteStore can preserve notes across restarts while the handlers keep calling List and Create.

This article is an extension design, not a claim that the supplied server already has a database. To implement it, choose a database and driver, create a notes table with a generated integer primary key and a required title, and write a SQLStore that holds a shared *sql.DB. That value manages a connection pool; it is not a single connection to create for every request.

Create the pool once at startup, verify connectivity with PingContext, inject the store, and close the pool after request shutdown completes. Keep schema migrations as explicit versioned steps. Running a migration is an operational change, not something each request should attempt.''',
'''内存仓库让我们不必安装基础设施，就能学会 API。它接下来的限制是无法持久保存。实现一个 SQL 版 NoteStore 后，处理函数仍然调用 List 和 Create，笔记却能在重启之后保留。

本篇是扩展设计，不代表配套服务器已经连接数据库。实现时，需要选择数据库和驱动，创建包含自动生成整数主键与必填标题的 notes 表，再编写持有共享 *sql.DB 的 SQLStore。这个值管理的是连接池，并不是每次请求都应新建的单条连接。

启动时创建连接池，用 PingContext 检查连通性，注入仓库；请求关闭完成后，再关闭连接池。表结构迁移应使用明确、有版本的步骤。迁移属于运维变更，不应该由每次请求顺便执行。''')
section(a,'Pass data as parameters','通过参数传递数据',
'''SQL and user input must remain separate. The query below is a PostgreSQL-style illustration: $1 is a parameter placeholder, and title is supplied separately. Other drivers may use different placeholders. Do not turn this into string concatenation, even if your current title validator looks strict.

A useful Create operation returns the actual generated ID, so the client can identify the saved note. If a business operation changes several related records, place those changes inside a transaction and handle commit errors. A transaction groups database changes; it does not make an email or another remote service part of the same atomic operation.

List should use a defined order and eventually pagination. Without an ORDER BY, SQL results do not promise a stable order. Test the SQL implementation against a real test database as well as testing handlers with a memory store.''',
'''SQL 与用户输入必须分开。下面是 PostgreSQL 风格的示意：$1 是参数占位符，title 作为独立参数传入。其他驱动可能使用不同的占位符。即使当前标题校验看起来很严格，也不要改成拼接 SQL 字符串。

Create 应返回实际生成的编号，让客户端能识别保存的笔记。如果一次业务操作要修改多条相关记录，就把数据库操作放在事务里，并处理提交错误。事务能组织数据库变更，但不能自动把发邮件或调用其他服务也变成同一项原子操作。

List 应定义排序方式，并最终支持分页。没有 ORDER BY，SQL 结果不承诺稳定顺序。除了用内存仓库测试处理函数，还需要用真实测试数据库验证 SQL 实现。''',
'''// Design excerpt: requires a configured PostgreSQL driver,
// an existing notes table, db *sql.DB, ctx, and title.
var id int
err := db.QueryRowContext(ctx,
    "INSERT INTO notes (title) VALUES ($1) RETURNING id",
    title,
).Scan(&id)
// Check err before returning Note{ID: id, Title: title}.''','go','Design excerpt · not part of the runnable memory example')
section(a,'A cache creates a freshness problem','缓存会引入新鲜度问题',
'''Do not add a cache just because the project has a database. First measure a repeated slow read. A cache can save a result temporarily, but then every write raises a question: what happens to the old cached result?

For a small notes list, a first design might cache GET results briefly and invalidate the list key after a successful Create. Even that has a race: a reader may load old data before a write and put it into the cache after invalidation. Expiration limits how long it stays stale but does not guarantee perfect consistency.

Write down the acceptable freshness window before choosing Redis or any cache library. Keep the database as the durable source of truth. If the cache is unavailable, decide whether the application can fall back to the database without overwhelming it. These are behavioral choices, not just connection settings.''',
'''不要因为有了数据库，就顺手添加缓存。先测量一个确实缓慢、重复发生的读取。缓存能暂存结果，但每次写入都会带来一个问题：旧的缓存结果怎么办？

对于小型笔记列表，可以先考虑短时间缓存 GET 结果，并在 Create 成功后删除列表缓存键。即使这样仍有竞争：读请求可能在写入前取到旧数据，却在缓存删除后才把旧结果重新放回。过期时间能限制陈旧数据存在多久，但不保证完全一致。

选择 Redis 或其他缓存库之前，先明确允许多长的数据延迟。数据库仍然是持久数据来源。缓存不可用时，要决定能否回退数据库，以及回退会不会压垮数据库。这些是行为设计，不只是连接参数。''')
exercise(a,'A note was committed to the database, but updating the cache failed. Should the client blindly retry creation?','笔记已提交到数据库，但更新缓存失败。客户端应该直接重试创建吗？','No. Creation already happened, so an unguarded retry can create a duplicate. Separate the durable write result from cache maintenance and define retry/idempotency behavior.','不应该。创建已经发生，无保护重试可能产生重复数据。应区分持久写入结果与缓存维护结果，并设计重试或幂等行为。')
refs(a,('Database access','https://go.dev/doc/database/'),('SQL parameters','https://go.dev/doc/database/sql-injection'),('Managing connections','https://go.dev/doc/database/manage-connections'))

a=article('11-workflow','Make the easy path repeatable','让正确的工作流程容易重复','Organize files, document the API, and automate a few useful steps.','组织目录、记录接口，并自动化几项真正有用的操作。',2,13)
section(a,'A folder should explain a responsibility','用目录表达职责',
'''Open examples/notebook and read the filenames as a map. main.go owns process startup and shutdown. app.go owns HTTP behavior. store.go owns note storage. mini/mini.go owns reusable HTTP helpers. app_test.go checks the contract across those pieces.

Files in the same directory share package main, so go run . compiles them together. Running go run main.go alone leaves out app.go and store.go and will produce undefined-name errors. This is a frequent beginner problem that has nothing to do with the framework design.

As an application grows, it may deserve cmd/notebook and internal packages. Moving files early is not automatically an improvement. Create a new package when it gives a clear boundary, not because a large repository you saw has more folders.''',
'''打开 examples/notebook，把文件名当成地图。main.go 负责进程启动和关闭，app.go 负责 HTTP 行为，store.go 负责笔记存储，mini/mini.go 负责可复用的 HTTP 辅助能力，app_test.go 检查这些部分共同形成的接口约定。

同一目录的文件共享 package main，因此 go run . 会把它们一起编译。如果只运行 go run main.go，就会漏掉 app.go 和 store.go，出现名称未定义的错误。这是初学者常遇到的问题，与框架设计无关。

随着应用扩大，可以引入 cmd/notebook 和 internal 包。但提前搬文件不一定带来改进。只有在新的包能表达清晰边界时才创建它，不必因为见过大型仓库就模仿更多目录。''')
section(a,'Automate what you already understand','自动化已经理解的步骤',
'''Before writing a generator, agree on one correct example by hand. A generator multiplies the quality of its template, including any mistakes. For this project, formatting, testing, and building are enough useful automation to start with.

The commands below should run from examples/notebook. gofmt rewrites source formatting. go test checks behavior. go build produces a binary you can run without the go run wrapper. Keep generated binaries out of source control.

A file watcher can run these commands after changes, but it must stop the old process before starting the next one. Otherwise “address already in use” may simply mean your watcher left the earlier server alive. Hot reload is a development convenience; it is not the same as graceful deployment.''',
'''写代码生成器之前，先手工确定一个正确示例。生成器会放大模板的质量，也会放大错误。对于当前项目，先自动化格式化、测试和构建，已经足够实用。

下面的命令在 examples/notebook 中运行。gofmt 统一源码格式，go test 验证行为，go build 生成可以直接运行的二进制。生成的二进制文件不应进入源码版本控制。

文件监听器可以在修改后执行这些步骤，但必须先停止旧进程，再启动新进程。否则“address already in use”可能只是监听器遗留了旧服务。热重载是开发便利功能，与优雅发布不是一回事。''',
'''gofmt -w main.go app.go store.go app_test.go mini/mini.go
go test ./...
go build -o notebook .''','sh','Terminal · examples/notebook')
section(a,'Document behavior, including errors','接口文档也要写清楚错误',
'''An API document should let someone use the service without reading its implementation. For POST /notes, include the media type, a request example, the 201 response, title constraints, and the 400, 413, and 415 failure cases. Include the fact that the current store loses data on restart.

The repository supplies api-contract.json as a small human-readable contract, not an OpenAPI document. When another team needs client generation or an interactive explorer, translate the contract into a validated OpenAPI specification and keep it in step with tests. A generated page is only as correct as the specification behind it.

Background jobs deserve a separate lifecycle too. If you later add periodic cleanup, a ticker can trigger local work, but two server instances would both run it. Decide whether duplicate execution is harmless, or whether the job needs a dedicated scheduler and coordination.''',
'''一份 API 文档应该让读者不看实现也能调用服务。对于 POST /notes，要写明媒体类型、请求示例、201 响应、标题限制，以及 400、413、415 失败情况。还要说明当前仓库在重启后会丢失数据。

仓库提供了便于阅读的 api-contract.json，它不是 OpenAPI 文档。当其他团队需要生成客户端或交互式接口浏览器时，可以把约定转换成经过验证的 OpenAPI 规范，并用测试保持同步。生成页面是否正确，取决于背后的规范是否正确。

后台任务也需要独立的生命周期。如果以后添加定时清理，ticker 能触发本地任务，但启动两个服务实例就会执行两次。需要先确定重复执行是否无害，否则就需要专门的调度器和协调机制。''')
exercise(a,'Why can go run main.go fail even though go run . succeeds?','为什么 go run main.go 可能失败，而 go run . 能成功？','The first command builds only the named file. The second builds the package, including app.go and store.go in that directory.','前者只编译指定文件，后者编译整个包，包括同目录的 app.go 和 store.go。')
refs(a,('Go command','https://pkg.go.dev/cmd/go'),('gofmt','https://pkg.go.dev/cmd/gofmt'))

a=article('12-browser','Connect a browser, then draw the trust boundary','连接浏览器，再明确访问边界','Render notes safely and understand what adding accounts really requires.','安全地显示笔记，理解加入账户功能意味着什么。',3,15)
section(a,'The browser is another client','浏览器也是一个客户端',
'''curl helped us focus on HTTP. A browser adds a user interface, but it still sends the same GET and POST requests. The supplied browser-client.html is a small page that reads notes and submits a new title.

To serve it from the notebook application, add the optional route below inside newApp before the return statement. Run the server from examples/notebook so the relative file path resolves. Visit http://127.0.0.1:8080/. The page and API now share an origin, so this experiment does not require cross-origin configuration.

This is an optional extension; the core server intentionally has only the three API routes. Adding the page makes the same data visible in a different client. It does not change where notes are stored or make them durable.''',
'''curl 帮助我们专注 HTTP。浏览器增加了用户界面，但发送的仍然是相同的 GET 和 POST 请求。配套的 browser-client.html 是一个小页面，可以读取笔记并提交新标题。

要通过笔记应用提供它，把下面的可选路由加到 newApp 的 return 之前。从 examples/notebook 目录启动服务，让相对文件路径正确解析。访问 http://127.0.0.1:8080/，页面和 API 就处于同一来源，不需要额外配置跨域。

这是可选扩展。核心服务器刻意只提供三个 API 路由。增加页面只是让另一个客户端看见同一份数据，不会改变笔记存储位置，也不会让它获得持久化能力。''',
'''app.Handle("GET /{$}", func(c *mini.Context) {
    http.ServeFile(c.Writer, c.Request, "browser-client.html")
})''','go','Optional addition · inside newApp in app.go')
section(a,'A successful fetch can still be an HTTP error','fetch 成功返回，不等于业务成功',
'''fetch resolves when it receives an HTTP response, even if that response has a 400 or 500 status. Check response.ok before treating the result as success. A network failure instead rejects the promise, so the page should also catch exceptions and show a useful message.

Render note titles using textContent, not innerHTML. A note is text supplied by a user; interpreting that text as HTML would give it a different and dangerous meaning. The sample page creates list elements and assigns their text content.

The form disables its submit button while saving and refreshes the list only after a successful write. This avoids accidental double clicks in one page, though it is not a complete server-side solution for duplicate requests. Reliable retries require an explicit idempotency design.''',
'''fetch 收到 HTTP 响应后就会正常返回，即使状态码是 400 或 500。因此，把结果当成成功之前需要检查 response.ok。网络故障则会让 Promise 拒绝，所以页面也要捕获异常并显示有用的信息。

显示笔记标题时使用 textContent，不要使用 innerHTML。笔记是用户提供的文字，把它解释成 HTML，会改变它的含义并带来风险。示例页面会创建列表元素，再赋值文本内容。

保存时，表单暂时禁用提交按钮；写入成功后才刷新列表。这能避免同一页面上的误双击，但并不等于服务器已经能处理所有重复请求。可靠重试需要明确的幂等设计。''',
'''const response = await fetch('/notes');
if (!response.ok) throw new Error(`HTTP ${response.status}`);
const notes = await response.json();
for (const note of notes) {
    const item = document.createElement('li');
    item.textContent = note.title;
    list.append(item);
}''','js','browser-client.html · rendering pattern')
section(a,'Accounts change the data model','账户功能会改变数据模型',
'''The local notebook has no accounts. Do not mistake a working form for an access-controlled service. If you add users, each note needs an owner, and both reads and writes must be scoped to the authenticated user. Hiding a button in the browser does not enforce that rule.

Authentication answers who is making the request. Authorization answers whether that person may access this note. A session cookie may help with the first question, but the store query must still enforce ownership for the second. Never trust an owner ID simply because the client included it.

For an account-enabled extension, use established authentication components, password hashing designed for passwords, expiring sessions, secure cookie settings, and a CSRF strategy for cookie-authenticated writes. These features are not implemented in this local example. Add their failure cases to the test plan before exposing personal notes to other users.''',
'''本地笔记程序没有账户。表单能使用，并不代表服务已经有访问控制。如果加入用户，每条笔记都需要归属者，读取和写入都必须限定在已认证用户的范围内。在浏览器里隐藏按钮并不能执行这个规则。

身份认证回答“请求者是谁”，授权回答“这个人能否访问这条笔记”。会话 Cookie 可以帮助解决前一个问题，但后一个问题仍然需要在仓库查询中限制归属。不能因为客户端传来了 owner ID，就相信它。

扩展账户功能时，应使用成熟的认证组件、适合密码的哈希算法、有过期时间的会话、合适的 Cookie 安全属性，以及针对 Cookie 认证写操作的 CSRF 策略。这些不属于当前本地示例已实现的功能。向其他用户开放私人笔记之前，应先补齐相应失败场景的测试。''')
exercise(a,'A user changes a request from note 7 to note 8. Where should ownership be checked?','用户把请求中的笔记 7 改成笔记 8，应该在哪里检查归属？','On the server, using the authenticated identity and a query or service check that scopes access to that owner. Browser controls cannot enforce authorization.','在服务器端，用已认证身份进行限定归属的查询或服务检查。浏览器控件不能承担授权。')
refs(a,('Fetch API','https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch'),('textContent','https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent'))

a=article('13-finish','Ship a small thing you understand','交付一个自己理解的小作品','Run the complete project, inspect its boundaries, and plan the next iteration.','运行完整项目，检查能力边界，规划下一次迭代。',3,15)
section(a,'Trace the whole path once more','重新走一遍完整路径',
'''A POST request reaches the server, passes through the timing middleware, matches a route in Engine, and receives a mini.Context. The handler checks the media type, decodes one bounded JSON value, validates its title, and calls NoteStore.Create. The store assigns an ID under a lock. The handler sends a JSON response and the middleware records elapsed time.

Every piece now has a reason to exist. The framework handles reusable HTTP mechanics. The application owns note rules. The storage implementation owns its synchronization and state. main owns the process lifecycle. You can explain the architecture by following one request rather than memorizing a diagram.

Use the commands below from examples/notebook. In a fresh process, GET /notes returns []; after one successful POST, it returns one note. Run the test suite before and after making your own change.''',
'''一个 POST 请求到达服务器，经过计时中间件，在 Engine 中匹配路由，再获得 mini.Context。处理函数检查媒体类型，解码一个有大小限制的 JSON 值，验证标题，并调用 NoteStore.Create。仓库在锁保护下分配编号，处理函数发送 JSON 响应，中间件记录耗时。

现在，每一部分都有存在的理由。框架负责可复用的 HTTP 机制，应用负责笔记规则，存储实现负责同步和状态，main 负责进程生命周期。你可以通过追踪一次请求解释架构，而不是死记一张图。

下面的命令在 examples/notebook 中执行。新进程的 GET /notes 返回 []；成功 POST 一次后，就会返回一条笔记。尝试自己的修改前后，都运行一次测试。''',
'''go test ./...
go build -o notebook .
./notebook
# In a second terminal:
# curl http://127.0.0.1:8080/notes
# curl -H 'Content-Type: application/json' \
#   -d '{"title":"I can trace a request"}' http://127.0.0.1:8080/notes''','sh','Terminal · examples/notebook')
section(a,'Release is a repeatable process','发布是一套可重复的过程',
'''For this local project, delivery means a tested source tree and a binary built for your operating system. A Linux machine cannot run a macOS binary. Build for the intended target, record the source revision, and keep the runtime configuration separate from the executable.

Before a real deployment, implement durable storage and the access model your users need. Put the server behind appropriate HTTPS termination, run it under a process supervisor, and arrange logs and backups. Changing 127.0.0.1 to a public listen address is not a deployment plan.

A useful release exercise has four steps: start the new version in a test environment, check readiness and one real create/list flow, stop it with the expected signal, and rehearse returning to the previous version. Database migrations may make rollback harder than swapping binaries, so test those changes separately.''',
'''对于这个本地项目，交付意味着经过测试的源码，以及针对目标操作系统构建的二进制。Linux 机器不能直接运行 macOS 二进制。应按目标环境构建，记录源码版本，并把运行配置与可执行文件分开。

真正部署之前，需要实现持久化存储和用户所需的访问模型，配置合适的 HTTPS 入口、进程管理、日志和备份。把监听地址从 127.0.0.1 改成公网地址，并不等于完成了部署方案。

一个实用的发布演练有四步：在测试环境启动新版本，检查就绪状态和真实的创建、读取流程，用预期信号停止服务，再演练恢复上一版本。数据库迁移可能让回退比替换二进制更复杂，因此需要单独验证。''')
section(a,'Choose one next feature and define done','选一个下一步，并写清完成标准',
'''A good next feature is GET /notes/{id}. Start with observable behavior: an existing ID returns one note, an absent ID returns 404, and a malformed ID returns 400. Add a store method, implement it with the same locking discipline, register the route, then test those three cases.

Another useful feature is pagination. Define a maximum page size and a stable ordering before writing the query. A third is persistent storage, using the adapter plan from article 10. Pick one; changing routing, storage, accounts, and deployment together makes failures difficult to isolate.

You have built a small educational framework, not a replacement for every production framework. That is still a meaningful result: you can now judge a library by the work it removes, the behavior it guarantees, and the complexity it adds. Keep the parts that help your application, and let real requirements justify the next abstraction.''',
'''一个合适的下一步是 GET /notes/{id}。先规定可观察行为：存在的编号返回一条笔记，不存在的编号返回 404，格式错误的编号返回 400。然后增加仓库方法，按相同的加锁规则实现，注册路由，再测试这三种情况。

另一个有用的功能是分页。写查询前，先定义最大页大小与稳定排序。第三个方向是按第 10 篇的适配层设计实现持久化。一次选一个方向；同时修改路由、存储、账户和部署，会让故障难以定位。

你已经做出了一个小型教学框架，这并不意味着它替代了所有生产框架。但这项成果很具体：现在你可以根据一个库减少了哪些工作、保证了哪些行为、增加了多少复杂度来评价它。保留真正帮助应用的部分，让实际需求推动下一次抽象。''')
exercise(a,'Define three acceptance checks for your first extension before writing its implementation.','在实现第一个扩展前，先写出三个验收条件。','For GET /notes/{id}: a saved ID returns 200 with the correct note; an absent ID returns 404; a non-integer ID returns 400. These checks guide both implementation and tests.','例如 GET /notes/{id}：已有编号返回 200 和正确笔记，不存在的编号返回 404，非整数编号返回 400。这些条件同时指导实现与测试。')
refs(a,('Go build command','https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies'))

out = ROOT/'content'
out.mkdir(exist_ok=True)
(out/'chapters.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2)+'\n')
(out/'chapters.js').write_text('window.CHAPTERS = '+json.dumps(chapters,ensure_ascii=False,indent=2)+';\n')
print(f'Wrote {len(chapters)} bilingual articles; {sum(len(x["sections"]) for x in chapters)} sections per language.')
