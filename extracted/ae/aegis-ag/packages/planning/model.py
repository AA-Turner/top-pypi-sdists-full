"""Core planning graph models and shared primitives."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime, timedelta
import re
from typing import Any, Literal, Mapping

from packages.contracts import GoalNode as ContractGoalNode
from packages.contracts import ActivityGraph

GoalStatus = Literal[
    "proposed",
    "queued",
    "active",
    "blocked",
    "deferred",
    "completed",
    "done",
    "failed",
    "dropped",
]
GoalOwner = Literal["user", "agent", "shared"]
GoalPriority = Literal["low", "medium", "high", "critical"]
TimeSensitivity = Literal["low", "normal", "high", "urgent"]
PlanningMode = Literal["reactive", "guided", "proactive"]
MoveKind = Literal[
    "answer_directly",
    "act_on_task",
    "ask_for_information",
    "update_plan",
    "defer_or_schedule",
]

GOAL_STATUS_ORDER: tuple[GoalStatus, ...] = (
    "proposed",
    "queued",
    "active",
    "blocked",
    "deferred",
    "completed",
    "done",
    "failed",
    "dropped",
)

GOAL_PRIORITY_ORDER: tuple[GoalPriority, ...] = ("low", "medium", "high", "critical")
TIME_SENSITIVITY_ORDER: tuple[TimeSensitivity, ...] = ("low", "normal", "high", "urgent")
PLANNING_MODES: tuple[PlanningMode, ...] = ("reactive", "guided", "proactive")
MOVE_KINDS: tuple[MoveKind, ...] = (
    "answer_directly",
    "act_on_task",
    "ask_for_information",
    "update_plan",
    "defer_or_schedule",
)

_PRIORITY_POINTS: Mapping[GoalPriority, float] = {
    "low": 1.0,
    "medium": 2.0,
    "high": 3.0,
    "critical": 4.0,
}

_STATUS_POINTS: Mapping[GoalStatus, float] = {
    "proposed": 0.8,
    "queued": 1.4,
    "active": 2.2,
    "blocked": 0.3,
    "deferred": 0.1,
    "completed": 0.0,
    "done": 0.0,
    "failed": 0.0,
    "dropped": 0.0,
}

_TIME_SENSITIVITY_POINTS: Mapping[TimeSensitivity, float] = {
    "low": 0.0,
    "normal": 0.3,
    "high": 0.7,
    "urgent": 1.1,
}

_TIME_SENSITIVITY_ALIASES: Mapping[str, TimeSensitivity] = {
    "low": "low",
    "normal": "normal",
    "medium": "normal",
    "high": "high",
    "urgent": "urgent",
}

_GOAL_STATUS_ALIASES: Mapping[str, GoalStatus] = {
    "proposed": "proposed",
    "queued": "queued",
    "active": "active",
    "in_progress": "active",
    "in-progress": "active",
    "blocked": "blocked",
    "deferred": "deferred",
    "completed": "completed",
    "complete": "completed",
    "done": "done",
    "failed": "failed",
    "dropped": "dropped",
    "cancelled": "dropped",
    "canceled": "dropped",
}

_GOAL_PRIORITY_ALIASES: Mapping[str, GoalPriority] = {
    "low": "low",
    "normal": "medium",
    "medium": "medium",
    "high": "high",
    "critical": "critical",
    "urgent": "critical",
}

_GOAL_OWNER_ALIASES: Mapping[str, GoalOwner] = {
    "user": "user",
    "agent": "agent",
    "assistant": "agent",
    "shared": "shared",
}

_INITIATIVE_CONTINUITY_BONUS: Mapping[str, float] = {
    "quiet": -0.1,
    "gentle": 0.0,
    "steady": 0.15,
    "proactive": 0.35,
    "direct": 0.2,
}


def _now() -> datetime:
    return datetime.now(UTC)


def _parse_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value)


def normalize_goal_status(value: object, *, default: GoalStatus = "proposed") -> GoalStatus:
    if value is None:
        return default
    normalized = str(value).strip().lower()
    return _GOAL_STATUS_ALIASES.get(normalized, default)


def normalize_goal_priority(value: object, *, default: GoalPriority = "medium") -> GoalPriority:
    if value is None:
        return default
    normalized = str(value).strip().lower()
    return _GOAL_PRIORITY_ALIASES.get(normalized, default)


def normalize_goal_owner(value: object, *, default: GoalOwner = "agent") -> GoalOwner:
    if value is None:
        return default
    normalized = str(value).strip().lower()
    return _GOAL_OWNER_ALIASES.get(normalized, default)


def normalize_time_sensitivity(value: object) -> TimeSensitivity:
    if value is None:
        return "normal"
    normalized = str(value).strip().lower()
    return _TIME_SENSITIVITY_ALIASES.get(normalized, "normal")


def _format_delta(delta: timedelta) -> str:
    seconds = int(delta.total_seconds())
    if seconds < 0:
        return f"{abs(seconds)}s overdue"
    minutes, rem_seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m"
    if minutes:
        return f"{minutes}m {rem_seconds}s"
    return f"{rem_seconds}s"


def _stringify(values: tuple[str, ...]) -> str:
    return ", ".join(values)


def _dedupe_strings(*groups: tuple[str, ...]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for group in groups:
        for item in group:
            text = str(item).strip()
            if not text or text in seen:
                continue
            seen.add(text)
            ordered.append(text)
    return tuple(ordered)


def _tokenize_goal_text(text: str) -> tuple[str, ...]:
    normalized = text.lower()
    tokens = re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]{1,4}", normalized)
    return tuple(token for token in tokens if len(token) > 1 or not token.isascii())


def _goal_similarity(left: str, right: str) -> float:
    left_tokens = set(_tokenize_goal_text(left))
    right_tokens = set(_tokenize_goal_text(right))
    if not left_tokens or not right_tokens:
        return 0.0
    overlap = len(left_tokens & right_tokens)
    return round(overlap / max(len(left_tokens), len(right_tokens)), 3)


def _goal_title_from_text(text: str) -> str:
    cleaned = " ".join(text.strip().split())
    if not cleaned:
        return "Follow the latest user request"
    for separator in ("。", ".", "!", "！", "?", "？", "\n"):
        if separator in cleaned:
            cleaned = cleaned.split(separator, 1)[0].strip()
            break
    return cleaned[:96].rstrip(" ,;:") or "Follow the latest user request"


def _normalize_initiative(initiative_hint: str | None) -> str:
    if initiative_hint is None:
        return "gentle"
    normalized = initiative_hint.strip().lower()
    return normalized or "gentle"


def _record_tuple(record: Mapping[str, Any], key: str) -> tuple[str, ...]:
    value = record.get(key)
    if value is None:
        return ()
    if isinstance(value, tuple):
        return tuple(str(item) for item in value)
    if isinstance(value, list):
        return tuple(str(item) for item in value)
    if isinstance(value, str):
        return () if value == "" else (value,)
    return tuple(str(item) for item in value)


def _continuity_note_bonus(notes: tuple[str, ...]) -> float:
    bonus = 0.0
    for note in notes:
        normalized = note.strip().lower()
        if not normalized:
            continue
        if any(token in normalized for token in ("check in", "follow up", "follow-up", "quiet gap", "resume", "reconnect")):
            bonus += 0.12
        elif any(token in normalized for token in ("continuity", "durable", "remember", "reach out")):
            bonus += 0.06
    return min(0.3, round(bonus, 3))


def _continuity_note_factors(notes: tuple[str, ...]) -> tuple[str, ...]:
    factors: list[str] = []
    for note in notes:
        normalized = "-".join(note.strip().lower().split())
        if normalized:
            factors.append(f"continuity-note={normalized[:48]}")
    return tuple(dict.fromkeys(factors))


def _dependencies_satisfied(goal: "GoalGraphNode", indexed: Mapping[str, "GoalGraphNode"]) -> bool:
    for dependency_id in goal.dependency_refs:
        dependency = indexed.get(dependency_id)
        if dependency is None:
            return False
        if dependency.status not in {"completed", "done", "queued", "active"}:
            return False
    return True


@dataclass(frozen=True, slots=True)
class GoalGraphNode:
    goal_id: str
    session_id: str
    title: str
    status: GoalStatus
    priority: GoalPriority
    owner: GoalOwner = "agent"
    parent_goal_id: str | None = None
    dependency_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    related_memory_ids: tuple[str, ...] = ()
    deadline: datetime | None = None
    time_sensitivity: TimeSensitivity = "normal"
    review_checkpoint: str | None = None
    revision_id: str | None = None
    updated_at: datetime = field(default_factory=_now)

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", normalize_goal_status(self.status))
        object.__setattr__(self, "priority", normalize_goal_priority(self.priority))
        object.__setattr__(self, "owner", normalize_goal_owner(self.owner))
        object.__setattr__(self, "time_sensitivity", normalize_time_sensitivity(self.time_sensitivity))

    def to_contract_goal(self) -> ContractGoalNode:
        return ContractGoalNode(
            goal_id=self.goal_id,
            session_id=self.session_id,
            title=self.title,
            status=self.status,
            priority=self.priority,
            dependencies=self.dependency_refs,
            evidence_refs=self.evidence_refs,
            owner=self.owner,
            parent_goal_id=self.parent_goal_id,
            related_memory_ids=self.related_memory_ids,
            deadline=self.deadline,
            time_sensitivity=self.time_sensitivity,
            review_checkpoint=self.review_checkpoint,
            revision_id=self.revision_id,
            updated_at=self.updated_at,
        )

    def to_record(self) -> dict[str, Any]:
        return {
            "goal_id": self.goal_id,
            "session_id": self.session_id,
            "title": self.title,
            "status": self.status,
            "priority": self.priority,
            "owner": self.owner,
            "parent_goal_id": self.parent_goal_id,
            "dependency_refs": self.dependency_refs,
            "evidence_refs": self.evidence_refs,
            "related_memory_ids": self.related_memory_ids,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "time_sensitivity": self.time_sensitivity,
            "review_checkpoint": self.review_checkpoint,
            "revision_id": self.revision_id,
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "GoalGraphNode":
        return cls(
            goal_id=str(record["goal_id"]),
            session_id=str(record["session_id"]),
            title=str(record["title"]),
            status=normalize_goal_status(record.get("status")),
            priority=normalize_goal_priority(record.get("priority")),
            owner=normalize_goal_owner(record.get("owner")),
            parent_goal_id=str(record["parent_goal_id"]) if record.get("parent_goal_id") is not None else None,
            dependency_refs=_record_tuple(record, "dependency_refs"),
            evidence_refs=_record_tuple(record, "evidence_refs"),
            related_memory_ids=_record_tuple(record, "related_memory_ids"),
            deadline=_parse_datetime(str(record["deadline"])) if record.get("deadline") is not None else None,
            time_sensitivity=normalize_time_sensitivity(record.get("time_sensitivity")),
            review_checkpoint=str(record["review_checkpoint"]) if record.get("review_checkpoint") is not None else None,
            revision_id=str(record["revision_id"]) if record.get("revision_id") is not None else None,
            updated_at=_parse_datetime(str(record["updated_at"])) if record.get("updated_at") is not None else _now(),
        )

    @classmethod
    def from_contract_goal(
        cls,
        goal: ContractGoalNode,
        *,
        deadline: datetime | None = None,
        time_sensitivity: TimeSensitivity = "normal",
        parent_goal_id: str | None = None,
        related_memory_ids: tuple[str, ...] = (),
        review_checkpoint: str | None = None,
        revision_id: str | None = None,
        updated_at: datetime | None = None,
    ) -> "GoalGraphNode":
        return cls(
            goal_id=goal.goal_id,
            session_id=goal.session_id,
            title=goal.title,
            status=normalize_goal_status(goal.status),
            priority=normalize_goal_priority(goal.priority),
            owner=normalize_goal_owner(goal.owner),
            parent_goal_id=goal.parent_goal_id if goal.parent_goal_id is not None else parent_goal_id,
            dependency_refs=goal.dependencies,
            evidence_refs=goal.evidence_refs,
            related_memory_ids=goal.related_memory_ids or related_memory_ids,
            deadline=goal.deadline if goal.deadline is not None else deadline,
            time_sensitivity=normalize_time_sensitivity(
                goal.time_sensitivity if goal.time_sensitivity is not None else time_sensitivity
            ),
            review_checkpoint=goal.review_checkpoint if goal.review_checkpoint is not None else review_checkpoint,
            revision_id=goal.revision_id if goal.revision_id is not None else revision_id,
            updated_at=goal.updated_at if goal.updated_at is not None else (_now() if updated_at is None else updated_at),
        )

    def transition(
        self,
        *,
        status: GoalStatus,
        revision_id: str | None = None,
        updated_at: datetime | None = None,
        dependency_refs: tuple[str, ...] | None = None,
        evidence_refs: tuple[str, ...] | None = None,
        related_memory_ids: tuple[str, ...] | None = None,
        review_checkpoint: str | None = None,
    ) -> "GoalGraphNode":
        return replace(
            self,
            status=status,
            revision_id=self.revision_id if revision_id is None else revision_id,
            updated_at=_now() if updated_at is None else updated_at,
            dependency_refs=self.dependency_refs if dependency_refs is None else dependency_refs,
            evidence_refs=self.evidence_refs if evidence_refs is None else evidence_refs,
            related_memory_ids=self.related_memory_ids if related_memory_ids is None else related_memory_ids,
            review_checkpoint=self.review_checkpoint if review_checkpoint is None else review_checkpoint,
        )


@dataclass(frozen=True, slots=True)
class GoalGraph:
    session_id: str
    nodes: tuple[GoalGraphNode, ...] = ()
    root_goal_id: str | None = None
    active_goal_id: str | None = None
    revision_id: str | None = None
    updated_at: datetime = field(default_factory=_now)

    def index(self) -> dict[str, GoalGraphNode]:
        return {node.goal_id: node for node in self.nodes}

    def goal(self, goal_id: str) -> GoalGraphNode | None:
        return self.index().get(goal_id)

    def active_goal(self) -> GoalGraphNode | None:
        if self.active_goal_id is None:
            return None
        return self.goal(self.active_goal_id)

    def status_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for node in self.nodes:
            counts[node.status] = counts.get(node.status, 0) + 1
        return counts

    def ready_goals(self) -> tuple[GoalGraphNode, ...]:
        indexed = self.index()
        return tuple(
            node
            for node in self.nodes
            if node.status in {"proposed", "queued", "active"}
            and _dependencies_satisfied(node, indexed)
        )

    def blocked_goals(self) -> tuple[GoalGraphNode, ...]:
        indexed = self.index()
        return tuple(
            node
            for node in self.nodes
            if node.status == "blocked"
            or (
                node.status not in {"deferred", "completed", "done", "failed", "dropped"}
                and not _dependencies_satisfied(node, indexed)
            )
        )

    def with_nodes(self, nodes: tuple[GoalGraphNode, ...]) -> "GoalGraph":
        return replace(self, nodes=nodes, updated_at=_now())

    def with_goal(self, goal: GoalGraphNode) -> "GoalGraph":
        indexed = self.index()
        nodes = tuple(goal if node.goal_id == goal.goal_id else node for node in self.nodes)
        if goal.goal_id not in indexed:
            nodes = self.nodes + (goal,)
        return replace(self, nodes=nodes, updated_at=_now())

    def transition_goal(
        self,
        goal_id: str,
        *,
        status: GoalStatus,
        revision_id: str | None = None,
        updated_at: datetime | None = None,
        active_goal_id: str | None = None,
        dependency_refs: tuple[str, ...] | None = None,
        evidence_refs: tuple[str, ...] | None = None,
        related_memory_ids: tuple[str, ...] | None = None,
        review_checkpoint: str | None = None,
    ) -> "GoalGraph":
        indexed = self.index()
        goal = indexed.get(goal_id)
        if goal is None:
            raise KeyError(goal_id)
        updated_goal = goal.transition(
            status=status,
            revision_id=revision_id,
            updated_at=updated_at,
            dependency_refs=dependency_refs,
            evidence_refs=evidence_refs,
            related_memory_ids=related_memory_ids,
            review_checkpoint=review_checkpoint,
        )
        updated_nodes = tuple(updated_goal if node.goal_id == goal_id else node for node in self.nodes)
        next_active_goal_id = self.active_goal_id
        if active_goal_id is not None:
            next_active_goal_id = active_goal_id
        elif status == "active":
            next_active_goal_id = goal_id
        elif self.active_goal_id == goal_id and status in {"blocked", "deferred", "completed", "done", "failed", "dropped"}:
            next_active_goal_id = None
        return replace(
            self,
            nodes=updated_nodes,
            active_goal_id=next_active_goal_id,
            revision_id=updated_goal.revision_id if updated_goal.revision_id is not None else self.revision_id,
            updated_at=_now() if updated_at is None else updated_at,
        )

    def to_record(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "root_goal_id": self.root_goal_id,
            "active_goal_id": self.active_goal_id,
            "revision_id": self.revision_id,
            "updated_at": self.updated_at.isoformat(),
            "nodes": tuple(node.to_record() for node in self.nodes),
        }

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "GoalGraph":
        raw_nodes = record.get("nodes") or record.get("goals") or ()
        nodes = tuple(
            node if isinstance(node, GoalGraphNode) else GoalGraphNode.from_record(node)
            for node in raw_nodes
        )
        return cls(
            session_id=str(record["session_id"]),
            nodes=nodes,
            root_goal_id=str(record["root_goal_id"]) if record.get("root_goal_id") is not None else None,
            active_goal_id=str(record["active_goal_id"]) if record.get("active_goal_id") is not None else None,
            revision_id=str(record["revision_id"]) if record.get("revision_id") is not None else None,
            updated_at=_parse_datetime(str(record["updated_at"])) if record.get("updated_at") is not None else _now(),
        )


@dataclass(frozen=True, slots=True)
class TemporalContext:
    resumed: bool
    session_resume_reason: str | None = None
    active_goal_id: str | None = None
    ready_goal_ids: tuple[str, ...] = ()
    blocked_goal_ids: tuple[str, ...] = ()
    recovery_goal_ids: tuple[str, ...] = ()
    blocked_active_goal_id: str | None = None
    overdue_goal_ids: tuple[str, ...] = ()
    due_soon_goal_ids: tuple[str, ...] = ()
    idle_for: timedelta | None = None

    def to_record(self) -> dict[str, Any]:
        return {
            "resumed": self.resumed,
            "session_resume_reason": self.session_resume_reason,
            "active_goal_id": self.active_goal_id,
            "ready_goal_ids": self.ready_goal_ids,
            "blocked_goal_ids": self.blocked_goal_ids,
            "recovery_goal_ids": self.recovery_goal_ids,
            "blocked_active_goal_id": self.blocked_active_goal_id,
            "overdue_goal_ids": self.overdue_goal_ids,
            "due_soon_goal_ids": self.due_soon_goal_ids,
            "idle_for": _format_delta(self.idle_for) if self.idle_for else None,
        }


@dataclass(frozen=True, slots=True)
class ExecutionTracker:
    in_flight_goal_ids: tuple[str, ...] = ()
    blocker_refs: tuple[str, ...] = ()
    retry_goal_ids: tuple[str, ...] = ()
    completion_evidence_refs: tuple[str, ...] = ()

    def to_record(self) -> dict[str, Any]:
        return {
            "in_flight_goal_ids": self.in_flight_goal_ids,
            "blocker_refs": self.blocker_refs,
            "retry_goal_ids": self.retry_goal_ids,
            "completion_evidence_refs": self.completion_evidence_refs,
        }


@dataclass(frozen=True, slots=True)
class GoalGraphLifecycleUpdate:
    graph: GoalGraph | ActivityGraph
    changed: bool
    summary: str
    created_goal_ids: tuple[str, ...] = ()
    updated_goal_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CandidateMove:
    move_id: str
    kind: MoveKind
    goal_id: str | None
    title: str
    score: float
    priority_score: float
    status_score: float
    deadline_score: float
    time_sensitivity_score: float
    dependency_score: float
    resume_score: float
    continuity_score: float
    tracker_score: float
    evidence_score: float
    repair_score: float
    rationale: str
    rationale_factors: tuple[str, ...] = ()
    dependency_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    replay_score: float = 0.0
    replay_summary: str = ""
    replay_refs: tuple[str, ...] = ()
    confidence: float = 0.0

    def to_record(self) -> dict[str, Any]:
        return {
            "move_id": self.move_id,
            "kind": self.kind,
            "goal_id": self.goal_id,
            "title": self.title,
            "score": self.score,
            "priority_score": self.priority_score,
            "status_score": self.status_score,
            "deadline_score": self.deadline_score,
            "time_sensitivity_score": self.time_sensitivity_score,
            "dependency_score": self.dependency_score,
            "resume_score": self.resume_score,
            "continuity_score": self.continuity_score,
            "tracker_score": self.tracker_score,
            "evidence_score": self.evidence_score,
            "repair_score": self.repair_score,
            "rationale": self.rationale,
            "rationale_factors": self.rationale_factors,
            "dependency_refs": self.dependency_refs,
            "evidence_refs": self.evidence_refs,
            "replay_score": self.replay_score,
            "replay_summary": self.replay_summary,
            "replay_refs": self.replay_refs,
            "confidence": self.confidence,
        }


@dataclass(frozen=True, slots=True)
class PlanningRationale:
    summary: str
    factors: tuple[str, ...]
    candidate_ids: tuple[str, ...]
    selected_move_id: str
    selected_goal_id: str | None
    selected_goal_status: GoalStatus | None
    selected_goal_priority: GoalPriority | None
    progression_action: str
    active_goal_id_before: str | None
    planned_active_goal_id: str | None
    mode: PlanningMode
    replay_summary: str = ""
    replay_evidence_refs: tuple[str, ...] = ()

    def to_record(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "factors": self.factors,
            "candidate_ids": self.candidate_ids,
            "selected_move_id": self.selected_move_id,
            "selected_goal_id": self.selected_goal_id,
            "selected_goal_status": self.selected_goal_status,
            "selected_goal_priority": self.selected_goal_priority,
            "progression_action": self.progression_action,
            "active_goal_id_before": self.active_goal_id_before,
            "planned_active_goal_id": self.planned_active_goal_id,
            "mode": self.mode,
            "replay_summary": self.replay_summary,
            "replay_evidence_refs": self.replay_evidence_refs,
        }


@dataclass(frozen=True, slots=True)
class PlanningDecision:
    decision_id: str
    session_id: str
    mode: PlanningMode
    selected_move: CandidateMove
    rationale: PlanningRationale
    candidates: tuple[CandidateMove, ...]
    temporal_context: TemporalContext
    selected_at: datetime = field(default_factory=_now)
    goal_graph_revision: datetime | None = None

    def to_record(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "session_id": self.session_id,
            "mode": self.mode,
            "selected_move": self.selected_move.to_record(),
            "rationale": self.rationale.to_record(),
            "candidates": tuple(candidate.to_record() for candidate in self.candidates),
            "temporal_context": self.temporal_context.to_record(),
            "selected_at": self.selected_at.isoformat(),
            "goal_graph_revision": self.goal_graph_revision.isoformat() if self.goal_graph_revision else None,
        }


def _to_contract_goal(
    goal: GoalGraphNode | ContractGoalNode,
    *,
    updated_at: datetime | None = None,
) -> ContractGoalNode:
    if isinstance(goal, GoalGraphNode):
        return goal.to_contract_goal()
    if goal.updated_at is None and updated_at is not None:
        return replace(goal, updated_at=updated_at)
    return goal


def build_goal_graph(
    *,
    session_id: str,
    goals: tuple[GoalGraphNode, ...],
    root_goal_id: str | None = None,
    active_goal_id: str | None = None,
    revision_id: str | None = None,
    updated_at: datetime | None = None,
) -> GoalGraph:
    return GoalGraph(
        session_id=session_id,
        nodes=goals,
        root_goal_id=root_goal_id,
        active_goal_id=active_goal_id,
        revision_id=revision_id,
        updated_at=_now() if updated_at is None else updated_at,
    )


def build_activity_graph(
    *,
    session_id: str,
    goals: tuple[GoalGraphNode | ContractGoalNode, ...],
    root_goal_id: str | None = None,
    active_goal_id: str | None = None,
    revision_id: str | None = None,
    updated_at: datetime | None = None,
) -> ActivityGraph:
    return ActivityGraph(
        session_id=session_id,
        goals=tuple(_to_contract_goal(goal, updated_at=updated_at) for goal in goals),
        root_goal_id=root_goal_id,
        active_goal_id=active_goal_id,
        revision_id=revision_id,
    )


def normalize_activity_nodes(goals: tuple[ContractGoalNode, ...]) -> tuple[GoalGraphNode, ...]:
    return tuple(GoalGraphNode.from_contract_goal(goal) for goal in goals)


def goal_graph_to_activity_graph(graph: GoalGraph | ActivityGraph) -> ActivityGraph:
    if isinstance(graph, ActivityGraph):
        return graph
    return ActivityGraph(
        session_id=graph.session_id,
        goals=tuple(node.to_contract_goal() for node in graph.nodes),
        root_goal_id=graph.root_goal_id,
        active_goal_id=graph.active_goal_id,
        revision_id=graph.revision_id,
    )


def activity_graph_to_goal_graph(graph: ActivityGraph | GoalGraph) -> GoalGraph:
    if isinstance(graph, GoalGraph):
        return graph
    updated_at = graph.updated_at or _now()
    return GoalGraph(
        session_id=graph.session_id,
        nodes=tuple(
            GoalGraphNode.from_contract_goal(
                goal,
                updated_at=goal.updated_at if goal.updated_at is not None else updated_at,
            )
            for goal in graph.goals
        ),
        root_goal_id=graph.root_goal_id,
        active_goal_id=graph.active_goal_id,
        revision_id=graph.revision_id,
        updated_at=updated_at,
    )
