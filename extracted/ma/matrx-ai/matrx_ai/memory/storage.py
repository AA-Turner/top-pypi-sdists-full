"""
Abstract storage interface and in-memory implementation for Observational Memory.

In production, replace InMemoryStorage with a Postgres/SQLite/Redis-backed implementation.
The interface is minimal — the OM system only needs get/upsert on one table.
"""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from copy import deepcopy
from datetime import datetime
from typing import Any, Optional

from .types import (
    MemoryScope,
    ObservationalMemoryRecord,
)


# ---------------------------------------------------------------------------
# Abstract base
# ---------------------------------------------------------------------------

class ObservationalMemoryStorage(ABC):
    """
    Storage interface for ObservationalMemory records.
    
    Each record represents the observation context for one scope key:
    - THREAD scope: keyed by (resource_id, thread_id)
    - RESOURCE scope: keyed by resource_id alone
    """

    @abstractmethod
    async def get_record(
        self,
        resource_id: str,
        thread_id: Optional[str],
        scope: MemoryScope,
    ) -> Optional[ObservationalMemoryRecord]:
        """Fetch the observation record, or None if it doesn't exist yet."""
        ...

    @abstractmethod
    async def upsert_record(self, record: ObservationalMemoryRecord) -> ObservationalMemoryRecord:
        """Create or update an observation record. Returns the persisted record."""
        ...

    @abstractmethod
    async def delete_record(
        self,
        resource_id: str,
        thread_id: Optional[str],
        scope: MemoryScope,
    ) -> None:
        """Delete an observation record (e.g., when a thread is deleted)."""
        ...

    @abstractmethod
    async def add_buffered_observation_chunk(
        self,
        record_id: str,
        chunk: Any,
        message_tokens_processed: int,
        last_observed_at: Optional[datetime],
        observed_message_ids: list[str],
    ) -> None:
        """Add a buffered observation chunk."""
        ...

    @abstractmethod
    async def swap_buffered_chunks_to_active(
        self,
        record_id: str,
        token_count: int,
        messages_activated: int,
    ) -> None:
        """Activate all buffered chunks."""
        ...

    @abstractmethod
    async def update_buffered_reflection(
        self,
        record_id: str,
        reflection: str,
        token_count: int,
        input_token_count: int,
        reflected_observation_line_count: int,
    ) -> None:
        """Update the pending background reflection."""
        ...

    @abstractmethod
    async def swap_buffered_reflection_to_active(
        self,
        record_id: str,
        token_count: int,
    ) -> None:
        """Promote the buffered reflection to active observations."""
        ...

    @abstractmethod
    async def set_buffering_observation_flag(self, record_id: str, flag: bool) -> None:
        ...

    @abstractmethod
    async def set_buffering_reflection_flag(self, record_id: str, flag: bool) -> None:
        ...


# ---------------------------------------------------------------------------
# In-memory implementation (for testing / prototyping)
# ---------------------------------------------------------------------------

