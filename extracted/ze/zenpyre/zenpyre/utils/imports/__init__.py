r"""Helpers to detect and validate optional dependencies."""

from __future__ import annotations

__all__ = [
    "check_duckdb",
    "check_faker",
    "check_langchain_anthropic",
    "check_langchain_chroma",
    "check_langchain_google_genai",
    "check_langchain_huggingface",
    "check_langchain_ollama",
    "check_langchain_openai",
    "check_langchain_text_splitters",
    "check_persista",
    "duckdb_available",
    "faker_available",
    "is_duckdb_available",
    "is_faker_available",
    "is_langchain_anthropic_available",
    "is_langchain_chroma_available",
    "is_langchain_google_genai_available",
    "is_langchain_huggingface_available",
    "is_langchain_ollama_available",
    "is_langchain_openai_available",
    "is_langchain_text_splitters_available",
    "is_persista_available",
    "langchain_anthropic_available",
    "langchain_chroma_available",
    "langchain_google_genai_available",
    "langchain_huggingface_available",
    "langchain_ollama_available",
    "langchain_openai_available",
    "langchain_text_splitters_available",
    "persista_available",
    "raise_duckdb_missing_error",
    "raise_faker_missing_error",
    "raise_langchain_anthropic_missing_error",
    "raise_langchain_chroma_missing_error",
    "raise_langchain_google_genai_missing_error",
    "raise_langchain_huggingface_missing_error",
    "raise_langchain_ollama_missing_error",
    "raise_langchain_openai_missing_error",
    "raise_langchain_text_splitters_missing_error",
    "raise_persista_missing_error",
]

from zenpyre.utils.imports.duckdb import (
    check_duckdb,
    duckdb_available,
    is_duckdb_available,
    raise_duckdb_missing_error,
)
from zenpyre.utils.imports.faker import (
    check_faker,
    faker_available,
    is_faker_available,
    raise_faker_missing_error,
)
from zenpyre.utils.imports.langchain_anthropic import (
    check_langchain_anthropic,
    is_langchain_anthropic_available,
    langchain_anthropic_available,
    raise_langchain_anthropic_missing_error,
)
from zenpyre.utils.imports.langchain_chroma import (
    check_langchain_chroma,
    is_langchain_chroma_available,
    langchain_chroma_available,
    raise_langchain_chroma_missing_error,
)
from zenpyre.utils.imports.langchain_google_genai import (
    check_langchain_google_genai,
    is_langchain_google_genai_available,
    langchain_google_genai_available,
    raise_langchain_google_genai_missing_error,
)
from zenpyre.utils.imports.langchain_huggingface import (
    check_langchain_huggingface,
    is_langchain_huggingface_available,
    langchain_huggingface_available,
    raise_langchain_huggingface_missing_error,
)
from zenpyre.utils.imports.langchain_ollama import (
    check_langchain_ollama,
    is_langchain_ollama_available,
    langchain_ollama_available,
    raise_langchain_ollama_missing_error,
)
from zenpyre.utils.imports.langchain_openai import (
    check_langchain_openai,
    is_langchain_openai_available,
    langchain_openai_available,
    raise_langchain_openai_missing_error,
)
from zenpyre.utils.imports.langchain_text_splitters import (
    check_langchain_text_splitters,
    is_langchain_text_splitters_available,
    langchain_text_splitters_available,
    raise_langchain_text_splitters_missing_error,
)
from zenpyre.utils.imports.persista import (
    check_persista,
    is_persista_available,
    persista_available,
    raise_persista_missing_error,
)
