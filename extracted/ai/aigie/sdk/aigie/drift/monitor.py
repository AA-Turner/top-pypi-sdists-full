"""
DriftMonitor - Real-time context drift detection and monitoring.

Detects various types of drift:
- Topic drift: Conversation deviating from original topic
- Behavior drift: Model responses changing unexpectedly
- Quality drift: Response quality degradation
- Coherence drift: Loss of conversation coherence
"""

import logging
import re
import time
from collections import deque
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aigie.interceptor.protocols import InterceptionContext

logger = logging.getLogger("aigie.drift")


class DriftLevel(Enum):
    """Severity level of detected drift."""

    NONE = "none"
    """No drift detected."""

    LOW = "low"
    """Minor drift, monitoring only."""

    MODERATE = "moderate"
    """Moderate drift, consider intervention."""

    HIGH = "high"
    """High drift, intervention recommended."""

    CRITICAL = "critical"
    """Critical drift, immediate action required."""


class DriftType(Enum):
    """Type of drift detected."""

    TOPIC = "topic"
    """Topic has shifted from original conversation focus."""

    BEHAVIOR = "behavior"
    """Model behavior has changed unexpectedly."""

    QUALITY = "quality"
    """Response quality has degraded."""

    COHERENCE = "coherence"
    """Conversation has lost coherence."""

    CONTEXT_OVERFLOW = "context_overflow"
    """Context window approaching or exceeding limits."""

    REPETITION = "repetition"
    """Repetitive patterns detected in responses."""

    HALLUCINATION = "hallucination"
    """Potential hallucination indicators detected."""


@dataclass
class DriftAlert:
    """Alert generated when drift is detected."""

    drift_type: DriftType
    """Type of drift detected."""

    level: DriftLevel
    """Severity level."""

    score: float
    """Drift score (0.0-1.0)."""

    reason: str
    """Human-readable explanation."""

    timestamp: datetime = field(default_factory=datetime.utcnow)
    """When the drift was detected."""

    trace_id: str | None = None
    """Associated trace ID."""

    span_id: str | None = None
    """Associated span ID."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional context about the drift."""

    recommendations: list[str] = field(default_factory=list)
    """Recommended actions to address the drift."""


@dataclass
class DriftMetrics:
    """Metrics for drift monitoring."""

    total_checks: int = 0
    """Total drift checks performed."""

    alerts_generated: int = 0
    """Total alerts generated."""

    alerts_by_type: dict[str, int] = field(default_factory=lambda: {t.value: 0 for t in DriftType})
    """Alerts broken down by type."""

    alerts_by_level: dict[str, int] = field(
        default_factory=lambda: {level.value: 0 for level in DriftLevel}
    )
    """Alerts broken down by level."""

    avg_drift_score: float = 0.0
    """Average drift score across all checks."""

    max_drift_score: float = 0.0
    """Maximum drift score observed."""

    total_latency_ms: float = 0.0
    """Total time spent on drift checks."""


@dataclass
class DriftConfig:
    """Configuration for drift monitoring."""

    # Thresholds
    topic_drift_threshold: float = 0.6
    """Threshold for topic drift (0.0-1.0)."""

    behavior_drift_threshold: float = 0.5
    """Threshold for behavior drift."""

    quality_drift_threshold: float = 0.4
    """Threshold for quality drift."""

    coherence_drift_threshold: float = 0.5
    """Threshold for coherence drift."""

    # Detection settings
    min_messages_for_detection: int = 3
    """Minimum messages before drift detection activates."""

    history_window_size: int = 10
    """Number of recent exchanges to consider."""

    enable_topic_detection: bool = True
    """Enable topic drift detection."""

    enable_behavior_detection: bool = True
    """Enable behavior drift detection."""

    enable_quality_detection: bool = True
    """Enable quality drift detection."""

    enable_coherence_detection: bool = True
    """Enable coherence drift detection."""

    enable_repetition_detection: bool = True
    """Enable repetition detection."""

    # Alert settings
    cooldown_seconds: float = 30.0
    """Minimum time between alerts of the same type."""


