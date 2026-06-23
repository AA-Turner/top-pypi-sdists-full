"""
Loop Detection for AI Agents.

This module provides loop detection capabilities to identify when an agent
gets stuck in repetitive patterns. This is a key feature for predictive
prevention - detecting problems BEFORE they impact users.

Inspired by AutoGPT's challenge with infinite loops, this module provides:
- State-based loop detection using similarity scoring
- Configurable actions (warn, break, auto_fix)
- Integration with Aigie's remediation system
- Signal emission to backend Signal Hub

Usage:
    from aigie.agents import LoopDetector

    # Create detector with configuration
    detector = LoopDetector(
        max_similar_states=3,        # Alert after 3 similar states
        similarity_threshold=0.85,   # How similar = "same state"
        action="warn"                # "warn", "break", "auto_fix"
    )

    # Check for loops during agent execution
    for step in agent.execute():
        detector.check_state(
            messages=step.messages,
            tool_calls=step.tool_calls
        )
        if detector.is_looping:
            # Handle loop condition
            break

Signal Hub Integration:
    When loop detection is triggered, a TOOL_LOOP signal is emitted
    to the backend Signal Hub for correlation with other signals.
"""

import hashlib
import json
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from difflib import SequenceMatcher
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from aigie.signals import SignalReporter


class LoopAction(str, Enum):
    """Action to take when a loop is detected."""

    WARN = "warn"  # Log warning but continue
    BREAK = "break"  # Raise exception to stop execution
    AUTO_FIX = "auto_fix"  # Trigger Aigie remediation


@dataclass
class LoopState:
    """Represents a captured state for loop detection."""

    messages_hash: str
    tool_calls_hash: str
    state_hash: str
    timestamp: datetime
    raw_messages: list[dict[str, Any]] | None = None
    raw_tool_calls: list[dict[str, Any]] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __hash__(self) -> int:
        return hash(self.state_hash)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LoopState):
            return False
        return self.state_hash == other.state_hash


@dataclass
class LoopDetectionResult:
    """Result of a loop detection check."""

    is_looping: bool
    loop_count: int
    similarity_score: float
    similar_states: list[LoopState]
    action_taken: LoopAction | None = None
    message: str | None = None


