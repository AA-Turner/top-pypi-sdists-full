r"""Provide a configurable factory for zenpyre agents."""

from __future__ import annotations

__all__ = ["ConfigurableAgentFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.agents.factory.base import BaseAgentFactory
from zenpyre.runnables import resolve_runnable

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable


class ConfigurableAgentFactory(BaseAgentFactory, MultilineDisplayMixin):
    """A concrete agent factory that accepts either a pre-built agent (a
    :class:`~langchain_core.runnables.Runnable`, e.g.
    :class:`~zenpyre.agents.AgentChatModel`) or a configuration
    dictionary.

    When a dict is provided it is resolved at each :meth:`make_agent`
    call via :func:`~zenpyre.runnables.resolve_runnable`, which uses
    ``objectory`` to instantiate the configured class.  When an
    instance is provided it is returned as-is.

    Args:
        agent: A fully configured agent
            (:class:`~langchain_core.runnables.Runnable`) instance,
            or a :class:`dict` containing an ``objectory`` factory
            specification (must include a ``"_target_"`` key pointing
            to the fully-qualified class name).

    Example:
        ```pycon
        >>> from langchain_core.language_models import FakeListChatModel
        >>> from zenpyre.agents import AgentChatModel
        >>> from zenpyre.agents.factory import ConfigurableAgentFactory
        >>> agent = AgentChatModel(model=FakeListChatModel(responses=["hello"]))
        >>> factory = ConfigurableAgentFactory(agent)
        >>> agent = factory.make_agent()

        ```
    """

    def __init__(
        self,
        agent: Runnable[dict[str, Any], dict[str, Any]] | dict[str, Any],
    ) -> None:
        self._agent = agent

    def make_agent(self) -> Runnable[dict[str, Any], dict[str, Any]]:
        return resolve_runnable(self._agent)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"agent": self._agent}
