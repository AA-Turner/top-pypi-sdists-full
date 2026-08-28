"""oracle: route-to-best-result over hugpy's existing machinery.

k90a: contracts + the unified READ-ONLY capability catalog bridging the two
model registries (studio + legacy tasks) + GET /oracle/capabilities.
k90b: router (intent inference + best-eligible-route), runtime (execution via
the existing dispatch, wrapped into ExecutionReceipt), scorecard (mandatory
deterministic technical checks) + POST /oracle/route.
k90c: evaluation (capability-aware judge rubrics filling
``Scorecard.judge_results``, generalized from the movie VLM judge) + repair
(one bounded retry decision per failing card), both wired into the route.
k97: authority (the typed rights gate — required_authorities/check over a
GoalSpec's RightsManifest, refusing a route with FailureClass.REFUSED +
RepairCode.SOURCE_AUTHORITY_MISSING before any model is picked).
k98: speech (audio.tts / word_timestamps / speaker similarity checks).
k101: the CapabilityDescriptor upgrade — descriptor-grade CapabilityView,
registration probes (probes.py) run at catalog build, catalog.registry_version()
on every view and every receipt, and JSON-Schema export from the dataclasses
(schema_export.py).
k102: audio-first artifacts (DialogueTimeline / VoiceProfile / AudioMaster) and
the TTS candidate fan-out.
k103: the PlanGraph contract + its static validator.

Import is cheap: contracts are stdlib-only, probes' top level is stdlib +
contracts, plan/validator/audio_master pull no registry, and the catalog defers
every registry/worker read into its functions (see catalog.py's import
discipline).

k104: the production lock (GenerationSnapshot / ContinuityBible / ShotPlan /
ProductionLock) and the sibling SegmentSpec compiler.

This ``__init__`` "belonged to nobody this wave" (k101b's words) while five
agents landed modules around it, so k101 folds in every export block the
dispatch records asked for — k101b's bounded-dispatch names, k102's audio-first
artifacts, k103's plan/validator, k104's production+segments — in one place
where they can be seen together.
"""

from __future__ import annotations

