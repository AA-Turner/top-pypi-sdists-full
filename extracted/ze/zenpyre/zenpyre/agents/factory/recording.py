r"""Provide a concrete agent factory that wraps another agent factory
with recording."""

from __future__ import annotations

__all__ = ["RecordingAgentFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.agents.factory.base import BaseAgentFactory
from zenpyre.record_stores.factory.base import BaseRecordStoreFactory
from zenpyre.runnables import RecordingRunnable
from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING:
    from collections.abc import Callable

    from langchain_core.runnables import Runnable

    from zenpyre.utils.config import BaseConfig


class RecordingAgentFactory(BaseAgentFactory, MultilineDisplayMixin):
    """A concrete agent factory that wraps another agent factory and
    records the resulting agent's calls via
    :class:`~zenpyre.runnables.RecordingRunnable`.

    Each call to :meth:`make_agent` builds a fresh agent from
    ``agent_factory``, calls
    ``record_store_factory.make_record_store()``, and wraps the agent
    in a :class:`~zenpyre.runnables.RecordingRunnable`, so every call
    to the wrapped agent writes a record of its input and output to
    the resulting record store. This composes with any
    :class:`~zenpyre.record_stores.factory.base.BaseRecordStoreFactory`
    implementation (e.g.
    :class:`~zenpyre.record_stores.factory.RecordStoreFactory`,
    :class:`~zenpyre.record_stores.factory.ConfigurableRecordStoreFactory`),
    keeping record store creation and agent creation decoupled.

    Args:
        agent_factory: The factory used to build the underlying agent
            to record.
        record_store_factory: The factory used to build the store
            input/output records are written to.
        extra: Additional metadata merged into every record written by
            this wrapper, fixed for its lifetime (e.g. an experiment
            ID). See
            :class:`~zenpyre.runnables.RecordingRunnable` for the set
            of reserved keys this must not contain.
        serializer: A function applied to the whole assembled metadata
            dict before it's stored. If ``None``,
            :class:`~zenpyre.runnables.RecordingRunnable`'s default
            (:func:`~zenpyre.runnables.recording.default_serialize`)
            is used.

    Example:
        ```pycon
        >>> from langchain_core.language_models import FakeListChatModel
        >>> from zenpyre.agents import AgentChatModel
        >>> from zenpyre.agents.factory import AgentFactory, RecordingAgentFactory
        >>> from zenpyre.record_stores import InMemoryRecordStore
        >>> from zenpyre.record_stores.factory import RecordStoreFactory
        >>> inner_agent = AgentChatModel(model=FakeListChatModel(responses=["hello"]))
        >>> factory = RecordingAgentFactory(
        ...     agent_factory=AgentFactory(inner_agent),
        ...     record_store_factory=RecordStoreFactory(InMemoryRecordStore()),
        ... )
        >>> agent = factory.make_agent()

        ```
    """

    def __init__(
        self,
        agent_factory: BaseAgentFactory | dict[str, Any] | BaseConfig,
        record_store_factory: BaseRecordStoreFactory | dict[str, Any] | BaseConfig,
        extra: dict[str, Any] | None = None,
        serializer: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
    ) -> None:
        self._agent_factory = resolve_object(agent_factory, cls=BaseAgentFactory)
        self._record_store_factory = resolve_object(
            record_store_factory, cls=BaseRecordStoreFactory
        )
        self._extra = extra
        self._serializer = serializer

    def make_agent(self) -> Runnable[dict[str, Any], dict[str, Any]]:
        agent = self._agent_factory.make_agent()
        record_store = self._record_store_factory.make_record_store()
        return RecordingRunnable(
            runnable=agent,
            record_store=record_store,
            extra=self._extra,
            serializer=self._serializer,
        )

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {
            "agent_factory": self._agent_factory,
            "record_store_factory": self._record_store_factory,
            "extra": self._extra,
            "serializer": self._serializer,
        }
