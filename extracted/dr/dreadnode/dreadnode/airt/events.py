"""AIRT event hierarchy for tracing.

Follows the same pattern as ``core/optimization/events.py``: each event is a
Pydantic model with ``as_dict()`` for serialisation, ``_get_data()`` for
subclass-specific fields, and ``emit(span)`` for writing telemetry to a
:class:`TaskSpan`.

Hierarchy::

    AssessmentEvent          -- base: assessment_id, assessment_name, timestamp
    +-- AssessmentStart      -- target_model, planned_attacks, planned_goals
    +-- AssessmentEnd        -- status, total_attacks, total_trials, overall_asr, risk_score
    +-- AttackEvent          -- attack_name, goal, goal_category, transforms_applied
        +-- AttackStart      -- n_iterations, compliance_tags
        +-- AttackEnd        -- best_score, asr, is_jailbreak, execution_time_s, stop_reason
        +-- TrialResult      -- trial_index, score, is_jailbreak, candidate, response
        +-- TrialPruned      -- trial_index, reason
        +-- TrialFailed      -- trial_index, error

    TransformApplied         -- standalone (context via span hierarchy)
"""

from __future__ import annotations

import typing as t
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

from dreadnode.tracing.constants import (
    AIRT_ATTRIBUTE_ASR,
    AIRT_ATTRIBUTE_ASSESSMENT_ID,
    AIRT_ATTRIBUTE_ASSESSMENT_NAME,
    AIRT_ATTRIBUTE_ATTACK_NAME,
    AIRT_ATTRIBUTE_ATTACKER_MODEL,
    AIRT_ATTRIBUTE_BEST_CANDIDATE,
    AIRT_ATTRIBUTE_BEST_RESPONSE,
    AIRT_ATTRIBUTE_BEST_SCORE,
    AIRT_ATTRIBUTE_CANDIDATE,
    AIRT_ATTRIBUTE_CATEGORY,
    AIRT_ATTRIBUTE_COMPLIANCE_TAGS,
    AIRT_ATTRIBUTE_EVALUATOR_MODEL,
    AIRT_ATTRIBUTE_EXECUTION_TIME_S,
    AIRT_ATTRIBUTE_GOAL,
    AIRT_ATTRIBUTE_GOAL_CATEGORY,
    AIRT_ATTRIBUTE_IS_JAILBREAK,
    AIRT_ATTRIBUTE_OVERALL_ASR,
    AIRT_ATTRIBUTE_RESPONSE,
    AIRT_ATTRIBUTE_RISK_SCORE,
    AIRT_ATTRIBUTE_SUB_CATEGORY,
    AIRT_ATTRIBUTE_TARGET_MODEL,
    AIRT_ATTRIBUTE_TRANSFORM_CHAIN_LENGTH,
    AIRT_ATTRIBUTE_TRANSFORM_ERRORED,
    AIRT_ATTRIBUTE_TRANSFORM_INDEX,
    AIRT_ATTRIBUTE_TRANSFORM_MODALITY,
    AIRT_ATTRIBUTE_TRANSFORM_NAME,
    AIRT_ATTRIBUTE_TRANSFORMS,
    AIRT_ATTRIBUTE_TRIAL_INDEX,
)

if t.TYPE_CHECKING:
    from dreadnode.tracing.span import TaskSpan


def _truncate(text: str, max_len: int = 0) -> str:  # noqa: ARG001
    """Pass-through; no truncation applied to span inputs/outputs."""
    return text


# =============================================================================
# Assessment Events
# =============================================================================


