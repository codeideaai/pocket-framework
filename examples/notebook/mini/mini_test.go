package mini

import (
	"net/http"
	"net/http/httptest"
	"reflect"
	"testing"
)

func TestMiddlewareOrder(t *testing.T) {
	var order []string
	wrap := func(name string) Middleware {
		return func(next http.Handler) http.Handler {
			return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				order = append(order, name+" before")
				next.ServeHTTP(w, r)
				order = append(order, name+" after")
			})
		}
	}
	handler := Chain(http.HandlerFunc(func(http.ResponseWriter, *http.Request) { order = append(order, "app") }), wrap("A"), wrap("B"))
	handler.ServeHTTP(httptest.NewRecorder(), httptest.NewRequest("GET", "/", nil))
	want := []string{"A before", "B before", "app", "B after", "A after"}
	if !reflect.DeepEqual(order, want) {
		t.Fatalf("got %v, want %v", order, want)
	}
}

func TestJSONFailureDoesNotCommitResponse(t *testing.T) {
	response := httptest.NewRecorder()
	ctx := &Context{Writer: response, Request: httptest.NewRequest("GET", "/", nil)}
	if err := ctx.JSON(http.StatusCreated, make(chan int)); err == nil {
		t.Fatal("expected serialization failure")
	}
	if err := ctx.JSON(http.StatusInternalServerError, map[string]string{"error": "cannot encode"}); err != nil {
		t.Fatal(err)
	}
	if response.Code != 500 {
		t.Fatalf("got %d, want 500", response.Code)
	}
}
