"""Durable memory ledger, extraction, consolidation, retrieval, and governance."""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timedelta, timezone
from typing import Mapping, Protocol, runtime_checkable

from packages.contracts.runtime import (
    EmbeddingIndexPolicy,
    EventEnvelope,
    EvidenceCandidate,
    EvidenceRetrievalRequest,
    EvidenceRetrievalResult,
    MemoryRecord,
    RecallReason,
    RecallReasons,
    ResumePacket,
    StructuredTurnRecord,
    StructuredTurnSlot,
)
from .runtime import DefaultEvidenceRetriever, build_embedding_index_policy, build_resume_packet
from packages.storage import RuntimeStorageRepository, StoredMemoryLedgerEntry, StoredMemoryRecord


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _split_csv(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    tokens = [item.strip() for item in value.replace("\n", ",").split(",")]
    return tuple(item for item in tokens if item)


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[A-Za-z0-9_]+", text.lower()) if token}


_CONTINUITY_QUERY_TOKENS = frozenset(
    {
        "continue",
        "continuity",
        "handoff",
        "left",
        "next",
        "pick",
        "resume",
        "resumed",
        "step",
        "where",
    }
)


def _unique(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(item for item in items if item))


def _resolved_scope_session_ids(session_id: str, scope_session_ids: tuple[str, ...]) -> tuple[str, ...]:
    return _unique((session_id,) + tuple(scope_session_ids))


def _continuity_intent_score(
    record: MemoryRecord,
    *,
    query_tokens: set[str],
) -> tuple[float, tuple[str, ...]]:
    if not (query_tokens & _CONTINUITY_QUERY_TOKENS):
        return 0.0, ()

    reasons: list[str] = []
    score = 0.0
    if record.kind in {"procedural", "semantic", "summary", "decision"}:
        score += 1.75
        reasons.append(f"continuity intent: {record.kind}")
    if record.goal_refs:
        score += 0.4
        reasons.append("goal-linked continuity")
    continuity_tags = {"continuity", "handoff", "recovery", "resume"}
    if continuity_tags & set(record.tags):
        score += 0.35
        reasons.append("continuity tag")
    return score, tuple(reasons)


def _to_stored_ledger_entry(entry: MemoryLedgerEntry) -> StoredMemoryLedgerEntry:
    return StoredMemoryLedgerEntry(
        entry_id=entry.entry_id,
        session_id=entry.session_id,
        event_id=entry.event_id,
        event_type=entry.event_type,
        content=entry.content,
        kind=entry.kind,
        source_event_id=entry.source_event_id,
        goal_refs=entry.goal_refs,
        tags=entry.tags,
        created_at=entry.created_at,
        metadata=dict(entry.metadata),
    )


def _from_stored_ledger_entry(entry: StoredMemoryLedgerEntry) -> MemoryLedgerEntry:
    return MemoryLedgerEntry(
        entry_id=entry.entry_id,
        session_id=entry.session_id,
        event_id=entry.event_id,
        event_type=entry.event_type,
        content=entry.content,
        kind=entry.kind,
        source_event_id=entry.source_event_id,
        goal_refs=entry.goal_refs,
        tags=entry.tags,
        created_at=entry.created_at or _now(),
        metadata=entry.metadata,
    )


def _to_stored_record(record: MemoryRecord) -> StoredMemoryRecord:
    return StoredMemoryRecord(
        memory_id=record.memory_id,
        session_id=record.session_id,
        kind=record.kind,
        content=record.content,
        source_event_id=record.source_event_id,
        goal_refs=record.goal_refs,
        tags=record.tags,
        created_at=record.created_at,
        metadata=dict(record.metadata),
    )


def _from_stored_record(record: StoredMemoryRecord) -> MemoryRecord:
    return MemoryRecord(
        memory_id=record.memory_id,
        session_id=record.session_id,
        kind=record.kind,
        content=record.content,
        source_event_id=record.source_event_id,
        goal_refs=record.goal_refs,
        tags=record.tags,
        created_at=record.created_at,
        metadata=record.metadata,
    )


def _structured_turn_content(record: StructuredTurnRecord) -> str:
    primary_work = record.work_item_ids[0] if record.work_item_ids else "active work"
    focus = (
        record.reasoning.summary.strip()
        or record.outcome.summary.strip()
        or record.action.summary.strip()
        or record.observation.summary.strip()
    )
    if focus:
        return f"Structured turn for {primary_work}: {focus}"
    return f"Structured turn for {primary_work}"


def _structured_turn_tags(record: StructuredTurnRecord, extra_tags: tuple[str, ...] = ()) -> tuple[str, ...]:
    base = (
        "structured-turn",
        f"reasoning:{record.reasoning_availability}",
        f"compression:{record.compression_tier}",
        "turn-evidence",
    )
    continuity = ("continuity",) if record.work_item_ids else ()
    return _unique(base + continuity + extra_tags)


def build_structured_turn_memory(
    record: StructuredTurnRecord,
    *,
    memory_id: str | None = None,
    extra_tags: tuple[str, ...] = (),
) -> MemoryRecord:
    payload = asdict(record)
    payload["schema"] = "structured_turn/v1"
    return MemoryRecord(
        memory_id=memory_id or f"{record.turn_id}:memory",
        session_id=record.session_id,
        kind="structured_turn",
        content=_structured_turn_content(record),
        source_event_id=record.source_event_id,
        goal_refs=record.work_item_ids,
        tags=_structured_turn_tags(record, extra_tags),
        created_at=record.created_at,
        metadata={"structured_turn": payload},
    )


def _tuple_from_object(value: object) -> tuple[str, ...]:
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value if str(item))
    if value is None:
        return ()
    cleaned = str(value).strip()
    return (cleaned,) if cleaned else ()


