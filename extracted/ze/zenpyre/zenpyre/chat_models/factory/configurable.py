r"""Provide a configurable factory for LangChain BaseChatModel
models."""

from __future__ import annotations

__all__ = ["ConfigurableChatModelFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.chat_models.factory.base import BaseChatModelFactory
from zenpyre.chat_models.resolve import resolve_chat_model

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel


class ConfigurableChatModelFactory(BaseChatModelFactory, MultilineDisplayMixin):
    """A concrete BaseChatModel factory that accepts either a pre-built
    :class:`~langchain_core.language_models.BaseChatModel` instance or a
    configuration dictionary.

    When a dict is provided it is resolved at each
    :meth:`make_chat_model` call via
    :func:`~zenpyre.chat_models.resolve.resolve_chat_model`, which
    uses ``objectory`` to instantiate the configured class.  When an
    instance is provided it is returned as-is.

    Args:
        chat_model: A fully configured
            :class:`~langchain_core.language_models.BaseChatModel`
            instance, or a :class:`dict` containing an ``objectory``
            factory specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name).

    Example:
        ```pycon
        >>> from langchain_core.language_models import FakeListChatModel
        >>> from zenpyre.chat_models.factory import ConfigurableChatModelFactory
        >>> factory = ConfigurableChatModelFactory(FakeListChatModel(responses=["hello"]))
        >>> chat_model = factory.make_chat_model()

        ```
    """

    def __init__(self, chat_model: BaseChatModel | dict[str, Any]) -> None:
        self._chat_model = chat_model

    def make_chat_model(self) -> BaseChatModel:
        return resolve_chat_model(self._chat_model)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"chat_model": self._chat_model}