class AssessmentEvent(BaseModel):
    """Base class for assessment-level events."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC), kw_only=True)
    assessment_id: str = ""
    assessment_name: str = ""

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "type": self.__class__.__name__.lower(),
            "timestamp": self.timestamp.isoformat(),
            "assessment_id": self.assessment_id,
            "assessment_name": self.assessment_name,
            "data": self._get_data(),
        }

    def _get_data(self) -> dict[str, t.Any]:
        return {}

    def emit(self, span: TaskSpan) -> None:
        span.log_event(
            f"airt.{self.__class__.__name__}",
            {"event_type": self.__class__.__name__, "timestamp": self.timestamp.isoformat()},
        )


class AssessmentStart(AssessmentEvent):
    """Signals the beginning of an assessment."""

    target_model: str | None = None
    attacker_model: str | None = None
    evaluator_model: str | None = None
    planned_attacks: list[str] = Field(default_factory=list)
    planned_goals: list[str] = Field(default_factory=list)
    goal_categories: list[str] = Field(default_factory=list)
    compliance_frameworks: list[str] = Field(default_factory=list)
    project_id: str | None = None

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "target_model": self.target_model,
            "attacker_model": self.attacker_model,
            "evaluator_model": self.evaluator_model,
            "planned_attacks": self.planned_attacks,
            "planned_goals": self.planned_goals,
            "goal_categories": self.goal_categories,
            "compliance_frameworks": self.compliance_frameworks,
            "project_id": self.project_id,
        }

    def emit(self, span: TaskSpan) -> None:
        span.set_attribute(AIRT_ATTRIBUTE_ASSESSMENT_ID, self.assessment_id)
        span.set_attribute(AIRT_ATTRIBUTE_ASSESSMENT_NAME, self.assessment_name)
        if self.target_model:
            span.set_attribute(AIRT_ATTRIBUTE_TARGET_MODEL, self.target_model)
        if self.attacker_model:
            span.set_attribute(AIRT_ATTRIBUTE_ATTACKER_MODEL, self.attacker_model)
        if self.evaluator_model:
            span.set_attribute(AIRT_ATTRIBUTE_EVALUATOR_MODEL, self.evaluator_model)
        span.log_param("planned_attacks", self.planned_attacks)
        if self.planned_goals:
            span.log_param("planned_goals", self.planned_goals)
        span.log_input(
            "assessment_config",
            {
                "target_model": self.target_model,
                "attacker_model": self.attacker_model,
                "evaluator_model": self.evaluator_model,
                "planned_attacks": self.planned_attacks,
                "goal_categories": self.goal_categories,
                "compliance_frameworks": self.compliance_frameworks,
                "project_id": self.project_id,
            },
        )
        super().emit(span)


class AssessmentEnd(AssessmentEvent):
    """Signals the end of an assessment."""

    status: str = "completed"
    total_attacks: int = 0
    total_trials: int = 0
    finished_trials: int = 0
    failed_trials: int = 0
    pruned_trials: int = 0
    total_jailbreaks: int = 0
    overall_asr: float = 0.0
    risk_score: float = 0.0
    total_execution_time_s: float = 0.0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    goal_categories_tested: list[str] = Field(default_factory=list)
    attacks_used: list[str] = Field(default_factory=list)
    transforms_used: list[str] = Field(default_factory=list)

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "status": self.status,
            "total_attacks": self.total_attacks,
            "total_trials": self.total_trials,
            "finished_trials": self.finished_trials,
            "failed_trials": self.failed_trials,
            "pruned_trials": self.pruned_trials,
            "total_jailbreaks": self.total_jailbreaks,
            "overall_asr": self.overall_asr,
            "risk_score": self.risk_score,
            "total_execution_time_s": self.total_execution_time_s,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "goal_categories_tested": self.goal_categories_tested,
            "attacks_used": self.attacks_used,
            "transforms_used": self.transforms_used,
        }

    def emit(self, span: TaskSpan) -> None:
        span.set_attribute(AIRT_ATTRIBUTE_OVERALL_ASR, self.overall_asr)
        span.set_attribute(AIRT_ATTRIBUTE_RISK_SCORE, self.risk_score)
        span.set_attribute(AIRT_ATTRIBUTE_EXECUTION_TIME_S, self.total_execution_time_s)
        span.log_output(
            "assessment_result",
            {
                "status": self.status,
                "total_attacks": self.total_attacks,
                "total_trials": self.total_trials,
                "finished_trials": self.finished_trials,
                "failed_trials": self.failed_trials,
                "pruned_trials": self.pruned_trials,
                "total_jailbreaks": self.total_jailbreaks,
                "overall_asr": self.overall_asr,
                "risk_score": self.risk_score,
                "total_execution_time_s": self.total_execution_time_s,
                "total_input_tokens": self.total_input_tokens,
                "total_output_tokens": self.total_output_tokens,
                "goal_categories_tested": self.goal_categories_tested,
                "attacks_used": self.attacks_used,
                "transforms_used": self.transforms_used,
            },
        )
        span.log_metric("airt/overall_asr", self.overall_asr)
        span.log_metric("airt/risk_score", self.risk_score)
        span.log_metric("airt/total_attacks", self.total_attacks)
        span.log_metric("airt/total_trials", self.total_trials)
        span.log_metric("airt/total_jailbreaks", self.total_jailbreaks)
        span.log_metric("airt/total_execution_time_s", self.total_execution_time_s)
        super().emit(span)


# =============================================================================
# Attack Events
# =============================================================================


class AttackEvent(AssessmentEvent):
    """Base class for attack-level events (inherits assessment context)."""

    attack_name: str = ""
    goal: str = ""
    goal_category: str = ""
    category: str = ""
    sub_category: str = ""
    transforms_applied: list[str] = Field(default_factory=list)

    def as_dict(self) -> dict[str, t.Any]:
        base = super().as_dict()
        base["data"].update(
            {
                "attack_name": self.attack_name,
                "goal": self.goal,
                "goal_category": self.goal_category,
                "category": self.category,
                "sub_category": self.sub_category,
                "transforms_applied": self.transforms_applied,
            }
        )
        return base


class AttackStart(AttackEvent):
    """Signals the beginning of an attack."""

    n_iterations: int = 0
    compliance_tags: dict[str, t.Any] = Field(default_factory=dict)
    target_model: str | None = None
    attacker_model: str | None = None
    evaluator_model: str | None = None
    scorer_names: list[str] = Field(default_factory=list)
    early_stopping_score: float | None = None

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "n_iterations": self.n_iterations,
            "compliance_tags": self.compliance_tags,
            "target_model": self.target_model,
            "attacker_model": self.attacker_model,
            "evaluator_model": self.evaluator_model,
            "scorer_names": self.scorer_names,
            "early_stopping_score": self.early_stopping_score,
        }

    def emit(self, span: TaskSpan) -> None:
        # Propagate assessment context to attack span for CH queries
        span.set_attribute(AIRT_ATTRIBUTE_ASSESSMENT_ID, self.assessment_id)
        span.set_attribute(AIRT_ATTRIBUTE_ASSESSMENT_NAME, self.assessment_name)
        span.set_attribute(AIRT_ATTRIBUTE_ATTACK_NAME, self.attack_name)
        span.set_attribute(AIRT_ATTRIBUTE_GOAL, self.goal)
        span.set_attribute(AIRT_ATTRIBUTE_GOAL_CATEGORY, self.goal_category)
        span.set_attribute(AIRT_ATTRIBUTE_CATEGORY, self.category)
        span.set_attribute(AIRT_ATTRIBUTE_SUB_CATEGORY, self.sub_category)
        span.set_attribute(AIRT_ATTRIBUTE_TRANSFORMS, self.transforms_applied)
        if self.compliance_tags:
            span.set_attribute(AIRT_ATTRIBUTE_COMPLIANCE_TAGS, self.compliance_tags)
        span.set_attribute(AIRT_ATTRIBUTE_TARGET_MODEL, self.target_model or "")
        if self.attacker_model:
            span.set_attribute(AIRT_ATTRIBUTE_ATTACKER_MODEL, self.attacker_model)
        if self.evaluator_model:
            span.set_attribute(AIRT_ATTRIBUTE_EVALUATOR_MODEL, self.evaluator_model)
        span.log_param("n_iterations", self.n_iterations)
        span.log_input("goal", self.goal)
        span.log_input(
            "attack_config",
            {
                "attack_name": self.attack_name,
                "goal": self.goal,
                "goal_category": self.goal_category,
                "category": self.category,
                "sub_category": self.sub_category,
                "transforms_applied": self.transforms_applied,
                "n_iterations": self.n_iterations,
                "target_model": self.target_model,
                "attacker_model": self.attacker_model,
                "evaluator_model": self.evaluator_model,
                "scorer_names": self.scorer_names,
                "early_stopping_score": self.early_stopping_score,
                "compliance_tags": self.compliance_tags,
            },
        )
        super().emit(span)


class AttackEnd(AttackEvent):
    """Signals the end of an attack."""

    status: str = "completed"
    best_score: float | None = None
    asr: float = 0.0
    is_jailbreak: bool = False
    execution_time_s: float = 0.0
    stop_reason: str = ""
    total_trials: int = 0
    finished_trials: int = 0
    pruned_trials: int = 0
    failed_trials: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    best_candidate: str = ""
    best_response: str = ""
    best_trial_index: int = -1
    secondary_scores: dict[str, float] = Field(default_factory=dict)

    def _get_data(self) -> dict[str, t.Any]:
        data: dict[str, t.Any] = {
            "status": self.status,
            "asr": self.asr,
            "is_jailbreak": self.is_jailbreak,
            "execution_time_s": self.execution_time_s,
            "total_trials": self.total_trials,
            "finished_trials": self.finished_trials,
            "pruned_trials": self.pruned_trials,
            "failed_trials": self.failed_trials,
        }
        if self.best_score is not None:
            data["best_score"] = self.best_score
        if self.stop_reason:
            data["stop_reason"] = self.stop_reason
        if self.best_candidate:
            data["best_candidate"] = self.best_candidate
        if self.best_response:
            data["best_response"] = self.best_response
        if self.best_trial_index >= 0:
            data["best_trial_index"] = self.best_trial_index
        if self.secondary_scores:
            data["secondary_scores"] = self.secondary_scores
        return data

    def emit(self, span: TaskSpan) -> None:
        # Propagate assessment context to attack span for CH queries
        span.set_attribute(AIRT_ATTRIBUTE_ASSESSMENT_ID, self.assessment_id)
        span.set_attribute(AIRT_ATTRIBUTE_ASSESSMENT_NAME, self.assessment_name)
        span.set_attribute(AIRT_ATTRIBUTE_ASR, self.asr)
        span.set_attribute(AIRT_ATTRIBUTE_IS_JAILBREAK, self.is_jailbreak)
        span.set_attribute(AIRT_ATTRIBUTE_EXECUTION_TIME_S, self.execution_time_s)
        if self.best_score is not None:
            span.set_attribute(AIRT_ATTRIBUTE_BEST_SCORE, self.best_score)
        if self.best_candidate:
            span.set_attribute(AIRT_ATTRIBUTE_BEST_CANDIDATE, _truncate(self.best_candidate))
        if self.best_response:
            span.set_attribute(AIRT_ATTRIBUTE_BEST_RESPONSE, _truncate(self.best_response))
        span.log_output(
            "attack_result",
            {
                "best_score": self.best_score,
                "asr": self.asr,
                "is_jailbreak": self.is_jailbreak,
                "execution_time_s": self.execution_time_s,
                "stop_reason": self.stop_reason,
                "total_trials": self.total_trials,
                "finished_trials": self.finished_trials,
                "pruned_trials": self.pruned_trials,
                "failed_trials": self.failed_trials,
                "best_candidate": _truncate(self.best_candidate),
                "best_response": _truncate(self.best_response),
                "best_trial_index": self.best_trial_index,
            },
        )
        span.log_metric("airt/attack_asr", self.asr)
        if self.best_score is not None:
            span.log_metric("airt/best_score", self.best_score)
        if self.input_tokens > 0:
            span.log_metric("airt/input_tokens", self.input_tokens)
        if self.output_tokens > 0:
            span.log_metric("airt/output_tokens", self.output_tokens)
        super().emit(span)


class TrialResult(AttackEvent):
    """Records a completed trial result."""

    trial_index: int = 0
    score: float = 0.0
    is_jailbreak: bool = False
    candidate: str = ""
    response: str = ""
    secondary_scores: dict[str, float] = Field(default_factory=dict)
    transform_chain: list[str] = Field(default_factory=list)

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "trial_index": self.trial_index,
            "score": self.score,
            "is_jailbreak": self.is_jailbreak,
            "candidate": self.candidate,
            "response": self.response,
            "secondary_scores": self.secondary_scores,
            "transform_chain": self.transform_chain,
        }

    def emit(self, span: TaskSpan) -> None:
        # Propagate assessment context to trial span for CH queries
        span.set_attribute(AIRT_ATTRIBUTE_ASSESSMENT_ID, self.assessment_id)
        span.set_attribute(AIRT_ATTRIBUTE_ASSESSMENT_NAME, self.assessment_name)
        span.set_attribute(AIRT_ATTRIBUTE_TRIAL_INDEX, self.trial_index)
        span.set_attribute(AIRT_ATTRIBUTE_BEST_SCORE, self.score)
        span.set_attribute(AIRT_ATTRIBUTE_IS_JAILBREAK, self.is_jailbreak)
        span.set_attribute(AIRT_ATTRIBUTE_ATTACK_NAME, self.attack_name)
        span.set_attribute(AIRT_ATTRIBUTE_GOAL, self.goal)
        span.set_attribute(AIRT_ATTRIBUTE_GOAL_CATEGORY, self.goal_category)
        span.set_attribute(AIRT_ATTRIBUTE_CATEGORY, self.category)
        span.set_attribute(AIRT_ATTRIBUTE_SUB_CATEGORY, self.sub_category)
        span.set_attribute(
            AIRT_ATTRIBUTE_TRANSFORMS, self.transform_chain or self.transforms_applied
        )
        if self.candidate:
            span.set_attribute(AIRT_ATTRIBUTE_CANDIDATE, _truncate(self.candidate))
        if self.response:
            span.set_attribute(AIRT_ATTRIBUTE_RESPONSE, _truncate(self.response))
        span.log_input("candidate", _truncate(self.candidate))
        span.log_output("response", _truncate(self.response))
        span.log_metric("airt/trial_score", self.score, step=self.trial_index)
        for scorer_name, scorer_val in self.secondary_scores.items():
            span.log_metric(f"airt/secondary/{scorer_name}", scorer_val, step=self.trial_index)
        super().emit(span)


class TrialPruned(AttackEvent):
    """Records a pruned trial."""

    trial_index: int = 0
    reason: str = ""

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "trial_index": self.trial_index,
            "reason": self.reason,
        }

    def emit(self, span: TaskSpan) -> None:
        span.set_attribute(AIRT_ATTRIBUTE_TRIAL_INDEX, self.trial_index)
        span.log_output("pruned_reason", self.reason or "pruned")
        super().emit(span)


class TrialFailed(AttackEvent):
    """Records a failed trial."""

    trial_index: int = 0
    error: str = ""

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "trial_index": self.trial_index,
            "error": self.error,
        }

    def emit(self, span: TaskSpan) -> None:
        span.set_attribute(AIRT_ATTRIBUTE_TRIAL_INDEX, self.trial_index)
        span.log_output("error", self.error or "failed")
        super().emit(span)


# =============================================================================
# Transform Event (standalone -- context comes from parent span hierarchy)
# =============================================================================


class TransformApplied(BaseModel):
    """Records a single transform application during prompt evaluation.

    Standalone (not inheriting AttackEvent) because AIRT context comes
    from the parent span hierarchy, not threaded through the objective function.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC), kw_only=True)
    transform_name: str = ""
    transform_index: int = 0
    chain_length: int = 0
    modality: str = "text"
    input_text: str = ""
    output_text: str = ""
    execution_time_ms: float = 0.0
    errored: bool = False
    compliance_tags: dict[str, t.Any] = Field(default_factory=dict)

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "type": "transformapplied",
            "timestamp": self.timestamp.isoformat(),
            "data": self._get_data(),
        }

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "transform_name": self.transform_name,
            "transform_index": self.transform_index,
            "chain_length": self.chain_length,
            "modality": self.modality,
            "input_text": self.input_text,
            "output_text": self.output_text,
            "execution_time_ms": self.execution_time_ms,
            "errored": self.errored,
            "compliance_tags": self.compliance_tags,
        }

    def emit(self, span: TaskSpan) -> None:
        span.set_attribute(AIRT_ATTRIBUTE_TRANSFORM_NAME, self.transform_name)
        span.set_attribute(AIRT_ATTRIBUTE_TRANSFORM_INDEX, self.transform_index)
        span.set_attribute(AIRT_ATTRIBUTE_TRANSFORM_CHAIN_LENGTH, self.chain_length)
        span.set_attribute(AIRT_ATTRIBUTE_TRANSFORM_MODALITY, self.modality)
        span.set_attribute(AIRT_ATTRIBUTE_TRANSFORM_ERRORED, self.errored)
        if self.compliance_tags:
            span.set_attribute(AIRT_ATTRIBUTE_COMPLIANCE_TAGS, self.compliance_tags)
        span.log_input("transform_input", _truncate(self.input_text))
        span.log_output("transform_output", _truncate(self.output_text))
        if self.execution_time_ms > 0:
            span.log_metric("airt/transform_time_ms", self.execution_time_ms)
        span.log_event(
            "airt.TransformApplied",
            {
                "event_type": "TransformApplied",
                "timestamp": self.timestamp.isoformat(),
                "transform_name": self.transform_name,
            },
        )
