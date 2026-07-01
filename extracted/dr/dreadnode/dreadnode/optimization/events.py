import typing as t
from datetime import UTC, datetime
from uuid import UUID, uuid4

import typing_extensions as te
from pydantic import BaseModel, ConfigDict, Field

from dreadnode.tracing.constants import (
    STUDY_ATTRIBUTE_MAX_TRIALS,
    STUDY_ATTRIBUTE_OBJECTIVES,
    STUDY_ATTRIBUTE_SEARCH_STRATEGY,
    TRIAL_ATTRIBUTE_CANDIDATE,
    TRIAL_ATTRIBUTE_ID,
    TRIAL_ATTRIBUTE_SCORES,
    TRIAL_ATTRIBUTE_STATUS,
    TRIAL_ATTRIBUTE_STEP,
)

if t.TYPE_CHECKING:
    from dreadnode.optimization.result import OptimizationResult, StudyResult
    from dreadnode.optimization.trial import Trial
    from dreadnode.tracing.span import TaskSpan

CandidateT = te.TypeVar("CandidateT", default=t.Any)


# =============================================================================
# Study Events (study-level, emitted to study span)
# =============================================================================


class StudyEvent(BaseModel, t.Generic[CandidateT]):
    """Base class for study-level events."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC), kw_only=True)
    study_id: UUID = Field(default_factory=uuid4)
    study_name: str | None = None

    def as_dict(self) -> dict[str, t.Any]:
        """Serialize event for transport."""
        return {
            "type": self.__class__.__name__.lower(),
            "timestamp": self.timestamp.isoformat(),
            "study_id": str(self.study_id),
            "study_name": self.study_name,
            "data": self._get_data(),
        }

    def _get_data(self) -> dict[str, t.Any]:
        """Override to provide event-specific data for serialization."""
        return {}

    def emit(self, span: "TaskSpan") -> None:
        """Emit this event's telemetry to the span."""
        span.log_event(
            f"study.{self.__class__.__name__}",
            {"event_type": self.__class__.__name__, "timestamp": self.timestamp.isoformat()},
        )


class StudyStart(StudyEvent[CandidateT]):
    """Signals the beginning of a study."""

    max_trials: int = 0
    objectives: list[str] = Field(default_factory=list)
    search_strategy: str | None = None

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "max_trials": self.max_trials,
            "objectives": self.objectives,
            "search_strategy": self.search_strategy,
        }

    def emit(self, span: "TaskSpan") -> None:
        span.set_attribute(STUDY_ATTRIBUTE_MAX_TRIALS, self.max_trials)
        span.set_attribute(STUDY_ATTRIBUTE_OBJECTIVES, self.objectives)
        if self.search_strategy:
            span.set_attribute(STUDY_ATTRIBUTE_SEARCH_STRATEGY, self.search_strategy)
        span.log_param("max_trials", self.max_trials)
        super().emit(span)


class StudyEnd(StudyEvent[CandidateT]):
    """Signals the end of the study."""

    result: "StudyResult[CandidateT] | None" = Field(default=None, repr=False)
    stop_reason: str = ""
    stop_explanation: str | None = None
    total_trials: int = 0
    finished_trials: int = 0
    failed_trials: int = 0
    pruned_trials: int = 0
    best_trial_id: UUID | None = None
    best_trial_step: int | None = None
    best_score: float | None = None
    best_candidate: t.Any = None
    best_scores: dict[str, float] | None = None

    def _get_data(self) -> dict[str, t.Any]:
        data: dict[str, t.Any] = {
            "stop_reason": self.stop_reason,
            "total_trials": self.total_trials,
            "finished_trials": self.finished_trials,
            "failed_trials": self.failed_trials,
            "pruned_trials": self.pruned_trials,
        }
        if self.stop_explanation:
            data["stop_explanation"] = self.stop_explanation
        if self.best_trial_id is not None:
            data["best_trial_id"] = str(self.best_trial_id)
        if self.best_scores:
            data["best_scores"] = self.best_scores
        return data

    def emit(self, span: "TaskSpan") -> None:
        outputs: dict[str, t.Any] = {
            "stop_reason": self.stop_reason,
            "stop_explanation": self.stop_explanation,
            "completed_trials": self.total_trials,
            "finished_trials": self.finished_trials,
            "failed_trials": self.failed_trials,
            "pruned_trials": self.pruned_trials,
        }
        if self.best_trial_id is not None:
            outputs["best_trial_id"] = str(self.best_trial_id)
            outputs["best_trial_step"] = self.best_trial_step
            outputs["best_score"] = self.best_score
            outputs["best_candidate"] = self.best_candidate
            outputs["best_scores"] = self.best_scores
        span.log_output("study_result", outputs)
        span.log_metric("study/completed_trials", self.total_trials)
        super().emit(span)


