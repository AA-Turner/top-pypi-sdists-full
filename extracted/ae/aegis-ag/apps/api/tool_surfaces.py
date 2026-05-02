"""API adapters that expose canonical work and memory owners to built-in tools."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, cast

from packages.contracts.runtime import EvidenceRetrievalRequest, EvidenceRetrievalResult, GoalNode, MemoryRecord
from packages.evidence import MemoryRuntime
from packages.tools.surfaces import MemoryManagementSurface, RecallSearchSurface


class _MemoryApp(Protocol):
    repository: object
    session_lineage: object
    memory_runtime: MemoryRuntime

    def list_memories(self, session_id: str) -> tuple[MemoryRecord, ...]:
        """List durable memories for a session."""

    def inspect_memory(self, session_id: str, memory_id: str) -> dict[str, Any]:
        """Inspect one durable memory."""

    def correct_memory(
        self,
        session_id: str,
        memory_id: str,
        *,
        corrected_content: str,
        reason: str = "",
        actor: str = "user",
    ) -> dict[str, Any]:
        """Correct a durable memory."""

    def delete_memory(
        self,
        session_id: str,
        memory_id: str,
        *,
        reason: str,
        actor: str = "user",
    ) -> dict[str, Any]:
        """Delete a durable memory."""

    def list_goals(self, session_id: str) -> tuple[GoalNode, ...]:
        """List durable goals for a session."""

@dataclass(frozen=True, slots=True)
class APIMemoryManagementSurface(MemoryManagementSurface):
    app: _MemoryApp

    def inspect_memories(self, session_id: str) -> tuple[MemoryRecord, ...]:
        return self.app.list_memories(session_id)

    def inspect_memory(self, session_id: str, memory_id: str) -> MemoryRecord:
        payload = self.app.inspect_memory(session_id, memory_id)
        return cast(MemoryRecord, payload["memory"])

    def search_memories(self, session_id: str, query: str, *, limit: int = 5) -> tuple[MemoryRecord, ...]:
        result = self.app.memory_runtime.retrieve(session_id, query)
        return tuple(candidate.record for candidate in result.candidates[:limit])

    def correct_memory(
        self,
        session_id: str,
        memory_id: str,
        *,
        corrected_content: str,
        reason: str = "",
    ) -> tuple[MemoryRecord | None, MemoryRecord | None, str, str | None]:
        original = self.inspect_memory(session_id, memory_id)
        payload = self.app.correct_memory(
            session_id,
            memory_id,
            corrected_content=corrected_content,
            reason=reason,
            actor="assistant",
        )
        decision = payload["decision"]
        return (
            original,
            cast(MemoryRecord | None, payload.get("memory")),
            str(getattr(decision, "reason", reason or "memory corrected")),
            cast(str | None, payload.get("memory_lineage")),
        )

    def delete_memory(self, session_id: str, memory_id: str, *, reason: str) -> tuple[MemoryRecord, str | None]:
        original = self.inspect_memory(session_id, memory_id)
        payload = self.app.delete_memory(
            session_id,
            memory_id,
            reason=reason,
            actor="assistant",
        )
        decision = payload["decision"]
        return original, str(getattr(decision, "reason", reason or "memory deleted"))

    def pin_memory(self, session_id: str, memory_id: str, *, reason: str = "") -> tuple[MemoryRecord, str]:
        original = self.inspect_memory(session_id, memory_id)
        result = self.app.memory_runtime.pin_memory(memory_id, actor="assistant", reason=reason)
        return result.record or original, result.decision.reason

    def unpin_memory(self, session_id: str, memory_id: str, *, reason: str = "") -> tuple[MemoryRecord, str]:
        original = self.inspect_memory(session_id, memory_id)
        result = self.app.memory_runtime.unpin_memory(memory_id, actor="assistant", reason=reason)
        return result.record or original, result.decision.reason

    def memory_lineage(self, memory_id: str) -> str | None:
        return self.app.memory_runtime.store.lineage(memory_id)

    def memory_state(self, memory_id: str) -> str | None:
        return self.app.memory_runtime.store.state(memory_id)


@dataclass(frozen=True, slots=True)
class APIRecallSearchSurface(RecallSearchSurface):
    app: _MemoryApp

    def recall(self, session_id: str, query: str, *, limit: int = 5) -> EvidenceRetrievalResult:
        session = self.app.repository.load_session(session_id)  # type: ignore[attr-defined]
        if session is None:
            raise KeyError(session_id)
        lineage = tuple(
            item.session_id
            for item in self.app.session_lineage.lineage(session_id)  # type: ignore[attr-defined]
        ) or (session_id,)
        return self.app.memory_runtime.retrieve_evidence(
            EvidenceRetrievalRequest(
                session_id=session_id,
                profile_id=session.profile_id,
                workspace_id=session.workspace_id,
                lineage_session_ids=lineage,
                work_item_ids=tuple(goal.goal_id for goal in self.app.list_goals(session_id)),
                query=query,
                scopes=("session", "lineage") if len(lineage) > 1 else ("session",),
                latency_mode="fast",
                limit=limit,
                scope_reason="tool.memory.recall",
            )
        )


__all__ = [
    "APIMemoryManagementSurface",
    "APIRecallSearchSurface",
]
