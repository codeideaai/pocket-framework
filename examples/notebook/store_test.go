package main

import (
	"context"
	"sync"
	"testing"
)

func TestConcurrentCreatesAndSnapshot(t *testing.T) {
	store := &MemoryStore{}
	const total = 64
	var group sync.WaitGroup
	for i := 0; i < total; i++ {
		group.Add(1)
		go func() {
			defer group.Done()
			if _, err := store.Create(context.Background(), "note"); err != nil {
				t.Error(err)
			}
		}()
	}
	group.Wait()
	notes, err := store.List(context.Background())
	if err != nil {
		t.Fatal(err)
	}
	if len(notes) != total {
		t.Fatalf("got %d notes, want %d", len(notes), total)
	}
	seen := make(map[int]bool)
	for _, note := range notes {
		if seen[note.ID] {
			t.Fatalf("duplicate ID %d", note.ID)
		}
		seen[note.ID] = true
	}
	notes[0].Title = "changed outside the store"
	again, _ := store.List(context.Background())
	if again[0].Title != "note" {
		t.Fatal("List leaked the store's slice")
	}
}

func TestCanceledCreateDoesNotWrite(t *testing.T) {
	store := &MemoryStore{}
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	if _, err := store.Create(ctx, "should not exist"); err != context.Canceled {
		t.Fatalf("got %v, want context.Canceled", err)
	}
	notes, _ := store.List(context.Background())
	if len(notes) != 0 {
		t.Fatal("canceled operation changed state")
	}
}
