"""
Execution Cycle for AI Agents (Think-Act-Observe Pattern).

This module provides structured execution phases for AI agents,
enabling better observability and drift detection at each phase.

The Think-Act-Observe pattern decomposes agent execution into:
- Think: Reasoning and planning phase
- Act: Tool execution and action phase
- Observe: Result evaluation and observation phase

This structure enables:
- Better drift detection (compare actual vs expected at each phase)
- Clearer debugging (see exactly where agent went wrong)
- More precise auto-fix (know which phase to retry)
- Signal emission to backend Signal Hub

Usage:
    from aigie.agents import ExecutionCycle

    async with aigie.trace("agent_run") as trace:
        cycle = ExecutionCycle(trace)

        async with cycle.think() as thought:
            plan = agent.plan(query)
            thought.set_output(plan)

        async with cycle.act() as action:
            result = await agent.execute_tools(plan)
            action.set_output(result)

        async with cycle.observe() as observation:
            evaluation = agent.evaluate(result)
            observation.set_output(evaluation)

Signal Hub Integration:
    When drift is detected during execution cycles, CONTEXT_DRIFT
    signals are emitted to the backend Signal Hub for correlation.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..signals import SignalReporter


class CyclePhase(str, Enum):
    """Phase of the execution cycle."""

    THINK = "think"  # Reasoning/planning phase
    ACT = "act"  # Action/execution phase
    OBSERVE = "observe"  # Observation/evaluation phase
    REFLECT = "reflect"  # Optional reflection phase


@dataclass
class PhaseResult:
    """Result of an execution phase."""

    phase: CyclePhase
    input: Any | None = None
    output: Any | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_ms: float | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    drift_detected: bool = False
    drift_score: float = 0.0

    def set_output(self, output: Any) -> None:
        """Set the phase output."""
        self.output = output

    def set_error(self, error: str) -> None:
        """Set an error for this phase."""
        self.error = error

    def set_metadata(self, metadata: dict[str, Any]) -> None:
        """Set metadata for this phase."""
        self.metadata.update(metadata)


@dataclass
class CycleMetrics:
    """Metrics for an execution cycle."""

    cycle_number: int
    total_duration_ms: float
    think_duration_ms: float
    act_duration_ms: float
    observe_duration_ms: float
    phases_completed: int
    errors: list[str]
    drift_detected: bool
    overall_drift_score: float


class PhaseContext:
    """
    Context manager for a single execution phase.

    Provides a clean interface for tracking phase execution
    and integrating with Aigie tracing.
    """

    def __init__(
        self,
        phase: CyclePhase,
        trace_context: Any = None,
        span_type: str = "agent",
        expected_output: Any | None = None,
    ):
        """
        Initialize phase context.

        Args:
            phase: The phase type
            trace_context: TraceContext for creating spans
            span_type: Span type to use for tracing
            expected_output: Optional expected output for drift detection
        """
        self.phase = phase
        self._trace_context = trace_context
        self._span_type = span_type
        self._expected_output = expected_output
        self._result = PhaseResult(phase=phase)
        self._span = None

    @property
    def result(self) -> PhaseResult:
        """Get the phase result."""
        return self._result

    async def __aenter__(self) -> "PhaseContext":
        """Enter the phase context."""
        self._result.started_at = datetime.utcnow()

        # Create span if we have trace context
        if self._trace_context:
            self._span = self._trace_context.span(
                name=f"phase:{self.phase.value}",
                type=self._span_type,
            )
            await self._span.__aenter__()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the phase context."""
        self._result.completed_at = datetime.utcnow()

        if self._result.started_at:
            self._result.duration_ms = (
                self._result.completed_at - self._result.started_at
            ).total_seconds() * 1000

        if exc_val:
            self._result.error = str(exc_val)

        # Check for drift if we have expected output
        if self._expected_output is not None and self._result.output is not None:
            self._check_drift()

        # Complete span if we have one
        if self._span:
            try:
                self._span.set_input(self._result.input)
                self._span.set_output(self._result.output)
                if self._result.error:
                    self._span.set_metadata({"error": self._result.error})
                if self._result.drift_detected:
                    self._span.set_metadata(
                        {
                            "drift_detected": True,
                            "drift_score": self._result.drift_score,
                        }
                    )
            except Exception:
                pass  # Don't fail on span errors

            await self._span.__aexit__(exc_type, exc_val, exc_tb)

    def set_input(self, input: Any) -> None:
        """Set the phase input."""
        self._result.input = input

    def set_output(self, output: Any) -> None:
        """Set the phase output."""
        self._result.output = output

    def set_error(self, error: str) -> None:
        """Set an error for this phase."""
        self._result.error = error

    def set_metadata(self, metadata: dict[str, Any]) -> None:
        """Set metadata for this phase."""
        self._result.metadata.update(metadata)

    def _check_drift(self) -> None:
        """Check for drift between expected and actual output."""
        # Simple drift check - can be extended with more sophisticated comparison
        if self._expected_output != self._result.output:
            self._result.drift_detected = True
            # Calculate simple drift score based on type matching
            if type(self._expected_output) != type(self._result.output):
                self._result.drift_score = 1.0
            else:
                self._result.drift_score = 0.5


