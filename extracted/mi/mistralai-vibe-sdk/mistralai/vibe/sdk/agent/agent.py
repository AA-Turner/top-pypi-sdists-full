"""Concrete Agent runtime."""

from collections.abc import Sequence

from mistralai.vibe.sdk.agent.config import AgentConfig
from mistralai.vibe.sdk.agent.sessions import (
    AsyncSession,
    IdFactory,
    SyncSession,
    default_id_factory,
)
from mistralai.vibe.sdk.agent.tasks.helpers import AgentTaskFactory, create_agent_task
from mistralai.vibe.sdk.execution_record.state import HistoryEntry
from mistralai.vibe.sdk.observability import ObservabilityAttributes


class Agent:
    """Agent entity that creates stateful sessions."""

    def __init__(
        self,
        *,
        config: AgentConfig,
        agent_task_factory: AgentTaskFactory | None = None,
        id_factory: IdFactory | None = None,
        observability_attributes: ObservabilityAttributes | None = None,
    ) -> None:
        """Create an agent."""
        self._config = config.clone()
        self._task_config = self._config.to_task_config()
        self._client_tool_registry = self._config.client_tool_registry()
        self._agent_task_factory = agent_task_factory or create_agent_task
        self._id_factory = id_factory or default_id_factory
        self._observability_attributes = dict(observability_attributes or {})

    def set_config(self, config: AgentConfig) -> None:
        """Replace the default config used for future sessions."""
        self._config = config.clone()
        self._task_config = self._config.to_task_config()
        self._client_tool_registry = self._config.client_tool_registry()

    def session(
        self,
        history: Sequence[HistoryEntry] | None = None,
        conversation_id: str | None = None,
    ) -> AsyncSession:
        """Create a new async conversation session."""
        return AsyncSession(
            task_config=self._task_config,
            agent_task_factory=self._agent_task_factory,
            history=history,
            id_factory=self._id_factory,
            client_tool_registry=self._client_tool_registry,
            conversation_id=conversation_id,
            observability_attributes=self._observability_attributes,
        )

    def session_sync(
        self,
        history: Sequence[HistoryEntry] | None = None,
        conversation_id: str | None = None,
    ) -> SyncSession:
        """Create a new synchronous conversation session."""
        return SyncSession(
            task_config=self._task_config,
            agent_task_factory=self._agent_task_factory,
            history=history,
            id_factory=self._id_factory,
            client_tool_registry=self._client_tool_registry,
            conversation_id=conversation_id,
            observability_attributes=self._observability_attributes,
        )
