import pytest
import os
from unittest.mock import patch, MagicMock
import numpy as np

def test_retrieve_similar_chunks(monkeypatch):
    # Ensure OpenAI API key is available
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")

    import app.qa_chain as qa_chain

    # Patch the client.chat.completions.create method
    mock_create = MagicMock()
    mock_create.return_value.choices = [{"message": {"content": "fake answer"}}]
    qa_chain.client.chat.completions.create = mock_create

    mock_model = MagicMock()
    mock_model.encode.return_value = np.ones((1, 384), dtype=np.float32)  # Replace 384 with the actual dimension if different

    results = qa_chain.retrieve_similar_chunks("¿Qué dice la ley?", "argentina", mock_model, 1)
    assert isinstance(results, list)


def test_generate_answer(monkeypatch):
    # Ensure OpenAI API key is available
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")

    import app.qa_chain as qa_chain

    # Mock the client response
    mock_message = MagicMock()
    mock_message.content = "Mock answer"
    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock(message=mock_message)]
    qa_chain.client.chat.completions.create = MagicMock(return_value=mock_resp)

    # Prepare context chunks: (text, id, distance)
    context_chunks = [
        ("chunk one text", "chunk-1", 0.0),
        ("chunk two text", "chunk-2", 0.0),
    ]

    result = qa_chain.generate_answer("Test question?", context_chunks)

    # Validate that the mocked answer appears and sources + references are included
    assert "Mock answer" in result
    assert "Fuentes:" in result
    assert "[chunk-1]:" in result
    assert "Referencias utilizadas:" in result