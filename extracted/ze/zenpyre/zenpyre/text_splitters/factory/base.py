r"""Provide the base factory interface for creating LangChain text
splitter models."""

from __future__ import annotations

__all__ = ["BaseTextSplitterFactory"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_text_splitters import TextSplitter


class BaseTextSplitterFactory(ABC):
    """Abstract base class for text splitter factories.

    Subclasses implement :meth:`make_text_splitter` to instantiate and
    return a configured :class:`~langchain_text_splitters.TextSplitter`
    object.  This pattern decouples text splitter creation from the rest
    of the codebase, making it easy to swap strategies (e.g.
    character-based, recursive, token-based) without changing call sites.

    Example:
        ```pycon
        >>> from langchain_text_splitters import CharacterTextSplitter
        >>> from zenpyre.text_splitters.factory import BaseTextSplitterFactory
        >>> class CharacterTextSplitterFactory(BaseTextSplitterFactory):
        ...     def make_text_splitter(self) -> CharacterTextSplitter:
        ...         return CharacterTextSplitter()
        ...

        ```
    """

    @abstractmethod
    def make_text_splitter(self) -> TextSplitter:
        """Create and return a configured text splitter instance.

        Returns:
            A :class:`~langchain_text_splitters.TextSplitter` instance
            ready for use.
        """