class DriftMonitor:
    """
    Real-time drift monitor for LLM conversations.

    Monitors conversation context and responses to detect:
    - Topic shifts from original conversation intent
    - Unexpected behavior changes
    - Quality degradation
    - Coherence loss
    - Repetition patterns

    Features:
    - Multiple drift detection algorithms
    - Configurable thresholds
    - Alert generation with recommendations
    - Historical pattern analysis
    - Performance tracking
    """

    def __init__(self, config: DriftConfig | None = None):
        """
        Initialize the drift monitor.

        Args:
            config: Configuration for drift detection
        """
        self._config = config or DriftConfig()

        # Conversation tracking
        self._topic_embeddings: dict[str, list[float]] = {}
        self._response_history: dict[str, deque] = {}
        self._quality_scores: dict[str, deque] = {}

        # Alert management
        self._last_alert_time: dict[str, dict[DriftType, datetime]] = {}
        self._alert_callbacks: list[Callable[[DriftAlert], Awaitable[None]]] = []

        # Metrics
        self._metrics = DriftMetrics()

        # Keyword extraction patterns
        self._topic_patterns = re.compile(
            r"\b(?:about|regarding|discuss|explain|help with|question about)\s+(.+?)(?:\.|,|$)",
            re.IGNORECASE,
        )

    def on_alert(self, callback: Callable[[DriftAlert], Awaitable[None]]) -> None:
        """Register callback for drift alerts."""
        self._alert_callbacks.append(callback)

    async def check_drift(
        self,
        ctx: "InterceptionContext",
    ) -> list[DriftAlert]:
        """
        Check for drift in the given context.

        Runs multiple drift detection algorithms and returns
        any alerts that exceed configured thresholds.

        Args:
            ctx: The interception context to check

        Returns:
            List of DriftAlert objects (empty if no drift detected)
        """
        start_time = time.perf_counter()
        self._metrics.total_checks += 1

        alerts: list[DriftAlert] = []
        trace_key = ctx.trace_id or "default"

        # Initialize tracking for this trace
        if trace_key not in self._response_history:
            self._response_history[trace_key] = deque(maxlen=self._config.history_window_size)
            self._quality_scores[trace_key] = deque(maxlen=self._config.history_window_size)
            self._last_alert_time[trace_key] = {}

        # Skip if not enough messages
        if len(ctx.messages) < self._config.min_messages_for_detection:
            return alerts

        # Run detection algorithms
        if self._config.enable_topic_detection:
            alert = await self._detect_topic_drift(ctx, trace_key)
            if alert:
                alerts.append(alert)

        if self._config.enable_behavior_detection:
            alert = await self._detect_behavior_drift(ctx, trace_key)
            if alert:
                alerts.append(alert)

        if self._config.enable_quality_detection:
            alert = await self._detect_quality_drift(ctx, trace_key)
            if alert:
                alerts.append(alert)

        if self._config.enable_coherence_detection:
            alert = await self._detect_coherence_drift(ctx, trace_key)
            if alert:
                alerts.append(alert)

        if self._config.enable_repetition_detection:
            alert = await self._detect_repetition(ctx, trace_key)
            if alert:
                alerts.append(alert)

        # Update response history
        if ctx.response_content:
            self._response_history[trace_key].append(
                {
                    "content": ctx.response_content,
                    "timestamp": datetime.utcnow(),
                    "tokens": ctx.actual_output_tokens or 0,
                }
            )

        # Update metrics
        latency = (time.perf_counter() - start_time) * 1000
        self._metrics.total_latency_ms += latency

        if alerts:
            max_score = max(a.score for a in alerts)
            self._metrics.max_drift_score = max(self._metrics.max_drift_score, max_score)

            # Calculate running average
            n = self._metrics.total_checks
            self._metrics.avg_drift_score = (
                self._metrics.avg_drift_score * (n - 1) + max_score
            ) / n

            # Update alert counters
            for alert in alerts:
                self._metrics.alerts_generated += 1
                self._metrics.alerts_by_type[alert.drift_type.value] += 1
                self._metrics.alerts_by_level[alert.level.value] += 1

                # Fire callbacks
                for callback in self._alert_callbacks:
                    try:
                        await callback(alert)
                    except Exception as e:
                        logger.error(f"Alert callback error: {e}")

        return alerts

    async def _detect_topic_drift(
        self,
        ctx: "InterceptionContext",
        trace_key: str,
    ) -> DriftAlert | None:
        """Detect topic drift from original conversation intent."""
        if not self._can_alert(trace_key, DriftType.TOPIC):
            return None

        # Extract topics from messages
        original_topics = self._extract_topics(ctx.messages[:3])
        recent_topics = self._extract_topics(ctx.messages[-3:])

        if not original_topics or not recent_topics:
            return None

        # Calculate topic overlap
        original_set = set(original_topics)
        recent_set = set(recent_topics)

        if not original_set:
            return None

        overlap = len(original_set & recent_set) / len(original_set)
        drift_score = 1.0 - overlap

        # Check if response continues topic drift
        if ctx.response_content:
            response_topics = self._extract_topics([{"content": ctx.response_content}])
            if response_topics:
                response_overlap = len(original_set & set(response_topics)) / len(original_set)
                drift_score = max(drift_score, 1.0 - response_overlap)

        if drift_score >= self._config.topic_drift_threshold:
            self._record_alert(trace_key, DriftType.TOPIC)
            return DriftAlert(
                drift_type=DriftType.TOPIC,
                level=self._score_to_level(drift_score),
                score=drift_score,
                reason=f"Conversation has drifted from original topic (score: {drift_score:.2f})",
                trace_id=ctx.trace_id,
                span_id=ctx.span_id,
                metadata={
                    "original_topics": original_topics,
                    "recent_topics": recent_topics,
                },
                recommendations=[
                    "Consider refocusing the conversation on the original topic",
                    "Add a system prompt reminder about the conversation goal",
                ],
            )

        return None

    async def _detect_behavior_drift(
        self,
        ctx: "InterceptionContext",
        trace_key: str,
    ) -> DriftAlert | None:
        """Detect unexpected behavior changes in model responses."""
        if not self._can_alert(trace_key, DriftType.BEHAVIOR):
            return None

        history = self._response_history.get(trace_key, [])
        if len(history) < 2:
            return None

        # Analyze response characteristics
        current_response = ctx.response_content or ""
        recent_responses = [h["content"] for h in list(history)[-3:]]

        # Calculate behavior metrics
        avg_length = (
            sum(len(r) for r in recent_responses) / len(recent_responses) if recent_responses else 0
        )
        current_length = len(current_response)

        # Detect significant length deviation
        if avg_length > 0:
            length_ratio = current_length / avg_length
            if length_ratio < 0.3 or length_ratio > 3.0:
                drift_score = min(1.0, abs(1.0 - length_ratio) / 2)

                if drift_score >= self._config.behavior_drift_threshold:
                    self._record_alert(trace_key, DriftType.BEHAVIOR)
                    return DriftAlert(
                        drift_type=DriftType.BEHAVIOR,
                        level=self._score_to_level(drift_score),
                        score=drift_score,
                        reason=f"Response length significantly different from pattern (ratio: {length_ratio:.2f})",
                        trace_id=ctx.trace_id,
                        span_id=ctx.span_id,
                        metadata={
                            "current_length": current_length,
                            "avg_length": avg_length,
                            "ratio": length_ratio,
                        },
                        recommendations=[
                            "Check if the model is responding appropriately",
                            "Consider adjusting max_tokens parameter",
                        ],
                    )

        # Detect tone/style shifts (simplified heuristic)
        if current_response and recent_responses:
            tone_indicators = {
                "formal": r"\b(therefore|furthermore|additionally|consequently)\b",
                "informal": r"\b(gonna|wanna|kinda|yeah|ok)\b",
                "technical": r"\b(implement|function|parameter|algorithm|data)\b",
                "casual": r"[!?]{2,}|\b(hey|hi|awesome|cool)\b",
            }

            current_tone = self._detect_tone(current_response, tone_indicators)
            prev_tone = self._detect_tone(recent_responses[-1], tone_indicators)

            if current_tone not in (prev_tone, "neutral") and prev_tone != "neutral":
                drift_score = 0.5  # Moderate drift for tone change
                if drift_score >= self._config.behavior_drift_threshold:
                    self._record_alert(trace_key, DriftType.BEHAVIOR)
                    return DriftAlert(
                        drift_type=DriftType.BEHAVIOR,
                        level=DriftLevel.MODERATE,
                        score=drift_score,
                        reason=f"Response tone shifted from {prev_tone} to {current_tone}",
                        trace_id=ctx.trace_id,
                        span_id=ctx.span_id,
                        metadata={
                            "previous_tone": prev_tone,
                            "current_tone": current_tone,
                        },
                        recommendations=[
                            "Verify the model is maintaining consistent communication style",
                        ],
                    )

        return None

    async def _detect_quality_drift(
        self,
        ctx: "InterceptionContext",
        trace_key: str,
    ) -> DriftAlert | None:
        """Detect quality degradation in responses."""
        if not self._can_alert(trace_key, DriftType.QUALITY):
            return None

        if not ctx.response_content:
            return None

        response = ctx.response_content

        # Quality indicators
        quality_score = 1.0

        # Check for very short responses (potential quality issue)
        if len(response) < 50 and len(ctx.messages) > 3:
            quality_score -= 0.3

        # Check for error indicators
        error_patterns = [
            r"I cannot",
            r"I'm unable to",
            r"I don't have",
            r"error",
            r"failed",
            r"sorry.*but",
            r"I apologize.*cannot",
        ]
        for pattern in error_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                quality_score -= 0.2
                break

        # Check for incomplete sentences
        if response and not response.strip().endswith((".", "!", "?", "`", '"')):
            quality_score -= 0.15

        # Check for gibberish (high ratio of unusual characters)
        alpha_ratio = sum(c.isalpha() or c.isspace() for c in response) / max(len(response), 1)
        if alpha_ratio < 0.6:
            quality_score -= 0.3

        # Track quality over time
        self._quality_scores[trace_key].append(quality_score)

        # Calculate drift from initial quality
        scores = list(self._quality_scores[trace_key])
        if len(scores) >= 3:
            initial_avg = sum(scores[:3]) / 3
            current_avg = sum(scores[-3:]) / 3
            drift_score = max(0, initial_avg - current_avg)

            if drift_score >= self._config.quality_drift_threshold:
                self._record_alert(trace_key, DriftType.QUALITY)
                return DriftAlert(
                    drift_type=DriftType.QUALITY,
                    level=self._score_to_level(drift_score),
                    score=drift_score,
                    reason=f"Response quality has degraded (initial: {initial_avg:.2f}, current: {current_avg:.2f})",
                    trace_id=ctx.trace_id,
                    span_id=ctx.span_id,
                    metadata={
                        "initial_quality": initial_avg,
                        "current_quality": current_avg,
                        "quality_history": scores,
                    },
                    recommendations=[
                        "Consider resetting the conversation context",
                        "Check if the model is reaching context limits",
                        "Review recent messages for confusing inputs",
                    ],
                )

        return None

    async def _detect_coherence_drift(
        self,
        ctx: "InterceptionContext",
        trace_key: str,
    ) -> DriftAlert | None:
        """Detect loss of conversation coherence."""
        if not self._can_alert(trace_key, DriftType.COHERENCE):
            return None

        if len(ctx.messages) < 4:
            return None

        # Get last exchange
        user_msgs = [m for m in ctx.messages if m.get("role") == "user"]
        assistant_msgs = [m for m in ctx.messages if m.get("role") == "assistant"]

        if not user_msgs or not assistant_msgs:
            return None

        last_user = str(user_msgs[-1].get("content", ""))
        str(assistant_msgs[-1].get("content", "")) if assistant_msgs else ""
        current_response = ctx.response_content or ""

        # Check for response relevance to user query
        if last_user and current_response:
            # Extract key terms from user query
            user_terms = set(self._extract_key_terms(last_user))
            response_terms = set(self._extract_key_terms(current_response))

            if user_terms:
                relevance = len(user_terms & response_terms) / len(user_terms)
                if relevance < 0.2:  # Response seems unrelated
                    drift_score = 1.0 - relevance

                    if drift_score >= self._config.coherence_drift_threshold:
                        self._record_alert(trace_key, DriftType.COHERENCE)
                        return DriftAlert(
                            drift_type=DriftType.COHERENCE,
                            level=self._score_to_level(drift_score),
                            score=drift_score,
                            reason=f"Response appears unrelated to user query (relevance: {relevance:.2f})",
                            trace_id=ctx.trace_id,
                            span_id=ctx.span_id,
                            metadata={
                                "user_terms": list(user_terms),
                                "response_terms": list(response_terms),
                                "relevance": relevance,
                            },
                            recommendations=[
                                "The model may have lost track of the conversation",
                                "Consider providing clearer context in the system prompt",
                            ],
                        )

        return None

    async def _detect_repetition(
        self,
        ctx: "InterceptionContext",
        trace_key: str,
    ) -> DriftAlert | None:
        """Detect repetitive patterns in responses."""
        if not self._can_alert(trace_key, DriftType.REPETITION):
            return None

        history = self._response_history.get(trace_key, [])
        if len(history) < 2 or not ctx.response_content:
            return None

        current = ctx.response_content
        recent = [h["content"] for h in list(history)[-5:]]

        # Check for exact or near-exact repetition
        for prev in recent:
            similarity = self._calculate_similarity(current, prev)
            if similarity > 0.85:  # 85% similarity threshold
                drift_score = similarity

                self._record_alert(trace_key, DriftType.REPETITION)
                return DriftAlert(
                    drift_type=DriftType.REPETITION,
                    level=DriftLevel.HIGH if similarity > 0.95 else DriftLevel.MODERATE,
                    score=drift_score,
                    reason=f"Response is very similar to a previous response (similarity: {similarity:.2f})",
                    trace_id=ctx.trace_id,
                    span_id=ctx.span_id,
                    metadata={
                        "similarity": similarity,
                    },
                    recommendations=[
                        "The model is producing repetitive responses",
                        "Consider increasing temperature parameter",
                        "Add variety prompts to the system message",
                    ],
                )

        # Check for internal repetition (same phrases repeated)
        sentences = re.split(r"[.!?]+", current)
        if len(sentences) >= 4:
            unique_sentences = set(s.strip().lower() for s in sentences if len(s.strip()) > 20)
            if len(unique_sentences) < len(sentences) * 0.6:
                repetition_ratio = 1 - (len(unique_sentences) / len(sentences))
                if repetition_ratio > 0.3:
                    self._record_alert(trace_key, DriftType.REPETITION)
                    return DriftAlert(
                        drift_type=DriftType.REPETITION,
                        level=DriftLevel.MODERATE,
                        score=repetition_ratio,
                        reason=f"Response contains repetitive content (ratio: {repetition_ratio:.2f})",
                        trace_id=ctx.trace_id,
                        span_id=ctx.span_id,
                        metadata={
                            "total_sentences": len(sentences),
                            "unique_sentences": len(unique_sentences),
                        },
                        recommendations=[
                            "The response is internally repetitive",
                            "Consider adjusting frequency_penalty or presence_penalty",
                        ],
                    )

        return None

    def _extract_topics(self, messages: list[dict[str, Any]]) -> list[str]:
        """Extract topic keywords from messages."""
        topics = []
        for msg in messages:
            content = str(msg.get("content", ""))

            # Extract from explicit topic patterns
            matches = self._topic_patterns.findall(content)
            topics.extend(matches)

            # Extract key noun phrases (simplified)
            words = content.lower().split()
            # Filter common words and keep potential topic words
            stopwords = {
                "the",
                "a",
                "an",
                "is",
                "are",
                "was",
                "were",
                "be",
                "been",
                "being",
                "have",
                "has",
                "had",
                "do",
                "does",
                "did",
                "will",
                "would",
                "could",
                "should",
                "may",
                "might",
                "must",
                "shall",
                "can",
                "need",
                "dare",
                "ought",
                "used",
                "to",
                "of",
                "in",
                "for",
                "on",
                "with",
                "at",
                "by",
                "from",
                "as",
                "into",
                "through",
                "during",
                "before",
                "after",
                "above",
                "below",
                "between",
                "under",
                "again",
                "further",
                "then",
                "once",
                "i",
                "me",
                "my",
                "you",
                "your",
                "we",
                "our",
                "they",
                "their",
                "it",
                "its",
                "this",
                "that",
                "these",
                "those",
                "what",
                "which",
                "who",
                "whom",
                "where",
                "when",
                "why",
                "how",
                "all",
                "each",
                "every",
                "both",
                "few",
                "more",
                "most",
                "other",
                "some",
                "such",
                "no",
                "nor",
                "not",
                "only",
                "own",
                "same",
                "so",
                "than",
                "too",
                "very",
                "just",
                "also",
                "now",
                "and",
                "but",
                "or",
                "if",
                "please",
            }
            topic_words = [w for w in words if w not in stopwords and len(w) > 3]
            topics.extend(topic_words[:5])  # Limit per message

        return list(set(topics))

    def _extract_key_terms(self, text: str) -> list[str]:
        """Extract key terms from text."""
        words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
        stopwords = {
            "about",
            "after",
            "again",
            "also",
            "been",
            "before",
            "being",
            "between",
            "both",
            "could",
            "does",
            "each",
            "from",
            "have",
            "here",
            "just",
            "like",
            "made",
            "make",
            "many",
            "more",
            "most",
            "much",
            "must",
            "only",
            "other",
            "over",
            "said",
            "same",
            "some",
            "such",
            "than",
            "that",
            "them",
            "then",
            "there",
            "these",
            "they",
            "this",
            "through",
            "very",
            "want",
            "well",
            "were",
            "what",
            "when",
            "where",
            "which",
            "while",
            "will",
            "with",
            "would",
            "your",
        }
        return [w for w in words if w not in stopwords]

    def _detect_tone(self, text: str, patterns: dict[str, str]) -> str:
        """Detect predominant tone of text."""
        scores = {
            tone: len(re.findall(pattern, text, re.IGNORECASE))
            for tone, pattern in patterns.items()
        }
        max_tone = max(scores, key=scores.get)
        return max_tone if scores[max_tone] > 0 else "neutral"

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using character-level comparison."""
        if not text1 or not text2:
            return 0.0

        # Normalize texts
        t1 = text1.lower().strip()
        t2 = text2.lower().strip()

        # Quick exact match check
        if t1 == t2:
            return 1.0

        # Character trigram similarity
        def get_trigrams(s):
            return set(s[i : i + 3] for i in range(len(s) - 2))

        trigrams1 = get_trigrams(t1)
        trigrams2 = get_trigrams(t2)

        if not trigrams1 or not trigrams2:
            return 0.0

        intersection = len(trigrams1 & trigrams2)
        union = len(trigrams1 | trigrams2)

        return intersection / union if union > 0 else 0.0

    def _score_to_level(self, score: float) -> DriftLevel:
        """Convert drift score to severity level."""
        if score >= 0.8:
            return DriftLevel.CRITICAL
        if score >= 0.6:
            return DriftLevel.HIGH
        if score >= 0.4:
            return DriftLevel.MODERATE
        if score >= 0.2:
            return DriftLevel.LOW
        return DriftLevel.NONE

    def _can_alert(self, trace_key: str, drift_type: DriftType) -> bool:
        """Check if we can generate an alert (respecting cooldown)."""
        if trace_key not in self._last_alert_time:
            return True

        last_time = self._last_alert_time[trace_key].get(drift_type)
        if last_time is None:
            return True

        elapsed = (datetime.utcnow() - last_time).total_seconds()
        return elapsed >= self._config.cooldown_seconds

    def _record_alert(self, trace_key: str, drift_type: DriftType) -> None:
        """Record that an alert was generated."""
        if trace_key not in self._last_alert_time:
            self._last_alert_time[trace_key] = {}
        self._last_alert_time[trace_key][drift_type] = datetime.utcnow()

    def analyze(self, ctx: "InterceptionContext") -> list[DriftAlert]:
        """
        Synchronous wrapper around check_drift for use in sync contexts.

        Schedules the async check_drift coroutine on a running event loop if
        available, or runs it in a new loop. Returns empty list on any error.
        """
        import asyncio

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Already in an async context — schedule as a task and return
                # an empty list; callers in async code should use check_drift directly.
                # For sync callers embedded in running loops we fall back gracefully.
                return []
            return loop.run_until_complete(self.check_drift(ctx))
        except Exception as e:
            logger.warning(f"DriftMonitor.analyze failed: {e}")
            return []

    def get_metrics(self) -> DriftMetrics:
        """Get drift monitoring metrics."""
        return self._metrics

    def reset_metrics(self) -> None:
        """Reset metrics."""
        self._metrics = DriftMetrics()

    def clear_trace(self, trace_id: str) -> None:
        """Clear tracking data for a specific trace."""
        self._response_history.pop(trace_id, None)
        self._quality_scores.pop(trace_id, None)
        self._last_alert_time.pop(trace_id, None)
        self._topic_embeddings.pop(trace_id, None)

    def clear_all(self) -> None:
        """Clear all tracking data."""
        self._response_history.clear()
        self._quality_scores.clear()
        self._last_alert_time.clear()
        self._topic_embeddings.clear()
