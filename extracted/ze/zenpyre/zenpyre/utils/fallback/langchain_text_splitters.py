r"""Contain fallback implementations used when
``langchain_text_splitters`` dependency is not available."""

from __future__ import annotations

__all__ = ["TextSplitter", "langchain_text_splitters"]

from types import ModuleType
from typing import Any

from zenpyre.utils.imports import raise_langchain_text_splitters_missing_error


class FakeClass:
    r"""Fake class that raises an error because langchain_text_splitters
    is not installed.

    Args:
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Raises:
        RuntimeError: langchain_text_splitters is required for this functionality.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
        raise_langchain_text_splitters_missing_error()


TextSplitter = FakeClass

# Create a fake langchain_text_splitters package
langchain_text_splitters: ModuleType = ModuleType("langchain_text_splitters")
langchain_text_splitters.TextSplitter = TextSplitter
