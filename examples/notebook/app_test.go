package main

import (
	"encoding/json"
	"io"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestNotebookContract(t *testing.T) {
	handler := newApp(&MemoryStore{}, slog.New(slog.NewTextHandler(io.Discard, nil)))
	cases := []struct {
		method, path, contentType, body string
		status                          int
	}{
		{"GET", "/notes", "", "", 200},
		{"POST", "/notes", "application/json", `{"title":"First note"}`, 201},
		{"POST", "/notes", "application/json", `{"title":" "}`, 400},
		{"POST", "/notes", "application/json", `{"title":"a","extra":true}`, 400},
		{"POST", "/notes", "application/json", `{"title":"a"} {}`, 400},
		{"POST", "/notes", "application/json", `{"title":`, 400},
		{"POST", "/notes", "text/plain", `{"title":"a"}`, 415},
		{"POST", "/notes", "application/json", `{"title":"` + strings.Repeat("x", 5000) + `"}`, 413},
		{"DELETE", "/notes", "", "", 405},
		{"GET", "/missing", "", "", 404},
	}
	for _, tc := range cases {
		req := httptest.NewRequest(tc.method, tc.path, strings.NewReader(tc.body))
		if tc.contentType != "" {
			req.Header.Set("Content-Type", tc.contentType)
		}
		res := httptest.NewRecorder()
		handler.ServeHTTP(res, req)
		if res.Code != tc.status {
			t.Errorf("%s %s: got %d, want %d: %s", tc.method, tc.path, res.Code, tc.status, res.Body.String())
		}
	}
	res := httptest.NewRecorder()
	handler.ServeHTTP(res, httptest.NewRequest(http.MethodGet, "/notes", nil))
	var notes []Note
	if err := json.Unmarshal(res.Body.Bytes(), &notes); err != nil {
		t.Fatal(err)
	}
	if len(notes) != 1 || notes[0].Title != "First note" {
		t.Fatalf("unexpected saved notes: %+v", notes)
	}
}