from .contracts import (
    DEFAULT_CAPABILITY_VERSION,
    AccessKind,
    ArtifactKind,
    ArtifactRef,
    Authorization,
    AuthorityKind,
    BudgetHints,
    CapabilityView,
    Check,
    CheckKind,
    Eligibility,
    ExecutionReceipt,
    FailureClass,
    FrozenMap,
    GoalSpec,
    InputKind,
    InputRef,
    JudgeResult,
    PlannerMode,
    ProbeCheck,
    ProbeResult,
    ProbeStatus,
    Provenance,
    QualityProfile,
    RepairCode,
    ResourceHints,
    RightsManifest,
    Scorecard,
    SourceRegistry,
    canonical_json,
    coerce_artifact_kind,
)
from .authority import (
    AuthorityDecision,
    CAPABILITY_ACCESS,
    IDENTITY_CONDITIONED,
    VOICE_CONDITIONED,
    refusal_receipt,
    refusal_scorecard,
    required_authorities,
)
from .authority import check as check_authority
from .router import (
    CAPABILITY_TASK,
    RouteDecision,
    RouteRefusal,
    infer_capability,
    resolve_route,
)
from .runtime import (
    SYNC_DEADLINE_ENV,
    DispatchTimeout,
    GoalShapeError,
    execute_route,
    run_bounded,
    sync_deadline_s,
)
from .scorecard import (
    build_deferred_scorecard,
    build_gap_scorecard,
    build_technical_scorecard,
)
from .evaluation import (
    DEFAULT_EVALUATED,
    RUBRICS,
    THRESHOLDS,
    evaluate,
    parse_judge_verdict,
)
from .repair import RepairDecision, attempt_repair, execute_repair
from .catalog import (
    LEGACY_TASK_CAPABILITY,
    LEGACY_TASK_EXCLUDED,
    STUDIO_CAPABILITY_EXCLUDED,
    STUDIO_CAPABILITY_NAME,
    capability_version,
    get_capability,
    list_capabilities,
    registry_snapshot,
    registry_version,
    resolve_owners,
    unmapped_tasks,
)
# --- registration probes (k101) ------------------------------------------
from .probes import (
    PROBE_BUDGET_S,
    PROBE_SPECS,
    ProbeSpec,
    probe_capability,
    register_probe,
    run_probe,
)
from .schema_export import export_all, json_schema_for
# --- audio-first timing (k102) -------------------------------------------
from .audio_master import (
    AudioBuildResult,
    AudioGap,
    AudioMaster,
    DialogueTimeline,
    Line,
    LineTiming,
    SpeechCandidate,
    SpeechPolicy,
    VoiceKind,
    VoiceProfile,
    WordTiming,
    build_audio_master,
    candidate_seed,
)
# --- plan graph + static validator (k103) --------------------------------
from .plan import (
    AcceptanceTest,
    CycleError,
    Edge,
    FrozenParams,
    NodeKind,
    PlanGraph,
    PlanNode,
    Port,
    ResourceRequest,
    RetryPolicy,
    goal_digest,
    sibling_check,
    sibling_violations,
)
from .validator import ErrorCode, ValidationError, ValidationReport, validate
from .dag_runtime import (  # k111
    DagRuntime,
    JournalError,
    NodeContext,
    NodeRecord,
    NodeResult,
    NodeState,
    RepairBudgetExceeded,
    ResourceBroker,
    RunJournal,
    RunRecord,
    RunState,
    StepReport,
    derive_cache_key,
)
from .repair_controller import RepairController, RepairPlan, RepairPolicy  # k112
from .selection import (  # k113a
    ReliabilityLedger,
    SelectionDecision,
    SelectionPolicy,
    Selector,
)
from .prompt_compiler import ContextPlan, compile_context, render_prompt  # k113b
from .steward import HealthReport, Steward, StewardPolicy  # k113c
from .tone_scale import to_operator as tone_to_operator, to_unit as tone_to_unit  # TODO-14
from .spatial import (  # k116
    CANONICAL,
    ConditioningRequest,
    SpatialSceneManifest,
    SpatialValidation,
    TierFallback,
    TierProfile,
    ToneProfile,
    convert_points,
    frame_alignment_report,
    tone_profile,
    validate_manifest,
)
from .recipes.video_performance import (  # unit A
    VisualResult,
    build_visual_graph,
    resume_visual_stages,
    run_performance_on_dag,
    run_visual_stages,
)
# --- production lock + sibling segments (k104) ----------------------------
from .production import (
    CAMERA_KEYS,
    CAMERA_MOVES,
    CAMERA_VIEWS,
    SHOT_SIZES,
    ContinuityBible,
    ContinuityState,
    GenerationSnapshot,
    LockRefused,
    ProductionError,
    ProductionLock,
    RunPromptLedger,
    RunPromptRefused,
    ShotPlan,
    ShotPlanEntry,
    prompt_digest,
)
from .segments import (
    JOINT_MODES,
    SEGMENT_CAPABILITY,
    CompileRefused,
    LockedContext,
    LockedSegmentBrief,
    SegmentSpec,
    SiblingViolation,
    assert_siblings,
    build_locked_context,
    compile_segments,
    default_prompt_writer,
    execution_order,
    render_dependencies,
    segment_seed,
    shot_plan_from_windows,
    shot_windows_from_audio,
    to_plan_graph,
)
# ``validate`` is a generic name at package level (k103 flagged it): the
# plan-specific alias is the one to reach for when a second validator lands.
validate_plan = validate