# =============================================================================
# Trial Events (trial-level, emitted to trial span - linked via span hierarchy)
# =============================================================================


class TrialEvent(BaseModel, t.Generic[CandidateT]):
    """Base class for trial-level events. Linked to study via span hierarchy."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC), kw_only=True)
    trial_id: UUID = Field(default_factory=uuid4)
    trial_step: int = 0
    trial: "Trial[CandidateT] | None" = Field(default=None, repr=False, exclude=True)

    def as_dict(self) -> dict[str, t.Any]:
        """Serialize event for transport."""
        return {
            "type": self.__class__.__name__.lower(),
            "timestamp": self.timestamp.isoformat(),
            "trial_id": str(self.trial_id),
            "trial_step": self.trial_step,
            "data": self._get_data(),
        }

    def _get_data(self) -> dict[str, t.Any]:
        """Override to provide event-specific data for serialization."""
        return {}

    def emit(self, span: "TaskSpan") -> None:
        """Emit this event's telemetry to the span."""
        span.log_event(
            f"trial.{self.__class__.__name__}",
            {"event_type": self.__class__.__name__, "timestamp": self.timestamp.isoformat()},
        )


class TrialStart(TrialEvent[CandidateT]):
    """Signals the start of a trial."""

    candidate: t.Any = None

    def _get_data(self) -> dict[str, t.Any]:
        data: dict[str, t.Any] = {}
        if self.candidate is not None:
            data["candidate"] = self.candidate
        return data

    def emit(self, span: "TaskSpan") -> None:
        span.set_attribute(TRIAL_ATTRIBUTE_ID, str(self.trial_id))
        span.set_attribute(TRIAL_ATTRIBUTE_STEP, self.trial_step)
        if self.candidate is not None:
            from dreadnode.optimization.study import _serialize_candidate

            serialized = _serialize_candidate(self.candidate)
            span.set_attribute(TRIAL_ATTRIBUTE_CANDIDATE, serialized)
            span.log_input("candidate", serialized)
        super().emit(span)


class TrialComplete(TrialEvent[CandidateT]):
    """Signals that a trial has completed successfully."""

    scores: dict[str, float] = Field(default_factory=dict)

    def _get_data(self) -> dict[str, t.Any]:
        data: dict[str, t.Any] = {}
        if self.scores:
            data["scores"] = self.scores
        return data

    def emit(self, span: "TaskSpan") -> None:
        span.set_attribute(TRIAL_ATTRIBUTE_ID, str(self.trial_id))
        span.set_attribute(TRIAL_ATTRIBUTE_STATUS, "finished")
        if self.scores:
            span.set_attribute(TRIAL_ATTRIBUTE_SCORES, self.scores)
            span.log_output("scores", self.scores)
            for name, score in self.scores.items():
                span.log_metric(f"trial/{name}", score, step=self.trial_step)
        super().emit(span)


class TrialFailed(TrialEvent[CandidateT]):
    """Signals that a trial has failed."""

    error: str = ""

    def _get_data(self) -> dict[str, t.Any]:
        data: dict[str, t.Any] = {}
        if self.error:
            data["error"] = self.error
        return data

    def emit(self, span: "TaskSpan") -> None:
        span.set_attribute(TRIAL_ATTRIBUTE_ID, str(self.trial_id))
        span.set_attribute(TRIAL_ATTRIBUTE_STATUS, "failed")
        if self.error:
            span.log_output("error", self.error[:500])
        super().emit(span)


class TrialPruned(TrialEvent[CandidateT]):
    """Signals that a trial was pruned (constraint not satisfied)."""

    def _get_data(self):
        return {}

    def emit(self, span: "TaskSpan") -> None:
        span.set_attribute(TRIAL_ATTRIBUTE_ID, str(self.trial_id))
        span.set_attribute(TRIAL_ATTRIBUTE_STATUS, "pruned")
        super().emit(span)


class NewBestTrial(TrialEvent[CandidateT]):
    """Signals that a new best trial has been found."""

    candidate: t.Any = None
    scores: dict[str, float] = Field(default_factory=dict)

    def _get_data(self) -> dict[str, t.Any]:
        data: dict[str, t.Any] = {}
        if self.scores:
            data["scores"] = self.scores
        if self.candidate is not None:
            data["candidate"] = self.candidate
        return data

    def emit(self, span: "TaskSpan") -> None:
        span.set_attribute(TRIAL_ATTRIBUTE_ID, str(self.trial_id))
        if self.scores:
            span.set_attribute(TRIAL_ATTRIBUTE_SCORES, self.scores)
            span.log_output("best_scores", self.scores)
        if self.candidate is not None:
            span.log_output("best_candidate", self.candidate)
        super().emit(span)


