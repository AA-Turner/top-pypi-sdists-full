r"""Define some pytest fixtures for testing.

`pytest` is required to use these fixtures.
"""

from __future__ import annotations

__all__ = [
    "duckdb_available",
    "duckdb_not_available",
    "faker_available",
    "faker_not_available",
    "langchain_anthropic_available",
    "langchain_anthropic_not_available",
    "langchain_chroma_available",
    "langchain_chroma_not_available",
    "langchain_google_genai_available",
    "langchain_google_genai_not_available",
    "langchain_huggingface_available",
    "langchain_huggingface_not_available",
    "langchain_ollama_available",
    "langchain_ollama_not_available",
    "langchain_openai_available",
    "langchain_openai_not_available",
    "langchain_text_splitters_available",
    "langchain_text_splitters_not_available",
    "persista_available",
    "persista_not_available",
]

import pytest

from zenpyre.utils.imports import (
    is_duckdb_available,
    is_faker_available,
    is_langchain_anthropic_available,
    is_langchain_chroma_available,
    is_langchain_google_genai_available,
    is_langchain_huggingface_available,
    is_langchain_ollama_available,
    is_langchain_openai_available,
    is_langchain_text_splitters_available,
    is_persista_available,
)

duckdb_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_duckdb_available(), reason="Requires duckdb"
)
duckdb_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_duckdb_available(), reason="Skip if duckdb is available"
)

faker_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_faker_available(), reason="Requires faker"
)
faker_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_faker_available(), reason="Skip if faker is available"
)

langchain_anthropic_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_langchain_anthropic_available(), reason="Requires langchain_anthropic"
)
langchain_anthropic_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_langchain_anthropic_available(), reason="Skip if langchain_anthropic is available"
)

langchain_chroma_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_langchain_chroma_available(), reason="Requires langchain_chroma"
)
langchain_chroma_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_langchain_chroma_available(), reason="Skip if langchain_chroma is available"
)


langchain_google_genai_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_langchain_google_genai_available(), reason="Requires langchain_google_genai"
)
langchain_google_genai_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_langchain_google_genai_available(), reason="Skip if langchain_google_genai is available"
)

langchain_huggingface_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_langchain_huggingface_available(), reason="Requires langchain_huggingface"
)
langchain_huggingface_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_langchain_huggingface_available(), reason="Skip if langchain_huggingface is available"
)

langchain_ollama_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_langchain_ollama_available(), reason="Requires langchain_ollama"
)
langchain_ollama_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_langchain_ollama_available(), reason="Skip if langchain_ollama is available"
)

langchain_openai_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_langchain_openai_available(), reason="Requires langchain_openai"
)
langchain_openai_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_langchain_openai_available(), reason="Skip if langchain_openai is available"
)

langchain_text_splitters_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_langchain_text_splitters_available(), reason="Requires langchain_text_splitters"
)
langchain_text_splitters_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_langchain_text_splitters_available(), reason="Skip if langchain_text_splitters is available"
)

persista_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_persista_available(), reason="Requires persista"
)
persista_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_persista_available(), reason="Skip if persista is available"
)
