package main

import (
	"encoding/json"
	"errors"
	"io"
	"log/slog"
	"mime"
	"net/http"
	"strings"
	"time"
	"unicode/utf8"

	"example.com/notebook/mini"
)

func reply(c *mini.Context, logger *slog.Logger, status int, value any) {
	if err := c.JSON(status, value); err != nil {
		logger.Error("response failed", "error", err)
	}
}

func newApp(store NoteStore, logger *slog.Logger) http.Handler {
	app := mini.New()
	app.Handle("GET /health", func(c *mini.Context) {
		reply(c, logger, http.StatusOK, map[string]string{"status": "ok"})
	})
	app.Handle("GET /notes", func(c *mini.Context) {
		notes, err := store.List(c.Request.Context())
		if err != nil {
			reply(c, logger, http.StatusInternalServerError, map[string]string{"error": "cannot list notes"})
			return
		}
		reply(c, logger, http.StatusOK, notes)
	})
	app.Handle("POST /notes", func(c *mini.Context) {
		mediaType, _, err := mime.ParseMediaType(c.Request.Header.Get("Content-Type"))
		if err != nil || mediaType != "application/json" {
			reply(c, logger, http.StatusUnsupportedMediaType, map[string]string{"error": "use application/json"})
			return
		}
		c.Request.Body = http.MaxBytesReader(c.Writer, c.Request.Body, 4096)
		defer c.Request.Body.Close()
		var input struct {
			Title string `json:"title"`
		}
		dec := json.NewDecoder(c.Request.Body)
		dec.DisallowUnknownFields()
		err = dec.Decode(&input)
		if err == nil {
			var extra any
			if nextErr := dec.Decode(&extra); nextErr != io.EOF {
				if nextErr == nil {
					err = errors.New("multiple JSON values")
				} else {
					err = nextErr
				}
			}
		}
		if err != nil {
			status := http.StatusBadRequest
			var sizeErr *http.MaxBytesError
			if errors.As(err, &sizeErr) {
				status = http.StatusRequestEntityTooLarge
			}
			reply(c, logger, status, map[string]string{"error": "send one JSON object, at most 4096 bytes"})
			return
		}
		title := strings.TrimSpace(input.Title)
		if title == "" || utf8.RuneCountInString(title) > 120 {
			reply(c, logger, http.StatusBadRequest, map[string]string{"error": "title must contain 1–120 Unicode code points"})
			return
		}
		note, err := store.Create(c.Request.Context(), title)
		if err != nil {
			reply(c, logger, http.StatusInternalServerError, map[string]string{"error": "cannot create note"})
			return
		}
		reply(c, logger, http.StatusCreated, note)
	})
	return mini.Chain(app, accessLog(logger))
}

func accessLog(logger *slog.Logger) mini.Middleware {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			start := time.Now()
			next.ServeHTTP(w, r)
			logger.Info("request", "method", r.Method, "path", r.URL.Path, "duration", time.Since(start))
		})
	}
}
