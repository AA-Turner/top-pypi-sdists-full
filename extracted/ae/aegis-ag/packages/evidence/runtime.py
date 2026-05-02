"""Explainable evidence retrieval and wake-recovery helpers."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from packages.contracts.runtime import (
    EmbeddingIndexInvalidation,
    EmbeddingIndexPolicy,
    EmbeddingIndexRebuildPlan,
    EvidenceCandidate,
    EvidenceRetrievalRequest,
    EvidenceRetrievalResult,
    MemoryRecord,
    RecallReason,
    RecallReasons,
    StructuredTurnRecord,
    StructuredTurnSlot,
)
from packages.embeddings import (
    AEGIS_EMBED_MODEL_ID,
    AEGIS_EMBED_ONLINE_DIMENSIONS,
    EmbeddingPreloadEntry,
    EmbeddingService,
    build_default_embedding_service,
    cosine_similarity,
    embedding_runtime_is_loaded,
    embedding_mode_for_latency,
    resolve_embedding_dimensions,
)
from packages.storage import RuntimeStorageRepository
from .intent_support import build_resume_packet, focus_work_item_ids, intent_scope_hints, intent_score_adjustments

if TYPE_CHECKING:
    from .memory_runtime import MemoryStore


_LEXICAL_INDEX_VERSION = "fts5-memory-v1"
_EMBEDDING_INDEX_VERSION = f"{AEGIS_EMBED_MODEL_ID}@2026-04"
_EVIDENCE_EMBED_TEXT_LIMIT = 8_192
_EVIDENCE_BACKFILL_TOP_K = 8
_CONTINUITY_QUERY_TOKENS = frozenset(
    {
        "continue",
        "continuity",
        "handoff",
        "left",
        "next",
        "pick",
        "recover",
        "recovery",
        "resume",
        "resumed",
        "step",
        "where",
    }
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[A-Za-z0-9_]+", text.lower()) if token}


def _query_session_ids(
    repository: RuntimeStorageRepository,
    *,
    profile_id: str | None = None,
    workspace_id: str | None = None,
) -> tuple[str, ...]:
    clauses: list[str] = []
    params: list[str] = []
    if profile_id:
        clauses.append("profile_id = ?")
        params.append(profile_id)
    if workspace_id:
        clauses.append("workspace_id = ?")
        params.append(workspace_id)
    if not clauses:
        return ()
    where_sql = " AND ".join(clauses)
    with repository.connection() as connection:
        rows = connection.execute(
            f"""
            SELECT session_id
            FROM sessions
            WHERE {where_sql}
            ORDER BY updated_at DESC, started_at DESC, session_id DESC
            """,
            tuple(params),
        ).fetchall()
    return tuple(dict.fromkeys(str(row["session_id"]) for row in rows))


@dataclass(frozen=True, slots=True)
class _ResolvedScope:
    session_ids: tuple[str, ...]
    opened_scopes: tuple[str, ...]
    scope_reason: str
    lineage_session_ids: tuple[str, ...]
    workspace_session_ids: tuple[str, ...]
    profile_session_ids: tuple[str, ...]
_REPLAY_SLOT_NAMES = ("observation", "reasoning", "action", "outcome")
_REPLAY_SLOT_LABELS = {
    "observation": "observation",
    "reasoning": "reasoning",
    "action": "action",
    "outcome": "outcome",
}
_REPLAY_DETAIL_RANK = {
    "summary_only": 0,
    "episode_summary": 1,
    "structured_summary": 2,
    "structured": 3,
    "raw_turn": 4,
    "raw_trace": 5,
}
def _tuple_from_metadata(value: object) -> tuple[str, ...]:
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value if str(item))
    if value is None:
        return ()
    cleaned = str(value).strip()
    return (cleaned,) if cleaned else ()
def _record_search_text(record: MemoryRecord, *, structured_text: str = "") -> str:
    return "\n".join(part for part in (record.content, structured_text) if part)
def _embedding_text(value: str, *, max_chars: int = _EVIDENCE_EMBED_TEXT_LIMIT) -> str:
    normalized = re.sub(r"\s+", " ", value).strip()
    if len(normalized) <= max_chars:
        return normalized
    return normalized[:max_chars].rstrip()
def _record_embedding_text(record: MemoryRecord, *, structured_text: str | None = None) -> str:
    if structured_text is None:
        structured_turn = _structured_turn_from_record(record)
        structured_text = (
            _replay_text(structured_turn, selected_slots=_REPLAY_SLOT_NAMES)
            if structured_turn is not None
            else ""
        )
    search_text = _record_search_text(record, structured_text=structured_text) or record.content
    return _embedding_text(search_text)
def _evidence_cache_key(record: MemoryRecord, *, search_text: str) -> str:
    created_at = record.created_at.isoformat() if record.created_at is not None else ""
    digest = hashlib.sha256(search_text.encode("utf-8")).hexdigest()[:16]
    return f"{record.memory_id}:{created_at}:{digest}"
def _evidence_preload_entry(record: MemoryRecord, *, structured_text: str = "") -> EmbeddingPreloadEntry:
    search_text = _record_embedding_text(record, structured_text=structured_text or None)
    return EmbeddingPreloadEntry(
        cache_key=_evidence_cache_key(record, search_text=search_text),
        text=search_text or record.content,
        metadata={
            "memory_id": record.memory_id,
            "memory_kind": record.kind,
            "session_id": record.session_id,
        },
    )
def _structured_slot_from_metadata(value: object) -> StructuredTurnSlot:
    if not isinstance(value, dict):
        return StructuredTurnSlot()
    return StructuredTurnSlot(
        summary=str(value.get("summary", "")),
        detail=_tuple_from_metadata(value.get("detail")),
        compression=str(value.get("compression", "structured")),
        provenance=str(value.get("provenance", "")),
        source_refs=_tuple_from_metadata(value.get("source_refs")),
        linkage_refs=_tuple_from_metadata(value.get("linkage_refs")),
    )
def _structured_turn_from_record(record: MemoryRecord) -> StructuredTurnRecord | None:
    if record.kind != "structured_turn":
        return None
    payload = record.metadata.get("structured_turn")
    if not isinstance(payload, dict):
        return None
    return StructuredTurnRecord(
        turn_id=str(payload.get("turn_id", record.memory_id)),
        session_id=str(payload.get("session_id", record.session_id)),
        source=str(payload.get("source", "runtime")),
        observation=_structured_slot_from_metadata(payload.get("observation")),
        reasoning=_structured_slot_from_metadata(payload.get("reasoning")),
        action=_structured_slot_from_metadata(payload.get("action")),
        outcome=_structured_slot_from_metadata(payload.get("outcome")),
        profile_id=str(payload.get("profile_id")) if payload.get("profile_id") is not None else None,
        workspace_id=str(payload.get("workspace_id")) if payload.get("workspace_id") is not None else None,
        source_event_id=str(payload.get("source_event_id")) if payload.get("source_event_id") is not None else record.source_event_id,
        reasoning_availability=str(payload.get("reasoning_availability", "summary_only")),
        reasoning_provenance=str(payload.get("reasoning_provenance", "runtime.decision_summary")),
        compression_tier=str(payload.get("compression_tier", "raw_turn")),
        work_item_ids=_tuple_from_metadata(payload.get("work_item_ids") or record.goal_refs),
        source_turn_ids=_tuple_from_metadata(payload.get("source_turn_ids")),
        correction_memory_ids=_tuple_from_metadata(payload.get("correction_memory_ids")),
        artifact_ids=_tuple_from_metadata(payload.get("artifact_ids")),
        created_at=record.created_at,
    )
def _normalize_target_slots(target_slots: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        dict.fromkeys(
            slot.strip().lower()
            for slot in target_slots
            if slot.strip().lower() in _REPLAY_SLOT_NAMES
        )
    )



def _detail_rank(compression: str) -> int:
    return _REPLAY_DETAIL_RANK.get(compression.strip().lower(), _REPLAY_DETAIL_RANK["structured_summary"])



def _project_slot(
    slot: StructuredTurnSlot,
    *,
    max_compression: str,
) -> tuple[StructuredTurnSlot, bool]:
    allowed_rank = _detail_rank(max_compression)
    slot_rank = _detail_rank(slot.compression)
    if slot_rank <= allowed_rank:
        return slot, False
    return (
        StructuredTurnSlot(
            summary=slot.summary,
            detail=(),
            compression=max_compression,
            provenance=slot.provenance,
            source_refs=slot.source_refs,
            linkage_refs=slot.linkage_refs,
        ),
        True,
    )



def _selected_replay_slots(
    request: EvidenceRetrievalRequest,
    turn: StructuredTurnRecord | None,
) -> tuple[str, ...]:
    explicit = _normalize_target_slots(request.target_slots)
    if explicit:
        return explicit
    if turn is None or request.replay_mode == "off":
        return ()
    return tuple(
        slot_name
        for slot_name in _REPLAY_SLOT_NAMES
        if getattr(turn, slot_name).summary or getattr(turn, slot_name).detail
    )



def _project_replay_record(
    turn: StructuredTurnRecord,
    *,
    selected_slots: tuple[str, ...],
    max_compression: str,
) -> tuple[StructuredTurnRecord, tuple[str, ...]]:
    slots = set(selected_slots)
    degraded_slots: list[str] = []

    def project(slot_name: str) -> StructuredTurnSlot:
        slot = getattr(turn, slot_name)
        if slot_name not in slots:
            return StructuredTurnSlot()
        projected, degraded = _project_slot(slot, max_compression=max_compression)
        if degraded:
            degraded_slots.append(slot_name)
        return projected

    return (
        StructuredTurnRecord(
            turn_id=turn.turn_id,
            session_id=turn.session_id,
            source=turn.source,
            observation=project("observation"),
            reasoning=project("reasoning"),
            action=project("action"),
            outcome=project("outcome"),
            profile_id=turn.profile_id,
            workspace_id=turn.workspace_id,
            source_event_id=turn.source_event_id,
            reasoning_availability=turn.reasoning_availability,
            reasoning_provenance=turn.reasoning_provenance,
            compression_tier=turn.compression_tier,
            work_item_ids=turn.work_item_ids,
            source_turn_ids=turn.source_turn_ids,
            correction_memory_ids=turn.correction_memory_ids,
            artifact_ids=turn.artifact_ids,
            created_at=turn.created_at,
        ),
        tuple(dict.fromkeys(degraded_slots)),
    )



def _slot_text(slot_name: str, slot: StructuredTurnSlot) -> tuple[str, ...]:
    label = _REPLAY_SLOT_LABELS.get(slot_name, slot_name)
    lines: list[str] = []
    if slot.summary:
        lines.append(f"{label}: {slot.summary}")
    lines.extend(slot.detail)
    return tuple(lines)



def _replay_text(turn: StructuredTurnRecord, *, selected_slots: tuple[str, ...]) -> str:
    lines: list[str] = []
    for slot_name in selected_slots:
        lines.extend(_slot_text(slot_name, getattr(turn, slot_name)))
    return "\n".join(line for line in lines if line)



def _replay_summary(turn: StructuredTurnRecord, *, selected_slots: tuple[str, ...]) -> str:
    slot_summary = ", ".join(selected_slots) or "structured evidence"
    work_summary = ", ".join(turn.work_item_ids[:2]) or "the active thread"
    if turn.compression_tier == "episode_summary" or len(turn.source_turn_ids) > 1:
        boundary = f"episode replay across {len(turn.source_turn_ids) or 1} turn(s)"
    else:
        boundary = "turn replay"
    selected_compressions = tuple(
        dict.fromkeys(
            getattr(turn, slot_name).compression
            for slot_name in selected_slots
            if getattr(turn, slot_name).summary or getattr(turn, slot_name).detail
        )
    )
    compression = ",".join(selected_compressions) if selected_compressions else turn.compression_tier
    return (
        f"{boundary} for {work_summary}; slots={slot_summary}; "
        f"compression={compression}; reasoning={turn.reasoning_availability}"
    )


class DefaultEvidenceRetriever:
    def __init__(
        self,
        store: "MemoryStore",
        repository: RuntimeStorageRepository | None = None,
        *,
        embedding_service: EmbeddingService | None = None,
    ) -> None:
        self.store = store
        self.repository = repository
        self.embedding_service = embedding_service or build_default_embedding_service()

    def retrieve(self, request: EvidenceRetrievalRequest) -> EvidenceRetrievalResult:
        resolved_scope = self._resolve_scope(request)
        scope_set = set(resolved_scope.session_ids)
        query_tokens = _tokenize(request.query)
        dims = resolve_embedding_dimensions(request.latency_mode)
        scope_records = tuple(
            record
            for record in self.store.list(include_inactive=request.include_inactive)
            if record.session_id in scope_set
        )
        query_vector: tuple[float, ...] = ()
        embeddings_allowed = bool(request.allow_embeddings)
        if embeddings_allowed:
            health = getattr(self.embedding_service, "health", None)
            if callable(health):
                try:
                    embeddings_allowed = embedding_runtime_is_loaded(health())
                except Exception:
                    embeddings_allowed = False
        if embeddings_allowed:
            try:
                query_embedding = self.embedding_service.embed_text(
                    request.query,
                    request_id=f"{request.session_id}:evidence-query",
                    task="evidence.retrieve",
                    latency_mode=request.latency_mode,
                )
                query_vector = query_embedding.values
                dims = query_embedding.dimensions
            except RuntimeError:
                query_vector = ()
        candidates: list[EvidenceCandidate] = []
        for record in scope_records:
            candidate = self._candidate_for_record(
                request,
                record,
                resolved_scope=resolved_scope,
                query_tokens=query_tokens,
                query_vector=query_vector,
                dims=dims,
            )
            if candidate is not None:
                candidates.append(candidate)
        candidates.sort(
            key=lambda item: (
                -item.score,
                -(
                    item.memory.created_at.timestamp()
                    if item.memory.created_at is not None
                    else 0.0
                ),
                item.evidence_id,
            )
        )
        selected = tuple(candidates[: request.limit])
        self._queue_candidate_backfill(
            request=request,
            candidates=tuple(candidates[: max(_EVIDENCE_BACKFILL_TOP_K, request.limit * 2)]),
            query_vector=query_vector,
        )
        recall_reasons = RecallReasons(
            opened_scopes=resolved_scope.opened_scopes,
            evidence_ids=tuple(candidate.evidence_id for candidate in selected),
            scope_reason=resolved_scope.scope_reason,
            rerank_summary=self._rerank_summary(selected),
            reasons=tuple(reason for candidate in selected for reason in candidate.reasons[:3]),
        )
        return EvidenceRetrievalResult(
            request=request,
            scope_session_ids=resolved_scope.session_ids,
            scope_reason=resolved_scope.scope_reason,
            candidates=selected,
            recall_reasons=recall_reasons,
            index_policy=build_embedding_index_policy(self.store),
        )

    def _resolve_scope(self, request: EvidenceRetrievalRequest) -> _ResolvedScope:
        requested_scopes = tuple(
            dict.fromkeys(
                (
                    *(scope for scope in request.scopes if scope),
                    *intent_scope_hints(request),
                )
            )
        ) or ("session",)
        session_ids: list[str] = [request.session_id]
        opened_scopes: list[str] = []

        lineage_session_ids = tuple(
            dict.fromkeys(
                request.lineage_session_ids
                or self._lineage_session_ids(request.session_id)
            )
        )
        workspace_session_ids = (
            _query_session_ids(self.repository, workspace_id=request.workspace_id)
            if self.repository is not None and request.workspace_id is not None and "workspace" in requested_scopes
            else ()
        )
        profile_session_ids = (
            _query_session_ids(self.repository, profile_id=request.profile_id)
            if self.repository is not None and request.profile_id and "profile" in requested_scopes
            else ()
        )

        for scope in requested_scopes:
            if scope == "turn":
                opened_scopes.append("turn")
            elif scope == "session":
                opened_scopes.append("session")
            elif scope == "lineage":
                opened_scopes.append("lineage")
                session_ids.extend(lineage_session_ids)
            elif scope == "workspace" and workspace_session_ids:
                opened_scopes.append("workspace")
                session_ids.extend(workspace_session_ids)
            elif scope == "profile" and profile_session_ids:
                opened_scopes.append("profile")
                session_ids.extend(profile_session_ids)

        resolved_session_ids = tuple(dict.fromkeys(session_ids))
        explicit_reason = request.scope_reason.strip()
        if explicit_reason:
            scope_reason = explicit_reason
        else:
            scope_reason = self._default_scope_reason(
                request,
                opened_scopes=tuple(opened_scopes),
                resolved_session_ids=resolved_session_ids,
            )
        return _ResolvedScope(
            session_ids=resolved_session_ids,
            opened_scopes=tuple(opened_scopes) or ("session",),
            scope_reason=scope_reason,
            lineage_session_ids=lineage_session_ids,
            workspace_session_ids=workspace_session_ids,
            profile_session_ids=profile_session_ids,
        )

    def _queue_candidate_backfill(
        self,
        *,
        request: EvidenceRetrievalRequest,
        candidates: tuple[EvidenceCandidate, ...],
        query_vector: tuple[float, ...],
    ) -> None:
        if not candidates or not query_vector:
            return
        self.embedding_service.queue_backfill(
            target="evidence",
            entries=tuple(_evidence_preload_entry(candidate.memory) for candidate in candidates),
            latency_mode=request.latency_mode,
        )

    def _lineage_session_ids(self, session_id: str) -> tuple[str, ...]:
        if self.repository is None:
            return (session_id,)
        lineage = self.repository.lineage(session_id)
        if not lineage:
            return (session_id,)
        return tuple(dict.fromkeys(state.session_id for state in lineage))

    def _default_scope_reason(
        self,
        request: EvidenceRetrievalRequest,
        *,
        opened_scopes: tuple[str, ...],
        resolved_session_ids: tuple[str, ...],
    ) -> str:
        intent = request.intent_decision
        focus_ids = focus_work_item_ids(request)
        reasons: list[str] = []
        if "lineage" in opened_scopes and len(resolved_session_ids) > 1:
            reasons.append("resume recovery expands recall across the durable session lineage")
        else:
            reasons.append("recovery stays inside the active session scope")
        if focus_ids:
            reasons.append(f"intent focus {', '.join(focus_ids[:2])} outranks generic recall")
        elif request.work_item_ids:
            reasons.append(f"active work {', '.join(request.work_item_ids[:2])} outranks generic recall")
        if intent is not None and intent.resume_signal != "none":
            reasons.append(f"intent signaled {intent.resume_signal} recovery handling")
        if request.relationship_hints:
            reasons.append("relationship continuity stays explicit during rerank")
        if "workspace" in opened_scopes:
            reasons.append("workspace scope opened because the active clone spans multiple sessions")
        if "profile" in opened_scopes:
            reasons.append("profile scope opened to preserve long-horizon continuity beyond one workspace")
        return "; ".join(reasons)

    def _candidate_for_record(
        self,
        request: EvidenceRetrievalRequest,
        record: MemoryRecord,
        *,
        resolved_scope: _ResolvedScope,
        query_tokens: set[str],
        query_vector: tuple[float, ...],
        dims: int,
    ) -> EvidenceCandidate | None:
        focus_ids = focus_work_item_ids(request)
        reasons: list[RecallReason] = []
        matched_scopes = self._matched_scopes(record, resolved_scope=resolved_scope)
        scope_score = 0.0
        if record.session_id == request.session_id:
            scope_score += 2.5
            reasons.append(RecallReason("scope.session", "current-session scope", 2.5))
        elif record.session_id in set(resolved_scope.lineage_session_ids):
            scope_score += 1.5
            reasons.append(RecallReason("scope.lineage", "recovery-scope session", 1.5))
        elif record.session_id in set(resolved_scope.workspace_session_ids):
            scope_score += 1.0
            reasons.append(RecallReason("scope.workspace", "workspace continuity scope", 1.0))
        elif record.session_id in set(resolved_scope.profile_session_ids):
            scope_score += 0.75
            reasons.append(RecallReason("scope.profile", "profile continuity scope", 0.75))

        structured_turn = _structured_turn_from_record(record)
        selected_slots = _selected_replay_slots(request, structured_turn)
        replay_record: StructuredTurnRecord | None = None
        replay_summary = ""
        degraded_slots: tuple[str, ...] = ()
        replay_text = ""
        structured_text = ""
        if structured_turn is not None:
            structured_text = _replay_text(structured_turn, selected_slots=_REPLAY_SLOT_NAMES)
            if selected_slots:
                replay_record, degraded_slots = _project_replay_record(
                    structured_turn,
                    selected_slots=selected_slots,
                    max_compression=request.max_compression,
                )
                replay_text = _replay_text(replay_record, selected_slots=selected_slots)
                replay_summary = _replay_summary(replay_record, selected_slots=selected_slots)

        search_text = "\n".join(part for part in (record.content, structured_text) if part)
        content_tokens = _tokenize(search_text)
        overlap = sorted(query_tokens & content_tokens)
        lexical_score = float(len(overlap)) * 2.0
        if overlap:
            reasons.append(RecallReason("lexical.query", f"query overlap: {','.join(overlap)}", lexical_score))
        tag_tokens = _tokenize(" ".join(record.tags))
        tag_overlap = sorted(query_tokens & tag_tokens)
        if tag_overlap:
            tag_score = float(len(tag_overlap)) * 1.25
            lexical_score += tag_score
            reasons.append(RecallReason("lexical.tags", f"tag overlap: {','.join(tag_overlap)}", tag_score))
            novel_tag_overlap = tuple(token for token in tag_overlap if token not in overlap)
            if novel_tag_overlap:
                novel_tag_score = float(len(novel_tag_overlap)) * 0.75
                lexical_score += novel_tag_score
                reasons.append(
                    RecallReason(
                        "lexical.tags.novel",
                        f"novel tag overlap: {','.join(novel_tag_overlap)}",
                        novel_tag_score,
                    )
                )

        vector_input = _record_embedding_text(record, structured_text=structured_text)
        vector_score = 0.0
        if query_vector:
            candidate_embedding = self.embedding_service.cached_vector(
                target="evidence",
                cache_key=_evidence_cache_key(record, search_text=vector_input),
                dimensions=dims,
            )
            if candidate_embedding is not None:
                vector_score = max(0.0, cosine_similarity(query_vector, candidate_embedding.values)) * 3.0
                if vector_score > 0.0:
                    reasons.append(
                        RecallReason(
                            "vector.aegis-embed",
                            f"matryoshka vector similarity via {embedding_mode_for_latency(request.latency_mode)}",
                            vector_score,
                        )
                    )

        graph_score = 0.0
        goal_overlap = tuple(goal_id for goal_id in focus_ids if goal_id in record.goal_refs)
        if goal_overlap:
            graph_score += float(len(goal_overlap)) * 3.5
            reasons.append(
                RecallReason(
                    "work.goal-overlap",
                    f"goal overlap: {','.join(goal_overlap)}",
                    graph_score,
                )
            )
        elif focus_ids and not record.goal_refs:
            graph_score -= 0.5
            reasons.append(
                RecallReason(
                    "work.generic-penalty",
                    "generic recall deprioritized behind active work",
                    -0.5,
                )
            )
        graph_delta, continuity_delta, intent_reasons = intent_score_adjustments(
            request,
            record=record,
            goal_overlap=goal_overlap,
        )
        graph_score += graph_delta
        reasons.extend(intent_reasons)

        relationship_score = 0.0
        relationship_tokens = _tokenize(" ".join(request.relationship_hints))
        relationship_overlap = sorted(relationship_tokens & (content_tokens | tag_tokens))
        if relationship_overlap:
            relationship_score += float(len(relationship_overlap)) * 0.8
            reasons.append(
                RecallReason(
                    "relationship.continuity",
                    f"relationship continuity overlap: {','.join(relationship_overlap)}",
                    relationship_score,
                )
            )

        continuity_score = 0.0
        if query_tokens & _CONTINUITY_QUERY_TOKENS:
            if record.kind in {"procedural", "semantic", "summary", "decision", "structured_turn"}:
                continuity_score += 1.75
                reasons.append(
                    RecallReason(
                        "continuity.intent",
                        f"continuity intent prefers durable kind {record.kind}",
                        continuity_score,
                    )
                )
            if record.goal_refs:
                continuity_score += 0.4
                reasons.append(
                    RecallReason(
                        "continuity.goal-link",
                        "goal-linked continuity",
                        0.4,
                    )
                )
            continuity_tags = {"continuity", "handoff", "recovery", "resume", "scope-aware"}
            if continuity_tags & set(record.tags):
                continuity_score += 0.4
                reasons.append(
                    RecallReason(
                        "continuity.tags",
                        "continuity-tag boost",
                        0.4,
                    )
                )

        continuity_score += continuity_delta

        replay_score = 0.0
        if structured_turn is not None:
            replay_score += 0.75
            reasons.append(RecallReason("replay.structured-turn", "structured turn evidence is replayable", 0.75))
            if request.replay_mode != "off":
                replay_score += 0.8
                reasons.append(
                    RecallReason(
                        "replay.mode",
                        f"explicit {request.replay_mode} replay requested",
                        0.8,
                    )
                )
                if selected_slots:
                    slot_score = float(len(selected_slots)) * 0.35
                    replay_score += slot_score
                    reasons.append(
                        RecallReason(
                            "replay.slots",
                            f"replay targets slots: {','.join(selected_slots)}",
                            slot_score,
                        )
                    )
                replay_overlap = sorted(query_tokens & _tokenize(replay_text))
                if replay_overlap:
                    overlap_score = float(len(replay_overlap)) * 2.25
                    replay_score += overlap_score
                    reasons.append(
                        RecallReason(
                            "replay.slot-overlap",
                            f"replay overlap: {','.join(replay_overlap)}",
                            overlap_score,
                        )
                    )
                if request.replay_mode == "turn":
                    if structured_turn.compression_tier == "raw_turn":
                        replay_score += 1.25
                        reasons.append(
                            RecallReason(
                                "replay.turn-boundary",
                                "turn replay prefers raw turn evidence",
                                1.25,
                            )
                        )
                elif request.replay_mode == "episode":
                    if structured_turn.compression_tier == "episode_summary" or len(structured_turn.source_turn_ids) > 1:
                        replay_score += 1.5
                        reasons.append(
                            RecallReason(
                                "replay.episode-boundary",
                                "episode replay prefers multi-turn summaries",
                                1.5,
                            )
                        )
                    else:
                        replay_score += 0.5
                        reasons.append(
                            RecallReason(
                                "replay.episode-rebuild",
                                "raw turns remain eligible when an episode summary is unavailable",
                                0.5,
                            )
                        )
                if degraded_slots:
                    replay_score += 0.35
                    reasons.append(
                        RecallReason(
                            "replay.compression-fallback",
                            f"replay fell back to {request.max_compression} for {','.join(degraded_slots)}",
                            0.35,
                        )
                    )
                elif selected_slots:
                    reasons.append(
                        RecallReason(
                            "replay.compression",
                            f"replay stayed within {request.max_compression}",
                            0.2,
                        )
                    )
            elif selected_slots:
                replay_score += 0.3
                reasons.append(
                    RecallReason(
                        "replay.slot-focus",
                        f"slot-aware retrieval focused on {','.join(selected_slots)}",
                        0.3,
                    )
                )
        elif request.replay_mode != "off":
            replay_score -= 0.5
            reasons.append(
                RecallReason(
                    "replay.generic-fallback",
                    "generic evidence stayed eligible because no structured turn record was available",
                    -0.5,
                )
            )

        lifecycle_score = 0.0
        if "corrected" in record.tags:
            lifecycle_score += 1.4
            reasons.append(RecallReason("lifecycle.corrected", "corrected memory", 1.4))

        recency_score = 0.0
        if record.created_at is not None:
            age_seconds = max(0.0, (_now() - record.created_at).total_seconds())
            recency_score = max(0.0, 2.0 - (age_seconds / 86400.0))
            reasons.append(RecallReason("time.recency", "recency boost", recency_score))

        total_score = (
            scope_score
            + lexical_score
            + vector_score
            + graph_score
            + relationship_score
            + continuity_score
            + replay_score
            + lifecycle_score
            + recency_score
        )
        if total_score <= 0.0 and not matched_scopes:
            return None
        return EvidenceCandidate(
            evidence_id=record.memory_id,
            memory=record,
            score=total_score,
            lexical_score=lexical_score,
            vector_score=vector_score,
            graph_score=graph_score + relationship_score + continuity_score,
            matched_scopes=matched_scopes,
            reasons=tuple(reasons),
            embedding_mode=embedding_mode_for_latency(request.latency_mode),
            replay_record=replay_record,
            replay_slots=selected_slots,
            replay_summary=replay_summary,
        )

    def _matched_scopes(self, record: MemoryRecord, *, resolved_scope: _ResolvedScope) -> tuple[str, ...]:
        scopes: list[str] = []
        if record.session_id in resolved_scope.session_ids:
            scopes.append("session")
        if record.session_id in resolved_scope.lineage_session_ids:
            scopes.append("lineage")
        if record.session_id in resolved_scope.workspace_session_ids:
            scopes.append("workspace")
        if record.session_id in resolved_scope.profile_session_ids:
            scopes.append("profile")
        return tuple(dict.fromkeys(scopes))

    def _rerank_summary(self, candidates: tuple[EvidenceCandidate, ...]) -> str:
        if not candidates:
            return "no evidence survived rerank"
        top = candidates[0]
        reasons = ", ".join(reason.code for reason in top.reasons[:4]) or "no explicit reasons"
        replay = f"; replay={top.replay_summary}" if top.replay_summary else ""
        return f"top evidence {top.evidence_id} survived rerank via {reasons}{replay}"


def _memory_sort_key(record: MemoryRecord) -> tuple[datetime, str]:
    return (
        record.created_at or datetime.min.replace(tzinfo=timezone.utc),
        record.memory_id,
    )


def _index_refresh_action(*, lifecycle_state: str, replacement_evidence_id: str | None) -> str:
    if lifecycle_state in {"superseded", "consolidated"} and replacement_evidence_id:
        return "replace"
    if lifecycle_state == "deleted":
        return "drop"
    return "refresh"


def _index_invalidation_reason(*, lifecycle_state: str, replacement_evidence_id: str | None) -> str:
    if lifecycle_state == "superseded" and replacement_evidence_id:
        return f"superseded evidence must be replaced by {replacement_evidence_id} before lexical and vector views are trusted"
    if lifecycle_state == "consolidated" and replacement_evidence_id:
        return f"consolidated evidence must be replaced by summary {replacement_evidence_id} before lexical and vector views are trusted"
    if lifecycle_state == "deleted":
        return "deleted evidence must be removed from lexical and vector views"
    return f"{lifecycle_state} evidence must refresh derived lexical and vector views from canonical rows"


def _embedding_index_invalidations(store: "MemoryStore") -> tuple[EmbeddingIndexInvalidation, ...]:
    invalidations: list[EmbeddingIndexInvalidation] = []
    ordered_records = tuple(sorted(store.list(include_inactive=True), key=_memory_sort_key))
    for record in ordered_records:
        lifecycle_state = store.state(record.memory_id)
        if lifecycle_state in {None, "active"}:
            continue
        replacement_evidence_id = store.lineage(record.memory_id)
        preload_entry = _evidence_preload_entry(record)
        invalidations.append(
            EmbeddingIndexInvalidation(
                evidence_id=record.memory_id,
                lifecycle_state=lifecycle_state,
                stale_cache_key=preload_entry.cache_key,
                replacement_evidence_id=replacement_evidence_id,
                refresh_action=_index_refresh_action(
                    lifecycle_state=lifecycle_state,
                    replacement_evidence_id=replacement_evidence_id,
                ),
                reason=_index_invalidation_reason(
                    lifecycle_state=lifecycle_state,
                    replacement_evidence_id=replacement_evidence_id,
                ),
            )
        )
    return tuple(invalidations)


def build_embedding_index_rebuild_plan(store: "MemoryStore") -> EmbeddingIndexRebuildPlan:
    ordered_records = tuple(sorted(store.list(include_inactive=True), key=_memory_sort_key))
    active_records = tuple(
        record
        for record in ordered_records
        if store.state(record.memory_id) in {None, "active"}
    )
    invalidations = _embedding_index_invalidations(store)
    active_entries = tuple(_evidence_preload_entry(record) for record in active_records)
    replacement_evidence_ids = tuple(
        dict.fromkeys(
            invalidation.replacement_evidence_id
            for invalidation in invalidations
            if invalidation.replacement_evidence_id is not None
        )
    )
    if not invalidations:
        return EmbeddingIndexRebuildPlan(
            target="evidence",
            refresh_scope="noop",
            active_evidence_ids=tuple(record.memory_id for record in active_records),
            active_cache_keys=tuple(entry.cache_key for entry in active_entries),
            stale_cache_keys=(),
            replacement_evidence_ids=(),
            dimensions=AEGIS_EMBED_ONLINE_DIMENSIONS,
            steps=(
                "no rebuild is required while canonical evidence rows, lexical views, and shared vector projections stay aligned",
            ),
            summary="derived lexical and vector views already match the active canonical evidence rows",
        )
    stale_cache_keys = tuple(invalidation.stale_cache_key for invalidation in invalidations)
    steps = [
        f"drop {len(stale_cache_keys)} stale vector cache entr{'y' if len(stale_cache_keys) == 1 else 'ies'} for inactive evidence rows",
        f"rebuild lexical evidence views from {len(active_records)} active canonical row(s)",
        (
            f"reseed shared {AEGIS_EMBED_MODEL_ID} candidate vectors for {len(active_entries)} active evidence row(s) "
            f"at dimensions {', '.join(str(value) for value in AEGIS_EMBED_ONLINE_DIMENSIONS)}"
        ),
    ]
    if replacement_evidence_ids:
        steps.insert(
            1,
            f"promote lineage replacements before rebuild: {', '.join(replacement_evidence_ids)}",
        )
    return EmbeddingIndexRebuildPlan(
        target="evidence",
        refresh_scope="full",
        active_evidence_ids=tuple(record.memory_id for record in active_records),
        active_cache_keys=tuple(entry.cache_key for entry in active_entries),
        stale_cache_keys=stale_cache_keys,
        replacement_evidence_ids=replacement_evidence_ids,
        dimensions=AEGIS_EMBED_ONLINE_DIMENSIONS,
        steps=tuple(steps),
        summary=(
            f"refresh the evidence index from {len(active_records)} active canonical row(s) after "
            f"invalidating {len(invalidations)} stale derived entr{'y' if len(invalidations) == 1 else 'ies'}"
        ),
    )


def build_embedding_index_policy(store: "MemoryStore") -> EmbeddingIndexPolicy:
    invalidations = _embedding_index_invalidations(store)
    rebuild_plan = build_embedding_index_rebuild_plan(store)
    invalidation_reason = (
        "superseded, consolidated, and deleted evidence must invalidate derived lexical and vector views"
        if invalidations
        else "derived lexical and vector views are aligned with the active canonical evidence rows"
    )
    return EmbeddingIndexPolicy(
        model_id=AEGIS_EMBED_MODEL_ID,
        lexical_index_version=_LEXICAL_INDEX_VERSION,
        embedding_index_version=_EMBEDDING_INDEX_VERSION,
        active_dimensions=AEGIS_EMBED_ONLINE_DIMENSIONS,
        tracked_evidence_count=len(rebuild_plan.active_evidence_ids),
        rebuild_required=bool(invalidations),
        invalidated_evidence_ids=tuple(invalidation.evidence_id for invalidation in invalidations),
        invalidation_reason=invalidation_reason,
        invalidations=invalidations,
        rebuild_plan=rebuild_plan,
    )
