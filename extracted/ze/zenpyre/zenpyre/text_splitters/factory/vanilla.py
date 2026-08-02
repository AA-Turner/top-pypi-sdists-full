r"""Provide a concrete default factory for LangChain text splitter
models."""

from __future__ import annotations

__all__ = ["TextSplitterFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.text_splitters.factory.base import BaseTextSplitterFactory

if TYPE_CHECKING:
    from langchain_text_splitters import TextSplitter


class TextSplitterFactory(BaseTextSplitterFactory, MultilineDisplayMixin):
    """A concrete text splitter factory that wraps a pre-built
    :class:`~langchain_text_splitters.TextSplitter` instance.

    Use this when the text splitter is already instantiated and you
    simply want to wrap it in the :class:`~BaseTextSplitterFactory`
    interface — for example, when injecting a fixed text splitter into
    a component that expects a factory.

    Args:
        text_splitter: A fully configured
            :class:`~langchain_text_splitters.TextSplitter` instance to
            return from :meth:`make_text_splitter`.

    Example:
        ```pycon
        >>> from langchain_text_splitters import CharacterTextSplitter
        >>> from zenpyre.text_splitters.factory import TextSplitterFactory
        >>> factory = TextSplitterFactory(CharacterTextSplitter())
        >>> text_splitter = factory.make_text_splitter()

        ```
    """

    def __init__(self, text_splitter: TextSplitter) -> None:
        self._text_splitter = text_splitter

    def make_text_splitter(self) -> TextSplitter:
        return self._text_splitter

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"text_splitter": self._text_splitter}
