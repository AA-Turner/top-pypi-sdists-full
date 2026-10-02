r"""Provide the base factory interface for creating LangChain
BaseChatModel models."""

from __future__ import annotations

__all__ = ["BaseChatModelFactory"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel


class BaseChatModelFactory(ABC):
    """Abstract base class for LangChain
    :class:`~langchain_core.language_models.BaseChatModel` factories.

    Subclasses implement :meth:`make_chat_model` to instantiate and
    return a configured
    :class:`~langchain_core.language_models.BaseChatModel` object.
    This pattern decouples chat model creation from the rest of the
    codebase, making it easy to swap chat models (e.g. OpenAI,
    Anthropic, a fake model for testing) without changing call sites.

    Example:
        ```pycon
        >>> from langchain_core.language_models import BaseChatModel, FakeListChatModel
        >>> from zenpyre.chat_models.factory import BaseChatModelFactory
        >>> class MyChatModelFactory(BaseChatModelFactory):
        ...     def make_chat_model(self) -> BaseChatModel:
        ...         return FakeListChatModel(responses=["hello"])
        ...
        >>> factory = MyChatModelFactory()
        >>> chat_model = factory.make_chat_model()

        ```
    """

    @abstractmethod
    def make_chat_model(self) -> BaseChatModel:
        """Create and return a configured BaseChatModel instance.

        Returns:
            A :class:`~langchain_core.language_models.BaseChatModel`
            instance ready for use.
        """
