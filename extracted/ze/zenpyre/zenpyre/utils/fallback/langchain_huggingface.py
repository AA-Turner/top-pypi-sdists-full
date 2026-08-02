r"""Contain fallback implementations used when ``langchain_huggingface``
dependency is not available."""

from __future__ import annotations

__all__ = ["HuggingFaceEmbeddings", "langchain_huggingface"]

from types import ModuleType
from typing import Any

from zenpyre.utils.imports import raise_langchain_huggingface_missing_error


class FakeClass:
    r"""Fake class that raises an error because langchain_huggingface is
    not installed.

    Args:
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Raises:
        RuntimeError: langchain_huggingface is required for this functionality.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
        raise_langchain_huggingface_missing_error()


HuggingFaceEmbeddings = FakeClass

# Create a fake langchain_huggingface package
langchain_huggingface: ModuleType = ModuleType("langchain_huggingface")
langchain_huggingface.HuggingFaceEmbeddings = HuggingFaceEmbeddings
