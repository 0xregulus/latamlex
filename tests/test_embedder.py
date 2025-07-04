

import json
import numpy as np
import pytest
from pathlib import Path
from app.embedder import load_chunks, build_faiss_index

def test_load_chunks(tmp_path):
    # Prepare a temporary JSONL file
    data = [
        {"id": "test-0", "text": "chunk zero"},
        {"id": "test-1", "text": "chunk one"},
    ]
    file_path = tmp_path / "chunks.jsonl"
    with open(file_path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    # Call load_chunks
    ids, chunks = load_chunks(file_path)
    assert ids == ["test-0", "test-1"]
    assert chunks == ["chunk zero", "chunk one"]

def test_build_faiss_index():
    # Create dummy embeddings of shape (4, 5)
    embeddings = np.random.rand(4, 5).astype(np.float32)
    index = build_faiss_index(embeddings)
    # Verify number of indexed vectors
    assert index.ntotal == 4
    # Test search returns correct shapes and values
    query = embeddings[:2]
    D, I = index.search(query, 2)
    assert D.shape == (2, 2)
    assert I.shape == (2, 2)
    # Nearest neighbor of each vector should be itself (distance=0)
    assert np.allclose(D[:, 0], 0.0)
    assert all(I[i, 0] == i for i in range(2))