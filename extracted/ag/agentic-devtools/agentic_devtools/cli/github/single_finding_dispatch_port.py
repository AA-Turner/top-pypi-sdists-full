"""Provider-facing protocol for single-finding dispatch."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from agentic_devtools.ai_providers.agent_tasks_payload import AgentTasksPayload
    from agentic_devtools.cli.github.single_finding_dispatch import SingleFindingHandoff, TaskAcceptance


class SingleFindingDispatchHost(Protocol):
    """Provider-facing boundary for one reserved, expected-head-protected task.

    ``reserve_branch_write`` atomically acquires the complete reservation within
    the supplied timeout and returns ``False`` when another attempt owns an
    overlapping resource. A lock-storage ``OSError`` maps to a blocked result.
    ``release_branch_write`` releases a reservation acquired by this adapter.
    ``create_task_if_head`` re-reads the assigned thread, task-deduplication
    state, and authoritative PR refs/SHA immediately before task creation.
    It returns ``already_resolved``, ``already_active``, ``blocked`` or
    ``head_changed`` without writing when those checks fail.
    Ambiguous delivery failures map to ``TaskAcceptance("unknown", ...)`` or
    ``AmbiguousTaskCreationError``. Every operation honors its timeout.
    ``persist_acceptance`` durably records the result before the adapter
    returns and releases the reservation on every exit; expected persistence
    failures raise ``AcceptancePersistenceError``.

    ``create_task_if_head`` releases on no-write or exceptional exits; for an
    ``accepted`` or ``unknown`` result, it retains the reservation until
    ``persist_acceptance`` completes.
    """

    def reserve_branch_write(self, handoff: SingleFindingHandoff, timeout_seconds: int) -> bool:
        """Acquire the serialized branch-write reservation."""

    def release_branch_write(self, handoff: SingleFindingHandoff) -> None:
        """Release the reservation previously acquired for this handoff."""

    def create_task_if_head(
        self,
        handoff: SingleFindingHandoff,
        payload: AgentTasksPayload,
        timeout_seconds: int,
    ) -> TaskAcceptance:
        """Re-read thread state and create one task only after all checks match atomically."""

    def persist_acceptance(
        self,
        handoff: SingleFindingHandoff,
        acceptance: TaskAcceptance,
        timeout_seconds: int,
    ) -> bool:
        """Persist accepted task/session identity within the timeout."""
