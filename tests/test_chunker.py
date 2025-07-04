from app.chunker import chunk_text

def test_chunk_text_returns_expected_length():
    text = "palabra " * 1000
    chunks = chunk_text(text, max_tokens=100, overlap=10)
    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)