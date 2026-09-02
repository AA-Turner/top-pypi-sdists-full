"""Database-backed ObservationalMemoryStorage using the cx_observational_memory table.

Swaps out the in-memory implementation for production. Stateless — every method
is a single await-chain over ``cxm.om_memory``. BufferingCoordinator owns
process-global in-flight task state; this storage does not.

All writes go through the request/standalone WriteCoordinator. A missing
coordinator is a caller bug — we raise rather than open a bare Session
(coordinator-owned tables reject ``write_scope=None``).

Thread-safety caveat: ``get_record → mutate → upsert_record`` is not atomic.
The DB ``is_buffering_*`` flags limit duplicate-work damage; optimistic
locking on ``updated_at`` can be added later if real races are observed.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import asdict, is_dataclass
from datetime import UTC, datetime
from typing import Any

from .storage import ObservationalMemoryStorage
from .types import (
    BufferedObservationChunk,
    MemoryScope,
    ObservationalMemoryRecord,
)

logger = logging.getLogger(__name__)


def _cxm():
    # Lazy: resolving cxm constructs host-injected ORM managers, which requires
    # matrx_ai.configure() with real DB bases. Import at call time so
    # `import matrx_ai.memory.storage_db` works in an unconfigured or client-host
    # environment — config errors at CALL time, never import time.
    from matrx_ai.db import cxm

    return cxm


def _require_coordinator():
    """OM rows are coordinator-owned. No coordinator → the caller skipped ownership."""
    from matrx_ai.persistence.queue_helpers import get_coordinator

    coord = get_coordinator()
    if coord is None:
        raise RuntimeError(
            "ObservationalMemory writes require an active WriteCoordinator. "
            "Open a RequestLane (in-request) or standalone_coordinator "
            "(background OM post-hook / buffer task) before calling "
            "DbObservationalMemoryStorage."
        )
    return coord


def _pending_om_row(record_id: str) -> bool:
    """True if any Session on the stack already queued an op for this OM row.

    After ``queue_om_memory_create`` the DB SELECT still misses the row until
    flush — without this check a second upsert in the same coordinator would
    queue a duplicate INSERT.
    """
    if not record_id:
        return False
    from matrx_orm.session.session import _session_stack

    model = _cxm().om_memory.model
    for session in _session_stack.get():
        if session.pending_op_for_row(model, record_id) is not None:
            return True
    return False


def _parse_dt(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception:
        return None


def _serialize_chunks(chunks: list[BufferedObservationChunk]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for c in chunks or []:
        if is_dataclass(c):
            out.append(asdict(c))
        elif isinstance(c, dict):
            out.append(c)
    return out


def _deserialize_chunks(raw: Any) -> list[BufferedObservationChunk]:
    if not raw:
        return []
    out: list[BufferedObservationChunk] = []
    for item in raw:
        if isinstance(item, dict):
            # Filter to the fields the dataclass actually accepts — safety against
            # schema drift.
            allowed = {f for f in BufferedObservationChunk.__dataclass_fields__}
            payload = {k: v for k, v in item.items() if k in allowed}
            try:
                out.append(BufferedObservationChunk(**payload))
            except TypeError as exc:
                logger.warning("Dropping malformed BufferedObservationChunk: %s", exc)
    return out


def _scope_value(scope: MemoryScope | str) -> str:
    if isinstance(scope, MemoryScope):
        return scope.value
    return str(scope)


def _scope_enum(value: Any) -> MemoryScope:
    try:
        return MemoryScope(value)
    except Exception:
        return MemoryScope.THREAD


class DbObservationalMemoryStorage(ObservationalMemoryStorage):
    """Concrete storage backed by ``cx_observational_memory``.

    Serializes ``BufferedObservationChunk`` dataclasses into the
    ``buffered_observations`` JSONB column. Soft-delete only — records are
    marked ``deleted_at`` rather than removed outright, mirroring other
    ``cx_*`` tables.
    """

    def _row_to_record(self, row: Any) -> ObservationalMemoryRecord:
        scope = _scope_enum(getattr(row, "scope", "thread"))
        return ObservationalMemoryRecord(
            id=str(row.id),
            resource_id=str(row.created_by),
            scope=scope,
            thread_id=str(row.conversation_id)
            if row.conversation_id and scope == MemoryScope.THREAD
            else None,
            active_observations=row.active_observations,
            observation_token_count=int(row.observation_token_count or 0),
            current_task=row.current_task,
            suggested_response=row.suggested_response,
            last_observed_at=_parse_dt(row.last_observed_at),
            observed_message_ids=list(row.observed_message_ids or []),
            pending_message_tokens=int(row.pending_message_tokens or 0),
            buffered_observations=_deserialize_chunks(row.buffered_observations),
            is_buffering_observation=bool(row.is_buffering_observation),
            last_buffered_at_tokens=int(row.last_buffered_at_tokens or 0),
            last_buffered_at_time=_parse_dt(row.last_buffered_at_time),
            buffered_reflection=row.buffered_reflection,
            buffered_reflection_input_tokens=int(row.buffered_reflection_input_tokens or 0),
            buffered_reflection_tokens=int(row.buffered_reflection_tokens or 0),
            is_buffering_reflection=bool(row.is_buffering_reflection),
            reflected_observation_line_count=int(row.reflected_observation_line_count or 0),
            generation_count=int(row.generation_count or 0),
            observed_timezone=row.observed_timezone or "UTC",
            config=row.config or {},
            created_at=_parse_dt(row.created_at) or datetime.now(UTC),
            updated_at=_parse_dt(row.updated_at) or datetime.now(UTC),
        )

    def _record_to_fields(self, record: ObservationalMemoryRecord) -> dict[str, Any]:
        fields = {
            "conversation_id": record.thread_id,
            "scope": _scope_value(record.scope),
            "active_observations": record.active_observations,
            "observation_token_count": int(record.observation_token_count or 0),
            "current_task": record.current_task,
            "suggested_response": record.suggested_response,
            "last_observed_at": record.last_observed_at,
            "observed_message_ids": list(record.observed_message_ids or []),
            "pending_message_tokens": int(record.pending_message_tokens or 0),
            "buffered_observations": _serialize_chunks(record.buffered_observations),
            "is_buffering_observation": bool(record.is_buffering_observation),
            "last_buffered_at_tokens": int(record.last_buffered_at_tokens or 0),
            "last_buffered_at_time": record.last_buffered_at_time,
            "buffered_reflection": record.buffered_reflection,
            "buffered_reflection_input_tokens": int(record.buffered_reflection_input_tokens or 0),
            "buffered_reflection_tokens": int(record.buffered_reflection_tokens or 0),
            "is_buffering_reflection": bool(record.is_buffering_reflection),
            "reflected_observation_line_count": int(record.reflected_observation_line_count or 0),
            "generation_count": int(record.generation_count or 0),
            "observed_timezone": record.observed_timezone or "UTC",
            "config": record.config or {},
        }
        from matrx_ai.db.ownership_fields import stamp_row_owner

        stamp_row_owner(fields, record.resource_id)
        return fields

    # ------------------------------------------------------------------ #
    # Read
    # ------------------------------------------------------------------ #

    async def _find_live_row(
        self,
        resource_id: str,
        thread_id: str | None,
        scope: MemoryScope,
    ) -> Any | None:
        filters: dict[str, Any] = {
            "created_by": resource_id,
            "scope": _scope_value(scope),
            "deleted_at": None,
        }
        if scope == MemoryScope.THREAD and thread_id:
            filters["conversation_id"] = thread_id
        elif scope == MemoryScope.RESOURCE:
            filters["conversation_id"] = None
        rows = await _cxm().om_memory.filter_observational_memories(**filters)
        if not rows:
            return None
        # Partial unique indexes guarantee at most one live row per key.
        return rows[0]

    async def _find_row_by_id(self, record_id: str) -> Any | None:
        try:
            return await _cxm().om_memory.load_item_or_none(id=record_id)
        except Exception:
            return None

    async def get_record(
        self,
        resource_id: str,
        thread_id: str | None,
        scope: MemoryScope,
    ) -> ObservationalMemoryRecord | None:
        row = await self._find_live_row(resource_id, thread_id, scope)
        if row is None:
            return None
        return self._row_to_record(row)

    # ------------------------------------------------------------------ #
    # Write
    # ------------------------------------------------------------------ #

    async def upsert_record(self, record: ObservationalMemoryRecord) -> ObservationalMemoryRecord:
        from matrx_ai.persistence.queue_helpers import (
            queue_om_memory_create,
            queue_om_memory_update,
        )

        _require_coordinator()
        fields = self._record_to_fields(record)
        now = datetime.now(UTC)

        existing = await self._find_row_by_id(record.id)
        if existing is None:
            existing = await self._find_live_row(record.resource_id, record.thread_id, record.scope)

        row_id = str(existing.id) if existing is not None else (record.id or str(uuid.uuid4()))
        fields["updated_at"] = now
        if existing is None and not _pending_om_row(row_id):
            fields["created_at"] = now
            queue_om_memory_create(id=row_id, **fields)
        else:
            queue_om_memory_update(row_id, **fields)
        record.id = row_id

        record.updated_at = now
        return record

    async def delete_record(
        self,
        resource_id: str,
        thread_id: str | None,
        scope: MemoryScope,
    ) -> None:
        from matrx_ai.persistence.queue_helpers import queue_om_memory_update

        row = await self._find_live_row(resource_id, thread_id, scope)
        if row is None:
            return
        _require_coordinator()
        queue_om_memory_update(str(row.id), deleted_at=datetime.now(UTC))

    async def _update_by_id(self, record_id: str, **fields: Any) -> None:
        from matrx_ai.persistence.queue_helpers import queue_om_memory_update

        fields.setdefault("updated_at", datetime.now(UTC))
        try:
            _require_coordinator()
            queue_om_memory_update(record_id, **fields)
        except Exception as exc:
            logger.warning("OM storage update failed on %s: %s", record_id, exc)

    async def add_buffered_observation_chunk(
        self,
        record_id: str,
        chunk: Any,
        message_tokens_processed: int,
        last_observed_at: datetime | None,
        observed_message_ids: list[str],
    ) -> None:
        row = await self._find_row_by_id(record_id)
        if row is None:
            return
        existing_chunks = list(row.buffered_observations or [])
        existing_chunks.append(asdict(chunk) if is_dataclass(chunk) else chunk)
        existing_ids = list(row.observed_message_ids or [])
        if observed_message_ids:
            existing_ids.extend(observed_message_ids)
        updates: dict[str, Any] = {
            "buffered_observations": existing_chunks,
            "last_buffered_at_tokens": int(row.last_buffered_at_tokens or 0)
            + int(message_tokens_processed or 0),
            "observed_message_ids": existing_ids,
        }
        if last_observed_at is not None:
            updates["last_buffered_at_time"] = last_observed_at
        await self._update_by_id(record_id, **updates)

    async def swap_buffered_chunks_to_active(
        self,
        record_id: str,
        token_count: int,
        messages_activated: int,
    ) -> None:
        row = await self._find_row_by_id(record_id)
        if row is None:
            return
        combined: list[str] = []
        if row.active_observations:
            combined.append(row.active_observations)
        for chunk in row.buffered_observations or []:
            if isinstance(chunk, dict):
                text = chunk.get("observations")
                if text:
                    combined.append(text)
        new_active = "\n\n".join(combined)
        await self._update_by_id(
            record_id,
            active_observations=new_active,
            observation_token_count=int(token_count or 0),
            buffered_observations=[],
            is_buffering_observation=False,
            last_buffered_at_tokens=0,
            generation_count=int(row.generation_count or 0) + 1,
        )

    async def update_buffered_reflection(
        self,
        record_id: str,
        reflection: str,
        token_count: int,
        input_token_count: int,
        reflected_observation_line_count: int,
    ) -> None:
        await self._update_by_id(
            record_id,
            buffered_reflection=reflection,
            buffered_reflection_tokens=int(token_count or 0),
            buffered_reflection_input_tokens=int(input_token_count or 0),
            reflected_observation_line_count=int(reflected_observation_line_count or 0),
        )

    async def swap_buffered_reflection_to_active(
        self,
        record_id: str,
        token_count: int,
    ) -> None:
        row = await self._find_row_by_id(record_id)
        if row is None or not row.buffered_reflection:
            return
        current_lines = (row.active_observations or "").split("\n")
        line_count = int(row.reflected_observation_line_count or 0)
        unreflected_lines = current_lines[line_count:] if line_count else []
        new_obs = row.buffered_reflection
        if unreflected_lines:
            new_obs += "\n\n" + "\n".join(unreflected_lines)
        await self._update_by_id(
            record_id,
            active_observations=new_obs,
            observation_token_count=int(token_count or 0),
            buffered_reflection=None,
            buffered_reflection_tokens=0,
            buffered_reflection_input_tokens=0,
            reflected_observation_line_count=0,
            generation_count=int(row.generation_count or 0) + 1,
        )

    async def set_buffering_observation_flag(self, record_id: str, flag: bool) -> None:
        await self._update_by_id(record_id, is_buffering_observation=bool(flag))

    async def set_buffering_reflection_flag(self, record_id: str, flag: bool) -> None:
        await self._update_by_id(record_id, is_buffering_reflection=bool(flag))
