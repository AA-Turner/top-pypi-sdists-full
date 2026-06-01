"""
Unified Signal Reporter - Backend Signal Hub Integration.

This module provides a unified signal reporting interface for the SDK
to communicate with the backend's Signal Hub. It consolidates signals
from various detectors into a common format.

Signal Types:
- ERROR_CLUSTER: Grouped error patterns
- CONTEXT_DRIFT: Semantic/structural/behavioral drift
- TOOL_LOOP: Repetitive tool call patterns
- GOAL_DEVIATION: Deviation from expected plan

Integration:
The backend Signal Hub correlates signals from multiple sources to
identify complex issues and trigger appropriate responses.

Usage:
    from aigie import SignalReporter, SignalType, SignalSeverity

    # Initialize signal reporter
    reporter = SignalReporter(api_url=api_url, api_key=api_key)

    # Report a loop detection signal
    await reporter.report_loop(
        trace_id="trace_123",
        pattern="search_api",
        count=5,
        severity=SignalSeverity.HIGH,
    )

    # Report drift detection
    await reporter.report_drift(
        trace_id="trace_123",
        drift_type="semantic",
        score=0.75,
        details={"topic_shift": "finance -> cooking"},
    )
"""

import asyncio
import contextlib
import logging
import time
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger("aigie.signals")


class SignalType(str, Enum):
    """Types of signals that can be reported."""

    ERROR_CLUSTER = "error_cluster"  # Grouped error patterns
    CONTEXT_DRIFT = "context_drift"  # Semantic/structural/behavioral drift
    TOOL_LOOP = "tool_loop"  # Repetitive tool call patterns
    GOAL_DEVIATION = "goal_deviation"  # Deviation from expected plan
    HALLUCINATION = "hallucination"  # Potential hallucination detected
    QUALITY_DROP = "quality_drop"  # Output quality degradation
    LATENCY_SPIKE = "latency_spike"  # Unusual latency increase
    TOKEN_OVERFLOW = "token_overflow"  # Context window issues
    SAFETY_VIOLATION = "safety_violation"  # Safety/policy violations
    CUSTOM = "custom"  # Custom user-defined signal


class SignalSeverity(str, Enum):
    """Severity levels for signals."""

    LOW = "low"  # Informational, no action needed
    MEDIUM = "medium"  # Worth monitoring
    HIGH = "high"  # Requires attention
    CRITICAL = "critical"  # Immediate action required


class DriftType(str, Enum):
    """Types of context drift."""

    SEMANTIC = "semantic"  # Topic/meaning drift
    STRUCTURAL = "structural"  # Response format drift
    BEHAVIORAL = "behavioral"  # Agent behavior drift
    TEMPORAL = "temporal"  # Time-based drift


