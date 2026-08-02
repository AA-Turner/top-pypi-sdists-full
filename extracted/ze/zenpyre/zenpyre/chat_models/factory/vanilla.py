r"""Provide a concrete default factory for LangChain BaseChatModel
models."""

from __future__ import annotations

__all__ = ["ChatModelFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.chat_models.factory.base import BaseChatModelFactory

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel


class ChatModelFactory(BaseChatModelFactory, MultilineDisplayMixin):
    """A concrete BaseChatModel factory that wraps a pre-built
    :class:`~langchain_core.language_models.BaseChatModel` instance.

    Use this when the chat model is already instantiated and you
    simply want to wrap it in the :class:`~BaseChatModelFactory`
    interface — for example, when injecting a fixed chat model into a
    component that expects a factory.

    Args:
        chat_model: A fully configured
            :class:`~langchain_core.language_models.BaseChatModel`
            instance to return from :meth:`make_chat_model`.

    Example:
        ```pycon
        >>> from langchain_core.language_models import FakeListChatModel
        >>> from zenpyre.chat_models.factory import ChatModelFactory
        >>> factory = ChatModelFactory(FakeListChatModel(responses=["hello"]))
        >>> chat_model = factory.make_chat_model()

        ```
    """

    def __init__(self, chat_model: BaseChatModel) -> None:
        self._chat_model = chat_model

    def make_chat_model(self) -> BaseChatModel:
        return self._chat_model

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"chat_model": self._chat_model}
