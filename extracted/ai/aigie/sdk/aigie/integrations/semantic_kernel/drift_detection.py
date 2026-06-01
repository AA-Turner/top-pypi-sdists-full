"""
Drift Detection for Semantic Kernel.

Tracks planned vs actual execution to detect behavioral drifts.
Useful for monitoring planner effectiveness and function reliability.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


class DriftType(Enum):
    """Types of behavioral drift in Semantic Kernel workflows."""

    # Planner drifts
    PLAN_DEVIATION = "plan_deviation"  # Execution diverged from plan
    EXTRA_FUNCTION_CALL = "extra_function"  # Function called not in plan
    MISSING_FUNCTION_CALL = "missing_function"  # Planned function not called
    FUNCTION_ORDER_CHANGE = "function_order"  # Functions executed in different order
    PLAN_RETRY = "plan_retry"  # Plan needed to be regenerated

    # Function drifts
    FUNCTION_FAILURE = "function_failure"  # Expected function failed
    FUNCTION_TIMEOUT = "function_timeout"  # Function took too long
    RESULT_UNEXPECTED = "result_unexpected"  # Function result unexpected
    ARGUMENT_MISMATCH = "argument_mismatch"  # Arguments differ from expected

    # Plugin drifts
    PLUGIN_UNAVAILABLE = "plugin_unavailable"  # Expected plugin not available
    PLUGIN_CHANGE = "plugin_change"  # Different plugin used than expected

    # Output drifts
    OUTPUT_FORMAT_CHANGE = "output_format"  # Output format differs from expected
    OUTPUT_TRUNCATED = "output_truncated"  # Output appears truncated
    OUTPUT_EMPTY = "output_empty"  # No output when expected

    # Token/Cost drifts
    TOKEN_ANOMALY = "token_anomaly"  # Unusual token usage
    DURATION_ANOMALY = "duration_anomaly"  # Execution took unusually long


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
    function_name: str | None = None
    plugin_name: str | None = None
    planner_type: str | None = None
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
            "function_name": self.function_name,
            "plugin_name": self.plugin_name,
            "planner_type": self.planner_type,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class PlannedStep:
    """Represents a single step in a plan."""

    function_name: str
    plugin_name: str | None = None
    arguments: Dict[str, Any] = field(default_factory=dict)
    expected_output_type: str | None = None
    step_number: int = 0


@dataclass
class KernelPlan:
    """Captures the expected execution plan from a Semantic Kernel planner."""

    # Plan info
    planner_type: str = ""  # Sequential, Action, Handlebars
    goal: str = ""
    steps: List[PlannedStep] = field(default_factory=list)
    expected_functions: Set[str] = field(default_factory=set)
    available_plugins: Set[str] = field(default_factory=set)

    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    llm_model: str | None = None

    def add_step(
        self,
        function_name: str,
        plugin_name: str | None = None,
        arguments: Dict[str, Any] | None = None,
    ) -> None:
        """Add a step to the plan."""
        step = PlannedStep(
            function_name=function_name,
            plugin_name=plugin_name,
            arguments=arguments or {},
            step_number=len(self.steps),
        )
        self.steps.append(step)

        full_name = f"{plugin_name}.{function_name}" if plugin_name else function_name
        self.expected_functions.add(full_name)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "planner_type": self.planner_type,
            "goal": self.goal[:500],
            "step_count": len(self.steps),
            "steps": [
                {
                    "step": s.step_number,
                    "function": f"{s.plugin_name}.{s.function_name}"
                    if s.plugin_name
                    else s.function_name,
                    "arguments": list(s.arguments.keys()),
                }
                for s in self.steps
            ],
            "expected_functions": list(self.expected_functions),
            "available_plugins": list(self.available_plugins),
            "timestamp": self.timestamp.isoformat(),
            "llm_model": self.llm_model,
        }


@dataclass
class ExecutedStep:
    """Records an executed function step."""

    function_name: str
    plugin_name: str | None = None
    arguments: Dict[str, Any] = field(default_factory=dict)
    result: str | None = None
    success: bool = True
    duration_ms: float = 0.0
    error: str | None = None
    step_number: int = 0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ExecutionTrace:
    """Tracks actual execution for comparison against plan."""

    # Execution events
    executed_steps: List[ExecutedStep] = field(default_factory=list)
    executed_functions: Set[str] = field(default_factory=set)
    failed_functions: Set[str] = field(default_factory=set)

    # Metrics
    total_duration_ms: float = 0.0
    total_tokens: int = 0
    total_cost: float = 0.0
    plan_retries: int = 0

    # Final result
    success: bool = False
    final_result: str | None = None

    def add_step(
        self,
        function_name: str,
        plugin_name: str | None = None,
        arguments: Dict[str, Any] | None = None,
        result: str | None = None,
        success: bool = True,
        duration_ms: float = 0.0,
        error: str | None = None,
    ) -> None:
        """Record an executed step."""
        step = ExecutedStep(
            function_name=function_name,
            plugin_name=plugin_name,
            arguments=arguments or {},
            result=result[:500] if result else None,
            success=success,
            duration_ms=duration_ms,
            error=error[:200] if error else None,
            step_number=len(self.executed_steps),
        )
        self.executed_steps.append(step)

        full_name = f"{plugin_name}.{function_name}" if plugin_name else function_name
        self.executed_functions.add(full_name)

        if not success:
            self.failed_functions.add(full_name)

        self.total_duration_ms += duration_ms

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "step_count": len(self.executed_steps),
            "executed_functions": list(self.executed_functions),
            "failed_functions": list(self.failed_functions),
            "total_duration_ms": self.total_duration_ms,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "plan_retries": self.plan_retries,
            "success": self.success,
        }


class DriftDetector:
    """
    Detects drift between planned and actual execution in Semantic Kernel.

    Captures:
    - Planner-generated plans
    - Actual function executions
    - Compares and reports deviations
    """

    def __init__(self):
        self.plan = KernelPlan()
        self.execution = ExecutionTrace()
        self.detected_drifts: List[DetectedDrift] = []

    def capture_plan(
        self,
        planner_type: str,
        goal: str,
        plan: Any = None,
        available_plugins: List[str] | None = None,
        llm_model: str | None = None,
    ) -> None:
        """
        Capture a generated plan for drift comparison.

        Args:
            planner_type: Type of planner (Sequential, Action, Handlebars)
            goal: The planning goal
            plan: The generated plan object
            available_plugins: List of available plugins
            llm_model: LLM model used for planning
        """
        self.plan.planner_type = planner_type
        self.plan.goal = goal
        self.plan.llm_model = llm_model

        if available_plugins:
            self.plan.available_plugins = set(available_plugins)

        # Extract steps from plan object
        if plan:
            self._extract_plan_steps(plan)

    def _extract_plan_steps(self, plan: Any) -> None:
        """Extract steps from various plan formats."""
        try:
            # Sequential planner format
            if hasattr(plan, "steps"):
                steps = plan.steps
                if isinstance(steps, (list, tuple)):
                    for step in steps:
                        func_name = getattr(step, "function_name", None) or getattr(
                            step, "name", str(step)
                        )
                        plugin_name = getattr(step, "plugin_name", None)
                        arguments = getattr(step, "parameters", {}) or getattr(
                            step, "arguments", {}
                        )
                        self.plan.add_step(func_name, plugin_name, arguments)

            # Action planner format (single function)
            elif hasattr(plan, "function"):
                func = plan.function
                func_name = getattr(func, "name", str(func))
                plugin_name = getattr(func, "plugin_name", None)
                self.plan.add_step(func_name, plugin_name)

            # Handlebars planner format
            elif hasattr(plan, "generated_plan"):
                # Parse from string if necessary
                pass

        except Exception as e:
            logger.debug(f"Error extracting plan steps: {e}")

    def record_function_execution(
        self,
        function_name: str,
        plugin_name: str | None = None,
        arguments: Dict[str, Any] | None = None,
        result: str | None = None,
        success: bool = True,
        duration_ms: float = 0.0,
        error: str | None = None,
    ) -> DetectedDrift | None:
        """
        Record a function execution and check for drift.

        Returns DetectedDrift if drift is detected.
        """
        full_name = f"{plugin_name}.{function_name}" if plugin_name else function_name

        self.execution.add_step(
            function_name=function_name,
            plugin_name=plugin_name,
            arguments=arguments,
            result=result,
            success=success,
            duration_ms=duration_ms,
            error=error,
        )

        drift = None

        # Check if this function was in the plan
        if self.plan.expected_functions and full_name not in self.plan.expected_functions:
            drift = DetectedDrift(
                drift_type=DriftType.EXTRA_FUNCTION_CALL,
                severity=DriftSeverity.WARNING,
                description=f"Function '{full_name}' was called but not in original plan",
                expected="Not in plan",
                actual=f"Called: {full_name}",
                function_name=function_name,
                plugin_name=plugin_name,
                planner_type=self.plan.planner_type,
            )
            self.detected_drifts.append(drift)

        # Check for failure
        if not success:
            drift = DetectedDrift(
                drift_type=DriftType.FUNCTION_FAILURE,
                severity=DriftSeverity.ALERT,
                description=f"Function '{full_name}' failed: {error[:100] if error else 'unknown'}",
                expected="Success",
                actual=f"Failed: {error[:100] if error else 'unknown'}",
                function_name=function_name,
                plugin_name=plugin_name,
                metadata={"error": error[:200] if error else None},
            )
            self.detected_drifts.append(drift)

        # Check for duration anomaly (> 30 seconds)
        if duration_ms > 30000:
            drift = DetectedDrift(
                drift_type=DriftType.DURATION_ANOMALY,
                severity=DriftSeverity.WARNING,
                description=f"Function '{full_name}' took {duration_ms / 1000:.1f}s (>30s threshold)",
                expected="< 30 seconds",
                actual=f"{duration_ms / 1000:.1f} seconds",
                function_name=function_name,
                plugin_name=plugin_name,
            )
            self.detected_drifts.append(drift)

        return drift

    def record_plan_retry(self, reason: str | None = None) -> DetectedDrift:
        """Record when a plan needs to be regenerated."""
        self.execution.plan_retries += 1

        drift = DetectedDrift(
            drift_type=DriftType.PLAN_RETRY,
            severity=DriftSeverity.WARNING,
            description=f"Plan needed to be regenerated (attempt {self.execution.plan_retries})",
            expected="Single plan execution",
            actual=f"Retry #{self.execution.plan_retries}",
            planner_type=self.plan.planner_type,
            metadata={"reason": reason[:200] if reason else None},
        )
        self.detected_drifts.append(drift)
        return drift

    def finalize(
        self,
        success: bool,
        final_result: str | None = None,
        total_tokens: int = 0,
        total_cost: float = 0.0,
    ) -> List[DetectedDrift]:
        """
        Finalize execution tracking and perform final drift analysis.

        Returns all detected drifts.
        """
        self.execution.success = success
        self.execution.final_result = final_result[:500] if final_result else None
        self.execution.total_tokens = total_tokens
        self.execution.total_cost = total_cost

        final_drifts = []

        # Check for missing function calls from plan
        if self.plan.expected_functions:
            missing = self.plan.expected_functions - self.execution.executed_functions
            for func_name in missing:
                drift = DetectedDrift(
                    drift_type=DriftType.MISSING_FUNCTION_CALL,
                    severity=DriftSeverity.WARNING,
                    description=f"Planned function '{func_name}' was never called",
                    expected=f"Call: {func_name}",
                    actual="Not called",
                    function_name=func_name.split(".")[-1] if "." in func_name else func_name,
                    plugin_name=func_name.split(".")[0] if "." in func_name else None,
                    planner_type=self.plan.planner_type,
                )
                final_drifts.append(drift)
                self.detected_drifts.append(drift)

        # Check for empty output when expected
        if success and not final_result:
            drift = DetectedDrift(
                drift_type=DriftType.OUTPUT_EMPTY,
                severity=DriftSeverity.WARNING,
                description="Execution succeeded but produced no output",
                expected="Non-empty result",
                actual="Empty result",
                planner_type=self.plan.planner_type,
            )
            final_drifts.append(drift)
            self.detected_drifts.append(drift)

        # Check execution order if we have a plan
        if self.plan.steps and self.execution.executed_steps:
            order_drift = self._check_execution_order()
            if order_drift:
                final_drifts.append(order_drift)
                self.detected_drifts.append(order_drift)

        return final_drifts

    def _check_execution_order(self) -> DetectedDrift | None:
        """Check if execution order matches plan order."""
        planned_order = [
            f"{s.plugin_name}.{s.function_name}" if s.plugin_name else s.function_name
            for s in self.plan.steps
        ]
        executed_order = [
            f"{s.plugin_name}.{s.function_name}" if s.plugin_name else s.function_name
            for s in self.execution.executed_steps
        ]

        # Filter executed to only include planned functions
        executed_planned = [f for f in executed_order if f in self.plan.expected_functions]

        # Check if order matches
        if executed_planned and planned_order:
            # Simple order check: first N executed should match first N planned
            match_count = min(len(executed_planned), len(planned_order))
            if executed_planned[:match_count] != planned_order[:match_count]:
                return DetectedDrift(
                    drift_type=DriftType.FUNCTION_ORDER_CHANGE,
                    severity=DriftSeverity.INFO,
                    description="Functions executed in different order than planned",
                    expected=f"Order: {', '.join(planned_order[:5])}{'...' if len(planned_order) > 5 else ''}",
                    actual=f"Order: {', '.join(executed_planned[:5])}{'...' if len(executed_planned) > 5 else ''}",
                    planner_type=self.plan.planner_type,
                )

        return None

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of planned vs actual execution."""
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
            return "No drifts detected - execution matched plan"

        report = f"Detected {len(self.detected_drifts)} drift(s):\n"
        for i, drift in enumerate(self.detected_drifts, 1):
            report += f"\n{i}. [{drift.severity.value.upper()}] {drift.drift_type.value}"
            if drift.function_name:
                full_name = (
                    f"{drift.plugin_name}.{drift.function_name}"
                    if drift.plugin_name
                    else drift.function_name
                )
                report += f" (function: {full_name})"
            report += f"\n   {drift.description}\n"
            if drift.expected:
                report += f"   Expected: {drift.expected}\n"
            if drift.actual:
                report += f"   Actual: {drift.actual}\n"

        return report
