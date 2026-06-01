"""
Goal and Plan Tracking for AI Agents.

This module provides hierarchical goal and plan tracking capabilities
to measure agent reliability through plan adherence scoring.

Key features:
- Define expected execution plans with steps
- Track step completion during agent execution
- Calculate plan adherence scores (reliability metrics)
- Detect deviations from expected behavior
- Signal emission to backend Signal Hub

Usage:
    from aigie.agents import GoalTracker, Goal

    # Create a goal tracker
    tracker = GoalTracker(
        goal="Book travel to Paris",
        expected_steps=["search_flights", "compare_prices", "book_ticket"],
    )

    # Track step completion
    tracker.mark_step_complete("search_flights")
    tracker.mark_step_complete("compare_prices")

    # Get reliability metrics
    metrics = tracker.get_metrics()
    print(f"Plan adherence: {metrics['plan_adherence_score']:.2%}")

Signal Hub Integration:
    When goal deviations are detected, GOAL_DEVIATION signals are
    emitted to the backend Signal Hub for correlation with other signals.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..signals import SignalReporter


class StepStatus(str, Enum):
    """Status of a plan step."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    FAILED = "failed"


class DeviationType(str, Enum):
    """Type of deviation from the plan."""

    UNEXPECTED_STEP = "unexpected_step"  # Step not in plan
    MISSING_STEP = "missing_step"  # Expected step not executed
    WRONG_ORDER = "wrong_order"  # Steps executed out of order
    REPEATED_STEP = "repeated_step"  # Step executed multiple times


@dataclass
class Step:
    """Represents a step in the execution plan."""

    name: str
    status: StepStatus = StepStatus.PENDING
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_ms: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def start(self) -> None:
        """Mark step as started."""
        self.status = StepStatus.IN_PROGRESS
        self.started_at = datetime.utcnow()

    def complete(self, error: str | None = None) -> None:
        """Mark step as completed."""
        self.completed_at = datetime.utcnow()
        if error:
            self.status = StepStatus.FAILED
            self.error = error
        else:
            self.status = StepStatus.COMPLETED

        if self.started_at:
            self.duration_ms = (self.completed_at - self.started_at).total_seconds() * 1000


@dataclass
class Deviation:
    """Represents a deviation from the plan."""

    type: DeviationType
    step_name: str
    expected_position: int | None = None
    actual_position: int | None = None
    message: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Goal:
    """Represents a hierarchical goal with sub-goals."""

    name: str
    description: str = ""
    expected_steps: list[str] = field(default_factory=list)
    sub_goals: list["Goal"] = field(default_factory=list)
    parent: Optional["Goal"] = None
    achieved: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_sub_goal(self, sub_goal: "Goal") -> "Goal":
        """Add a sub-goal to this goal."""
        sub_goal.parent = self
        self.sub_goals.append(sub_goal)
        return sub_goal


@dataclass
class PlanMetrics:
    """Metrics for plan execution."""

    plan_adherence_score: float  # 0.0-1.0 - how well agent followed plan
    step_completion_rate: float  # completed / expected
    deviation_count: int  # number of deviations
    goal_achieved: bool  # was the main goal achieved
    expected_steps: int  # number of expected steps
    completed_steps: int  # number of completed steps
    unexpected_steps: int  # number of unexpected steps
    missing_steps: int  # number of missing steps
    execution_order_score: float  # 0.0-1.0 - how well order was followed
    total_duration_ms: float  # total execution time


