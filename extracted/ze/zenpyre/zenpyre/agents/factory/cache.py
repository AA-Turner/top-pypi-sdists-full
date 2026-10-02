r"""Provide a concrete agent factory that wraps another agent factory
with caching."""

from __future__ import annotations

__all__ = ["CachingAgentFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.agents.factory.base import BaseAgentFactory
from zenpyre.runnables import CachingRunnable
from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING:
    from collections.abc import Callable

    from langchain_core.runnables import Runnable
    from persista.cache import Cache

    from zenpyre.utils.config import BaseConfig


class CachingAgentFactory(BaseAgentFactory, MultilineDisplayMixin):
    """A concrete agent factory that wraps another agent factory and
    caches the resulting agent's outputs via
    :class:`~zenpyre.runnables.CachingRunnable`.

    Each call to :meth:`make_agent` builds a fresh agent from
    ``agent_factory`` and wraps it in a
    :class:`~zenpyre.runnables.CachingRunnable`, so repeated calls to
    the wrapped agent with the same (or equivalent, per ``key_fn``)
    input are served from ``cache`` instead of re-invoking the
    underlying agent.

    Args:
        agent_factory: The factory used to build the underlying agent
            to cache.
        cache: The :class:`~persista.cache.Cache` instance used
            to store cached results. If ``None``, caching is disabled.
        key_fn: An optional function used to compute a cache key from
            the agent's input. If ``None``,
            :class:`~zenpyre.runnables.CachingRunnable`'s default
            key-computation strategy is used.

    Example:
        ```pycon
        >>> from langchain_core.language_models import FakeListChatModel
        >>> from persista.cache import Cache
        >>> from zenpyre.agents import AgentChatModel
        >>> from zenpyre.agents.factory import AgentFactory, CachingAgentFactory
        >>> inner_agent = AgentChatModel(model=FakeListChatModel(responses=["hello"]))
        >>> factory = CachingAgentFactory(
        ...     agent_factory=AgentFactory(inner_agent),
        ...     cache=Cache(),
        ... )
        >>> agent = factory.make_agent()  # doctest: +SKIP

        ```
    """

    def __init__(
        self,
        agent_factory: BaseAgentFactory | dict[str, Any] | BaseConfig,
        cache: Cache | None = None,
        key_fn: Callable[[dict[str, Any]], str] | None = None,
    ) -> None:
        self._agent_factory = resolve_object(agent_factory, cls=BaseAgentFactory)
        self._cache = cache
        self._key_fn = key_fn

    def make_agent(self) -> Runnable[dict[str, Any], dict[str, Any]]:
        agent = self._agent_factory.make_agent()
        return CachingRunnable(
            runnable=agent,
            cache=self._cache,
            key_fn=self._key_fn,
        )

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {
            "agent_factory": self._agent_factory,
            "cache": self._cache,
            "key_fn": self._key_fn,
        }
