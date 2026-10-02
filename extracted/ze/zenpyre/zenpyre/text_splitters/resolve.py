r"""Provide a resolution utility for creating LangChain text splitter
models."""

from __future__ import annotations

__all__ = ["resolve_text_splitter"]

from typing import TYPE_CHECKING, Any

from zenpyre.utils.imports import is_langchain_text_splitters_available
from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING or is_langchain_text_splitters_available():
    from langchain_text_splitters import TextSplitter
else:  # pragma: no cover
    from zenpyre.utils.fallback.langchain_text_splitters import TextSplitter

if TYPE_CHECKING:
    from zenpyre.utils.config import BaseConfig


def resolve_text_splitter(
    text_splitter: TextSplitter | dict[str, Any] | BaseConfig,
) -> TextSplitter:
    """Resolve a LangChain
    :class:`~langchain_text_splitters.TextSplitter` instance from an
    existing object, a configuration dictionary, or a
    :class:`~zenpyre.utils.config.BaseConfig`.

    If ``text_splitter`` is already a
    :class:`~langchain_text_splitters.TextSplitter` instance it is
    returned as-is.  If it is a :class:`dict` or a
    :class:`~zenpyre.utils.config.BaseConfig`, it is treated as an
    ``objectory`` factory configuration and instantiated via
    :func:`objectory.factory`. See
    :func:`~zenpyre.utils.resolve.resolve_object` for details.

    Args:
        text_splitter: Either a fully configured
            :class:`~langchain_text_splitters.TextSplitter` instance, a
            :class:`dict` containing an ``objectory`` factory
            specification (must include a ``"_target_"`` key pointing to
            the fully-qualified class name), or a
            :class:`~zenpyre.utils.config.BaseConfig` whose
            ``to_kwargs()`` includes a ``"_target_"`` key.

    Returns:
        A configured :class:`~langchain_text_splitters.TextSplitter`
        instance.

    Raises:
        TypeError: If the resolved object is not a
            :class:`~langchain_text_splitters.TextSplitter` instance.

    Example:
        ```pycon
        >>> from zenpyre.text_splitters import resolve_text_splitter
        >>> from langchain_text_splitters import CharacterTextSplitter
        >>> # From an existing instance:
        >>> text_splitter = resolve_text_splitter(CharacterTextSplitter())
        >>> # From a configuration dictionary:
        >>> text_splitter = resolve_text_splitter(
        ...     {"_target_": "langchain_text_splitters.CharacterTextSplitter"}
        ... )

        ```
    """
    return resolve_object(text_splitter, cls=TextSplitter)
