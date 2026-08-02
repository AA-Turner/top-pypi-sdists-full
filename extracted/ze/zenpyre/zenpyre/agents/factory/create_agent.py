r"""Provide an agent factory that wraps
``langchain.agents.create_agent``."""

from __future__ import annotations

__all__ = ["CreateAgentFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin
from coola.utils.string import truncate_str
from langchain.agents import create_agent

from zenpyre.agents.factory.base import BaseAgentFactory
from zenpyre.chat_models.factory.base import BaseChatModelFactory
from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable

    from zenpyre.utils.config import BaseConfig


class CreateAgentFactory(BaseAgentFactory, MultilineDisplayMixin):
    """A concrete agent factory that wraps
    ``langchain.agents.create_agent``, building a fresh tool-calling
    agent graph on each :meth:`make_agent` call.

    Each call to :meth:`make_agent` calls
    ``chat_model_factory.make_chat_model()`` and forwards the
    resulting chat model, together with any additional keyword
    arguments (e.g. ``tools``, ``system_prompt``, ``response_format``,
    ``middleware``), to ``create_agent``. This composes with any
    :class:`~zenpyre.chat_models.factory.base.BaseChatModelFactory`
    implementation (e.g.
    :class:`~zenpyre.chat_models.factory.ChatModelFactory`,
    :class:`~zenpyre.chat_models.factory.ConfigurableChatModelFactory`),
    keeping chat model creation and agent creation decoupled.

    Unlike :class:`~zenpyre.agents.factory.AgentChatModelFactory`
    (which builds a tool-free :class:`~zenpyre.agents.AgentChatModel`),
    the agent produced here can call tools in a loop before returning
    a final answer, as implemented by ``create_agent``.

    Args:
        chat_model_factory: The factory used to build the chat model
            wrapped by the created agent.
        **kwargs: Additional keyword arguments forwarded as-is to
            ``create_agent`` (e.g. ``tools``, ``system_prompt``,
            ``response_format``, ``middleware``, ``checkpointer``,
            ``store``, ``name``). See ``create_agent``'s own
            documentation for the full list of accepted arguments.

    Example:
        ```pycon
        >>> from langchain_core.language_models import FakeListChatModel
        >>> from zenpyre.agents.factory import CreateAgentFactory
        >>> from zenpyre.chat_models.factory import ChatModelFactory
        >>> factory = CreateAgentFactory(
        ...     chat_model_factory=ChatModelFactory(FakeListChatModel(responses=["hello"])),
        ...     system_prompt="You are helpful.",
        ... )
        >>> agent = factory.make_agent()

        ```
    """

    def __init__(
        self, chat_model_factory: BaseChatModelFactory | dict[str, Any] | BaseConfig, **kwargs: Any
    ) -> None:
        self._chat_model_factory = resolve_object(chat_model_factory, cls=BaseChatModelFactory)
        self._kwargs = kwargs

    def make_agent(self) -> Runnable[dict[str, Any], dict[str, Any]]:
        return create_agent(model=self._chat_model_factory.make_chat_model(), **self._kwargs)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        kwargs = {"chat_model_factory": self._chat_model_factory, **self._kwargs}
        if isinstance(kwargs.get("system_prompt"), str):
            kwargs["system_prompt"] = truncate_str(kwargs["system_prompt"])
        return kwargs
