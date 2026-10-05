package main

import (
	"context"
	"sync"
)

type Note struct {
	ID    int    `json:"id"`
	Title string `json:"title"`
}

type NoteStore interface {
	List(context.Context) ([]Note, error)
	Create(context.Context, string) (Note, error)
}

type MemoryStore struct {
	mu     sync.Mutex
	notes  []Note
	nextID int
}

func (s *MemoryStore) List(ctx context.Context) ([]Note, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if err := ctx.Err(); err != nil {
		return nil, err
	}
	result := make([]Note, len(s.notes))
	copy(result, s.notes)
	return result, nil
}

func (s *MemoryStore) Create(ctx context.Context, title string) (Note, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if err := ctx.Err(); err != nil {
		return Note{}, err
	}
	s.nextID++
	note := Note{ID: s.nextID, Title: title}
	s.notes = append(s.notes, note)
	return note, nil
}