def _slot_from_object(value: object) -> StructuredTurnSlot:
    if not isinstance(value, dict):
        return StructuredTurnSlot()
    return StructuredTurnSlot(
        summary=str(value.get("summary", "")),
        detail=_tuple_from_object(value.get("detail")),
        compression=str(value.get("compression", "structured")),
        provenance=str(value.get("provenance", "")),
        source_refs=_tuple_from_object(value.get("source_refs")),
        linkage_refs=_tuple_from_object(value.get("linkage_refs")),
    )


def parse_structured_turn_memory(record: MemoryRecord | None) -> StructuredTurnRecord | None:
    if record is None or record.kind != "structured_turn":
        return None
    payload = record.metadata.get("structured_turn")
    if not isinstance(payload, dict):
        return None
    return StructuredTurnRecord(
        turn_id=str(payload.get("turn_id", record.memory_id)),
        session_id=str(payload.get("session_id", record.session_id)),
        source=str(payload.get("source", "runtime")),
        observation=_slot_from_object(payload.get("observation")),
        reasoning=_slot_from_object(payload.get("reasoning")),
        action=_slot_from_object(payload.get("action")),
        outcome=_slot_from_object(payload.get("outcome")),
        profile_id=str(payload.get("profile_id")) if payload.get("profile_id") is not None else None,
        workspace_id=str(payload.get("workspace_id")) if payload.get("workspace_id") is not None else None,
        source_event_id=str(payload.get("source_event_id")) if payload.get("source_event_id") is not None else record.source_event_id,
        reasoning_availability=str(payload.get("reasoning_availability", "summary_only")),
        reasoning_provenance=str(payload.get("reasoning_provenance", "runtime.decision_summary")),
        compression_tier=str(payload.get("compression_tier", "raw_turn")),
        work_item_ids=_tuple_from_object(payload.get("work_item_ids") or record.goal_refs),
        source_turn_ids=_tuple_from_object(payload.get("source_turn_ids")),
        correction_memory_ids=_tuple_from_object(payload.get("correction_memory_ids")),
        artifact_ids=_tuple_from_object(payload.get("artifact_ids")),
        created_at=record.created_at,
    )


def _merge_reasoning_availability(values: tuple[str, ...]) -> str:
    resolved = tuple(value for value in values if value)
    if not resolved:
        return "unavailable"
    if len(set(resolved)) == 1:
        return resolved[0]
    if "raw_trace" in resolved:
        return "mixed"
    return resolved[-1]


def _merge_reasoning_provenance(values: tuple[str, ...]) -> str:
    resolved = _unique(tuple(value for value in values if value))
    return ",".join(resolved)