class LoopDetector:
    """
    Detects when an AI agent gets stuck in repetitive patterns.

    The detector tracks agent states and identifies when similar states
    are repeated, indicating the agent may be stuck in a loop.

    Attributes:
        max_similar_states: Number of similar states before triggering detection
        similarity_threshold: How similar states must be (0.0-1.0) to count as "same"
        action: What to do when a loop is detected
        is_looping: Whether a loop has been detected
        loop_count: Number of times the same pattern has been seen
    """

    def __init__(
        self,
        max_similar_states: int = 3,
        similarity_threshold: float = 0.85,
        action: str | LoopAction = LoopAction.WARN,
        window_size: int = 10,
        on_loop_detected: Callable[["LoopDetector", LoopDetectionResult], None] | None = None,
        signal_reporter: Optional["SignalReporter"] = None,
        trace_id: str | None = None,
    ):
        """
        Initialize the loop detector.

        Args:
            max_similar_states: Number of similar states to trigger loop detection
            similarity_threshold: Minimum similarity (0.0-1.0) to consider states similar
            action: Action to take when loop detected ("warn", "break", "auto_fix")
            window_size: Number of recent states to keep for comparison
            on_loop_detected: Optional callback when loop is detected
            signal_reporter: Optional signal reporter for emitting to Signal Hub
            trace_id: Optional trace ID for signal context
        """
        self.max_similar_states = max_similar_states
        self.similarity_threshold = similarity_threshold
        self.action = LoopAction(action) if isinstance(action, str) else action
        self.window_size = window_size
        self.on_loop_detected = on_loop_detected
        self._signal_reporter = signal_reporter
        self._trace_id = trace_id

        # State tracking
        self._states: list[LoopState] = []
        self._is_looping: bool = False
        self._loop_count: int = 0
        self._similar_states: list[LoopState] = []
        self._last_similarity_score: float = 0.0

    def set_signal_reporter(self, reporter: "SignalReporter", trace_id: str | None = None) -> None:
        """Set the signal reporter for emitting loop signals to Signal Hub."""
        self._signal_reporter = reporter
        if trace_id:
            self._trace_id = trace_id

    def set_trace_id(self, trace_id: str) -> None:
        """Set the trace ID for signal context."""
        self._trace_id = trace_id

    @property
    def is_looping(self) -> bool:
        """Whether a loop has been detected."""
        return self._is_looping

    @property
    def loop_count(self) -> int:
        """Number of similar states detected."""
        return self._loop_count

    @property
    def states(self) -> list[LoopState]:
        """List of captured states."""
        return self._states.copy()

    def _hash_content(self, content: Any) -> str:
        """Create a hash of content for comparison."""
        if content is None:
            return ""
        try:
            # Normalize content to JSON string for consistent hashing
            normalized = json.dumps(content, sort_keys=True, default=str)
            return hashlib.md5(normalized.encode()).hexdigest()
        except (TypeError, ValueError):
            # Fallback to string representation
            return hashlib.md5(str(content).encode()).hexdigest()

    def _normalize_messages(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Normalize messages for comparison by removing non-essential fields."""
        normalized = []
        for msg in messages:
            normalized_msg = {
                "role": msg.get("role", ""),
                "content": msg.get("content", ""),
            }
            # Include tool calls if present
            if "tool_calls" in msg:
                normalized_msg["tool_calls"] = msg["tool_calls"]
            normalized.append(normalized_msg)
        return normalized

    def _normalize_tool_calls(self, tool_calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Normalize tool calls for comparison."""
        normalized = []
        for tc in tool_calls:
            normalized_tc = {
                "name": tc.get("name") or tc.get("function", {}).get("name", ""),
                "arguments": tc.get("arguments") or tc.get("function", {}).get("arguments", {}),
            }
            normalized.append(normalized_tc)
        return sorted(normalized, key=lambda x: x["name"])

    def _compute_similarity(self, state1: LoopState, state2: LoopState) -> float:
        """
        Compute similarity between two states.

        Uses a combination of hash comparison and content similarity.
        """
        # Exact match
        if state1.state_hash == state2.state_hash:
            return 1.0

        # If we have raw content, do deeper comparison
        similarity_scores = []

        # Compare messages
        if state1.raw_messages and state2.raw_messages:
            msg1_str = json.dumps(state1.raw_messages, sort_keys=True, default=str)
            msg2_str = json.dumps(state2.raw_messages, sort_keys=True, default=str)
            msg_similarity = SequenceMatcher(None, msg1_str, msg2_str).ratio()
            similarity_scores.append(msg_similarity)
        elif state1.messages_hash == state2.messages_hash:
            similarity_scores.append(1.0)

        # Compare tool calls
        if state1.raw_tool_calls and state2.raw_tool_calls:
            tc1_str = json.dumps(state1.raw_tool_calls, sort_keys=True, default=str)
            tc2_str = json.dumps(state2.raw_tool_calls, sort_keys=True, default=str)
            tc_similarity = SequenceMatcher(None, tc1_str, tc2_str).ratio()
            similarity_scores.append(tc_similarity)
        elif state1.tool_calls_hash == state2.tool_calls_hash:
            similarity_scores.append(1.0)

        if not similarity_scores:
            return 0.0

        # Average similarity
        return sum(similarity_scores) / len(similarity_scores)

    def _find_similar_states(self, current_state: LoopState) -> list[LoopState]:
        """Find states similar to the current state."""
        similar = []
        for state in self._states[:-1]:  # Exclude current state
            similarity = self._compute_similarity(current_state, state)
            if similarity >= self.similarity_threshold:
                similar.append(state)
                self._last_similarity_score = max(self._last_similarity_score, similarity)
        return similar

    def check_state(
        self,
        messages: list[dict[str, Any]] | None = None,
        tool_calls: list[dict[str, Any]] | None = None,
        state: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> LoopDetectionResult:
        """
        Check if the current state indicates a loop.

        Args:
            messages: Current conversation messages
            tool_calls: Current tool calls
            state: Optional custom state object
            metadata: Additional metadata to store with state

        Returns:
            LoopDetectionResult with detection status and details
        """
        # Normalize inputs
        normalized_messages = self._normalize_messages(messages or [])
        normalized_tool_calls = self._normalize_tool_calls(tool_calls or [])

        # Create state hashes
        messages_hash = self._hash_content(normalized_messages)
        tool_calls_hash = self._hash_content(normalized_tool_calls)

        # Combined state hash
        combined = {
            "messages": normalized_messages,
            "tool_calls": normalized_tool_calls,
            "custom_state": state,
        }
        state_hash = self._hash_content(combined)

        # Create LoopState
        loop_state = LoopState(
            messages_hash=messages_hash,
            tool_calls_hash=tool_calls_hash,
            state_hash=state_hash,
            timestamp=datetime.utcnow(),
            raw_messages=normalized_messages,
            raw_tool_calls=normalized_tool_calls,
            metadata=metadata or {},
        )

        # Add to state history
        self._states.append(loop_state)

        # Maintain window size
        if len(self._states) > self.window_size:
            self._states = self._states[-self.window_size :]

        # Find similar states
        similar_states = self._find_similar_states(loop_state)
        self._similar_states = similar_states
        self._loop_count = len(similar_states)

        # Check if we've exceeded the threshold
        is_looping = len(similar_states) >= self.max_similar_states
        self._is_looping = is_looping

        result = LoopDetectionResult(
            is_looping=is_looping,
            loop_count=len(similar_states),
            similarity_score=self._last_similarity_score,
            similar_states=similar_states,
        )

        if is_looping:
            result.action_taken = self.action
            result.message = (
                f"Loop detected: {len(similar_states)} similar states found "
                f"(threshold: {self.max_similar_states}, "
                f"similarity: {self._last_similarity_score:.2f})"
            )

            # Emit signal to Signal Hub
            self._emit_loop_signal(result)

            # Execute action
            if self.action == LoopAction.BREAK:
                from aigie.exceptions import LoopDetectedError

                raise LoopDetectedError(
                    result.message,
                    loop_count=len(similar_states),
                    similarity_score=self._last_similarity_score,
                    similar_states=[s.state_hash for s in similar_states],
                )
            if self.action == LoopAction.WARN:
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(result.message)
            elif self.action == LoopAction.AUTO_FIX:
                # Trigger remediation callback if provided
                if self.on_loop_detected:
                    self.on_loop_detected(self, result)

        return result

    def _emit_loop_signal(self, result: LoopDetectionResult) -> None:
        """Emit a loop signal to the Signal Hub."""
        if not self._signal_reporter or not self._trace_id:
            return

        try:
            import asyncio

            # Get or create event loop
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            # Build tool calls list from similar states
            tool_calls = []
            for state in result.similar_states[:5]:
                if state.raw_tool_calls:
                    for tc in state.raw_tool_calls:
                        name = tc.get("name", "")
                        if name and name not in tool_calls:
                            tool_calls.append(name)

            # Determine pattern name
            pattern = tool_calls[0] if tool_calls else "unknown_pattern"

            if loop is not None:
                # Running in async context
                asyncio.create_task(
                    self._signal_reporter.report_loop(
                        trace_id=self._trace_id,
                        pattern=pattern,
                        count=result.loop_count,
                        similarity_score=result.similarity_score,
                        tool_calls=tool_calls,
                        metadata={
                            "action": result.action_taken.value if result.action_taken else None,
                            "max_similar_states": self.max_similar_states,
                            "similarity_threshold": self.similarity_threshold,
                        },
                    )
                )
            else:
                # Not in async context, try to run in new loop
                asyncio.run(
                    self._signal_reporter.report_loop(
                        trace_id=self._trace_id,
                        pattern=pattern,
                        count=result.loop_count,
                        similarity_score=result.similarity_score,
                        tool_calls=tool_calls,
                        metadata={
                            "action": result.action_taken.value if result.action_taken else None,
                            "max_similar_states": self.max_similar_states,
                            "similarity_threshold": self.similarity_threshold,
                        },
                    )
                )
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.debug(f"Failed to emit loop signal: {e}")

    def reset(self) -> None:
        """Reset the detector state."""
        self._states.clear()
        self._is_looping = False
        self._loop_count = 0
        self._similar_states.clear()
        self._last_similarity_score = 0.0

    def get_state_summary(self) -> dict[str, Any]:
        """Get a summary of the detector's current state."""
        return {
            "total_states": len(self._states),
            "is_looping": self._is_looping,
            "loop_count": self._loop_count,
            "last_similarity_score": self._last_similarity_score,
            "max_similar_states": self.max_similar_states,
            "similarity_threshold": self.similarity_threshold,
            "action": self.action.value,
        }


class TracingLoopDetector(LoopDetector):
    """
    Loop detector that integrates with Aigie tracing.

    Creates spans for loop detection events and integrates
    with the remediation system.
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
            **kwargs: Arguments passed to LoopDetector
        """
        super().__init__(**kwargs)
        self._trace_context = trace_context
        self._detection_count = 0

    async def check_state_async(
        self,
        messages: list[dict[str, Any]] | None = None,
        tool_calls: list[dict[str, Any]] | None = None,
        state: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> LoopDetectionResult:
        """
        Async version of check_state with tracing support.

        Creates a span for the loop check operation.
        """
        result = self.check_state(messages, tool_calls, state, metadata)
        self._detection_count += 1

        # Create span if we have a trace context
        if self._trace_context and result.is_looping:
            try:
                async with self._trace_context.span(
                    name="loop_detection",
                    type="drift_detection",
                ) as span:
                    span.set_input(
                        {
                            "check_number": self._detection_count,
                            "messages_count": len(messages) if messages else 0,
                            "tool_calls_count": len(tool_calls) if tool_calls else 0,
                        }
                    )
                    span.set_output(
                        {
                            "is_looping": result.is_looping,
                            "loop_count": result.loop_count,
                            "similarity_score": result.similarity_score,
                            "action_taken": result.action_taken.value
                            if result.action_taken
                            else None,
                        }
                    )
                    if result.message:
                        span.set_metadata({"detection_message": result.message})
            except Exception:
                pass  # Don't fail on tracing errors

        return result

    def attach_to_trace(self, trace_context: Any) -> "TracingLoopDetector":
        """
        Attach this detector to a trace context.

        Args:
            trace_context: TraceContext to attach to

        Returns:
            Self for method chaining
        """
        self._trace_context = trace_context
        return self
