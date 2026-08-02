r"""Provide the base factory interface for creating zenpyre agents."""

from __future__ import annotations

__all__ = ["BaseAgentFactory"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable


class BaseAgentFactory(ABC):
    """Abstract base class for agent factories.

    Subclasses implement :meth:`make_agent` to instantiate and return
    a configured agent — a
    :class:`~langchain_core.runnables.Runnable` that accepts the same
    flexible input shapes as :class:`~zenpyre.agents.AgentChatModel`
    (a ``str``, a list of messages, or a dict with a ``"messages"``
    key) and returns a ``{"messages": ...}`` dict shape. This pattern
    decouples agent creation from the rest of the codebase, making it
    easy to swap agents (e.g. a plain chat model wrapped in
    :class:`~zenpyre.agents.AgentChatModel`, or a tool-calling agent
    built with ``create_agent``) without changing call sites.

    Example:
        ```pycon
        >>> from typing import Any
        >>> from langchain_core.language_models import FakeListChatModel
        >>> from langchain_core.runnables import Runnable
        >>> from zenpyre.agents import AgentChatModel
        >>> from zenpyre.agents.factory import BaseAgentFactory
        >>> class MyAgentFactory(BaseAgentFactory):
        ...     def make_agent(self) -> Runnable[dict[str, Any], dict[str, Any]]:
        ...         return AgentChatModel(model=FakeListChatModel(responses=["hello"]))
        ...
        >>> factory = MyAgentFactory()
        >>> agent = factory.make_agent()

        ```
    """

    @abstractmethod
    def make_agent(self) -> Runnable[dict[str, Any], dict[str, Any]]:
        """Create and return a configured agent instance.

        Returns:
            A :class:`~langchain_core.runnables.Runnable` instance
            ready for use as an agent.
        """