class ExecutionCycle:
    """
    Manages the Think-Act-Observe execution cycle for agents.

    Provides structured phase management and integrates with
    Aigie tracing for observability.
    """

    def __init__(
        self,
        trace_context: Any = None,
        cycle_number: int = 1,
        expected_phases: dict[CyclePhase, Any] | None = None,
        signal_reporter: Optional["SignalReporter"] = None,
        trace_id: str | None = None,
    ):
        """
        Initialize the execution cycle.

        Args:
            trace_context: TraceContext for creating spans
            cycle_number: Cycle number (for multi-cycle agents)
            expected_phases: Optional expected outputs per phase for drift detection
            signal_reporter: Optional signal reporter for emitting to Signal Hub
            trace_id: Optional trace ID for signal context
        """
        self._trace_context = trace_context
        self._cycle_number = cycle_number
        self._expected_phases = expected_phases or {}
        self._phases: dict[CyclePhase, PhaseResult] = {}
        self._current_phase: CyclePhase | None = None
        self._started_at: datetime | None = None
        self._completed_at: datetime | None = None
        self._signal_reporter = signal_reporter
        self._trace_id = trace_id

    def set_signal_reporter(self, reporter: "SignalReporter", trace_id: str | None = None) -> None:
        """Set the signal reporter for emitting drift signals to Signal Hub."""
        self._signal_reporter = reporter
        if trace_id:
            self._trace_id = trace_id

    def set_trace_id(self, trace_id: str) -> None:
        """Set the trace ID for signal context."""
        self._trace_id = trace_id

    @property
    def cycle_number(self) -> int:
        """Get the cycle number."""
        return self._cycle_number

    @property
    def phases(self) -> dict[CyclePhase, PhaseResult]:
        """Get all phase results."""
        return self._phases.copy()

    @property
    def current_phase(self) -> CyclePhase | None:
        """Get the current active phase."""
        return self._current_phase

    def _get_span_type(self, phase: CyclePhase) -> str:
        """Get the span type for a phase."""
        span_types = {
            CyclePhase.THINK: "reasoning",
            CyclePhase.ACT: "tool",
            CyclePhase.OBSERVE: "observation",
            CyclePhase.REFLECT: "evaluator",
        }
        return span_types.get(phase, "agent")

    @asynccontextmanager
    async def think(
        self,
        expected_output: Any | None = None,
    ) -> AsyncIterator[PhaseContext]:
        """
        Enter the Think phase.

        The Think phase is for reasoning and planning.

        Args:
            expected_output: Optional expected output for drift detection

        Yields:
            PhaseContext for the Think phase
        """
        if self._started_at is None:
            self._started_at = datetime.utcnow()

        expected = expected_output or self._expected_phases.get(CyclePhase.THINK)
        phase_ctx = PhaseContext(
            phase=CyclePhase.THINK,
            trace_context=self._trace_context,
            span_type=self._get_span_type(CyclePhase.THINK),
            expected_output=expected,
        )

        self._current_phase = CyclePhase.THINK

        async with phase_ctx:
            yield phase_ctx

        self._phases[CyclePhase.THINK] = phase_ctx.result
        self._current_phase = None

    @asynccontextmanager
    async def act(
        self,
        expected_output: Any | None = None,
    ) -> AsyncIterator[PhaseContext]:
        """
        Enter the Act phase.

        The Act phase is for executing tools and actions.

        Args:
            expected_output: Optional expected output for drift detection

        Yields:
            PhaseContext for the Act phase
        """
        if self._started_at is None:
            self._started_at = datetime.utcnow()

        expected = expected_output or self._expected_phases.get(CyclePhase.ACT)
        phase_ctx = PhaseContext(
            phase=CyclePhase.ACT,
            trace_context=self._trace_context,
            span_type=self._get_span_type(CyclePhase.ACT),
            expected_output=expected,
        )

        self._current_phase = CyclePhase.ACT

        async with phase_ctx:
            yield phase_ctx

        self._phases[CyclePhase.ACT] = phase_ctx.result
        self._current_phase = None

    @asynccontextmanager
    async def observe(
        self,
        expected_output: Any | None = None,
    ) -> AsyncIterator[PhaseContext]:
        """
        Enter the Observe phase.

        The Observe phase is for evaluating results.

        Args:
            expected_output: Optional expected output for drift detection

        Yields:
            PhaseContext for the Observe phase
        """
        expected = expected_output or self._expected_phases.get(CyclePhase.OBSERVE)
        phase_ctx = PhaseContext(
            phase=CyclePhase.OBSERVE,
            trace_context=self._trace_context,
            span_type=self._get_span_type(CyclePhase.OBSERVE),
            expected_output=expected,
        )

        self._current_phase = CyclePhase.OBSERVE

        async with phase_ctx:
            yield phase_ctx

        self._phases[CyclePhase.OBSERVE] = phase_ctx.result
        self._completed_at = datetime.utcnow()
        self._current_phase = None

    @asynccontextmanager
    async def reflect(
        self,
        expected_output: Any | None = None,
    ) -> AsyncIterator[PhaseContext]:
        """
        Enter the optional Reflect phase.

        The Reflect phase is for meta-cognition and learning.

        Args:
            expected_output: Optional expected output for drift detection

        Yields:
            PhaseContext for the Reflect phase
        """
        expected = expected_output or self._expected_phases.get(CyclePhase.REFLECT)
        phase_ctx = PhaseContext(
            phase=CyclePhase.REFLECT,
            trace_context=self._trace_context,
            span_type=self._get_span_type(CyclePhase.REFLECT),
            expected_output=expected,
        )

        self._current_phase = CyclePhase.REFLECT

        async with phase_ctx:
            yield phase_ctx

        self._phases[CyclePhase.REFLECT] = phase_ctx.result
        self._current_phase = None

    def get_metrics(self) -> CycleMetrics:
        """
        Get metrics for this execution cycle.

        Returns:
            CycleMetrics with timing and drift information
        """
        total_duration = 0.0
        think_duration = 0.0
        act_duration = 0.0
        observe_duration = 0.0
        errors = []
        drift_detected = False
        drift_scores = []

        for phase, result in self._phases.items():
            duration = result.duration_ms or 0.0
            total_duration += duration

            if phase == CyclePhase.THINK:
                think_duration = duration
            elif phase == CyclePhase.ACT:
                act_duration = duration
            elif phase == CyclePhase.OBSERVE:
                observe_duration = duration

            if result.error:
                errors.append(f"{phase.value}: {result.error}")

            if result.drift_detected:
                drift_detected = True
                drift_scores.append(result.drift_score)
                # Emit drift signal
                self._emit_drift_signal(phase, result)

        overall_drift = sum(drift_scores) / len(drift_scores) if drift_scores else 0.0

        return CycleMetrics(
            cycle_number=self._cycle_number,
            total_duration_ms=total_duration,
            think_duration_ms=think_duration,
            act_duration_ms=act_duration,
            observe_duration_ms=observe_duration,
            phases_completed=len(self._phases),
            errors=errors,
            drift_detected=drift_detected,
            overall_drift_score=overall_drift,
        )

    def _emit_drift_signal(self, phase: CyclePhase, result: PhaseResult) -> None:
        """Emit a drift signal to the Signal Hub."""
        if not self._signal_reporter or not self._trace_id:
            return

        try:
            import asyncio

            # Get or create event loop
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            # Map phase to drift type
            drift_type_map = {
                CyclePhase.THINK: "behavioral",
                CyclePhase.ACT: "structural",
                CyclePhase.OBSERVE: "semantic",
                CyclePhase.REFLECT: "behavioral",
            }
            drift_type = drift_type_map.get(phase, "behavioral")

            if loop is not None:
                asyncio.create_task(
                    self._signal_reporter.report_drift(
                        trace_id=self._trace_id,
                        drift_type=drift_type,
                        score=result.drift_score,
                        details={
                            "phase": phase.value,
                            "cycle_number": self._cycle_number,
                            "duration_ms": result.duration_ms,
                            "has_error": result.error is not None,
                        },
                        metadata={
                            "source": "execution_cycle",
                            "phase_type": phase.value,
                        },
                    )
                )
            else:
                asyncio.run(
                    self._signal_reporter.report_drift(
                        trace_id=self._trace_id,
                        drift_type=drift_type,
                        score=result.drift_score,
                        details={
                            "phase": phase.value,
                            "cycle_number": self._cycle_number,
                            "duration_ms": result.duration_ms,
                            "has_error": result.error is not None,
                        },
                        metadata={
                            "source": "execution_cycle",
                            "phase_type": phase.value,
                        },
                    )
                )
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.debug(f"Failed to emit drift signal: {e}")

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of the cycle execution."""
        metrics = self.get_metrics()
        return {
            "cycle_number": self._cycle_number,
            "phases": {
                phase.value: {
                    "duration_ms": result.duration_ms,
                    "has_output": result.output is not None,
                    "has_error": result.error is not None,
                    "drift_detected": result.drift_detected,
                    "drift_score": result.drift_score,
                }
                for phase, result in self._phases.items()
            },
            "metrics": {
                "total_duration_ms": metrics.total_duration_ms,
                "phases_completed": metrics.phases_completed,
                "drift_detected": metrics.drift_detected,
                "overall_drift_score": metrics.overall_drift_score,
            },
            "errors": metrics.errors,
        }


class MultiCycleExecutor:
    """
    Manages multiple execution cycles for iterative agents.

    Useful for agents that go through multiple Think-Act-Observe
    cycles before completing a task.
    """

    def __init__(
        self,
        trace_context: Any = None,
        max_cycles: int = 10,
        on_cycle_complete: callable | None = None,
    ):
        """
        Initialize the multi-cycle executor.

        Args:
            trace_context: TraceContext for creating spans
            max_cycles: Maximum number of cycles allowed
            on_cycle_complete: Callback after each cycle completes
        """
        self._trace_context = trace_context
        self._max_cycles = max_cycles
        self._on_cycle_complete = on_cycle_complete
        self._cycles: list[ExecutionCycle] = []
        self._current_cycle: ExecutionCycle | None = None

    @property
    def cycles(self) -> list[ExecutionCycle]:
        """Get all completed cycles."""
        return self._cycles.copy()

    @property
    def cycle_count(self) -> int:
        """Get the number of completed cycles."""
        return len(self._cycles)

    def new_cycle(
        self,
        expected_phases: dict[CyclePhase, Any] | None = None,
    ) -> ExecutionCycle:
        """
        Start a new execution cycle.

        Args:
            expected_phases: Optional expected outputs per phase

        Returns:
            New ExecutionCycle

        Raises:
            RuntimeError: If max cycles exceeded
        """
        if len(self._cycles) >= self._max_cycles:
            raise RuntimeError(
                f"Maximum cycles ({self._max_cycles}) exceeded. Agent may be stuck in a loop."
            )

        cycle = ExecutionCycle(
            trace_context=self._trace_context,
            cycle_number=len(self._cycles) + 1,
            expected_phases=expected_phases,
        )

        self._current_cycle = cycle
        return cycle

    def complete_cycle(self) -> CycleMetrics:
        """
        Complete the current cycle.

        Returns:
            Metrics for the completed cycle
        """
        if self._current_cycle is None:
            raise RuntimeError("No active cycle to complete")

        metrics = self._current_cycle.get_metrics()
        self._cycles.append(self._current_cycle)

        if self._on_cycle_complete:
            self._on_cycle_complete(self._current_cycle, metrics)

        self._current_cycle = None
        return metrics

    def get_overall_metrics(self) -> dict[str, Any]:
        """Get aggregated metrics across all cycles."""
        if not self._cycles:
            return {
                "total_cycles": 0,
                "total_duration_ms": 0.0,
                "average_cycle_duration_ms": 0.0,
                "total_errors": 0,
                "drift_detected": False,
            }

        total_duration = sum(c.get_metrics().total_duration_ms for c in self._cycles)
        total_errors = sum(len(c.get_metrics().errors) for c in self._cycles)
        drift_detected = any(c.get_metrics().drift_detected for c in self._cycles)

        return {
            "total_cycles": len(self._cycles),
            "total_duration_ms": total_duration,
            "average_cycle_duration_ms": total_duration / len(self._cycles),
            "total_errors": total_errors,
            "drift_detected": drift_detected,
            "cycles": [c.get_summary() for c in self._cycles],
        }
