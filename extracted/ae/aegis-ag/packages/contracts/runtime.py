"""Core shared contract shapes.

The goal here is to define durable, serializable records for the runtime.
These shapes are intentionally plain so the rest of the system can depend on
them without creating import cycles or backend-specific coupling.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import Mapping


def _ensure_unique_ids(values: tuple[str, ...], *, name: str) -> None:
    if len(set(values)) != len(values):
        raise ValueError(f"{name} ids must be unique")


def _ensure_non_empty_text(value: str, *, name: str) -> None:
    if not str(value).strip():
        raise ValueError(f"{name} must not be empty")


_ALLOWED_INTENT_MODES = frozenset({"embedded", "skip"})
_ALLOWED_INDEX_REFRESH_SCOPES = frozenset({"noop", "full"})
_ALLOWED_INTENT_FAMILIES = frozenset({"execution", "exploration", "creation", "reference", "profile", "resume"})
_ALLOWED_INTENT_CANDIDATE_KINDS = frozenset({"activity", "guardian", "skill"})
_ALLOWED_RESUME_SIGNALS = frozenset({"none", "continue", "resume", "interrupted", "inherit"})
_ALLOWED_SCOPE_SUGGESTIONS = frozenset({"session", "lineage", "workspace", "profile"})
_ALLOWED_BUDGET_CLASSES = frozenset({"narrow", "standard", "broad"})
_ALLOWED_INTENT_DEGRADATION_MODES = frozenset({"none", "skip", "embedding-unavailable", "conservative"})
_ALLOWED_WEAK_ASSIST_OUTCOMES = frozenset(
    {"not-requested", "confirmed", "suggested", "unresolved", "unsupported", "error"}
)


@dataclass(frozen=True, slots=True)
class StrongModelProfile:
    profile_id: str
    provider_id: str
    model_id: str
    base_url: str | None = None
    transport_id: str | None = None
    reasoning_effort: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _ensure_non_empty_text(self.profile_id, name="strong model profile_id")
        _ensure_non_empty_text(self.provider_id, name="strong model provider_id")
        _ensure_non_empty_text(self.model_id, name="strong model model_id")


@dataclass(frozen=True, slots=True)
class WeakModelProfile:
    profile_id: str
    provider_id: str
    model_id: str
    base_url: str | None = None
    transport_id: str | None = None
    reasoning_effort: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _ensure_non_empty_text(self.profile_id, name="weak model profile_id")
        _ensure_non_empty_text(self.provider_id, name="weak model provider_id")
        _ensure_non_empty_text(self.model_id, name="weak model model_id")


@dataclass(frozen=True, slots=True)
class MixtureModelSelection:
    strong_model: StrongModelProfile
    weak_model: WeakModelProfile
    intent_mode: str = "skip"

    def __post_init__(self) -> None:
        normalized_mode = self.intent_mode.strip().lower()
        if normalized_mode not in _ALLOWED_INTENT_MODES:
            raise ValueError(
                f"intent_mode must be one of {sorted(_ALLOWED_INTENT_MODES)}: {self.intent_mode}"
            )


@dataclass(frozen=True, slots=True)
class ProfileState:
    profile_id: str
    display_name: str
    mode: str
    clone_path: str | None = None
    preferences: tuple[str, ...] = ()
    enabled_capabilities: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CloneIdentityRecord:
    clone_id: str
    profile_id: str
    display_name: str
    identity_mode: str
    personality_preset: str
    initiative: str
    relational_stance: str
    voice_contract: str
    working_style_contract: str
    charter_extension: str | None = None
    governance_flags: tuple[str, ...] = ()
    source_manifest_path: str | None = None
    source_clone_path: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class UserCardRecord:
    user_card_id: str
    profile_id: str
    preferred_name: str | None = None
    locale: str | None = None
    timezone: str | None = None
    communication_preferences: tuple[str, ...] = ()
    boundaries: tuple[str, ...] = ()
    biography_fragments: tuple[str, ...] = ()
    durable_notes: tuple[str, ...] = ()
    shared_preferences: tuple[str, ...] = ()
    source_user_profile_path: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class RelationshipMemoryRecord:
    relationship_id: str
    profile_id: str
    clone_id: str
    user_card_id: str | None = None
    interaction_preferences: tuple[str, ...] = ()
    repair_history: tuple[str, ...] = ()
    trust_markers: tuple[str, ...] = ()
    expectations: tuple[str, ...] = ()
    local_corrections: tuple[str, ...] = ()
    continuity_notes: tuple[str, ...] = ()
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class ProfileGraph:
    profile: ProfileState
    clone_identity: CloneIdentityRecord
    user_card: UserCardRecord
    relationship_memory: RelationshipMemoryRecord

    def __post_init__(self) -> None:
        profile_id = self.profile.profile_id
        if self.clone_identity.profile_id != profile_id:
            raise ValueError("clone identity must reference the same profile")
        if self.user_card.profile_id != profile_id:
            raise ValueError("user card must reference the same profile")
        if self.relationship_memory.profile_id != profile_id:
            raise ValueError("relationship memory must reference the same profile")
        if self.relationship_memory.clone_id != self.clone_identity.clone_id:
            raise ValueError("relationship memory must reference the same clone identity")
        if (
            self.relationship_memory.user_card_id is not None
            and self.relationship_memory.user_card_id != self.user_card.user_card_id
        ):
            raise ValueError("relationship memory must reference the same user card")


@dataclass(frozen=True, slots=True)
class SessionState:
    session_id: str
    profile_id: str
    workspace_id: str | None
    status: str
    started_at: datetime
    updated_at: datetime
    parent_session_id: str | None = None
    interruption_state: str | None = None


@dataclass(frozen=True, slots=True)
class SessionContinuityState:
    session_id: str
    mode: str
    origin_session_id: str
    lineage_session_ids: tuple[str, ...] = ()
    inherited_interruption_state: str | None = None
    active_goal_id: str | None = None
    summary: str = ""

    @property
    def requires_recovery(self) -> bool:
        return self.mode != "foreground"


@dataclass(frozen=True, slots=True)
class ProfileGrowthState:
    profile_id: str
    growth_score: int = 0
    total_dialogues: int = 0
    total_tokens: int = 0
    total_experiences: int = 0
    promoted_experiences: int = 0
    active_days: int = 0
    streak_days: int = 0
    first_dialogue_at: datetime | None = None
    last_dialogue_at: datetime | None = None
    last_active_day: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class GoalNode:
    goal_id: str
    session_id: str
    title: str
    status: str
    priority: str
    dependencies: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    owner: str | None = None
    parent_goal_id: str | None = None
    related_memory_ids: tuple[str, ...] = ()
    deadline: datetime | None = None
    time_sensitivity: str | None = None
    review_checkpoint: str | None = None
    revision_id: str | None = None
    updated_at: datetime | None = None

    def to_contract_goal(self) -> "GoalNode":
        return self

    @property
    def dependency_refs(self) -> tuple[str, ...]:
        return self.dependencies

    def transition(
        self,
        *,
        status: str,
        revision_id: str | None = None,
        updated_at: datetime | None = None,
        dependencies: tuple[str, ...] | None = None,
        evidence_refs: tuple[str, ...] | None = None,
        related_memory_ids: tuple[str, ...] | None = None,
        review_checkpoint: str | None = None,
    ) -> "GoalNode":
        return replace(
            self,
            status=status,
            revision_id=self.revision_id if revision_id is None else revision_id,
            updated_at=datetime.now(self.updated_at.tzinfo) if updated_at is None and self.updated_at is not None else updated_at,
            dependencies=self.dependencies if dependencies is None else dependencies,
            evidence_refs=self.evidence_refs if evidence_refs is None else evidence_refs,
            related_memory_ids=self.related_memory_ids if related_memory_ids is None else related_memory_ids,
            review_checkpoint=self.review_checkpoint if review_checkpoint is None else review_checkpoint,
        )


@dataclass(frozen=True, slots=True)
class ActivityGraph:
    session_id: str
    goals: tuple[GoalNode, ...] = ()
    root_goal_id: str | None = None
    active_goal_id: str | None = None
    revision_id: str | None = None

    def __post_init__(self) -> None:
        goal_ids = tuple(goal.goal_id for goal in self.goals)
        _ensure_unique_ids(goal_ids, name="goal")
        for goal in self.goals:
            if goal.session_id != self.session_id:
                raise ValueError("every goal must reference the same session")
        if self.root_goal_id is not None and self.root_goal_id not in goal_ids:
            raise ValueError("root goal id must reference a goal in the graph")
        if self.active_goal_id is not None and self.active_goal_id not in goal_ids:
            raise ValueError("active goal id must reference a goal in the graph")

    def index(self) -> dict[str, GoalNode]:
        return {goal.goal_id: goal for goal in self.goals}

    def goal(self, goal_id: str) -> GoalNode | None:
        return self.index().get(goal_id)

    def active_goal(self) -> GoalNode | None:
        if self.active_goal_id is None:
            return None
        return self.goal(self.active_goal_id)

    def with_goals(self, goals: tuple[GoalNode, ...]) -> "ActivityGraph":
        return replace(self, goals=goals)

    def with_goal(self, goal: GoalNode) -> "ActivityGraph":
        indexed = self.index()
        goals = tuple(goal if existing.goal_id == goal.goal_id else existing for existing in self.goals)
        if goal.goal_id not in indexed:
            goals = self.goals + (goal,)
        return replace(self, goals=goals)

    def transition_goal(
        self,
        goal_id: str,
        *,
        status: str,
        revision_id: str | None = None,
        updated_at: datetime | None = None,
        active_goal_id: str | None = None,
        dependencies: tuple[str, ...] | None = None,
        evidence_refs: tuple[str, ...] | None = None,
        related_memory_ids: tuple[str, ...] | None = None,
        review_checkpoint: str | None = None,
    ) -> "ActivityGraph":
        indexed = self.index()
        goal = indexed.get(goal_id)
        if goal is None:
            raise KeyError(goal_id)
        updated_goal = goal.transition(
            status=status,
            revision_id=revision_id,
            updated_at=updated_at,
            dependencies=dependencies,
            evidence_refs=evidence_refs,
            related_memory_ids=related_memory_ids,
            review_checkpoint=review_checkpoint,
        )
        updated_goals = tuple(updated_goal if existing.goal_id == goal_id else existing for existing in self.goals)
        next_active_goal_id = self.active_goal_id
        if active_goal_id is not None:
            next_active_goal_id = active_goal_id
        elif status == "active":
            next_active_goal_id = goal_id
        elif self.active_goal_id == goal_id and status in {"blocked", "deferred", "completed", "done", "failed", "dropped"}:
            next_active_goal_id = None
        return replace(
            self,
            goals=updated_goals,
            active_goal_id=next_active_goal_id,
            revision_id=updated_goal.revision_id if updated_goal.revision_id is not None else self.revision_id,
        )

    def status_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for goal in self.goals:
            counts[goal.status] = counts.get(goal.status, 0) + 1
        return counts

    @property
    def updated_at(self) -> datetime | None:
        timestamps = [goal.updated_at for goal in self.goals if goal.updated_at is not None]
        if not timestamps:
            return None
        return max(timestamps)


@dataclass(frozen=True, slots=True)
class IntentReason:
    code: str
    detail: str
    weight: float = 0.0

    def __post_init__(self) -> None:
        _ensure_non_empty_text(self.code, name="intent reason code")
        _ensure_non_empty_text(self.detail, name="intent reason detail")


@dataclass(frozen=True, slots=True)
class IntentCandidate:
    candidate_id: str
    kind: str
    label: str
    summary: str
    cache_key: str = ""
    tags: tuple[str, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _ensure_non_empty_text(self.candidate_id, name="intent candidate id")
        if self.kind not in _ALLOWED_INTENT_CANDIDATE_KINDS:
            raise ValueError(
                f"intent candidate kind must be one of {sorted(_ALLOWED_INTENT_CANDIDATE_KINDS)}: {self.kind}"
            )
        _ensure_non_empty_text(self.label, name="intent candidate label")
        _ensure_non_empty_text(self.summary, name="intent candidate summary")

    @property
    def resolved_cache_key(self) -> str:
        cache_key = self.cache_key.strip()
        return cache_key or self.candidate_id


@dataclass(frozen=True, slots=True)
class IntentCandidateScore:
    candidate_id: str
    kind: str
    label: str
    total_score: float
    heuristics_score: float = 0.0
    embedding_score: float = 0.0
    reasons: tuple[IntentReason, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _ensure_non_empty_text(self.candidate_id, name="intent candidate score id")
        if self.kind not in _ALLOWED_INTENT_CANDIDATE_KINDS:
            raise ValueError(
                f"intent candidate score kind must be one of {sorted(_ALLOWED_INTENT_CANDIDATE_KINDS)}: {self.kind}"
            )
        _ensure_non_empty_text(self.label, name="intent candidate score label")


@dataclass(frozen=True, slots=True)
class IntentDecision:
    intent: str
    confidence: float
    focus_activity_ids: tuple[str, ...] = ()
    provisional_activity_seed: str | None = None
    resume_signal: str = "none"
    scope_suggestion: str = "session"
    budget_class: str = "standard"
    embedding_available: bool = False
    degradation_mode: str = "none"
    needs_weak_model_assist: bool = False
    weak_assist_outcome: str = "not-requested"
    fallback_path: str = "direct"
    reasons: tuple[IntentReason, ...] = ()
    candidate_scores: tuple[IntentCandidateScore, ...] = ()
    audit_trace: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.intent not in _ALLOWED_INTENT_FAMILIES:
            raise ValueError(f"intent must be one of {sorted(_ALLOWED_INTENT_FAMILIES)}: {self.intent}")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("intent confidence must stay between 0.0 and 1.0")
        if self.resume_signal not in _ALLOWED_RESUME_SIGNALS:
            raise ValueError(
                f"resume_signal must be one of {sorted(_ALLOWED_RESUME_SIGNALS)}: {self.resume_signal}"
            )
        if self.scope_suggestion not in _ALLOWED_SCOPE_SUGGESTIONS:
            raise ValueError(
                f"scope_suggestion must be one of {sorted(_ALLOWED_SCOPE_SUGGESTIONS)}: {self.scope_suggestion}"
            )
        if self.budget_class not in _ALLOWED_BUDGET_CLASSES:
            raise ValueError(
                f"budget_class must be one of {sorted(_ALLOWED_BUDGET_CLASSES)}: {self.budget_class}"
            )
        if self.degradation_mode not in _ALLOWED_INTENT_DEGRADATION_MODES:
            raise ValueError(
                "degradation_mode must be one of "
                f"{sorted(_ALLOWED_INTENT_DEGRADATION_MODES)}: {self.degradation_mode}"
            )
        if self.weak_assist_outcome not in _ALLOWED_WEAK_ASSIST_OUTCOMES:
            raise ValueError(
                "weak_assist_outcome must be one of "
                f"{sorted(_ALLOWED_WEAK_ASSIST_OUTCOMES)}: {self.weak_assist_outcome}"
            )
        _ensure_non_empty_text(self.fallback_path, name="intent fallback path")
        _ensure_unique_ids(self.focus_activity_ids, name="intent focus activity")
        _ensure_unique_ids(
            tuple(score.candidate_id for score in self.candidate_scores),
            name="intent candidate score",
        )

    @property
    def primary_focus_activity_id(self) -> str | None:
        if not self.focus_activity_ids:
            return None
        return self.focus_activity_ids[0]


@dataclass(frozen=True, slots=True)
class IntentResolutionRequest:
    prompt: str
    session_id: str
    profile_id: str
    workspace_id: str | None = None
    continuity: SessionContinuityState | None = None
    activity_graph: ActivityGraph | None = None
    previous_decision: IntentDecision | None = None
    surface_hints: tuple[str, ...] = ()
    artifact_hints: tuple[str, ...] = ()
    recent_turn_summaries: tuple[str, ...] = ()
    relationship_hints: tuple[str, ...] = ()
    capability_hints: tuple[str, ...] = ()
    activity_candidates: tuple[IntentCandidate, ...] = ()
    guardian_candidates: tuple[IntentCandidate, ...] = ()
    skill_candidates: tuple[IntentCandidate, ...] = ()
    mixture: MixtureModelSelection | None = None
    embedding_available: bool = False


@dataclass(frozen=True, slots=True)
class StructuredTurnSlot:
    summary: str = ""
    detail: tuple[str, ...] = ()
    compression: str = "structured"
    provenance: str = ""
    source_refs: tuple[str, ...] = ()
    linkage_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class StructuredTurnRecord:
    turn_id: str
    session_id: str
    source: str
    observation: StructuredTurnSlot
    reasoning: StructuredTurnSlot
    action: StructuredTurnSlot
    outcome: StructuredTurnSlot
    profile_id: str | None = None
    workspace_id: str | None = None
    source_event_id: str | None = None
    reasoning_availability: str = "summary_only"
    reasoning_provenance: str = "runtime.decision_summary"
    compression_tier: str = "raw_turn"
    work_item_ids: tuple[str, ...] = ()
    source_turn_ids: tuple[str, ...] = ()
    correction_memory_ids: tuple[str, ...] = ()
    artifact_ids: tuple[str, ...] = ()
    created_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    memory_id: str
    session_id: str
    kind: str
    content: str
    source_event_id: str | None = None
    goal_refs: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    created_at: datetime | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ExperienceRecord:
    experience_id: str
    session_id: str
    profile_id: str
    workspace_id: str | None
    kind: str
    title: str
    summary: str
    status: str
    run_id: str | None = None
    source_event_id: str | None = None
    goal_id: str | None = None
    tool_call_count: int = 0
    model_turn_count: int = 0
    related_skill_ids: tuple[str, ...] = ()
    produced_artifact_ids: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class PatternCluster:
    cluster_id: str
    profile_id: str
    signature: str
    status: str
    experience_ids: tuple[str, ...] = ()
    source_evidence_ids: tuple[str, ...] = ()
    source_work_item_ids: tuple[str, ...] = ()
    related_skill_ids: tuple[str, ...] = ()
    summary: str = ""
    support_count: int = 0


@dataclass(frozen=True, slots=True)
class ProcedureCandidate:
    candidate_id: str
    profile_id: str
    cluster_id: str
    title: str
    summary: str
    trigger_conditions: tuple[str, ...] = ()
    ordered_steps: tuple["ProcedureStep", ...] = ()
    constraints: tuple[str, ...] = ()
    source_evidence_ids: tuple[str, ...] = ()
    source_work_item_ids: tuple[str, ...] = ()
    related_skill_ids: tuple[str, ...] = ()
    confidence: float = 0.0
    verification_status: str = "draft"
    promotion_decision: str = "pending"

    def __post_init__(self) -> None:
        _ensure_unique_ids(tuple(step.step_id for step in self.ordered_steps), name="procedure candidate step")


@dataclass(frozen=True, slots=True)
class VerificationBundle:
    bundle_id: str
    profile_id: str
    candidate_id: str
    method: str
    status: str
    notes: str = ""
    evidence_ids: tuple[str, ...] = ()
    scenario_ids: tuple[str, ...] = ()
    verified_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class ArtifactRecord:
    artifact_id: str
    session_id: str
    kind: str
    name: str
    uri: str
    checksum: str | None = None
    created_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class EvidenceGraph:
    session_id: str
    memories: tuple[MemoryRecord, ...] = ()
    artifacts: tuple[ArtifactRecord, ...] = ()

    def __post_init__(self) -> None:
        _ensure_unique_ids(tuple(memory.memory_id for memory in self.memories), name="memory")
        _ensure_unique_ids(tuple(artifact.artifact_id for artifact in self.artifacts), name="artifact")
        for memory in self.memories:
            if memory.session_id != self.session_id:
                raise ValueError("every memory must reference the same session")
        for artifact in self.artifacts:
            if artifact.session_id != self.session_id:
                raise ValueError("every artifact must reference the same session")


@dataclass(frozen=True, slots=True)
class RecallReason:
    code: str
    detail: str
    weight: float = 0.0


@dataclass(frozen=True, slots=True)
class RecallReasons:
    opened_scopes: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    scope_reason: str = ""
    rerank_summary: str = ""
    reasons: tuple[RecallReason, ...] = ()


@dataclass(frozen=True, slots=True)
class EvidenceRetrievalRequest:
    session_id: str
    profile_id: str
    workspace_id: str | None = None
    lineage_session_ids: tuple[str, ...] = ()
    work_item_ids: tuple[str, ...] = ()
    query: str = ""
    scopes: tuple[str, ...] = ("session",)
    latency_mode: str = "balanced"
    limit: int = 5
    include_inactive: bool = False
    explain: bool = True
    scope_reason: str = ""
    relationship_hints: tuple[str, ...] = ()
    target_slots: tuple[str, ...] = ()
    max_compression: str = "episode_summary"
    replay_mode: str = "off"
    intent_decision: IntentDecision | None = None
    allow_embeddings: bool = True


@dataclass(frozen=True, slots=True)
class EvidenceCandidate:
    evidence_id: str
    memory: MemoryRecord
    score: float
    lexical_score: float = 0.0
    vector_score: float = 0.0
    graph_score: float = 0.0
    matched_scopes: tuple[str, ...] = ()
    reasons: tuple[RecallReason, ...] = ()
    embedding_mode: str = ""
    replay_record: StructuredTurnRecord | None = None
    replay_slots: tuple[str, ...] = ()
    replay_summary: str = ""


@dataclass(frozen=True, slots=True)
class EmbeddingIndexInvalidation:
    evidence_id: str
    lifecycle_state: str
    stale_cache_key: str
    replacement_evidence_id: str | None = None
    refresh_action: str = "drop"
    reason: str = ""


@dataclass(frozen=True, slots=True)
class EmbeddingIndexRebuildPlan:
    target: str
    refresh_scope: str
    active_evidence_ids: tuple[str, ...] = ()
    active_cache_keys: tuple[str, ...] = ()
    stale_cache_keys: tuple[str, ...] = ()
    replacement_evidence_ids: tuple[str, ...] = ()
    dimensions: tuple[int, ...] = ()
    steps: tuple[str, ...] = ()
    summary: str = ""

    def __post_init__(self) -> None:
        if self.refresh_scope not in _ALLOWED_INDEX_REFRESH_SCOPES:
            raise ValueError(
                f"embedding index refresh_scope must be one of {sorted(_ALLOWED_INDEX_REFRESH_SCOPES)}: {self.refresh_scope}"
            )


@dataclass(frozen=True, slots=True)
class EmbeddingIndexPolicy:
    model_id: str
    lexical_index_version: str
    embedding_index_version: str
    active_dimensions: tuple[int, ...] = ()
    tracked_evidence_count: int = 0
    rebuild_required: bool = False
    invalidated_evidence_ids: tuple[str, ...] = ()
    invalidation_reason: str = ""
    invalidations: tuple[EmbeddingIndexInvalidation, ...] = ()
    rebuild_plan: EmbeddingIndexRebuildPlan | None = None


@dataclass(frozen=True, slots=True)
class EvidenceRetrievalResult:
    request: EvidenceRetrievalRequest
    scope_session_ids: tuple[str, ...]
    scope_reason: str
    candidates: tuple[EvidenceCandidate, ...]
    recall_reasons: RecallReasons
    index_policy: EmbeddingIndexPolicy


@dataclass(frozen=True, slots=True)
class ResumePacket:
    session_id: str
    profile_id: str
    workspace_id: str | None
    focus_work_item_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    artifact_ids: tuple[str, ...] = ()
    constraint_ids: tuple[str, ...] = ()
    summary: str = ""
    next_move: str = ""
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ProcedureStep:
    step_id: str
    title: str
    instruction: str
    tool_name: str | None = None


@dataclass(frozen=True, slots=True)
class ProcedureRecord:
    procedure_id: str
    title: str
    summary: str
    status: str
    trigger_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    verification_bundle_id: str | None = None
    skill_id: str | None = None
    steps: tuple[ProcedureStep, ...] = ()

    def __post_init__(self) -> None:
        _ensure_unique_ids(tuple(step.step_id for step in self.steps), name="procedure step")


@dataclass(frozen=True, slots=True)
class ProcedureLibrary:
    profile_id: str
    procedures: tuple[ProcedureRecord, ...] = ()

    def __post_init__(self) -> None:
        _ensure_unique_ids(tuple(procedure.procedure_id for procedure in self.procedures), name="procedure")


@dataclass(frozen=True, slots=True)
class PromptEnvelope:
    """Structured prompt sections used by live model requests."""

    frozen_prefix: str = ""
    session_snapshot: str = ""
    turn_injections: str = ""
    tool_schema: str = ""

    def system_prompt(self, *, include_tool_schema: bool = False) -> str:
        sections = [self.frozen_prefix.strip(), self.session_snapshot.strip()]
        if include_tool_schema:
            sections.append(self.tool_schema.strip())
        return "\n\n".join(section for section in sections if section)

    def user_prelude(self) -> str:
        return self.turn_injections.strip()

    def combined_prompt(self, *, include_tool_schema: bool = True) -> str:
        sections = [
            self.frozen_prefix.strip(),
            self.session_snapshot.strip(),
            self.turn_injections.strip(),
        ]
        if include_tool_schema:
            sections.append(self.tool_schema.strip())
        return "\n\n".join(section for section in sections if section)

    def append_turn_injection(self, text: str) -> "PromptEnvelope":
        normalized = str(text).strip()
        if not normalized:
            return self
        current = self.turn_injections.strip()
        updated = normalized if not current else f"{current}\n\n{normalized}"
        return PromptEnvelope(
            frozen_prefix=self.frozen_prefix,
            session_snapshot=self.session_snapshot,
            turn_injections=updated,
            tool_schema=self.tool_schema,
        )


@dataclass(frozen=True, slots=True)
class ContextBundle:
    bundle_id: str
    session_id: str
    instruction_refs: tuple[str, ...] = ()
    goal_ids: tuple[str, ...] = ()
    memory_ids: tuple[str, ...] = ()
    artifact_ids: tuple[str, ...] = ()
    token_budget: int = 0
    prompt_envelope: PromptEnvelope = field(default_factory=PromptEnvelope)
    rendered_prompt: str | None = None


@dataclass(frozen=True, slots=True)
class PlanStep:
    step_id: str
    title: str
    rationale: str
    dependency_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PlanDraft:
    plan_id: str
    goal_id: str
    session_id: str
    steps: tuple[PlanStep, ...] = ()
    rationale: str = ""


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    execution_id: str
    session_id: str
    outcome: str
    summary: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cached_prompt_tokens: int = 0
    cache_creation_prompt_tokens: int = 0
    cache_usage_reported: bool = False
    produced_artifact_ids: tuple[str, ...] = ()
    telemetry_event_ids: tuple[str, ...] = ()
    side_effects: tuple[str, ...] = ()
    tool_calls: tuple["ExecutionToolCall", ...] = ()


@dataclass(frozen=True, slots=True)
class ExecutionToolCall:
    tool_name: str
    arguments: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AgentRunState:
    run_id: str
    session_id: str
    source_event_id: str
    prompt: str
    status: str
    phase: str
    step_count: int
    model_turn_count: int
    tool_call_count: int
    max_model_turns: int
    max_wall_time_seconds: int
    created_at: datetime
    updated_at: datetime
    waiting_reason: str | None = None
    continuation_prompt: str | None = None
    last_summary: str | None = None


@dataclass(frozen=True, slots=True)
class AgentRunStep:
    step_id: str
    run_id: str
    session_id: str
    step_index: int
    kind: str
    title: str
    content: str
    created_at: datetime
    outcome: str | None = None
    tool_name: str | None = None


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    event_id: str
    event_type: str
    session_id: str
    source: str
    payload: dict[str, str] = field(default_factory=dict)
