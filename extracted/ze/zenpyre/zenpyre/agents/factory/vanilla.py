r"""Provide a concrete default factory for zenpyre agents."""

from __future__ import annotations

__all__ = ["AgentFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.agents.factory.base import BaseAgentFactory

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable


class AgentFactory(BaseAgentFactory, MultilineDisplayMixin):
    """A concrete agent factory that wraps a pre-built agent (a
    :class:`~langchain_core.runnables.Runnable`, e.g.
    :class:`~zenpyre.agents.AgentChatModel`).

    Use this when the agent is already instantiated and you simply
    want to wrap it in the :class:`~BaseAgentFactory` interface — for
    example, when injecting a fixed agent into a component that
    expects a factory.

    Args:
        agent: A fully configured agent
            (:class:`~langchain_core.runnables.Runnable`) instance to
            return from :meth:`make_agent`.

    Example:
        ```pycon
        >>> from langchain_core.language_models import FakeListChatModel
        >>> from zenpyre.agents import AgentChatModel
        >>> from zenpyre.agents.factory import AgentFactory
        >>> agent = AgentChatModel(model=FakeListChatModel(responses=["hello"]))
        >>> factory = AgentFactory(agent)
        >>> agent = factory.make_agent()

        ```
    """

    def __init__(self, agent: Runnable[dict[str, Any], dict[str, Any]]) -> None:
        self._agent = agent

    def make_agent(self) -> Runnable[dict[str, Any], dict[str, Any]]:
        return self._agent

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"agent": self._agent}