class GoalTracker:
    """
    Tracks goal and plan adherence for AI agent execution.

    Measures reliability by tracking how well an agent follows
    its intended execution plan.
    """

    def __init__(
        self,
        goal: str | None = None,
        expected_steps: list[str] | None = None,
        system_prompt: str | None = None,
        strict_order: bool = False,
        allow_repeats: bool = False,
        signal_reporter: Optional["SignalReporter"] = None,
        trace_id: str | None = None,
    ):
        """
        Initialize the goal tracker.

        Args:
            goal: Main goal description
            expected_steps: List of expected step names in order
            system_prompt: System prompt for context
            strict_order: Whether steps must be executed in order
            allow_repeats: Whether steps can be executed multiple times
            signal_reporter: Optional signal reporter for emitting to Signal Hub
            trace_id: Optional trace ID for signal context
        """
        self.goal = Goal(name=goal or "Unnamed Goal")
        self.system_prompt = system_prompt
        self.strict_order = strict_order
        self.allow_repeats = allow_repeats
        self._signal_reporter = signal_reporter
        self._trace_id = trace_id

        # Step tracking
        self._expected_steps: dict[str, Step] = {}
        self._execution_order: list[str] = []
        self._unexpected_steps: list[str] = []
        self._deviations: list[Deviation] = []

        # Initialize expected steps
        if expected_steps:
            self.set_expected_steps(expected_steps)

        self._started_at: datetime | None = None
        self._completed_at: datetime | None = None

    def set_signal_reporter(self, reporter: "SignalReporter", trace_id: str | None = None) -> None:
        """Set the signal reporter for emitting deviation signals to Signal Hub."""
        self._signal_reporter = reporter
        if trace_id:
            self._trace_id = trace_id

    def set_trace_id(self, trace_id: str) -> None:
        """Set the trace ID for signal context."""
        self._trace_id = trace_id

    def set_plan(
        self,
        goal: str,
        expected_steps: list[str],
        system_prompt: str | None = None,
    ) -> None:
        """
        Set the execution plan.

        Args:
            goal: Goal description
            expected_steps: List of expected step names
            system_prompt: Optional system prompt
        """
        self.goal = Goal(name=goal)
        self.system_prompt = system_prompt
        self.set_expected_steps(expected_steps)
        self._started_at = datetime.utcnow()

    def set_expected_steps(self, steps: list[str]) -> None:
        """Set the expected steps for this plan."""
        self.goal.expected_steps = steps
        self._expected_steps = {name: Step(name=name) for name in steps}

    def mark_step_started(self, step_name: str) -> Step:
        """
        Mark a step as started.

        Args:
            step_name: Name of the step

        Returns:
            The Step object
        """
        if not self._started_at:
            self._started_at = datetime.utcnow()

        if step_name in self._expected_steps:
            step = self._expected_steps[step_name]
            step.start()
            return step
        # Track unexpected step
        self._record_unexpected_step(step_name)
        step = Step(name=step_name)
        step.start()
        return step

    def mark_step_complete(
        self,
        step_name: str,
        error: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Step:
        """
        Mark a step as completed.

        Args:
            step_name: Name of the step
            error: Optional error message if step failed
            metadata: Optional metadata for the step

        Returns:
            The Step object
        """
        if not self._started_at:
            self._started_at = datetime.utcnow()

        step: Step
        if step_name in self._expected_steps:
            step = self._expected_steps[step_name]

            # Check for repeated execution
            if step_name in self._execution_order and not self.allow_repeats:
                self._deviations.append(
                    Deviation(
                        type=DeviationType.REPEATED_STEP,
                        step_name=step_name,
                        message=f"Step '{step_name}' executed multiple times",
                    )
                )
        else:
            # Create step for unexpected execution
            self._record_unexpected_step(step_name)
            step = Step(name=step_name)

        # Start if not already started
        if step.status == StepStatus.PENDING:
            step.start()

        step.complete(error=error)
        if metadata:
            step.metadata.update(metadata)

        # Track execution order
        self._execution_order.append(step_name)

        # Check order if strict
        if self.strict_order and step_name in self._expected_steps:
            self._check_order_deviation(step_name)

        return step

    def _record_unexpected_step(self, step_name: str) -> None:
        """Record an unexpected step."""
        if step_name not in self._unexpected_steps:
            self._unexpected_steps.append(step_name)
            deviation = Deviation(
                type=DeviationType.UNEXPECTED_STEP,
                step_name=step_name,
                actual_position=len(self._execution_order),
                message=f"Unexpected step '{step_name}' executed",
            )
            self._deviations.append(deviation)
            # Emit signal for deviation
            self._emit_deviation_signal(deviation)

    def _check_order_deviation(self, step_name: str) -> None:
        """Check if a step was executed out of order."""
        expected_order = list(self._expected_steps.keys())
        expected_position = expected_order.index(step_name)

        # Get actual position among expected steps only
        executed_expected = [s for s in self._execution_order if s in expected_order]
        if step_name in executed_expected:
            actual_position = len(executed_expected) - 1

            if actual_position != expected_position:
                # Check if there are unexecuted steps that should have come before
                for i in range(expected_position):
                    prev_step = expected_order[i]
                    if prev_step not in executed_expected[:-1]:  # Not yet executed
                        deviation = Deviation(
                            type=DeviationType.WRONG_ORDER,
                            step_name=step_name,
                            expected_position=expected_position,
                            actual_position=actual_position,
                            message=f"Step '{step_name}' executed before '{prev_step}'",
                        )
                        self._deviations.append(deviation)
                        # Emit signal for deviation
                        self._emit_deviation_signal(deviation)
                        break

    def _emit_deviation_signal(self, deviation: Deviation) -> None:
        """Emit a goal deviation signal to the Signal Hub."""
        if not self._signal_reporter or not self._trace_id:
            return

        try:
            import asyncio

            # Get or create event loop
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            # Calculate current metrics
            metrics = self.get_metrics()

            # Determine expected vs actual
            expected = f"Goal: {self.goal.name}, Steps: {list(self._expected_steps.keys())}"
            actual = f"Deviation: {deviation.message}"

            if loop is not None:
                # Running in async context
                asyncio.create_task(
                    self._signal_reporter.report_goal_deviation(
                        trace_id=self._trace_id,
                        expected=expected,
                        actual=actual,
                        adherence_score=metrics.plan_adherence_score,
                        missing_steps=[
                            s
                            for s, step in self._expected_steps.items()
                            if step.status == StepStatus.PENDING
                        ],
                        unexpected_steps=self._unexpected_steps,
                        metadata={
                            "deviation_type": deviation.type.value,
                            "step_name": deviation.step_name,
                            "total_deviations": len(self._deviations),
                        },
                    )
                )
            else:
                # Not in async context
                asyncio.run(
                    self._signal_reporter.report_goal_deviation(
                        trace_id=self._trace_id,
                        expected=expected,
                        actual=actual,
                        adherence_score=metrics.plan_adherence_score,
                        missing_steps=[
                            s
                            for s, step in self._expected_steps.items()
                            if step.status == StepStatus.PENDING
                        ],
                        unexpected_steps=self._unexpected_steps,
                        metadata={
                            "deviation_type": deviation.type.value,
                            "step_name": deviation.step_name,
                            "total_deviations": len(self._deviations),
                        },
                    )
                )
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.debug(f"Failed to emit goal deviation signal: {e}")

    def mark_goal_achieved(self, achieved: bool = True) -> None:
        """Mark whether the main goal was achieved."""
        self.goal.achieved = achieved
        self._completed_at = datetime.utcnow()

    def get_metrics(self) -> PlanMetrics:
        """
        Calculate and return plan adherence metrics.

        Returns:
            PlanMetrics with all calculated scores
        """
        expected_steps = len(self._expected_steps)
        completed_steps = sum(
            1 for step in self._expected_steps.values() if step.status == StepStatus.COMPLETED
        )
        unexpected_steps = len(self._unexpected_steps)

        # Calculate step completion rate
        step_completion_rate = completed_steps / expected_steps if expected_steps > 0 else 1.0

        # Calculate missing steps
        missing_steps = expected_steps - completed_steps

        # Calculate execution order score
        execution_order_score = self._calculate_order_score()

        # Calculate overall plan adherence score
        # Weighted combination of completion, order, and deviation penalty
        completion_weight = 0.5
        order_weight = 0.3
        deviation_weight = 0.2

        deviation_penalty = min(1.0, len(self._deviations) * 0.1)

        plan_adherence_score = (
            step_completion_rate * completion_weight
            + execution_order_score * order_weight
            + (1.0 - deviation_penalty) * deviation_weight
        )

        # Calculate total duration
        total_duration_ms = 0.0
        for step in self._expected_steps.values():
            if step.duration_ms:
                total_duration_ms += step.duration_ms

        return PlanMetrics(
            plan_adherence_score=plan_adherence_score,
            step_completion_rate=step_completion_rate,
            deviation_count=len(self._deviations),
            goal_achieved=self.goal.achieved,
            expected_steps=expected_steps,
            completed_steps=completed_steps,
            unexpected_steps=unexpected_steps,
            missing_steps=missing_steps,
            execution_order_score=execution_order_score,
            total_duration_ms=total_duration_ms,
        )

    def _calculate_order_score(self) -> float:
        """Calculate how well the execution order matches expected order."""
        if not self._expected_steps:
            return 1.0

        expected_order = list(self._expected_steps.keys())
        executed_expected = [s for s in self._execution_order if s in expected_order]

        if not executed_expected:
            return 1.0  # No steps executed yet

        # Calculate longest common subsequence ratio
        lcs_length = self._lcs_length(expected_order, executed_expected)
        return lcs_length / len(expected_order)

    def _lcs_length(self, seq1: list[str], seq2: list[str]) -> int:
        """Calculate length of longest common subsequence."""
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i - 1] == seq2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]

    def get_deviations(self) -> list[Deviation]:
        """Get all recorded deviations."""
        return self._deviations.copy()

    def get_step_status(self, step_name: str) -> StepStatus | None:
        """Get the status of a specific step."""
        if step_name in self._expected_steps:
            return self._expected_steps[step_name].status
        return None

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of the goal tracking state."""
        metrics = self.get_metrics()
        return {
            "goal": self.goal.name,
            "goal_achieved": self.goal.achieved,
            "expected_steps": list(self._expected_steps.keys()),
            "execution_order": self._execution_order,
            "unexpected_steps": self._unexpected_steps,
            "metrics": {
                "plan_adherence_score": metrics.plan_adherence_score,
                "step_completion_rate": metrics.step_completion_rate,
                "deviation_count": metrics.deviation_count,
                "execution_order_score": metrics.execution_order_score,
            },
            "deviations": [
                {
                    "type": d.type.value,
                    "step": d.step_name,
                    "message": d.message,
                }
                for d in self._deviations
            ],
        }


class TracingGoalTracker(GoalTracker):
    """
    Goal tracker that integrates with Aigie tracing.

    Creates spans for goal tracking events and reports
    metrics to the trace.
    """

    def __init__(
        self,
        trace_context: Any = None,
        **kwargs,
    ):
        """
        Initialize with tracing integration.

        Args:
            trace_context: TraceContext to use for creating spans
            **kwargs: Arguments passed to GoalTracker
        """
        super().__init__(**kwargs)
        self._trace_context = trace_context

    def attach_to_trace(self, trace_context: Any) -> "TracingGoalTracker":
        """
        Attach this tracker to a trace context.

        Args:
            trace_context: TraceContext to attach to

        Returns:
            Self for method chaining
        """
        self._trace_context = trace_context
        return self

    async def mark_step_complete_async(
        self,
        step_name: str,
        error: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Step:
        """
        Async version of mark_step_complete with tracing support.

        Creates a span for the step completion.
        """
        step = self.mark_step_complete(step_name, error, metadata)

        # Create span if we have a trace context
        if self._trace_context:
            try:
                metrics = self.get_metrics()
                async with self._trace_context.span(
                    name=f"goal_step:{step_name}",
                    type="checkpoint",
                ) as span:
                    span.set_input({"step_name": step_name})
                    span.set_output(
                        {
                            "status": step.status.value,
                            "duration_ms": step.duration_ms,
                            "plan_adherence": metrics.plan_adherence_score,
                            "completion_rate": metrics.step_completion_rate,
                        }
                    )
                    if error:
                        span.set_error(error)
                    if metadata:
                        span.set_metadata(metadata)
            except Exception:
                pass  # Don't fail on tracing errors

        return step

    async def finalize_async(self) -> PlanMetrics:
        """
        Finalize tracking and report metrics to trace.

        Returns:
            Final PlanMetrics
        """
        metrics = self.get_metrics()

        if self._trace_context:
            try:
                async with self._trace_context.span(
                    name="goal_tracking_summary",
                    type="evaluator",
                ) as span:
                    span.set_input({"goal": self.goal.name})
                    span.set_output(
                        {
                            "plan_adherence_score": metrics.plan_adherence_score,
                            "step_completion_rate": metrics.step_completion_rate,
                            "goal_achieved": metrics.goal_achieved,
                            "deviation_count": metrics.deviation_count,
                            "expected_steps": metrics.expected_steps,
                            "completed_steps": metrics.completed_steps,
                            "missing_steps": metrics.missing_steps,
                            "unexpected_steps": metrics.unexpected_steps,
                        }
                    )
                    span.set_metadata(
                        {
                            "execution_order": self._execution_order,
                            "deviations": [d.message for d in self._deviations],
                        }
                    )
            except Exception:
                pass  # Don't fail on tracing errors

        return metrics