class OptimizationEvent(BaseModel, t.Generic[CandidateT]):
    """Base event type for Dreadnode optimize_anything."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC), kw_only=True)
    optimization_id: UUID = Field(default_factory=uuid4)
    optimization_name: str | None = None

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "type": self.__class__.__name__.lower(),
            "timestamp": self.timestamp.isoformat(),
            "optimization_id": str(self.optimization_id),
            "optimization_name": self.optimization_name,
            "data": self._get_data(),
        }

    def _get_data(self) -> dict[str, t.Any]:
        return {}

    def emit(self, span: "TaskSpan") -> None:
        span.log_event(
            f"optimization.{self.__class__.__name__}",
            {"event_type": self.__class__.__name__, "timestamp": self.timestamp.isoformat()},
        )


class OptimizationStart(OptimizationEvent[CandidateT]):
    """Signals the beginning of an optimize_anything run."""

    backend: str = "gepa"
    dataset_size: int = 0
    valset_size: int = 0
    objective: str | None = None
    seed_candidate: t.Any = None
    uses_adapter: bool = False

    def _get_data(self) -> dict[str, t.Any]:
        data: dict[str, t.Any] = {
            "backend": self.backend,
            "dataset_size": self.dataset_size,
            "valset_size": self.valset_size,
        }
        if self.objective is not None:
            data["objective"] = self.objective
        if self.seed_candidate is not None:
            data["seed_candidate"] = self.seed_candidate
        data["uses_adapter"] = self.uses_adapter
        return data

    def emit(self, span: "TaskSpan") -> None:
        span.log_param("backend", self.backend)
        span.log_param("dataset_size", self.dataset_size)
        span.log_param("valset_size", self.valset_size)
        if self.objective is not None:
            span.log_param("objective", self.objective)
        span.log_param("uses_adapter", self.uses_adapter)
        super().emit(span)


class IterationStart(OptimizationEvent[CandidateT]):
    """Signals the start of an optimization iteration."""

    iteration: int = 0

    def _get_data(self) -> dict[str, t.Any]:
        return {"iteration": self.iteration}

    def emit(self, span: "TaskSpan") -> None:
        span.log_metric("optimization/iteration", self.iteration)
        super().emit(span)


class CandidateAccepted(OptimizationEvent[CandidateT]):
    """Signals that GEPA accepted a proposed candidate."""

    iteration: int = 0
    candidate_index: int = 0
    score: float | None = None
    parent_indices: list[int] = Field(default_factory=list)

    def _get_data(self) -> dict[str, t.Any]:
        data: dict[str, t.Any] = {
            "iteration": self.iteration,
            "candidate_index": self.candidate_index,
            "parent_indices": self.parent_indices,
        }
        if self.score is not None:
            data["score"] = self.score
        return data

    def emit(self, span: "TaskSpan") -> None:
        if self.score is not None:
            span.log_metric("optimization/accepted_score", self.score, step=self.iteration)
        span.log_param("accepted_candidate_index", self.candidate_index)
        super().emit(span)


class CandidateRejected(OptimizationEvent[CandidateT]):
    """Signals that GEPA rejected a proposed candidate."""

    iteration: int = 0
    previous_score: float | None = None
    candidate_score: float | None = None
    reason: str = ""

    def _get_data(self) -> dict[str, t.Any]:
        data: dict[str, t.Any] = {"iteration": self.iteration, "reason": self.reason}
        if self.previous_score is not None:
            data["previous_score"] = self.previous_score
        if self.candidate_score is not None:
            data["candidate_score"] = self.candidate_score
        return data

    def emit(self, span: "TaskSpan") -> None:
        if self.candidate_score is not None:
            span.log_metric(
                "optimization/rejected_score", self.candidate_score, step=self.iteration
            )
        if self.reason:
            span.log_output("optimization_rejection_reason", self.reason[:500])
        super().emit(span)


class ValsetEvaluated(OptimizationEvent[CandidateT]):
    """Signals that GEPA finished a validation-set evaluation."""

    iteration: int = 0
    candidate_index: int = 0
    candidate: t.Any = None
    average_score: float | None = None
    num_examples_evaluated: int = 0
    total_valset_size: int = 0
    is_best_program: bool = False
    parent_indices: list[int] = Field(default_factory=list)

    def _get_data(self) -> dict[str, t.Any]:
        data: dict[str, t.Any] = {
            "iteration": self.iteration,
            "candidate_index": self.candidate_index,
            "num_examples_evaluated": self.num_examples_evaluated,
            "total_valset_size": self.total_valset_size,
            "is_best_program": self.is_best_program,
            "parent_indices": self.parent_indices,
        }
        if self.average_score is not None:
            data["average_score"] = self.average_score
        if self.candidate is not None:
            data["candidate"] = self.candidate
        return data

    def emit(self, span: "TaskSpan") -> None:
        if self.average_score is not None:
            span.log_metric("optimization/val_score", self.average_score, step=self.iteration)
        span.log_param("val_candidate_index", self.candidate_index)
        super().emit(span)


class BudgetUpdated(OptimizationEvent[CandidateT]):
    """Signals that GEPA updated optimization budget usage."""

    iteration: int = 0
    metric_calls_used: int = 0
    metric_calls_delta: int = 0
    metric_calls_remaining: int | None = None

    def _get_data(self) -> dict[str, t.Any]:
        data: dict[str, t.Any] = {
            "iteration": self.iteration,
            "metric_calls_used": self.metric_calls_used,
            "metric_calls_delta": self.metric_calls_delta,
        }
        if self.metric_calls_remaining is not None:
            data["metric_calls_remaining"] = self.metric_calls_remaining
        return data

    def emit(self, span: "TaskSpan") -> None:
        span.log_metric(
            "optimization/metric_calls_used", self.metric_calls_used, step=self.iteration
        )
        if self.metric_calls_remaining is not None:
            span.log_metric(
                "optimization/metric_calls_remaining",
                self.metric_calls_remaining,
                step=self.iteration,
            )
        super().emit(span)


class ParetoFrontUpdated(OptimizationEvent[CandidateT]):
    """Signals that the Pareto frontier changed."""

    frontier_size: int = 0
    best_score: float | None = None
    iteration: int | None = None
    frontier_candidate_indices: list[int] = Field(default_factory=list)
    displaced_candidate_indices: list[int] = Field(default_factory=list)

    def _get_data(self) -> dict[str, t.Any]:
        data: dict[str, t.Any] = {"frontier_size": self.frontier_size}
        if self.best_score is not None:
            data["best_score"] = self.best_score
        if self.iteration is not None:
            data["iteration"] = self.iteration
        if self.frontier_candidate_indices:
            data["frontier_candidate_indices"] = self.frontier_candidate_indices
        if self.displaced_candidate_indices:
            data["displaced_candidate_indices"] = self.displaced_candidate_indices
        return data

    def emit(self, span: "TaskSpan") -> None:
        span.log_metric("optimization/frontier_size", self.frontier_size)
        if self.best_score is not None:
            span.log_metric("optimization/frontier_best_score", self.best_score)
        super().emit(span)


class OptimizationError(OptimizationEvent[CandidateT]):
    """Signals that optimize_anything failed before producing a result."""

    backend: str = "gepa"
    error: str = ""

    def _get_data(self) -> dict[str, t.Any]:
        return {"backend": self.backend, "error": self.error}

    def emit(self, span: "TaskSpan") -> None:
        span.log_output("optimization_error", self.error[:500])
        super().emit(span)


class OptimizationEnd(OptimizationEvent[CandidateT]):
    """Signals the end of an optimize_anything run."""

    backend: str = "gepa"
    result: "OptimizationResult[CandidateT] | None" = Field(default=None, repr=False)
    best_candidate: t.Any = None
    best_score: float | None = None
    best_scores: dict[str, float] = Field(default_factory=dict)
    frontier_size: int = 0
    history_length: int = 0

    def _get_data(self) -> dict[str, t.Any]:
        data: dict[str, t.Any] = {
            "backend": self.backend,
            "best_score": self.best_score,
            "best_scores": self.best_scores,
            "frontier_size": self.frontier_size,
            "history_length": self.history_length,
        }
        if self.best_candidate is not None:
            data["best_candidate"] = self.best_candidate
        return data

    def emit(self, span: "TaskSpan") -> None:
        span.log_output(
            "optimization_result",
            {
                "backend": self.backend,
                "best_candidate": self.best_candidate,
                "best_score": self.best_score,
                "best_scores": self.best_scores,
                "frontier_size": self.frontier_size,
                "history_length": self.history_length,
            },
        )
        if self.best_score is not None:
            span.log_metric("optimization/best_score", self.best_score)
        super().emit(span)


# Backwards compatibility alias
NewBestTrialFound = NewBestTrial
