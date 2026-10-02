r"""Provide a configurable factory for LangChain text splitter
models."""

from __future__ import annotations

__all__ = ["ConfigurableTextSplitterFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.text_splitters.factory.base import BaseTextSplitterFactory
from zenpyre.text_splitters.resolve import resolve_text_splitter

if TYPE_CHECKING:
    from langchain_text_splitters import TextSplitter


class ConfigurableTextSplitterFactory(BaseTextSplitterFactory, MultilineDisplayMixin):
    """A concrete text splitter factory that accepts either a pre-built
    :class:`~langchain_text_splitters.TextSplitter` instance or a
    configuration dictionary.

    When a dict is provided it is resolved at each
    :meth:`make_text_splitter` call via :func:`~resolve_text_splitter`,
    which uses ``objectory`` to instantiate the configured class.
    When an instance is provided it is returned as-is.

    Args:
        text_splitter: A fully configured
            :class:`~langchain_text_splitters.TextSplitter` instance, or
            a :class:`dict` containing an ``objectory`` factory
            specification (must include a ``"_target_"`` key pointing to
            the fully-qualified class name).

    Example:
        ```pycon
        >>> from langchain_text_splitters import CharacterTextSplitter
        >>> from zenpyre.text_splitters.factory import ConfigurableTextSplitterFactory
        >>> factory = ConfigurableTextSplitterFactory(CharacterTextSplitter())
        >>> text_splitter = factory.make_text_splitter()

        ```
    """

    def __init__(self, text_splitter: TextSplitter | dict[str, Any]) -> None:
        self._text_splitter = text_splitter

    def make_text_splitter(self) -> TextSplitter:
        return resolve_text_splitter(self._text_splitter)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"text_splitter": self._text_splitter}
