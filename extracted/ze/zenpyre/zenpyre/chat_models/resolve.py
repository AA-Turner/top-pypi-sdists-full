r"""Provide a resolution utility for creating LangChain BaseChatModel
models."""

from __future__ import annotations

__all__ = ["resolve_chat_model"]

from typing import TYPE_CHECKING, Any

from langchain_core.language_models import BaseChatModel

from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING:
    from zenpyre.utils.config import BaseConfig


def resolve_chat_model(
    chat_model: BaseChatModel | dict[str, Any] | BaseConfig,
) -> BaseChatModel:
    """Resolve a LangChain
    :class:`~langchain_core.language_models.BaseChatModel` instance from
    an existing object, a configuration dictionary, or a
    :class:`~zenpyre.utils.config.BaseConfig`.

    If ``chat_model`` is already a
    :class:`~langchain_core.language_models.BaseChatModel` instance
    it is returned as-is.  If it is a :class:`dict` or a
    :class:`~zenpyre.utils.config.BaseConfig`, it is treated as an
    ``objectory`` factory configuration and instantiated via
    :func:`objectory.factory`. See
    :func:`~zenpyre.utils.resolve.resolve_object` for details.

    Args:
        chat_model: Either a fully configured
            :class:`~langchain_core.language_models.BaseChatModel`
            instance, a :class:`dict` containing an ``objectory``
            factory specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name), or a
            :class:`~zenpyre.utils.config.BaseConfig` whose
            ``to_kwargs()`` includes a ``"_target_"`` key.

    Returns:
        A configured
        :class:`~langchain_core.language_models.BaseChatModel`
        instance.

    Raises:
        TypeError: If the resolved object is not a
            :class:`~langchain_core.language_models.BaseChatModel`
            instance.

    Example:
        ```pycon
        >>> from langchain_core.language_models import FakeListChatModel
        >>> from zenpyre.chat_models import resolve_chat_model
        >>> # From an existing instance:
        >>> chat_model = resolve_chat_model(FakeListChatModel(responses=["hello"]))
        >>> # From a configuration dictionary:
        >>> chat_model = resolve_chat_model(  # doctest: +SKIP
        ...     {
        ...         "_target_": "langchain_core.language_models.FakeListChatModel",
        ...         "responses": ["hello"],
        ...     }
        ... )

        ```
    """
    return resolve_object(chat_model, cls=BaseChatModel)
