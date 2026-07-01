from dreadnode.optimization import events, sampling, stopping
from dreadnode.optimization.adapters import (
    CapabilityEnvAdapter,
    DreadnodeAgentAdapter,
    SessionRuntimeAdapter,
    StackAwareCapabilityAdapter,
)
from dreadnode.optimization.api import Optimization, optimize_anything
from dreadnode.optimization.backends import (
    GEPABackend,
    OptimizationAdapter,
    OptimizationBackend,
    OptimizationBackendError,
    OptimizationDependencyError,
    OptimizationEvaluationBatch,
    OptimizationEvaluator,
)
from dreadnode.optimization.config import (
    EngineConfig,
    MergeConfig,
    OptimizationConfig,
    RefinerConfig,
    ReflectionConfig,
    TrackingConfig,
)
from dreadnode.optimization.events import (
    BudgetUpdated,
    CandidateAccepted,
    CandidateRejected,
    IterationStart,
    NewBestTrial,
    NewBestTrialFound,
    OptimizationEnd,
    OptimizationError,
    OptimizationEvent,
    OptimizationStart,
    ParetoFrontUpdated,
    StudyEnd,
    StudyEvent,
    StudyStart,
    TrialComplete,
    TrialEvent,
    TrialFailed,
    TrialPruned,
    TrialStart,
    ValsetEvaluated,
)
from dreadnode.optimization.result import (
    OptimizationEvaluation,
    OptimizationResult,
    StudyResult,
)
from dreadnode.optimization.sampler import Sample, Sampler
from dreadnode.optimization.search import (
    Categorical,
    Distribution,
    Float,
    Int,
    SearchSpace,
)
from dreadnode.optimization.stopping import StudyStopCondition
from dreadnode.optimization.study import Direction, Study
from dreadnode.optimization.trial import Trial, TrialStatus

# Backwards compatibility alias
Attack = Study

# Rebuild models to resolve forward references (Trial forward reference)
TrialEvent.model_rebuild()
TrialStart.model_rebuild()
TrialComplete.model_rebuild()
TrialPruned.model_rebuild()
TrialFailed.model_rebuild()
NewBestTrial.model_rebuild()
StudyEnd.model_rebuild()
OptimizationEnd.model_rebuild()

__all__ = [
    "BudgetUpdated",
    "CandidateAccepted",
    "CandidateRejected",
    "CapabilityEnvAdapter",
    "Categorical",
    "Direction",
    "Distribution",
    "DreadnodeAgentAdapter",
    "EngineConfig",
    "Float",
    "GEPABackend",
    "Int",
    "IterationStart",
    "MergeConfig",
    "NewBestTrial",
    "NewBestTrialFound",  # backwards compat alias
    "Optimization",
    "OptimizationAdapter",
    "OptimizationBackend",
    "OptimizationBackendError",
    "OptimizationConfig",
    "OptimizationDependencyError",
    "OptimizationEnd",
    "OptimizationError",
    "OptimizationEvaluation",
    "OptimizationEvaluationBatch",
    "OptimizationEvaluator",
    "OptimizationEvent",
    "OptimizationResult",
    "OptimizationStart",
    "ParetoFrontUpdated",
    "RefinerConfig",
    "ReflectionConfig",
    "Sample",
    "Sampler",
    "SearchSpace",
    "SessionRuntimeAdapter",
    "StackAwareCapabilityAdapter",
    "Study",
    "StudyEnd",
    "StudyEvent",
    "StudyResult",
    "StudyStart",
    "StudyStopCondition",
    "TrackingConfig",
    "Trial",
    "TrialComplete",
    "TrialEvent",
    "TrialFailed",
    "TrialPruned",
    "TrialStart",
    "TrialStatus",
    "ValsetEvaluated",
    "events",
    "optimize_anything",
    "sampling",
    "stopping",
]
