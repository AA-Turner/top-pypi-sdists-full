r"""Provide an agent factory that wraps a chat model factory in an
AgentChatModel."""

from __future__ import annotations

__all__ = ["AgentChatModelFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin
from coola.utils.string import truncate_str

from zenpyre.agents.chat_model import AgentChatModel
from zenpyre.agents.factory.base import BaseAgentFactory
from zenpyre.chat_models.factory.base import BaseChatModelFactory
from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING:
    from zenpyre.utils.config import BaseConfig


class AgentChatModelFactory(BaseAgentFactory, MultilineDisplayMixin):
    """A concrete agent factory that builds a fresh
    :class:`~zenpyre.agents.AgentChatModel` on each :meth:`make_agent`
    call, wrapping the chat model produced by a
    :class:`~zenpyre.chat_models.factory.base.BaseChatModelFactory`.

    Each call to :meth:`make_agent` calls
    ``chat_model_factory.make_chat_model()`` and wraps the resulting
    chat model in a new
    :class:`~zenpyre.agents.AgentChatModel`, together with
    ``system_prompt`` and ``response_format``. This composes with any
    :class:`~zenpyre.chat_models.factory.base.BaseChatModelFactory`
    implementation (e.g.
    :class:`~zenpyre.chat_models.factory.ChatModelFactory`,
    :class:`~zenpyre.chat_models.factory.ConfigurableChatModelFactory`),
    keeping chat model creation and agent creation decoupled.

    Args:
        chat_model_factory: The factory used to build the chat model
            wrapped by the created agent.
        system_prompt: An optional system prompt forwarded to
            :class:`~zenpyre.agents.AgentChatModel`. See its docstring
            for details.
        response_format: An optional schema forwarded to
            :class:`~zenpyre.agents.AgentChatModel`. See its docstring
            for details.

    Example:
        ```pycon
        >>> from langchain_core.language_models import FakeListChatModel
        >>> from zenpyre.agents.factory import AgentChatModelFactory
        >>> from zenpyre.chat_models.factory import ChatModelFactory
        >>> factory = AgentChatModelFactory(
        ...     chat_model_factory=ChatModelFactory(FakeListChatModel(responses=["hello"])),
        ...     system_prompt="You are helpful.",
        ... )
        >>> agent = factory.make_agent()

        ```
    """

    def __init__(
        self,
        chat_model_factory: BaseChatModelFactory | dict[str, Any] | BaseConfig,
        system_prompt: str | None = None,
        response_format: Any | None = None,
    ) -> None:
        self._chat_model_factory = resolve_object(chat_model_factory, cls=BaseChatModelFactory)
        self._system_prompt = system_prompt
        self._response_format = response_format

    def make_agent(self) -> AgentChatModel:
        return AgentChatModel(
            model=self._chat_model_factory.make_chat_model(),
            system_prompt=self._system_prompt,
            response_format=self._response_format,
        )

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {
            "chat_model_factory": self._chat_model_factory,
            "system_prompt": truncate_str(self._system_prompt) if self._system_prompt else None,
            "response_format": self._response_format,
        }