@dataclass
class Signal:
    """Represents a signal to be reported to the Signal Hub."""

    signal_id: str
    signal_type: SignalType
    severity: SignalSeverity
    trace_id: str

    # Context
    span_id: str | None = None
    workflow_id: str | None = None

    # Signal data
    title: str = ""
    description: str = ""
    score: float = 0.0  # 0.0 - 1.0, where 1.0 is most severe
    count: int = 1  # For counting occurrences

    # Details
    details: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)

    # Correlation
    correlation_id: str | None = None
    related_signals: list[str] = field(default_factory=list)

    # Timestamps
    timestamp: datetime = field(default_factory=datetime.utcnow)
    detected_at: datetime | None = None

    # Status
    acknowledged: bool = False
    resolved: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert signal to dictionary for transmission."""
        return {
            "signal_id": self.signal_id,
            "signal_type": self.signal_type.value,
            "severity": self.severity.value,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "workflow_id": self.workflow_id,
            "title": self.title,
            "description": self.description,
            "score": self.score,
            "count": self.count,
            "details": self.details,
            "metadata": self.metadata,
            "tags": self.tags,
            "correlation_id": self.correlation_id,
            "related_signals": self.related_signals,
            "timestamp": self.timestamp.isoformat(),
            "detected_at": self.detected_at.isoformat() if self.detected_at else None,
            "acknowledged": self.acknowledged,
            "resolved": self.resolved,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Signal":
        """Create signal from dictionary."""

        def parse_datetime(val):
            if not val:
                return None
            if isinstance(val, datetime):
                return val
            try:
                return datetime.fromisoformat(val.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                return None

        return cls(
            signal_id=data.get("signal_id", ""),
            signal_type=SignalType(data.get("signal_type", "custom")),
            severity=SignalSeverity(data.get("severity", "medium")),
            trace_id=data.get("trace_id", ""),
            span_id=data.get("span_id"),
            workflow_id=data.get("workflow_id"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            score=data.get("score", 0.0),
            count=data.get("count", 1),
            details=data.get("details", {}),
            metadata=data.get("metadata", {}),
            tags=data.get("tags", []),
            correlation_id=data.get("correlation_id"),
            related_signals=data.get("related_signals", []),
            timestamp=parse_datetime(data.get("timestamp")) or datetime.utcnow(),
            detected_at=parse_datetime(data.get("detected_at")),
            acknowledged=data.get("acknowledged", False),
            resolved=data.get("resolved", False),
        )


@dataclass
class SignalBatch:
    """A batch of signals for efficient transmission."""

    batch_id: str
    signals: list[Signal]
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "batch_id": self.batch_id,
            "signals": [s.to_dict() for s in self.signals],
            "created_at": self.created_at.isoformat(),
            "count": len(self.signals),
        }


@dataclass
class SignalMetrics:
    """Metrics for signal reporting."""

    signals_reported: int = 0
    signals_by_type: dict[str, int] = field(default_factory=dict)
    signals_by_severity: dict[str, int] = field(default_factory=dict)
    batches_sent: int = 0
    send_failures: int = 0
    total_latency_ms: float = 0.0

    def record_signal(self, signal: Signal):
        """Record a signal for metrics."""
        self.signals_reported += 1

        type_key = signal.signal_type.value
        self.signals_by_type[type_key] = self.signals_by_type.get(type_key, 0) + 1

        severity_key = signal.severity.value
        self.signals_by_severity[severity_key] = self.signals_by_severity.get(severity_key, 0) + 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "signals_reported": self.signals_reported,
            "signals_by_type": self.signals_by_type,
            "signals_by_severity": self.signals_by_severity,
            "batches_sent": self.batches_sent,
            "send_failures": self.send_failures,
            "avg_latency_ms": (
                self.total_latency_ms / self.batches_sent if self.batches_sent > 0 else 0
            ),
        }


class SignalReporter:
    """
    Report unified signals to backend Signal Hub.

    Provides methods for reporting different signal types with
    proper formatting and severity classification. Supports
    batching and async transmission.

    Features:
    - Report errors, drift, loops, and goal deviations
    - Signal batching for efficiency
    - Async transmission to backend
    - Local buffering when backend unavailable
    - Correlation metadata for signal matching
    """

    DEFAULT_BATCH_SIZE = 10
    DEFAULT_BATCH_INTERVAL_SEC = 5.0

    def __init__(
        self,
        api_url: str | None = None,
        api_key: str | None = None,
        *,
        batch_size: int = DEFAULT_BATCH_SIZE,
        batch_interval_sec: float = DEFAULT_BATCH_INTERVAL_SEC,
        auto_batch: bool = True,
        on_signal: Callable[[Signal], Awaitable[None]] | None = None,
    ):
        """
        Initialize the signal reporter.

        Args:
            api_url: Backend API URL
            api_key: API key for authentication
            batch_size: Number of signals per batch
            batch_interval_sec: Max time between batch sends
            auto_batch: Whether to automatically batch signals
            on_signal: Callback when signal is reported
        """
        self._api_url = api_url
        self._api_key = api_key
        self._batch_size = batch_size
        self._batch_interval_sec = batch_interval_sec
        self._auto_batch = auto_batch
        self._on_signal = on_signal

        # Signal buffer
        self._buffer: list[Signal] = []
        self._buffer_lock = asyncio.Lock()

        # Background task
        self._flush_task: asyncio.Task | None = None

        # Metrics
        self._metrics = SignalMetrics()

        # Signal counter
        self._signal_counter = 0

        # Persistent HTTP session (lazily initialized)
        self._session = None

    def _generate_signal_id(self) -> str:
        """Generate a unique signal ID."""
        self._signal_counter += 1
        return f"sig_{self._signal_counter}_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"

    async def report_error(
        self,
        trace_id: str,
        error: Exception | str,
        *,
        span_id: str | None = None,
        severity: SignalSeverity = SignalSeverity.HIGH,
        error_type: str | None = None,
        stack_trace: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Signal:
        """
        Report an error signal.

        Args:
            trace_id: Trace ID where error occurred
            error: The error or error message
            span_id: Optional span ID
            severity: Signal severity
            error_type: Type/category of error
            stack_trace: Optional stack trace
            metadata: Additional metadata

        Returns:
            The created Signal
        """
        error_msg = str(error) if isinstance(error, Exception) else error
        error_class = type(error).__name__ if isinstance(error, Exception) else "Error"

        signal = Signal(
            signal_id=self._generate_signal_id(),
            signal_type=SignalType.ERROR_CLUSTER,
            severity=severity,
            trace_id=trace_id,
            span_id=span_id,
            title=f"{error_class}: {error_msg[:100]}",
            description=error_msg,
            score=self._severity_to_score(severity),
            details={
                "error_type": error_type or error_class,
                "error_message": error_msg,
                "stack_trace": stack_trace,
            },
            metadata=metadata or {},
            tags=["error", error_class.lower()],
            detected_at=datetime.utcnow(),
        )

        await self._report(signal)
        return signal

    async def report_drift(
        self,
        trace_id: str,
        drift_type: str | DriftType,
        score: float,
        *,
        span_id: str | None = None,
        severity: SignalSeverity | None = None,
        expected: str | None = None,
        actual: str | None = None,
        details: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Signal:
        """
        Report a drift detection signal.

        Args:
            trace_id: Trace ID
            drift_type: Type of drift (semantic, structural, behavioral)
            score: Drift score (0.0-1.0, higher = more drift)
            span_id: Optional span ID
            severity: Signal severity (auto-calculated from score if not provided)
            expected: Expected behavior/output
            actual: Actual behavior/output
            details: Additional drift details
            metadata: Additional metadata

        Returns:
            The created Signal
        """
        drift_type_str = drift_type if isinstance(drift_type, str) else drift_type.value

        # Auto-calculate severity from score if not provided
        if severity is None:
            if score >= 0.8:
                severity = SignalSeverity.CRITICAL
            elif score >= 0.6:
                severity = SignalSeverity.HIGH
            elif score >= 0.4:
                severity = SignalSeverity.MEDIUM
            else:
                severity = SignalSeverity.LOW

        signal = Signal(
            signal_id=self._generate_signal_id(),
            signal_type=SignalType.CONTEXT_DRIFT,
            severity=severity,
            trace_id=trace_id,
            span_id=span_id,
            title=f"{drift_type_str.title()} Drift Detected (score: {score:.2f})",
            description=f"Context drift of type '{drift_type_str}' detected with score {score:.2f}",
            score=score,
            details={
                "drift_type": drift_type_str,
                "drift_score": score,
                "expected": expected,
                "actual": actual,
                **(details or {}),
            },
            metadata=metadata or {},
            tags=["drift", drift_type_str],
            detected_at=datetime.utcnow(),
        )

        await self._report(signal)
        return signal

    async def report_loop(
        self,
        trace_id: str,
        pattern: str,
        count: int,
        *,
        span_id: str | None = None,
        severity: SignalSeverity | None = None,
        similarity_score: float = 0.0,
        tool_calls: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Signal:
        """
        Report a tool loop detection signal.

        Args:
            trace_id: Trace ID
            pattern: Pattern or tool name that's looping
            count: Number of loop iterations detected
            span_id: Optional span ID
            severity: Signal severity (auto-calculated from count if not provided)
            similarity_score: Similarity between loop iterations
            tool_calls: List of tool calls in the loop
            metadata: Additional metadata

        Returns:
            The created Signal
        """
        # Auto-calculate severity from count
        if severity is None:
            if count >= 10:
                severity = SignalSeverity.CRITICAL
            elif count >= 5:
                severity = SignalSeverity.HIGH
            elif count >= 3:
                severity = SignalSeverity.MEDIUM
            else:
                severity = SignalSeverity.LOW

        signal = Signal(
            signal_id=self._generate_signal_id(),
            signal_type=SignalType.TOOL_LOOP,
            severity=severity,
            trace_id=trace_id,
            span_id=span_id,
            title=f"Tool Loop Detected: {pattern} ({count}x)",
            description=f"Repetitive pattern '{pattern}' detected {count} times",
            score=min(1.0, count / 10),  # Normalize to 0-1
            count=count,
            details={
                "pattern": pattern,
                "loop_count": count,
                "similarity_score": similarity_score,
                "tool_calls": tool_calls or [],
            },
            metadata=metadata or {},
            tags=["loop", "tool_loop", pattern],
            detected_at=datetime.utcnow(),
        )

        await self._report(signal)
        return signal

    async def report_goal_deviation(
        self,
        trace_id: str,
        expected: str,
        actual: str,
        *,
        span_id: str | None = None,
        severity: SignalSeverity = SignalSeverity.MEDIUM,
        adherence_score: float = 0.0,
        missing_steps: list[str] | None = None,
        unexpected_steps: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Signal:
        """
        Report a goal deviation signal.

        Args:
            trace_id: Trace ID
            expected: Expected goal/behavior
            actual: Actual goal/behavior
            span_id: Optional span ID
            severity: Signal severity
            adherence_score: Plan adherence score (0-1)
            missing_steps: Steps that were expected but not executed
            unexpected_steps: Steps that were executed but not expected
            metadata: Additional metadata

        Returns:
            The created Signal
        """
        signal = Signal(
            signal_id=self._generate_signal_id(),
            signal_type=SignalType.GOAL_DEVIATION,
            severity=severity,
            trace_id=trace_id,
            span_id=span_id,
            title=f"Goal Deviation (adherence: {adherence_score:.0%})",
            description=f"Expected: {expected}\nActual: {actual}",
            score=1.0 - adherence_score,  # Higher score = more deviation
            details={
                "expected_goal": expected,
                "actual_behavior": actual,
                "adherence_score": adherence_score,
                "missing_steps": missing_steps or [],
                "unexpected_steps": unexpected_steps or [],
            },
            metadata=metadata or {},
            tags=["goal_deviation", "plan_adherence"],
            detected_at=datetime.utcnow(),
        )

        await self._report(signal)
        return signal

    async def report_hallucination(
        self,
        trace_id: str,
        content: str,
        confidence: float,
        *,
        span_id: str | None = None,
        severity: SignalSeverity | None = None,
        detection_method: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Signal:
        """
        Report a potential hallucination signal.

        Args:
            trace_id: Trace ID
            content: The potentially hallucinated content
            confidence: Confidence in hallucination detection (0-1)
            span_id: Optional span ID
            severity: Signal severity
            detection_method: Method used to detect hallucination
            metadata: Additional metadata

        Returns:
            The created Signal
        """
        if severity is None:
            if confidence >= 0.8:
                severity = SignalSeverity.HIGH
            elif confidence >= 0.5:
                severity = SignalSeverity.MEDIUM
            else:
                severity = SignalSeverity.LOW

        signal = Signal(
            signal_id=self._generate_signal_id(),
            signal_type=SignalType.HALLUCINATION,
            severity=severity,
            trace_id=trace_id,
            span_id=span_id,
            title=f"Potential Hallucination (confidence: {confidence:.0%})",
            description=f"Potentially fabricated content detected: {content[:200]}...",
            score=confidence,
            details={
                "content": content,
                "detection_confidence": confidence,
                "detection_method": detection_method,
            },
            metadata=metadata or {},
            tags=["hallucination"],
            detected_at=datetime.utcnow(),
        )

        await self._report(signal)
        return signal

    async def report_custom(
        self,
        trace_id: str,
        title: str,
        description: str,
        *,
        span_id: str | None = None,
        severity: SignalSeverity = SignalSeverity.MEDIUM,
        score: float = 0.5,
        details: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Signal:
        """
        Report a custom signal.

        Args:
            trace_id: Trace ID
            title: Signal title
            description: Signal description
            span_id: Optional span ID
            severity: Signal severity
            score: Signal score (0-1)
            details: Signal details
            tags: Signal tags
            metadata: Additional metadata

        Returns:
            The created Signal
        """
        signal = Signal(
            signal_id=self._generate_signal_id(),
            signal_type=SignalType.CUSTOM,
            severity=severity,
            trace_id=trace_id,
            span_id=span_id,
            title=title,
            description=description,
            score=score,
            details=details or {},
            metadata=metadata or {},
            tags=tags or [],
            detected_at=datetime.utcnow(),
        )

        await self._report(signal)
        return signal

    async def _report(self, signal: Signal) -> None:
        """Internal method to report a signal."""
        # Record metrics
        self._metrics.record_signal(signal)

        # Callback
        if self._on_signal:
            try:
                await self._on_signal(signal)
            except Exception as e:
                logger.warning(f"Signal callback error: {e}")

        # Add to buffer
        async with self._buffer_lock:
            self._buffer.append(signal)

            # Flush if batch is full
            if len(self._buffer) >= self._batch_size:
                await self._flush_buffer()

        # Start background flush task if not running
        if self._auto_batch and (self._flush_task is None or self._flush_task.done()):
            self._flush_task = asyncio.create_task(self._background_flush())

    async def _flush_buffer(self) -> None:
        """Flush the signal buffer to backend."""
        if not self._buffer:
            return

        signals_to_send = self._buffer.copy()
        self._buffer.clear()

        if not self._api_url:
            logger.debug(f"No API URL configured, {len(signals_to_send)} signals not sent")
            return

        start_time = time.perf_counter()

        try:
            batch = SignalBatch(
                batch_id=f"batch_{int(time.time() * 1000)}",
                signals=signals_to_send,
            )

            await self._send_batch(batch)

            latency = (time.perf_counter() - start_time) * 1000
            self._metrics.batches_sent += 1
            self._metrics.total_latency_ms += latency

            logger.debug(f"Sent {len(signals_to_send)} signals in {latency:.1f}ms")

        except Exception as e:
            logger.warning(f"Failed to send signal batch: {e}")
            self._metrics.send_failures += 1

            # Put signals back in buffer for retry
            async with self._buffer_lock:
                self._buffer.extend(signals_to_send)

    async def _get_session(self):
        """Get or create persistent HTTP session."""
        if self._session is None:
            try:
                import aiohttp

                self._session = aiohttp.ClientSession(
                    headers={
                        "X-API-Key": self._api_key,
                        "Content-Type": "application/json",
                    },
                    timeout=aiohttp.ClientTimeout(total=10),
                )
            except ImportError:
                logger.debug("aiohttp not installed, cannot send signals to backend")
                return None
        return self._session

    async def _send_batch(self, batch: SignalBatch) -> None:
        """Send a batch of signals to the backend."""
        if not self._api_url or not self._api_key:
            return

        session = await self._get_session()
        if not session:
            return

        async with session.post(
            f"{self._api_url}/v1/signals/batch",
            json=batch.to_dict(),
        ) as response:
            if response.status not in (200, 201, 202):
                text = await response.text()
                raise Exception(f"Backend returned {response.status}: {text}")

    async def _background_flush(self) -> None:
        """Background task to periodically flush signals."""
        while True:
            try:
                await asyncio.sleep(self._batch_interval_sec)
                async with self._buffer_lock:
                    if self._buffer:
                        await self._flush_buffer()
            except asyncio.CancelledError:
                # Final flush on cancellation
                async with self._buffer_lock:
                    if self._buffer:
                        await self._flush_buffer()
                break
            except Exception as e:
                logger.warning(f"Background flush error: {e}")

    async def flush(self) -> None:
        """Manually flush the signal buffer."""
        async with self._buffer_lock:
            await self._flush_buffer()

    def _severity_to_score(self, severity: SignalSeverity) -> float:
        """Convert severity to numeric score."""
        mapping = {
            SignalSeverity.LOW: 0.25,
            SignalSeverity.MEDIUM: 0.5,
            SignalSeverity.HIGH: 0.75,
            SignalSeverity.CRITICAL: 1.0,
        }
        return mapping.get(severity, 0.5)

    def get_metrics(self) -> SignalMetrics:
        """Get signal reporter metrics."""
        return self._metrics

    def get_stats(self) -> dict[str, Any]:
        """Get signal reporter statistics."""
        return {
            **self._metrics.to_dict(),
            "buffer_size": len(self._buffer),
            "batch_size": self._batch_size,
            "batch_interval_sec": self._batch_interval_sec,
        }

    async def start(self) -> None:
        """Start the background flush task."""
        if self._auto_batch and (self._flush_task is None or self._flush_task.done()):
            self._flush_task = asyncio.create_task(self._background_flush())

    async def stop(self) -> None:
        """Stop the signal reporter and flush remaining signals."""
        if self._flush_task and not self._flush_task.done():
            self._flush_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._flush_task

        # Final flush
        await self.flush()

        # Close persistent session
        if self._session:
            await self._session.close()
            self._session = None


# Convenience function for global signal reporter
_global_reporter: SignalReporter | None = None


def get_signal_reporter() -> SignalReporter | None:
    """Get the global signal reporter instance."""
    return _global_reporter


def set_signal_reporter(reporter: SignalReporter) -> None:
    """Set the global signal reporter instance."""
    global _global_reporter
    _global_reporter = reporter