def _compress_structured_turn_records(
    session_id: str,
    records: tuple[MemoryRecord, ...],
) -> MemoryConsolidationResult | None:
    structured = tuple(parse_structured_turn_memory(record) for record in records)
    if not structured or any(item is None for item in structured):
        return None
    turns = tuple(item for item in structured if item is not None)
    work_item_ids = _unique(tuple(work_item_id for turn in turns for work_item_id in turn.work_item_ids))
    source_turn_ids = _unique(tuple(turn.turn_id for turn in turns))
    artifact_ids = _unique(tuple(artifact_id for turn in turns for artifact_id in turn.artifact_ids))
    correction_memory_ids = _unique(
        tuple(correction_id for turn in turns for correction_id in turn.correction_memory_ids)
    )
    observation_detail = _unique(
        tuple(turn.observation.summary for turn in turns if turn.observation.summary)
    )
    reasoning_detail = _unique(
        tuple(turn.reasoning.summary for turn in turns if turn.reasoning.summary)
        + tuple(detail for turn in turns for detail in turn.reasoning.detail)
    )
    action_detail = _unique(
        tuple(turn.action.summary for turn in turns if turn.action.summary)
        + tuple(detail for turn in turns for detail in turn.action.detail)
    )
    outcome_detail = _unique(
        tuple(turn.outcome.summary for turn in turns if turn.outcome.summary)
        + tuple(detail for turn in turns for detail in turn.outcome.detail)
    )
    episode = StructuredTurnRecord(
        turn_id="turn-episode." + hashlib.sha256("|".join(record.memory_id for record in records).encode("utf-8")).hexdigest()[:12],
        session_id=session_id,
        source="memory.consolidation",
        observation=StructuredTurnSlot(
            summary=f"{len(turns)} turns preserved for {work_item_ids[0] if work_item_ids else 'long-horizon work'}",
            detail=observation_detail,
            compression="episode_summary",
            provenance="memory.consolidation",
            source_refs=tuple(record.memory_id for record in records),
            linkage_refs=work_item_ids,
        ),
        reasoning=StructuredTurnSlot(
            summary=reasoning_detail[0] if reasoning_detail else "",
            detail=reasoning_detail,
            compression="episode_summary",
            provenance=_merge_reasoning_provenance(tuple(turn.reasoning_provenance for turn in turns)),
            source_refs=tuple(record.memory_id for record in records),
            linkage_refs=source_turn_ids,
        ),
        action=StructuredTurnSlot(
            summary=action_detail[0] if action_detail else "",
            detail=action_detail,
            compression="episode_summary",
            provenance="memory.consolidation",
            source_refs=tuple(record.memory_id for record in records),
            linkage_refs=work_item_ids,
        ),
        outcome=StructuredTurnSlot(
            summary=outcome_detail[0] if outcome_detail else "",
            detail=outcome_detail,
            compression="episode_summary",
            provenance="memory.consolidation",
            source_refs=tuple(record.memory_id for record in records),
            linkage_refs=artifact_ids or work_item_ids,
        ),
        profile_id=turns[-1].profile_id,
        workspace_id=turns[-1].workspace_id,
        source_event_id=turns[-1].source_event_id,
        reasoning_availability=_merge_reasoning_availability(tuple(turn.reasoning_availability for turn in turns)),
        reasoning_provenance=_merge_reasoning_provenance(tuple(turn.reasoning_provenance for turn in turns)),
        compression_tier="episode_summary",
        work_item_ids=work_item_ids,
        source_turn_ids=source_turn_ids,
        correction_memory_ids=correction_memory_ids,
        artifact_ids=artifact_ids,
        created_at=_now(),
    )
    digest_source = "|".join(record.memory_id for record in records)
    summary_id = "memory.summary." + hashlib.sha256(digest_source.encode("utf-8")).hexdigest()[:12]
    summary_record = build_structured_turn_memory(
        episode,
        memory_id=summary_id,
        extra_tags=("consolidated", "episode-summary"),
    )
    return MemoryConsolidationResult(
        session_id=session_id,
        input_memory_ids=tuple(record.memory_id for record in records),
        summary_record=summary_record,
        superseded_memory_ids=tuple(record.memory_id for record in records),
        rationale="consolidated related structured turns into one replayable episode summary",
    )


@dataclass(frozen=True, slots=True)
class MemoryLedgerEntry:
    entry_id: str
    session_id: str
    event_id: str
    event_type: str
    content: str
    kind: str
    source_event_id: str | None = None
    goal_refs: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=_now)
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class MemoryAppendResult:
    ledger_entry: MemoryLedgerEntry
    extracted_records: tuple[MemoryRecord, ...]