class InMemoryStorage(ObservationalMemoryStorage):
    """
    Simple dict-backed storage. Not thread-safe, not persistent.
    Good for unit tests and quick prototyping.
    """

    def __init__(self) -> None:
        self._records: dict[str, ObservationalMemoryRecord] = {}

    def _key(self, resource_id: str, thread_id: Optional[str], scope: MemoryScope) -> str:
        if scope == MemoryScope.RESOURCE:
            return f"resource:{resource_id}"
        return f"thread:{resource_id}:{thread_id}"

    async def get_record(
        self,
        resource_id: str,
        thread_id: Optional[str],
        scope: MemoryScope,
    ) -> Optional[ObservationalMemoryRecord]:
        return deepcopy(self._records.get(self._key(resource_id, thread_id, scope)))

    async def upsert_record(self, record: ObservationalMemoryRecord) -> ObservationalMemoryRecord:
        record.updated_at = datetime.utcnow()
        self._records[self._key(record.resource_id, record.thread_id, record.scope)] = deepcopy(record)
        return record

    async def delete_record(
        self,
        resource_id: str,
        thread_id: Optional[str],
        scope: MemoryScope,
    ) -> None:
        self._records.pop(self._key(resource_id, thread_id, scope), None)

    def _get_record_by_id(self, record_id: str) -> Optional[ObservationalMemoryRecord]:
        for record in self._records.values():
            if record.id == record_id:
                return record
        return None

    async def add_buffered_observation_chunk(
        self,
        record_id: str,
        chunk: Any,
        message_tokens_processed: int,
        last_observed_at: Optional[datetime],
        observed_message_ids: list[str],
    ) -> None:
        record = self._get_record_by_id(record_id)
        if not record: return
        record.buffered_observations.append(chunk)
        record.last_buffered_at_tokens = (record.last_buffered_at_tokens or 0) + message_tokens_processed
        if last_observed_at:
            record.last_buffered_at_time = last_observed_at
        if observed_message_ids:
            record.observed_message_ids.extend(observed_message_ids)
        self._records[self._key(record.resource_id, record.thread_id, record.scope)] = record

    async def swap_buffered_chunks_to_active(
        self,
        record_id: str,
        token_count: int,
        messages_activated: int,
    ) -> None:
        record = self._get_record_by_id(record_id)
        if not record: return
        
        # Combine active + buffered
        combined = []
        if record.active_observations:
            combined.append(record.active_observations)
        for chunk in record.buffered_observations:
            combined.append(chunk.observations)
            
        record.active_observations = "\n\n".join(combined)
        record.observation_token_count = token_count
        record.buffered_observations = []
        record.is_buffering_observation = False
        record.last_buffered_at_tokens = 0
        record.generation_count += 1
        
        self._records[self._key(record.resource_id, record.thread_id, record.scope)] = record

    async def update_buffered_reflection(
        self,
        record_id: str,
        reflection: str,
        token_count: int,
        input_token_count: int,
        reflected_observation_line_count: int,
    ) -> None:
        record = self._get_record_by_id(record_id)
        if not record: return
        record.buffered_reflection = reflection
        record.buffered_reflection_tokens = token_count
        record.buffered_reflection_input_tokens = input_token_count
        record.reflected_observation_line_count = reflected_observation_line_count
        self._records[self._key(record.resource_id, record.thread_id, record.scope)] = record

    async def swap_buffered_reflection_to_active(
        self,
        record_id: str,
        token_count: int,
    ) -> None:
        record = self._get_record_by_id(record_id)
        if not record or not record.buffered_reflection: return
        
        # We assume the unreflected lines were retained and buffered_reflection comes first
        current_lines = (record.active_observations or "").split("\n")
        unreflected_lines = current_lines[record.reflected_observation_line_count:]

        new_obs = record.buffered_reflection
        if unreflected_lines:
            new_obs += "\n\n" + "\n".join(unreflected_lines)
            
        record.active_observations = new_obs
        record.observation_token_count = token_count
        record.buffered_reflection = None
        record.buffered_reflection_tokens = 0
        record.buffered_reflection_input_tokens = 0
        record.reflected_observation_line_count = 0
        record.generation_count += 1
        
        self._records[self._key(record.resource_id, record.thread_id, record.scope)] = record

    async def set_buffering_observation_flag(self, record_id: str, flag: bool) -> None:
        record = self._get_record_by_id(record_id)
        if not record: return
        record.is_buffering_observation = flag
        self._records[self._key(record.resource_id, record.thread_id, record.scope)] = record

    async def set_buffering_reflection_flag(self, record_id: str, flag: bool) -> None:
        record = self._get_record_by_id(record_id)
        if not record: return
        record.is_buffering_reflection = flag
        self._records[self._key(record.resource_id, record.thread_id, record.scope)] = record


# ---------------------------------------------------------------------------
# Helper: get or create
# ---------------------------------------------------------------------------

async def get_or_create_record(
    storage: ObservationalMemoryStorage,
    resource_id: str,
    thread_id: Optional[str],
    scope: MemoryScope,
) -> ObservationalMemoryRecord:
    """
    Fetch the record, creating a new blank one if it doesn't exist.
    Does NOT persist the new record — call upsert_record after modification.
    """
    existing = await storage.get_record(resource_id, thread_id, scope)
    if existing is not None:
        return existing
    # A record's ID is the durable identity of its natural key, not an
    # attempt-specific random value. Multiple request lanes can legitimately
    # observe a missing row before either lane flushes; UUIDv5 makes those
    # concurrent creates target the same primary key. The Session's existing
    # primary-key idempotency handling then safely converges the inserts rather
    # than letting two random IDs collide on the live-row partial unique index.
    identity = f"matrx-ai:observational-memory:{_scope_identity(scope, resource_id, thread_id)}"
    return ObservationalMemoryRecord(
        id=str(uuid.uuid5(uuid.NAMESPACE_URL, identity)),
        resource_id=resource_id,
        thread_id=thread_id if scope == MemoryScope.THREAD else None,
        scope=scope,
    )


def _scope_identity(
    scope: MemoryScope,
    resource_id: str,
    thread_id: str | None,
) -> str:
    if scope == MemoryScope.RESOURCE:
        return f"resource:{resource_id}"
    return f"thread:{resource_id}:{thread_id or ''}"
