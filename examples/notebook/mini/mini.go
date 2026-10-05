package mini

import (
	"encoding/json"
	"net/http"
)

// Context belongs to one request. It is not a dependency container.
type Context struct {
	Writer  http.ResponseWriter
	Request *http.Request
}

func (c *Context) JSON(status int, value any) error {
	data, err := json.Marshal(value)
	if err != nil {
		return err
	}
	c.Writer.Header().Set("Content-Type", "application/json; charset=utf-8")
	c.Writer.WriteHeader(status)
	_, err = c.Writer.Write(append(data, '\n'))
	return err
}

type Handler func(*Context)
type Middleware func(http.Handler) http.Handler

type Engine struct{ mux *http.ServeMux }

func New() *Engine { return &Engine{mux: http.NewServeMux()} }

func (e *Engine) Handle(pattern string, handler Handler) {
	e.mux.HandleFunc(pattern, func(w http.ResponseWriter, r *http.Request) {
		handler(&Context{Writer: w, Request: r})
	})
}

func (e *Engine) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	e.mux.ServeHTTP(w, r)
}

// The first middleware is the outermost wrapper.
func Chain(handler http.Handler, middleware ...Middleware) http.Handler {
	for i := len(middleware) - 1; i >= 0; i-- {
		handler = middleware[i](handler)
	}
	return handler
}