@dataclass(frozen=True, slots=True)
class MemoryRetrievalCandidate:
    record: MemoryRecord
    score: float
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class MemoryRetrievalResult:
    session_id: str
    query: str
    goal_ids: tuple[str, ...]
    scope_session_ids: tuple[str, ...]
    scope_reason: str
    candidates: tuple[MemoryRetrievalCandidate, ...]


@dataclass(frozen=True, slots=True)
class MemoryConsolidationResult:
    session_id: str
    input_memory_ids: tuple[str, ...]
    summary_record: MemoryRecord | None
    superseded_memory_ids: tuple[str, ...] = ()
    rationale: str = ""


@dataclass(frozen=True, slots=True)
class MemoryMaintenanceResult:
    session_id: str
    maintained_memory_ids: tuple[str, ...]
    summary_record: MemoryRecord | None
    rationale: str


@dataclass(frozen=True, slots=True)
class MemoryGovernanceDecision:
    action: str
    target_memory_id: str | None
    allowed: bool
    reason: str
    actor: str = "user"
    replacement_memory_id: str | None = None


@dataclass(frozen=True, slots=True)
class MemoryGovernanceEvent:
    entry_id: str
    session_id: str
    action: str
    target_memory_id: str | None
    allowed: bool
    actor: str
    reason: str
    replacement_memory_id: str | None = None
    related_memory_ids: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=_now)


@dataclass(frozen=True, slots=True)
class MemoryGovernancePolicy:
    allow_user_corrections: bool = True
    allow_user_deletions: bool = True
    protected_tags: tuple[str, ...] = ("pinned", "system", "locked")
    minimum_content_length: int = 1
    semantic_kinds: tuple[str, ...] = ("semantic", "procedural", "artifact")


@runtime_checkable
class MemoryLedger(Protocol):
    def append(self, entry: MemoryLedgerEntry) -> None:
        """Append a ledger entry."""

    def list(self, session_id: str | None = None) -> tuple[MemoryLedgerEntry, ...]:
        """List entries, optionally filtered by session."""


@runtime_checkable
class MemoryStore(Protocol):
    def upsert(self, record: MemoryRecord) -> None:
        """Persist a memory record."""

    def get(self, memory_id: str) -> MemoryRecord | None:
        """Return a memory record by id."""

    def list(self, session_id: str | None = None, *, include_inactive: bool = False) -> tuple[MemoryRecord, ...]:
        """List memory records, optionally filtered by session."""

    def mark_consolidated(self, source_ids: tuple[str, ...], summary_id: str) -> None:
        """Mark source records as consolidated into a summary."""

    def mark_superseded(self, source_id: str, replacement_id: str) -> None:
        """Mark a record as superseded by a correction."""

    def mark_deleted(self, memory_id: str) -> None:
        """Mark a record as deleted."""

    def state(self, memory_id: str) -> str | None:
        """Return the current lifecycle state for a record."""

    def lineage(self, memory_id: str) -> str | None:
        """Return the current lineage target for a record, if any."""


@runtime_checkable
class MemoryExtractor(Protocol):
    def extract(self, event: EventEnvelope) -> MemoryAppendResult:
        """Turn a raw event into durable ledger and memory records."""


@runtime_checkable
class MemoryConsolidator(Protocol):
    def consolidate(self, session_id: str, records: tuple[MemoryRecord, ...]) -> MemoryConsolidationResult:
        """Derive a smaller summary memory from raw records."""


@runtime_checkable
class MemoryRetriever(Protocol):
    def retrieve(
        self,
        session_id: str,
        query: str,
        *,
        goal_ids: tuple[str, ...] = (),
        limit: int = 5,
        scope_session_ids: tuple[str, ...] = (),
        scope_reason: str = "",
    ) -> MemoryRetrievalResult:
        """Rank memories for a session and explicit recovery scope."""


@runtime_checkable
class MemoryGovernance(Protocol):
    def can_record(self, record: MemoryRecord) -> MemoryGovernanceDecision:
        """Check whether a memory record can be stored."""

    def can_consolidate(self, records: tuple[MemoryRecord, ...]) -> MemoryGovernanceDecision:
        """Check whether a consolidation is allowed."""

    def can_correct(
        self,
        original: MemoryRecord,
        corrected_content: str,
        *,
        actor: str,
    ) -> MemoryGovernanceDecision:
        """Check whether a correction is allowed."""

    def can_delete(
        self,
        original: MemoryRecord,
        *,
        actor: str,
        reason: str,
    ) -> MemoryGovernanceDecision:
        """Check whether deletion is allowed."""


