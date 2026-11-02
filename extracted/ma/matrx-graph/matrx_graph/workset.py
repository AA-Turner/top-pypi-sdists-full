"""Run-scoped durable work sets — incremental work discovery for workflows.

The canonical bridge between "a node discovered more work mid-run" and the
engine's dynamic fan-out. Implements the platform durable-work-queue standard
(common-docs/policies/durable-work-queue-standard.md) INSIDE the workflow
engine:

- The frontier lives in the database (``workflow.work_item``), never in
  process memory — deduped per ``(run_id, set_name)`` by ``canonical_key``.
- ``control.work_seed`` appends newly discovered items at any point in the
  run — including later waves, from workers processing earlier items. The
  total NEVER needs to be known at run start.
- ``control.work_queue`` claims batches (lease-fenced), Sends each item to
  its target node, and self-fires until the set drains. Each claimed item's
  id rides its Send (``Send.work_item_id``); the scheduler settles the item
  (succeeded/failed) when the target invocation's outcome is recorded — the
  ordering guarantee that makes the drain check sound: a worker's appends
  land DURING its execution, its settle lands AFTER, so
  ``pending == 0 and in_progress == 0`` proves no more discovery is coming
  from processing.
- Crash recovery: an item claimed by a process that died sits ``in_progress``
  until its lease expires; ``reclaim_expired`` (run at every queue firing)
  returns it to ``pending`` (or ``dead_letter`` past ``max_attempts``).
  At-least-once semantics, exactly like the platform standard.

The store is injected: ``MemoryWorkSetStore`` (default) keeps standalone /
in-memory graphs working with zero setup; the host app configures
``PostgresWorkSetStore`` at startup for durability
(``configure_work_set_store(PostgresWorkSetStore())`` — aidream does this in
``package_integration.py``).

The table deliberately mirrors ``runtime.work_item`` (the Request Management
Layer's batch primitive) so a later cutover onto the runtime spine is a
column-map, not a redesign — it is not reused directly because
``runtime.work_item`` hard-FKs ``runtime.global_execution`` and workflow runs
do not yet live on that spine.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta
from typing import Any, Literal, Protocol, runtime_checkable
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

# Default per-item retry budget for lease-reclaimed items (crash recovery).
# A CAPS constant — engine-level retries of a live invocation are separate
# (NodeDef retry_policy); this only bounds crash-reclaim loops.
DEFAULT_MAX_WORK_ITEM_ATTEMPTS = 3

WorkItemState = Literal["pending", "in_progress", "succeeded", "failed", "dead_letter"]


class WorkItemSeed(BaseModel):
    """One discovered unit of work. ``canonical_key`` is the caller's
    canonicalized identity — the dedup key within ``(run_id, set_name)``.
    ``payload`` is the opaque per-item data the worker node receives."""

    model_config = ConfigDict(frozen=True)

    canonical_key: str
    payload: dict[str, Any] = Field(default_factory=dict)
    max_attempts: int = DEFAULT_MAX_WORK_ITEM_ATTEMPTS


class WorkItemClaim(BaseModel):
    """A claimed item handed to the dispatcher — everything the queue needs
    to Send it and everything the visuals need to label it."""

    model_config = ConfigDict(frozen=True)

    id: str
    canonical_key: str
    payload: dict[str, Any] = Field(default_factory=dict)
    attempts: int = 1
    wave: int = 1


class WorkSetCounts(BaseModel):
    """Live state distribution of one run's work set — the progress truth
    the queue's drain check and the studio's progress badges both read."""

    model_config = ConfigDict(frozen=True)

    pending: int = 0
    in_progress: int = 0
    succeeded: int = 0
    failed: int = 0
    dead_letter: int = 0

    @property
    def discovered(self) -> int:
        return self.pending + self.in_progress + self.succeeded + self.failed + self.dead_letter

    @property
    def settled(self) -> int:
        return self.succeeded + self.failed + self.dead_letter

    @property
    def drained(self) -> bool:
        return self.pending == 0 and self.in_progress == 0


@runtime_checkable
class WorkSetStore(Protocol):
    """Durable frontier for one run's discovered work.

    Implementations MUST make ``append`` dedup by ``(run_id, set_name,
    canonical_key)`` (an existing key in ANY state is a no-op), ``claim``
    atomic under concurrency (one winner per item), and ``settle`` calls
    idempotent (settling an already-settled item is a no-op returning False).
    """

    async def append(
        self,
        run_id: str,
        set_name: str,
        items: list[WorkItemSeed],
        *,
        discovered_by: str = "",
    ) -> int:
        """Insert new items; returns how many were actually new."""
        ...

    async def claim(
        self,
        run_id: str,
        set_name: str,
        *,
        limit: int,
        holder: str,
        lease_seconds: int,
        wave: int,
    ) -> list[WorkItemClaim]: ...

    async def complete(self, item_id: str, *, run_id: str) -> bool: ...

    async def fail(
        self, item_id: str, *, run_id: str, error: dict[str, Any] | None = None
    ) -> bool: ...

    async def reclaim_expired(self, run_id: str, set_name: str) -> int:
        """Expired in_progress leases → pending (or dead_letter past
        max_attempts). Returns how many were reclaimed either way."""
        ...

    async def counts(self, run_id: str, set_name: str) -> WorkSetCounts: ...


def canonical_key_for(item: Any) -> str:
    """Default canonicalization: stable content hash of the JSON item.

    ONE shared function per the durable-work-queue standard — every caller
    that doesn't extract an explicit key funnels through here so the same
    payload can never enter one set twice under two spellings.
    """
    encoded = json.dumps(item, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:32]


# ---------------------------------------------------------------------------
# In-memory implementation — standalone graphs and tests
# ---------------------------------------------------------------------------


class _MemoryItem:
    __slots__ = (
        "attempts",
        "canonical_key",
        "id",
        "lease_expires_at",
        "max_attempts",
        "payload",
        "seq",
        "state",
        "wave",
    )

    def __init__(self, seq: int, seed: WorkItemSeed) -> None:
        self.id = str(uuid4())
        self.seq = seq
        self.canonical_key = seed.canonical_key
        self.payload = dict(seed.payload)
        self.max_attempts = seed.max_attempts
        self.state: WorkItemState = "pending"
        self.attempts = 0
        self.wave = 0
        self.lease_expires_at: datetime | None = None


class MemoryWorkSetStore:
    """Process-local WorkSetStore — the zero-setup default.

    Correct for a single-process run (the in-memory checkpointer pairing);
    NOT durable across restarts. Hosts that persist runs must configure
    ``PostgresWorkSetStore``.
    """

    def __init__(self) -> None:
        self._sets: dict[tuple[str, str], dict[str, _MemoryItem]] = {}
        self._by_id: dict[str, _MemoryItem] = {}
        self._seq = 0

    def _set(self, run_id: str, set_name: str) -> dict[str, _MemoryItem]:
        return self._sets.setdefault((run_id, set_name), {})

    async def append(
        self,
        run_id: str,
        set_name: str,
        items: list[WorkItemSeed],
        *,
        discovered_by: str = "",
    ) -> int:
        bucket = self._set(run_id, set_name)
        added = 0
        for seed in items:
            if seed.canonical_key in bucket:
                continue
            self._seq += 1
            item = _MemoryItem(self._seq, seed)
            bucket[seed.canonical_key] = item
            self._by_id[item.id] = item
            added += 1
        return added

    async def claim(
        self,
        run_id: str,
        set_name: str,
        *,
        limit: int,
        holder: str,
        lease_seconds: int,
        wave: int,
    ) -> list[WorkItemClaim]:
        bucket = self._set(run_id, set_name)
        now = datetime.now(UTC)
        claims: list[WorkItemClaim] = []
        for item in sorted(bucket.values(), key=lambda i: i.seq):
            if len(claims) >= limit:
                break
            if item.state != "pending":
                continue
            item.state = "in_progress"
            item.attempts += 1
            item.wave = wave
            item.lease_expires_at = now + timedelta(seconds=lease_seconds)
            claims.append(
                WorkItemClaim(
                    id=item.id,
                    canonical_key=item.canonical_key,
                    payload=dict(item.payload),
                    attempts=item.attempts,
                    wave=wave,
                )
            )
        return claims

    async def complete(self, item_id: str, *, run_id: str) -> bool:
        item = self._by_id.get(item_id)
        if item is None or item.state not in ("in_progress", "pending"):
            return False
        item.state = "succeeded"
        item.lease_expires_at = None
        return True

    async def fail(self, item_id: str, *, run_id: str, error: dict[str, Any] | None = None) -> bool:
        item = self._by_id.get(item_id)
        if item is None or item.state not in ("in_progress", "pending"):
            return False
        item.state = "failed"
        item.lease_expires_at = None
        return True

    async def reclaim_expired(self, run_id: str, set_name: str) -> int:
        bucket = self._set(run_id, set_name)
        now = datetime.now(UTC)
        reclaimed = 0
        for item in bucket.values():
            if item.state != "in_progress":
                continue
            if item.lease_expires_at is not None and item.lease_expires_at > now:
                continue
            item.state = "dead_letter" if item.attempts >= item.max_attempts else "pending"
            item.lease_expires_at = None
            reclaimed += 1
        return reclaimed

    async def counts(self, run_id: str, set_name: str) -> WorkSetCounts:
        bucket = self._set(run_id, set_name)
        tally: dict[str, int] = {}
        for item in bucket.values():
            tally[item.state] = tally.get(item.state, 0) + 1
        return WorkSetCounts(**tally)


# ---------------------------------------------------------------------------
# Postgres implementation — workflow.work_item via the injected ORM model
# ---------------------------------------------------------------------------


class PostgresWorkSetStore:
    """Durable WorkSetStore over ``workflow.work_item`` (host-injected
    ``WfWorkItem`` model, like every other matrx-graph store).

    Claim is a single-statement atomic batch via matrx-orm's ``claim_batch``
    (UPDATE … WHERE pk IN (SELECT … FOR UPDATE SKIP LOCKED) RETURNING) — the
    same primitive the workflow job queue uses; splitting it into
    SELECT-then-UPDATE would reopen the double-claim race SKIP LOCKED closes.
    """

    async def append(
        self,
        run_id: str,
        set_name: str,
        items: list[WorkItemSeed],
        *,
        discovered_by: str = "",
    ) -> int:
        from matrx_graph.db._registry import get_model

        if not items:
            return 0
        model = get_model("WfWorkItem")
        # A work item is a component of its run and carries the run's organization.
        run = await get_model("WfRun").load_by_id_or_none(str(UUID(run_id)), use_cache=False)
        if run is None or not getattr(run, "organization_id", None):
            raise ValueError(f"workset.append: run {run_id} has no organization to inherit")
        organization_id = str(run.organization_id)
        rows = [
            {
                "organization_id": organization_id,
                "run_id": str(UUID(run_id)),
                "set_name": set_name,
                "canonical_key": seed.canonical_key,
                "payload": seed.payload,
                "max_attempts": seed.max_attempts,
                "discovered_by": discovered_by,
                "state": "pending",
            }
            for seed in items
        ]
        landed = await model.bulk_insert_ignore(
            rows,
            on_conflict=["run_id", "set_name", "canonical_key"],
        )
        return int(landed) if isinstance(landed, int) else len(landed)

    async def claim(
        self,
        run_id: str,
        set_name: str,
        *,
        limit: int,
        holder: str,
        lease_seconds: int,
        wave: int,
    ) -> list[WorkItemClaim]:
        from matrx_orm import F, Now

        from matrx_graph.db._registry import get_model

        lease_until = datetime.now(UTC) + timedelta(seconds=lease_seconds)
        rows = await get_model("WfWorkItem").claim_batch(
            set_fields={
                "state": "in_progress",
                "claim_holder": holder,
                "claimed_at": Now(),
                "lease_expires_at": lease_until,
                "attempts": F("attempts") + 1,
                "wave": wave,
            },
            filters={
                "run_id": str(UUID(run_id)),
                "set_name": set_name,
                "state": "pending",
            },
            order_by="seq",
            limit=limit,
        )
        # claim_batch's RETURNING order is whatever the UPDATE emits, NOT the
        # inner SELECT's ORDER BY (documented in matrx_orm.operations.
        # queue_claim — "callers that need claim order should re-sort").
        # MemoryWorkSetStore returns seq order; keep the stores in parity so
        # a wave dispatches items in discovery order on both backends.
        rows.sort(key=lambda row: row["seq"])
        return [
            WorkItemClaim(
                id=str(row["id"]),
                canonical_key=row["canonical_key"],
                payload=row["payload"] or {},
                attempts=row["attempts"],
                wave=wave,
            )
            for row in rows
        ]

    async def complete(self, item_id: str, *, run_id: str) -> bool:
        from matrx_graph.db._registry import get_model

        result = await get_model("WfWorkItem").update_where(
            {
                "id": str(UUID(item_id)),
                "run_id": str(UUID(run_id)),
                "state__in": ["in_progress", "pending"],
            },
            state="succeeded",
            completed_at=datetime.now(UTC),
            lease_expires_at=None,
        )
        return result.rows_affected == 1

    async def fail(self, item_id: str, *, run_id: str, error: dict[str, Any] | None = None) -> bool:
        from matrx_graph.db._registry import get_model

        result = await get_model("WfWorkItem").update_where(
            {
                "id": str(UUID(item_id)),
                "run_id": str(UUID(run_id)),
                "state__in": ["in_progress", "pending"],
            },
            state="failed",
            error=error,
            completed_at=datetime.now(UTC),
            lease_expires_at=None,
        )
        return result.rows_affected == 1

    async def reclaim_expired(self, run_id: str, set_name: str) -> int:
        from matrx_orm import Compare, F

        from matrx_graph.db._registry import get_model

        now = datetime.now(UTC)
        model = get_model("WfWorkItem")
        # Two guarded UPDATEs, dead-letter first so an exhausted item can't
        # slip back to pending between statements.
        dead = await model.filter(
            Compare(F("attempts"), ">=", F("max_attempts")),
            run_id=str(UUID(run_id)),
            set_name=set_name,
            state="in_progress",
            lease_expires_at__lte=now,
        ).update(state="dead_letter", lease_expires_at=None)
        back = await model.filter(
            Compare(F("attempts"), "<", F("max_attempts")),
            run_id=str(UUID(run_id)),
            set_name=set_name,
            state="in_progress",
            lease_expires_at__lte=now,
        ).update(state="pending", lease_expires_at=None, claim_holder=None)
        return dead.rows_affected + back.rows_affected

    async def counts(self, run_id: str, set_name: str) -> WorkSetCounts:
        from matrx_graph.db._registry import get_model

        rows = await (
            get_model("WfWorkItem")
            .filter(run_id=str(UUID(run_id)), set_name=set_name)
            .values("state")
        )
        tally: dict[str, int] = {}
        for row in rows:
            tally[row["state"]] = tally.get(row["state"], 0) + 1
        return WorkSetCounts(**tally)


# ---------------------------------------------------------------------------
# Injection point
# ---------------------------------------------------------------------------

_store: WorkSetStore | None = None


def configure_work_set_store(store: WorkSetStore | None) -> None:
    """Install the host's WorkSetStore (aidream: PostgresWorkSetStore, wired
    in package_integration). None resets to the in-memory default (tests)."""
    global _store
    _store = store


def get_work_set_store() -> WorkSetStore:
    global _store
    if _store is None:
        _store = MemoryWorkSetStore()
    return _store
