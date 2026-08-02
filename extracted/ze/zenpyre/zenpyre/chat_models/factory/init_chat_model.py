r"""Provide a chat model factory that wraps
``langchain.chat_models.init_chat_model``."""

from __future__ import annotations

__all__ = ["InitChatModelFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin
from langchain.chat_models import init_chat_model

from zenpyre.chat_models.factory.base import BaseChatModelFactory

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel


class InitChatModelFactory(BaseChatModelFactory, MultilineDisplayMixin):
    """A concrete BaseChatModel factory that wraps
    ``langchain.chat_models.init_chat_model``, building a fresh chat
    model on each :meth:`make_chat_model` call.

    Each call to :meth:`make_chat_model` forwards ``model`` and any
    additional keyword arguments to ``init_chat_model``, which
    resolves the appropriate provider integration (e.g. from a
    ``"provider:model"`` string or ``model_provider``) and
    instantiates it.

    Args:
        model: The model name, optionally prefixed with its provider
            (e.g. ``"openai:gpt-4o"``). Forwarded as-is to
            ``init_chat_model``.
        **kwargs: Additional keyword arguments forwarded as-is to
            ``init_chat_model`` (e.g. ``model_provider``,
            ``configurable_fields``, ``config_prefix``, or any
            provider-specific parameter such as ``temperature``). See
            ``init_chat_model``'s own documentation for the full list
            of accepted arguments.

    Example:
        ```pycon
        >>> from zenpyre.chat_models.factory import InitChatModelFactory
        >>> factory = InitChatModelFactory(model="openai:gpt-4o-mini", api_key="sk-...")
        >>> chat_model = factory.make_chat_model()

        ```
    """

    def __init__(self, model: str | None = None, **kwargs: Any) -> None:
        self._model = model
        self._kwargs = kwargs

    def make_chat_model(self) -> BaseChatModel:
        return init_chat_model(self._model, **self._kwargs)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"model": self._model, **self._kwargs}