class InMemoryMemoryLedger:
    def __init__(self) -> None:
        self._entries: list[MemoryLedgerEntry] = []

    def append(self, entry: MemoryLedgerEntry) -> None:
        self._entries.append(entry)

    def list(self, session_id: str | None = None) -> tuple[MemoryLedgerEntry, ...]:
        entries = self._entries
        if session_id is not None:
            entries = [entry for entry in entries if entry.session_id == session_id]
        return tuple(entries)


class InMemoryMemoryStore:
    def __init__(self) -> None:
        self._records: dict[str, MemoryRecord] = {}
        self._states: dict[str, str] = {}
        self._lineage: dict[str, str] = {}

    def upsert(self, record: MemoryRecord) -> None:
        self._records[record.memory_id] = record
        self._states.setdefault(record.memory_id, "active")

    def get(self, memory_id: str) -> MemoryRecord | None:
        return self._records.get(memory_id)

    def list(self, session_id: str | None = None, *, include_inactive: bool = False) -> tuple[MemoryRecord, ...]:
        records = tuple(self._records.values())
        if session_id is not None:
            records = tuple(record for record in records if record.session_id == session_id)
        if include_inactive:
            return records
        return tuple(record for record in records if self._states.get(record.memory_id, "active") == "active")

    def mark_consolidated(self, source_ids: tuple[str, ...], summary_id: str) -> None:
        for source_id in source_ids:
            self._states[source_id] = "consolidated"
            self._lineage[source_id] = summary_id

    def mark_superseded(self, source_id: str, replacement_id: str) -> None:
        self._states[source_id] = "superseded"
        self._lineage[source_id] = replacement_id

    def mark_deleted(self, memory_id: str) -> None:
        self._states[memory_id] = "deleted"

    def state(self, memory_id: str) -> str | None:
        return self._states.get(memory_id)

    def lineage(self, memory_id: str) -> str | None:
        return self._lineage.get(memory_id)


class SQLiteMemoryLedger:
    def __init__(self, repository: RuntimeStorageRepository) -> None:
        self.repository = repository

    def append(self, entry: MemoryLedgerEntry) -> None:
        self.repository.append_memory_ledger(_to_stored_ledger_entry(entry))

    def list(self, session_id: str | None = None) -> tuple[MemoryLedgerEntry, ...]:
        return tuple(
            _from_stored_ledger_entry(entry) for entry in self.repository.list_memory_ledger(session_id=session_id)
        )


class SQLiteMemoryStore:
    def __init__(self, repository: RuntimeStorageRepository) -> None:
        self.repository = repository

    def upsert(self, record: MemoryRecord) -> None:
        self.repository.upsert_memory_record(_to_stored_record(record))

    def get(self, memory_id: str) -> MemoryRecord | None:
        record = self.repository.load_memory_record(memory_id)
        return _from_stored_record(record) if record is not None else None

    def list(self, session_id: str | None = None, *, include_inactive: bool = False) -> tuple[MemoryRecord, ...]:
        return tuple(
            _from_stored_record(record)
            for record in self.repository.list_memory_records(session_id=session_id, include_inactive=include_inactive)
        )

    def mark_consolidated(self, source_ids: tuple[str, ...], summary_id: str) -> None:
        self.repository.mark_memory_consolidated(source_ids, summary_id)

    def mark_superseded(self, source_id: str, replacement_id: str) -> None:
        self.repository.mark_memory_superseded(source_id, replacement_id)

    def mark_deleted(self, memory_id: str) -> None:
        self.repository.mark_memory_deleted(memory_id)

    def state(self, memory_id: str) -> str | None:
        return self.repository.memory_state(memory_id)

    def lineage(self, memory_id: str) -> str | None:
        return self.repository.memory_lineage(memory_id)


