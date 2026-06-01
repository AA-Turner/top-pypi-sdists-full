"""
ContextTracker - Track context changes across LLM calls for drift detection.

This module provides thread-safe context tracking using Python's contextvars,
enabling detection of context drift across nested LLM calls.
"""

import contextvars
import hashlib
import json
import logging
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger("aigie.interceptor")


@dataclass
class ContextSnapshot:
    """Snapshot of context at a point in time."""

    hash: str
    """Hash of the context for comparison."""

    timestamp: datetime
    """When this snapshot was taken."""

    span_id: str | None = None
    """Span ID when snapshot was taken."""

    message_count: int = 0
    """Number of messages in context."""

    last_message_role: str | None = None
    """Role of the last message (user, assistant, system)."""

    topics: list[str] = field(default_factory=list)
    """Detected topics in the context."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional metadata about the context."""


@dataclass
class DriftEvent:
    """Detected drift event between context snapshots."""

    from_hash: str
    """Hash of the previous context."""

    to_hash: str
    """Hash of the new context."""

    drift_score: float
    """Drift score (0.0 = no drift, 1.0 = complete drift)."""

    drift_type: str
    """Type of drift: 'gradual', 'sudden', 'topic_shift', 'role_change'."""

    details: dict[str, Any] = field(default_factory=dict)
    """Details about the drift."""

    timestamp: datetime = field(default_factory=datetime.utcnow)
    """When drift was detected."""


# Context variable to store the current context tracker
_context_tracker: contextvars.ContextVar[Optional["ContextTracker"]] = contextvars.ContextVar(
    "_context_tracker", default=None
)


def get_context_tracker() -> Optional["ContextTracker"]:
    """Get the current context tracker."""
    return _context_tracker.get()


def set_context_tracker(tracker: Optional["ContextTracker"]) -> None:
    """Set the current context tracker."""
    _context_tracker.set(tracker)


