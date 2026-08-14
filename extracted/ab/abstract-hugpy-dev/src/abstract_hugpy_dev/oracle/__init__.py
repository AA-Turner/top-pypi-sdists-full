"""oracle: route-to-best-result over hugpy's existing machinery.

k90: contracts + the unified READ-ONLY capability catalog bridging the two
model registries (studio + legacy tasks) + GET /oracle/capabilities.
k91: router (intent inference + best-eligible-route), runtime (execution via
the existing dispatch, wrapped into ExecutionReceipt), scorecard (mandatory
deterministic technical checks) + POST /oracle/route.
k92: evaluation (capability-aware judge rubrics filling
``Scorecard.judge_results``, generalized from the movie VLM judge) + repair
(one bounded retry decision per failing card), both wired into the route.

Import is cheap: contracts are stdlib-only and the catalog defers every
registry/worker read into its functions (see catalog.py's import discipline).
"""

from __future__ import annotations

from .contracts import (
    ArtifactKind,
    ArtifactRef,
    BudgetHints,
    CapabilityView,
    Check,
    CheckKind,
    Eligibility,
    ExecutionReceipt,
    FailureClass,
    GoalSpec,
    InputKind,
    InputRef,
    JudgeResult,
    QualityProfile,
    RepairCode,
    ResourceHints,
    Scorecard,
    SourceRegistry,
)
from .router import (
    CAPABILITY_TASK,
    RouteDecision,
    RouteRefusal,
    infer_capability,
    resolve_route,
)
from .runtime import GoalShapeError, execute_route
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
    get_capability,
    list_capabilities,
    resolve_owners,
    unmapped_tasks,
)

__all__ = [
    # contracts
    "ArtifactKind", "ArtifactRef", "BudgetHints", "CapabilityView", "Check",
    "CheckKind", "Eligibility", "ExecutionReceipt", "FailureClass", "GoalSpec",
    "InputKind", "InputRef", "JudgeResult", "QualityProfile", "RepairCode",
    "ResourceHints", "Scorecard", "SourceRegistry",
    # catalog
    "LEGACY_TASK_CAPABILITY", "LEGACY_TASK_EXCLUDED",
    "STUDIO_CAPABILITY_NAME", "STUDIO_CAPABILITY_EXCLUDED",
    "get_capability", "list_capabilities", "resolve_owners", "unmapped_tasks",
    # router / runtime / scorecard (k91)
    "CAPABILITY_TASK", "RouteDecision", "RouteRefusal", "infer_capability",
    "resolve_route", "GoalShapeError", "execute_route",
    "build_technical_scorecard", "build_gap_scorecard",
    "build_deferred_scorecard",
    # evaluation / repair (k92)
    "DEFAULT_EVALUATED", "RUBRICS", "THRESHOLDS", "evaluate",
    "parse_judge_verdict", "RepairDecision", "attempt_repair", "execute_repair",
]