class DefaultMemoryExtractor:
    def __init__(self, *, default_kind: str = "episodic") -> None:
        self.default_kind = default_kind

    def _kind_for_event(self, event: EventEnvelope, payload: Mapping[str, str]) -> str:
        explicit = payload.get("memory_kind") or payload.get("kind")
        if explicit:
            return explicit
        if event.event_type in {"goal_update", "goal_snapshot"}:
            return "semantic"
        if event.event_type in {"procedure", "preference", "skill"}:
            return "procedural"
        if event.event_type in {"artifact", "file", "link"}:
            return "artifact"
        return self.default_kind

    def extract(self, event: EventEnvelope) -> MemoryAppendResult:
        payload = event.payload
        content = payload.get("content") or payload.get("summary") or payload.get("text") or ""
        if not content.strip():
            content = payload.get("note", "")

        goal_refs = _unique(
            _split_csv(payload.get("goal_refs"))
            + _split_csv(payload.get("goal_ref"))
            + _split_csv(payload.get("goal_ids"))
            + _split_csv(payload.get("goal_id"))
        )
        tags = _unique(_split_csv(payload.get("tags")) + _split_csv(payload.get("tag")))
        kind = self._kind_for_event(event, payload)
        ledger_entry = MemoryLedgerEntry(
            entry_id=payload.get("ledger_entry_id", f"{event.event_id}:ledger"),
            session_id=event.session_id,
            event_id=event.event_id,
            event_type=event.event_type,
            content=content,
            kind=kind,
            source_event_id=payload.get("source_event_id", event.event_id),
            goal_refs=goal_refs,
            tags=tags,
            metadata={key: value for key, value in payload.items() if key not in {"content", "summary", "text"}},
        )
        if not content.strip():
            return MemoryAppendResult(ledger_entry=ledger_entry, extracted_records=())

        record = MemoryRecord(
            memory_id=payload.get("memory_id", f"{event.event_id}:memory"),
            session_id=event.session_id,
            kind=kind,
            content=content,
            source_event_id=ledger_entry.source_event_id,
            goal_refs=goal_refs,
            tags=tags,
            created_at=ledger_entry.created_at,
        )
        return MemoryAppendResult(ledger_entry=ledger_entry, extracted_records=(record,))


class DefaultMemoryConsolidator:
    def consolidate(self, session_id: str, records: tuple[MemoryRecord, ...]) -> MemoryConsolidationResult:
        if not records:
            return MemoryConsolidationResult(
                session_id=session_id,
                input_memory_ids=(),
                summary_record=None,
                rationale="no records available for consolidation",
            )

        ordered = tuple(
            sorted(
                records,
                key=lambda record: (
                    record.created_at or datetime.min.replace(tzinfo=timezone.utc),
                    record.memory_id,
                ),
            )
        )
        if len(ordered) == 1:
            return MemoryConsolidationResult(
                session_id=session_id,
                input_memory_ids=(ordered[0].memory_id,),
                summary_record=None,
                rationale="single record does not require consolidation",
            )

        if all(record.kind == "structured_turn" for record in ordered):
            compressed = _compress_structured_turn_records(session_id, ordered)
            if compressed is not None:
                return compressed

        content_fragments = []
        for record in ordered:
            fragment = record.content.strip().splitlines()[0]
            if fragment not in content_fragments:
                content_fragments.append(fragment)
        content = "; ".join(content_fragments[:3])
        goal_refs = _unique(tuple(ref for record in ordered for ref in record.goal_refs))
        tags = _unique(("consolidated",) + tuple(tag for record in ordered for tag in record.tags))
        kind = "semantic" if any(record.kind != "artifact" for record in ordered) else "artifact"
        digest_source = "|".join(record.memory_id for record in ordered)
        summary_id = "memory.summary." + hashlib.sha256(digest_source.encode("utf-8")).hexdigest()[:12]
        summary = MemoryRecord(
            memory_id=summary_id,
            session_id=session_id,
            kind=kind,
            content=f"Consolidated memory: {content}",
            source_event_id=ordered[-1].source_event_id,
            goal_refs=goal_refs,
            tags=tags,
            created_at=_now(),
            metadata={},
        )
        return MemoryConsolidationResult(
            session_id=session_id,
            input_memory_ids=tuple(record.memory_id for record in ordered),
            summary_record=summary,
            superseded_memory_ids=tuple(record.memory_id for record in ordered),
            rationale="consolidated related memories into one durable summary",
        )