__all__ = [
    # k111 / k112
    "DagRuntime", "JournalError", "NodeContext", "NodeRecord", "NodeResult", "NodeState",
    "RepairBudgetExceeded", "ResourceBroker", "RunJournal", "RunRecord", "RunState",
    "StepReport", "derive_cache_key", "RepairController", "RepairPlan", "RepairPolicy",
    "ReliabilityLedger", "SelectionDecision", "SelectionPolicy", "Selector",
    "ContextPlan", "compile_context", "render_prompt", "HealthReport", "Steward", "StewardPolicy",
    "VisualResult", "build_visual_graph", "resume_visual_stages", "run_performance_on_dag", "run_visual_stages",
    "tone_to_operator", "tone_to_unit",
    "CANONICAL", "ConditioningRequest", "SpatialSceneManifest", "SpatialValidation", "TierFallback",
    "TierProfile", "ToneProfile", "convert_points", "frame_alignment_report", "tone_profile", "validate_manifest",
    # contracts
    "ArtifactKind", "ArtifactRef", "Authorization", "AuthorityKind",
    "BudgetHints", "CapabilityView", "Check",
    "CheckKind", "Eligibility", "ExecutionReceipt", "FailureClass", "GoalSpec",
    "InputKind", "InputRef", "JudgeResult", "PlannerMode", "QualityProfile",
    "RepairCode", "ResourceHints", "RightsManifest", "Scorecard",
    "SourceRegistry",
    # descriptor contracts (k101)
    "AccessKind", "DEFAULT_CAPABILITY_VERSION", "FrozenMap", "ProbeCheck",
    "ProbeResult", "ProbeStatus", "Provenance", "canonical_json",
    "coerce_artifact_kind",
    # authority (k97)
    "AuthorityDecision", "CAPABILITY_ACCESS", "IDENTITY_CONDITIONED",
    "VOICE_CONDITIONED", "check_authority", "refusal_receipt",
    "refusal_scorecard", "required_authorities",
    # catalog
    "LEGACY_TASK_CAPABILITY", "LEGACY_TASK_EXCLUDED",
    "STUDIO_CAPABILITY_NAME", "STUDIO_CAPABILITY_EXCLUDED",
    "get_capability", "list_capabilities", "resolve_owners", "unmapped_tasks",
    # probes / registry snapshot / schema export (k101)
    "PROBE_BUDGET_S", "PROBE_SPECS", "ProbeSpec", "capability_version",
    "export_all", "json_schema_for", "probe_capability", "register_probe",
    "registry_snapshot", "registry_version", "run_probe",
    # audio-first timing (k102)
    "AudioBuildResult", "AudioGap", "AudioMaster", "DialogueTimeline", "Line",
    "LineTiming", "SpeechCandidate", "SpeechPolicy", "VoiceKind",
    "VoiceProfile", "WordTiming", "build_audio_master", "candidate_seed",
    # plan graph + validator (k103)
    "AcceptanceTest", "CycleError", "Edge", "FrozenParams", "NodeKind",
    "PlanGraph", "PlanNode", "Port", "ResourceRequest", "RetryPolicy",
    "goal_digest", "sibling_check", "sibling_violations",
    "ErrorCode", "ValidationError", "ValidationReport", "validate",
    "validate_plan",
    # production lock + sibling segments (k104)
    "CAMERA_KEYS", "CAMERA_MOVES", "CAMERA_VIEWS", "SHOT_SIZES",
    "ContinuityBible", "ContinuityState", "GenerationSnapshot", "LockRefused",
    "ProductionError", "ProductionLock", "RunPromptLedger", "RunPromptRefused",
    "ShotPlan", "ShotPlanEntry", "prompt_digest",
    "JOINT_MODES", "SEGMENT_CAPABILITY", "CompileRefused", "LockedContext",
    "LockedSegmentBrief", "SegmentSpec", "SiblingViolation", "assert_siblings",
    "build_locked_context", "compile_segments", "default_prompt_writer",
    "execution_order", "render_dependencies", "segment_seed",
    "shot_plan_from_windows", "shot_windows_from_audio", "to_plan_graph",
    # router / runtime / scorecard (k90b)
    "CAPABILITY_TASK", "RouteDecision", "RouteRefusal", "infer_capability",
    "resolve_route", "GoalShapeError", "execute_route",
    # bounded dispatch (k101b)
    "SYNC_DEADLINE_ENV", "DispatchTimeout", "run_bounded", "sync_deadline_s",
    "build_technical_scorecard", "build_gap_scorecard",
    "build_deferred_scorecard",
    # evaluation / repair (k90c)
    "DEFAULT_EVALUATED", "RUBRICS", "THRESHOLDS", "evaluate",
    "parse_judge_verdict", "RepairDecision", "attempt_repair", "execute_repair",
]