class ContextTracker:
    """
    Tracks context changes across LLM calls for drift detection.

    Features:
    - Context hashing for change detection
    - Drift score calculation
    - Historical context storage
    - Topic extraction (basic keyword-based)
    - Thread-safe via contextvars
    """

    def __init__(
        self,
        max_history: int = 100,
        drift_threshold: float = 0.7,
        enable_topic_tracking: bool = True,
    ):
        """
        Initialize the context tracker.

        Args:
            max_history: Maximum number of context snapshots to keep
            drift_threshold: Threshold for flagging significant drift (0.0-1.0)
            enable_topic_tracking: Whether to track topics in context
        """
        self._max_history = max_history
        self._drift_threshold = drift_threshold
        self._enable_topic_tracking = enable_topic_tracking

        self._history: deque[ContextSnapshot] = deque(maxlen=max_history)
        self._drift_events: deque[DriftEvent] = deque(maxlen=max_history)
        self._current_hash: str | None = None

        # Topic keywords for basic extraction
        self._topic_keywords = {
            "code": ["code", "function", "class", "variable", "programming", "debug"],
            "data": ["data", "database", "query", "sql", "table", "record"],
            "api": ["api", "endpoint", "request", "response", "http", "rest"],
            "error": ["error", "exception", "bug", "fix", "issue", "problem"],
            "config": ["config", "setting", "parameter", "option", "environment"],
            "security": ["security", "auth", "token", "password", "permission"],
            "performance": ["performance", "speed", "optimize", "cache", "memory"],
        }

    def snapshot(
        self,
        messages: list[dict[str, Any]],
        span_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ContextSnapshot:
        """
        Take a snapshot of the current context.

        Args:
            messages: Current messages in the context
            span_id: Current span ID
            metadata: Additional metadata

        Returns:
            ContextSnapshot of the current state
        """
        # Compute hash
        context_hash = self._compute_hash(messages)

        # Extract topics if enabled
        topics = []
        if self._enable_topic_tracking:
            topics = self._extract_topics(messages)

        # Get last message info
        last_role = None
        if messages:
            last_role = messages[-1].get("role")

        snapshot = ContextSnapshot(
            hash=context_hash,
            timestamp=datetime.utcnow(),
            span_id=span_id,
            message_count=len(messages),
            last_message_role=last_role,
            topics=topics,
            metadata=metadata or {},
        )

        # Store in history
        self._history.append(snapshot)

        # Check for drift
        if self._current_hash and self._current_hash != context_hash:
            drift_score = self._calculate_drift(self._current_hash, context_hash, messages)
            if drift_score > 0:
                drift_event = DriftEvent(
                    from_hash=self._current_hash,
                    to_hash=context_hash,
                    drift_score=drift_score,
                    drift_type=self._classify_drift(drift_score, topics),
                    details={
                        "message_count_change": len(messages)
                        - (self._history[-2].message_count if len(self._history) > 1 else 0),
                        "topics": topics,
                    },
                )
                self._drift_events.append(drift_event)

                if drift_score >= self._drift_threshold:
                    logger.warning(
                        f"Significant context drift detected: {drift_score:.2f} "
                        f"(type: {drift_event.drift_type})"
                    )

        self._current_hash = context_hash
        return snapshot

    def get_drift_score(
        self,
        messages: list[dict[str, Any]],
        previous_hash: str | None = None,
    ) -> float:
        """
        Calculate drift score between current messages and previous context.

        Args:
            messages: Current messages
            previous_hash: Previous context hash (default: last known hash)

        Returns:
            Drift score between 0.0 (no drift) and 1.0 (complete drift)
        """
        current_hash = self._compute_hash(messages)
        prev = previous_hash or self._current_hash

        if not prev:
            return 0.0

        return self._calculate_drift(prev, current_hash, messages)

    def get_recent_drift_events(self, count: int = 10) -> list[DriftEvent]:
        """Get the most recent drift events."""
        return list(self._drift_events)[-count:]

    def get_history(self, count: int = 10) -> list[ContextSnapshot]:
        """Get recent context snapshots."""
        return list(self._history)[-count:]

    def reset(self) -> None:
        """Reset the tracker state."""
        self._history.clear()
        self._drift_events.clear()
        self._current_hash = None

    def _compute_hash(self, messages: list[dict[str, Any]]) -> str:
        """Compute a hash of the messages for comparison."""
        # Use last N messages for hash (to handle growing conversations)
        recent_messages = messages[-10:] if len(messages) > 10 else messages

        # Create a stable representation
        hash_data = []
        for msg in recent_messages:
            hash_data.append(
                {
                    "role": msg.get("role", ""),
                    "content": str(msg.get("content", ""))[:500],  # Truncate long content
                }
            )

        hash_str = json.dumps(hash_data, sort_keys=True)
        return hashlib.sha256(hash_str.encode()).hexdigest()[:16]

    def _calculate_drift(
        self,
        prev_hash: str,
        curr_hash: str,
        messages: list[dict[str, Any]],
    ) -> float:
        """
        Calculate drift score between two context hashes.

        Uses a combination of:
        - Hash difference (binary: same or different)
        - Message content similarity (if available)
        - Topic continuity
        """
        if prev_hash == curr_hash:
            return 0.0

        # Base score for hash difference
        base_score = 0.3

        # Check topic continuity
        if self._enable_topic_tracking and len(self._history) > 1:
            prev_snapshot = self._history[-2] if len(self._history) > 1 else None
            if prev_snapshot:
                curr_topics = set(self._extract_topics(messages))
                prev_topics = set(prev_snapshot.topics)

                if prev_topics:
                    topic_overlap = len(curr_topics & prev_topics) / len(prev_topics)
                    topic_drift = 1.0 - topic_overlap
                    base_score += topic_drift * 0.4

        # Check for sudden message count changes
        if len(self._history) > 1:
            prev_count = self._history[-2].message_count
            curr_count = len(messages)
            if curr_count < prev_count:
                # Context was reset or truncated
                base_score += 0.3
            elif curr_count > prev_count + 5:
                # Large jump in messages
                base_score += 0.2

        return min(base_score, 1.0)

    def _classify_drift(self, score: float, topics: list[str]) -> str:
        """Classify the type of drift."""
        if score >= 0.8:
            return "sudden"
        if score >= 0.5:
            if topics and len(self._history) > 1:
                prev_topics = set(self._history[-2].topics) if self._history else set()
                curr_topics = set(topics)
                if not (prev_topics & curr_topics):
                    return "topic_shift"
            return "gradual"
        return "minor"

    def _extract_topics(self, messages: list[dict[str, Any]]) -> list[str]:
        """Extract topics from messages using keyword matching."""
        topics = set()

        # Combine all message content
        content = " ".join(str(msg.get("content", "")).lower() for msg in messages[-5:])

        # Match against topic keywords
        for topic, keywords in self._topic_keywords.items():
            if any(kw in content for kw in keywords):
                topics.add(topic)

        return list(topics)


class ScopedContextTracker:
    """
    Context manager for scoped context tracking.

    Usage:
        with ScopedContextTracker() as tracker:
            tracker.snapshot(messages)
            # ... do work ...
            drift = tracker.get_drift_score(new_messages)
    """

    def __init__(self, **kwargs):
        self._tracker = ContextTracker(**kwargs)
        self._token = None

    def __enter__(self) -> ContextTracker:
        self._token = _context_tracker.set(self._tracker)
        return self._tracker

    def __exit__(self, exc_type, exc_val, exc_tb):
        _context_tracker.reset(self._token)
        return False
