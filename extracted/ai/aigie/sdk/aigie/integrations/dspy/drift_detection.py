"""
Drift Detection for DSPy Workflows.

Tracks module execution expectations vs actual behavior to detect drifts.
Useful for monitoring prediction quality, retrieval effectiveness, and optimization progress.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


class DriftType(Enum):
    """Types of behavioral drift in DSPy workflows."""

    # Signature drifts
    SIGNATURE_CHANGE = "signature_change"  # Signature modified unexpectedly
    INPUT_FIELD_MISSING = "input_field_missing"  # Expected input not provided
    OUTPUT_FIELD_MISSING = "output_field_missing"  # Expected output not produced

    # Prediction drifts
    EMPTY_PREDICTION = "empty_prediction"  # No prediction output
    PREDICTION_TRUNCATED = "prediction_truncated"  # Output appears cut off
    PREDICTION_FORMAT = "prediction_format"  # Output format unexpected
    LOW_CONFIDENCE = "low_confidence"  # Model expressed uncertainty

    # Retrieval drifts
    EMPTY_RETRIEVAL = "empty_retrieval"  # No documents retrieved
    LOW_RELEVANCE = "low_relevance"  # Poor retrieval scores
    RETRIEVAL_COUNT = "retrieval_count"  # Unexpected retrieval count

    # Reasoning drifts (CoT, ReAct)
    REASONING_LOOP = "reasoning_loop"  # Repetitive reasoning
    EXCESSIVE_STEPS = "excessive_steps"  # Too many reasoning steps
    INCOMPLETE_REASONING = "incomplete_reasoning"  # Reasoning cut short

    # Optimization drifts
    NO_IMPROVEMENT = "no_improvement"  # Score didn't improve
    OPTIMIZATION_REGRESSION = "optimization_regression"  # Score got worse
    METRIC_ANOMALY = "metric_anomaly"  # Unusual metric values

    # Performance drifts
    DURATION_ANOMALY = "duration_anomaly"  # Execution took too long
    TOKEN_ANOMALY = "token_anomaly"  # Unusual token usage
    COST_ANOMALY = "cost_anomaly"  # Unusual cost

    # Module drifts
    MODULE_FAILURE = "module_failure"  # Module execution failed
    UNEXPECTED_MODULE = "unexpected_module"  # Unplanned module called


class DriftSeverity(Enum):
    """Severity of detected drift."""

    INFO = "info"  # Expected variation, informational
    WARNING = "warning"  # Notable deviation, worth monitoring
    ALERT = "alert"  # Significant drift, may need intervention


@dataclass
class DetectedDrift:
    """Represents a detected drift with full context."""

    drift_type: DriftType
    severity: DriftSeverity
    description: str
    expected: str | None = None
    actual: str | None = None
    module_name: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "drift_type": self.drift_type.value,
            "severity": self.severity.value,
            "description": self.description,
            "expected": self.expected,
            "actual": self.actual,
            "module_name": self.module_name,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class ModuleConfig:
    """Configuration for a DSPy module."""

    name: str
    module_type: str  # predict, cot, react, retriever, etc.
    signature: str | None = None
    input_fields: Set[str] = field(default_factory=set)
    output_fields: Set[str] = field(default_factory=set)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "module_type": self.module_type,
            "signature": self.signature,
            "input_fields": list(self.input_fields),
            "output_fields": list(self.output_fields),
        }


@dataclass
class ProgramPlan:
    """Captures expected DSPy program behavior."""

    # Program info
    program_name: str | None = None

    # Modules
    modules: Dict[str, ModuleConfig] = field(default_factory=dict)
    module_order: List[str] = field(default_factory=list)

    # Expected behaviors
    expected_retrievers: Set[str] = field(default_factory=set)
    max_reasoning_steps: int = 10

    # Optimization settings
    optimizer_name: str | None = None
    metric_name: str | None = None
    baseline_score: float | None = None

    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    llm_model: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "program_name": self.program_name,
            "modules": {k: v.to_dict() for k, v in self.modules.items()},
            "module_order": self.module_order,
            "expected_retrievers": list(self.expected_retrievers),
            "max_reasoning_steps": self.max_reasoning_steps,
            "optimizer_name": self.optimizer_name,
            "metric_name": self.metric_name,
            "baseline_score": self.baseline_score,
            "timestamp": self.timestamp.isoformat(),
            "llm_model": self.llm_model,
        }


@dataclass
class ExecutionTrace:
    """Tracks actual program execution for comparison against plan."""

    # Module tracking
    modules_called: List[str] = field(default_factory=list)
    module_calls: List[Dict[str, Any]] = field(default_factory=list)

    # Prediction tracking
    predictions: List[Dict[str, Any]] = field(default_factory=list)
    empty_predictions: int = 0

    # Retrieval tracking
    retrievals: List[Dict[str, Any]] = field(default_factory=list)
    empty_retrievals: int = 0
    avg_retrieval_score: float = 0.0

    # Reasoning tracking
    reasoning_steps: List[Dict[str, Any]] = field(default_factory=list)
    total_reasoning_steps: int = 0

    # Optimization tracking
    optimization_scores: List[float] = field(default_factory=list)
    best_score: float | None = None
    iterations: int = 0

    # Metrics
    total_duration_ms: float = 0
    total_tokens: int = 0
    total_cost: float = 0

    # Result
    success: bool = False
    final_output: str | None = None

    def add_module_call(
        self,
        module_name: str,
        module_type: str,
        input_fields: Dict[str, Any] | None = None,
        output_fields: Dict[str, Any] | None = None,
        success: bool = True,
        duration_ms: float = 0,
    ) -> None:
        """Record a module call."""
        self.modules_called.append(module_name)
        self.module_calls.append(
            {
                "module_name": module_name,
                "module_type": module_type,
                "input_fields": list(input_fields.keys()) if input_fields else [],
                "output_fields": list(output_fields.keys()) if output_fields else [],
                "success": success,
                "duration_ms": duration_ms,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def add_prediction(
        self,
        module_name: str,
        model: str | None,
        output_fields: Dict[str, Any] | None,
        input_tokens: int = 0,
        output_tokens: int = 0,
    ) -> None:
        """Record a prediction."""
        is_empty = not output_fields or all(not v for v in output_fields.values())
        self.predictions.append(
            {
                "module_name": module_name,
                "model": model,
                "output_fields": list(output_fields.keys()) if output_fields else [],
                "is_empty": is_empty,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "timestamp": datetime.now().isoformat(),
            }
        )
        if is_empty:
            self.empty_predictions += 1
        self.total_tokens += input_tokens + output_tokens

    def add_retrieval(
        self,
        retriever_name: str,
        num_results: int,
        scores: List[float] | None = None,
    ) -> None:
        """Record a retrieval operation."""
        avg_score = sum(scores) / len(scores) if scores else 0.0
        self.retrievals.append(
            {
                "retriever_name": retriever_name,
                "num_results": num_results,
                "avg_score": avg_score,
                "max_score": max(scores) if scores else None,
                "timestamp": datetime.now().isoformat(),
            }
        )
        if num_results == 0:
            self.empty_retrievals += 1
        # Update running average
        total_retrievals = len(self.retrievals)
        self.avg_retrieval_score = (
            self.avg_retrieval_score * (total_retrievals - 1) + avg_score
        ) / total_retrievals

    def add_reasoning_step(
        self,
        step_type: str,
        step_number: int,
        thought: str | None = None,
        action: str | None = None,
    ) -> None:
        """Record a reasoning step."""
        self.reasoning_steps.append(
            {
                "step_type": step_type,
                "step_number": step_number,
                "has_thought": bool(thought),
                "has_action": bool(action),
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.total_reasoning_steps += 1

    def add_optimization_score(self, score: float) -> None:
        """Record an optimization score."""
        self.optimization_scores.append(score)
        self.iterations += 1
        if self.best_score is None or score > self.best_score:
            self.best_score = score

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "modules_called": self.modules_called,
            "module_call_count": len(self.module_calls),
            "prediction_count": len(self.predictions),
            "empty_predictions": self.empty_predictions,
            "retrieval_count": len(self.retrievals),
            "empty_retrievals": self.empty_retrievals,
            "avg_retrieval_score": self.avg_retrieval_score,
            "total_reasoning_steps": self.total_reasoning_steps,
            "optimization_iterations": self.iterations,
            "best_score": self.best_score,
            "total_duration_ms": self.total_duration_ms,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "success": self.success,
        }


class DriftDetector:
    """
    Detects drift between expected and actual DSPy program behavior.

    Captures:
    - Module and signature configurations
    - Actual execution patterns
    - Compares and reports deviations
    """

    def __init__(self):
        self.plan = ProgramPlan()
        self.execution = ExecutionTrace()
        self.detected_drifts: List[DetectedDrift] = []

    def capture_module_config(
        self,
        module_name: str,
        module_type: str,
        signature: str | None = None,
        input_fields: List[str] | None = None,
        output_fields: List[str] | None = None,
    ) -> None:
        """
        Capture module configuration.

        Args:
            module_name: Name of the module
            module_type: Type (predict, cot, react, etc.)
            signature: Module signature
            input_fields: Expected input field names
            output_fields: Expected output field names
        """
        config = ModuleConfig(
            name=module_name,
            module_type=module_type,
            signature=signature,
            input_fields=set(input_fields or []),
            output_fields=set(output_fields or []),
        )
        self.plan.modules[module_name] = config
        self.plan.module_order.append(module_name)

    def capture_optimizer_config(
        self,
        optimizer_name: str,
        metric_name: str | None = None,
        baseline_score: float | None = None,
    ) -> None:
        """Capture optimization configuration."""
        self.plan.optimizer_name = optimizer_name
        self.plan.metric_name = metric_name
        self.plan.baseline_score = baseline_score

    def capture_llm_model(self, model: str) -> None:
        """Capture the LLM model being used."""
        self.plan.llm_model = model

    def record_module_call(
        self,
        module_name: str,
        module_type: str,
        input_fields: Dict[str, Any] | None = None,
        output_fields: Dict[str, Any] | None = None,
        success: bool = True,
        duration_ms: float = 0,
    ) -> DetectedDrift | None:
        """
        Record a module call and check for drift.

        Returns DetectedDrift if drift is detected.
        """
        self.execution.add_module_call(
            module_name, module_type, input_fields, output_fields, success, duration_ms
        )

        # Check for unexpected module
        if module_name not in self.plan.modules:
            drift = DetectedDrift(
                drift_type=DriftType.UNEXPECTED_MODULE,
                severity=DriftSeverity.INFO,
                description=f"Unexpected module '{module_name}' ({module_type}) called",
                expected=f"One of: {list(self.plan.modules.keys())[:5]}",
                actual=module_name,
                module_name=module_name,
            )
            self.detected_drifts.append(drift)
            return drift

        # Check for module failure
        if not success:
            drift = DetectedDrift(
                drift_type=DriftType.MODULE_FAILURE,
                severity=DriftSeverity.WARNING,
                description=f"Module '{module_name}' failed",
                module_name=module_name,
            )
            self.detected_drifts.append(drift)
            return drift

        # Check output fields
        if output_fields is not None:
            config = self.plan.modules.get(module_name)
            if config and config.output_fields:
                missing = config.output_fields - set(output_fields.keys())
                for field in missing:
                    drift = DetectedDrift(
                        drift_type=DriftType.OUTPUT_FIELD_MISSING,
                        severity=DriftSeverity.WARNING,
                        description=f"Expected output field '{field}' missing from '{module_name}'",
                        expected=f"Field: {field}",
                        actual="Field missing",
                        module_name=module_name,
                    )
                    self.detected_drifts.append(drift)
                    return drift

        return None

    def record_prediction(
        self,
        module_name: str,
        model: str | None,
        output_fields: Dict[str, Any] | None,
        input_tokens: int = 0,
        output_tokens: int = 0,
    ) -> DetectedDrift | None:
        """Record a prediction and check for drift."""
        self.execution.add_prediction(
            module_name, model, output_fields, input_tokens, output_tokens
        )

        # Check for empty prediction
        if not output_fields or all(not v for v in output_fields.values()):
            drift = DetectedDrift(
                drift_type=DriftType.EMPTY_PREDICTION,
                severity=DriftSeverity.WARNING,
                description=f"Empty prediction from module '{module_name}'",
                expected="Non-empty output",
                actual="Empty or null output fields",
                module_name=module_name,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_retrieval(
        self,
        retriever_name: str,
        num_results: int,
        scores: List[float] | None = None,
    ) -> DetectedDrift | None:
        """Record a retrieval and check for drift."""
        self.execution.add_retrieval(retriever_name, num_results, scores)

        # Check for empty retrieval
        if num_results == 0:
            drift = DetectedDrift(
                drift_type=DriftType.EMPTY_RETRIEVAL,
                severity=DriftSeverity.WARNING,
                description=f"Retriever '{retriever_name}' returned no results",
                expected="At least 1 result",
                actual="0 results",
                module_name=retriever_name,
            )
            self.detected_drifts.append(drift)
            return drift

        # Check for low relevance
        if scores and max(scores) < 0.5:
            drift = DetectedDrift(
                drift_type=DriftType.LOW_RELEVANCE,
                severity=DriftSeverity.INFO,
                description=f"Low relevance scores from '{retriever_name}'",
                expected="Max score >= 0.5",
                actual=f"Max score: {max(scores):.3f}",
                module_name=retriever_name,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_reasoning_step(
        self,
        step_type: str,
        step_number: int,
        thought: str | None = None,
        action: str | None = None,
    ) -> DetectedDrift | None:
        """Record a reasoning step and check for drift."""
        self.execution.add_reasoning_step(step_type, step_number, thought, action)

        # Check for excessive steps
        if self.execution.total_reasoning_steps > self.plan.max_reasoning_steps:
            drift = DetectedDrift(
                drift_type=DriftType.EXCESSIVE_STEPS,
                severity=DriftSeverity.WARNING,
                description=f"Exceeded max reasoning steps ({self.execution.total_reasoning_steps}/{self.plan.max_reasoning_steps})",
                expected=f"<= {self.plan.max_reasoning_steps} steps",
                actual=f"{self.execution.total_reasoning_steps} steps",
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_optimization_score(self, score: float) -> DetectedDrift | None:
        """Record an optimization score and check for drift."""
        prev_best = self.execution.best_score
        self.execution.add_optimization_score(score)

        # Check for regression (score getting worse after first few iterations)
        if self.execution.iterations > 3 and prev_best is not None:
            if score < prev_best * 0.9:  # More than 10% worse
                drift = DetectedDrift(
                    drift_type=DriftType.OPTIMIZATION_REGRESSION,
                    severity=DriftSeverity.WARNING,
                    description=f"Optimization score regressed from {prev_best:.4f} to {score:.4f}",
                    expected=f">= {prev_best:.4f}",
                    actual=f"{score:.4f}",
                )
                self.detected_drifts.append(drift)
                return drift

        return None

    def finalize(
        self,
        success: bool,
        final_output: Any | None = None,
        total_duration_ms: float = 0,
        total_cost: float = 0,
    ) -> List[DetectedDrift]:
        """
        Finalize program tracking and perform final drift analysis.

        Returns all detected drifts.
        """
        self.execution.success = success
        self.execution.total_duration_ms = total_duration_ms
        self.execution.total_cost = total_cost
        if final_output:
            self.execution.final_output = str(final_output)[:1000]

        # Check for no improvement in optimization
        if self.plan.optimizer_name and self.plan.baseline_score is not None:
            if self.execution.best_score is not None:
                if self.execution.best_score <= self.plan.baseline_score:
                    drift = DetectedDrift(
                        drift_type=DriftType.NO_IMPROVEMENT,
                        severity=DriftSeverity.WARNING,
                        description="Optimization did not improve over baseline",
                        expected=f"> {self.plan.baseline_score:.4f}",
                        actual=f"{self.execution.best_score:.4f}",
                    )
                    self.detected_drifts.append(drift)

        # Check for high empty prediction rate
        if len(self.execution.predictions) > 0:
            empty_rate = self.execution.empty_predictions / len(self.execution.predictions)
            if empty_rate > 0.2:  # More than 20% empty
                drift = DetectedDrift(
                    drift_type=DriftType.EMPTY_PREDICTION,
                    severity=DriftSeverity.WARNING,
                    description=f"High empty prediction rate: {empty_rate:.1%}",
                    expected="< 20% empty",
                    actual=f"{empty_rate:.1%} ({self.execution.empty_predictions}/{len(self.execution.predictions)})",
                )
                self.detected_drifts.append(drift)

        return self.detected_drifts

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of expected vs actual execution."""
        return {
            "plan": self.plan.to_dict(),
            "execution": self.execution.to_dict(),
            "drifts": [d.to_dict() for d in self.detected_drifts],
            "drift_count": len(self.detected_drifts),
            "has_warnings": any(
                d.severity in [DriftSeverity.WARNING, DriftSeverity.ALERT]
                for d in self.detected_drifts
            ),
        }

    def get_drift_report(self) -> str:
        """Get a human-readable drift report."""
        if not self.detected_drifts:
            return "No drifts detected - program execution matched expectations"

        report = f"Detected {len(self.detected_drifts)} drift(s):\n"
        for i, drift in enumerate(self.detected_drifts, 1):
            report += f"\n{i}. [{drift.severity.value.upper()}] {drift.drift_type.value}"
            if drift.module_name:
                report += f" (module: {drift.module_name})"
            report += f"\n   {drift.description}\n"
            if drift.expected:
                report += f"   Expected: {drift.expected}\n"
            if drift.actual:
                report += f"   Actual: {drift.actual}\n"

        return report