class DefaultMemoryRetriever:
    def __init__(
        self,
        store: MemoryStore,
        *,
        repository: RuntimeStorageRepository | None = None,
        embedding_service: EmbeddingService | None = None,
    ) -> None:
        self.store = store
        self.repository = repository
        self.evidence_retriever = DefaultEvidenceRetriever(
            store,
            repository=repository,
            embedding_service=embedding_service,
        )

    def retrieve_evidence(self, request: EvidenceRetrievalRequest) -> EvidenceRetrievalResult:
        return self.evidence_retriever.retrieve(request)

    def retrieve(
        self,
        session_id: str,
        query: str,
        *,
        goal_ids: tuple[str, ...] = (),
        limit: int = 5,
        scope_session_ids: tuple[str, ...] = (),
        scope_reason: str = "",
    ) -> MemoryRetrievalResult:
        session = self.repository.load_session(session_id) if self.repository is not None else None
        request = EvidenceRetrievalRequest(
            session_id=session_id,
            profile_id=session.profile_id if session is not None else "profile:unknown",
            workspace_id=session.workspace_id if session is not None else None,
            lineage_session_ids=_resolved_scope_session_ids(session_id, scope_session_ids),
            work_item_ids=goal_ids,
            query=query,
            scopes=("session", "lineage") if len(_resolved_scope_session_ids(session_id, scope_session_ids)) > 1 else ("session",),
            latency_mode="fast",
            limit=limit,
            scope_reason=scope_reason,
        )
        evidence = self.retrieve_evidence(request)
        return MemoryRetrievalResult(
            session_id=session_id,
            query=query,
            goal_ids=goal_ids,
            scope_session_ids=evidence.scope_session_ids,
            scope_reason=evidence.scope_reason,
            candidates=tuple(
                MemoryRetrievalCandidate(
                    record=candidate.memory,
                    score=candidate.score,
                    reasons=tuple(reason.detail for reason in candidate.reasons),
                )
                for candidate in evidence.candidates
            ),
        )


class DefaultMemoryGovernance:
    def __init__(self, policy: MemoryGovernancePolicy | None = None) -> None:
        self.policy = policy or MemoryGovernancePolicy()

    def _is_protected(self, record: MemoryRecord) -> bool:
        return any(tag in self.policy.protected_tags for tag in record.tags)

    def can_record(self, record: MemoryRecord) -> MemoryGovernanceDecision:
        if not record.content.strip():
            return MemoryGovernanceDecision("record", record.memory_id, False, "memory content is empty")
        return MemoryGovernanceDecision("record", record.memory_id, True, "memory can be stored")

    def can_consolidate(self, records: tuple[MemoryRecord, ...]) -> MemoryGovernanceDecision:
        if not records:
            return MemoryGovernanceDecision("consolidate", None, False, "no records supplied for consolidation")
        return MemoryGovernanceDecision("consolidate", ",".join(record.memory_id for record in records), True, "consolidation is allowed")

    def can_correct(
        self,
        original: MemoryRecord,
        corrected_content: str,
        *,
        actor: str,
    ) -> MemoryGovernanceDecision:
        if len(corrected_content.strip()) < self.policy.minimum_content_length:
            return MemoryGovernanceDecision("correct", original.memory_id, False, "corrected content is empty", actor=actor)
        if self._is_protected(original) and actor != "system":
            return MemoryGovernanceDecision("correct", original.memory_id, False, "protected memory requires system actor", actor=actor)
        if actor == "user" and not self.policy.allow_user_corrections:
            return MemoryGovernanceDecision("correct", original.memory_id, False, "user corrections are disabled", actor=actor)
        return MemoryGovernanceDecision("correct", original.memory_id, True, "correction is allowed", actor=actor)

    def can_delete(
        self,
        original: MemoryRecord,
        *,
        actor: str,
        reason: str,
    ) -> MemoryGovernanceDecision:
        if self._is_protected(original) and actor != "system":
            return MemoryGovernanceDecision("delete", original.memory_id, False, "protected memory cannot be deleted by this actor", actor=actor)
        if actor == "user" and not self.policy.allow_user_deletions:
            return MemoryGovernanceDecision("delete", original.memory_id, False, "user deletions are disabled", actor=actor)
        if not reason.strip():
            return MemoryGovernanceDecision("delete", original.memory_id, False, "deletion reason is required", actor=actor)
        return MemoryGovernanceDecision("delete", original.memory_id, True, "deletion is allowed", actor=actor)


@dataclass(frozen=True, slots=True)
class MemoryMutationResult:
    decision: MemoryGovernanceDecision
    record: MemoryRecord | None = None


__all__ = [name for name in globals() if not name.startswith("__")]

