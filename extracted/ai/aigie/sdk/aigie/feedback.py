"""
Feedback Collector for Aigie SDK.

Collects human feedback for:
- Eval ground truth (human overrides of LLM judgments)
- Trace quality feedback (thumbs up/down)
- Span-level feedback

This data is used to:
- Build ground truth datasets for improving LLM-as-judge accuracy
- Train better evaluation models
- Understand user satisfaction with AI outputs
"""

import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .buffer import EventBuffer

logger = logging.getLogger(__name__)


class FeedbackCollector:
    """
    Collects human feedback for eval ground truth and quality improvement.

    Usage:
        # Submit human override of LLM judgment
        await aigie.feedback.submit_eval_override(
            judge_run_id="judge-123",
            human_score=0.9,
            human_verdict="pass",
            human_reasoning="The response was actually helpful"
        )

        # Submit trace feedback (thumbs up/down)
        await aigie.feedback.submit_trace_feedback(
            trace_id="trace-abc",
            rating="positive",
            comment="Great response!"
        )
    """

    def __init__(self, buffer: "EventBuffer"):
        """
        Initialize feedback collector.

        Args:
            buffer: Event buffer for sending feedback events
        """
        self._buffer = buffer
        self._stats = {
            "eval_feedbacks_submitted": 0,
            "trace_feedbacks_submitted": 0,
            "span_feedbacks_submitted": 0,
        }

    async def submit_eval_override(
        self,
        judge_run_id: str,
        human_score: float,
        human_verdict: str,
        human_reasoning: str | None = None,
        user_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """
        Submit human override of LLM judgment for ground truth collection.

        This captures cases where a human disagrees with the LLM judge's
        assessment, building a training dataset for improving evaluations.

        Args:
            judge_run_id: ID of the judge evaluation run
            human_score: Human's score (same scale as LLM, typically 0-1)
            human_verdict: Human's verdict (pass, fail, etc.)
            human_reasoning: Human's reasoning for the override
            user_id: ID of the user providing feedback
            metadata: Additional metadata

        Returns:
            True if feedback was queued successfully
        """
        if not self._buffer:
            logger.warning("No buffer available, feedback not submitted")
            return False

        from .buffer import EventType

        payload = {
            "judge_run_id": judge_run_id,
            "human_score": human_score,
            "human_verdict": human_verdict,
            "human_reasoning": human_reasoning,
            "human_user_id": user_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }

        try:
            await self._buffer.add(EventType.EVAL_FEEDBACK, payload)
            self._stats["eval_feedbacks_submitted"] += 1
            logger.debug(f"Eval feedback submitted for judge run {judge_run_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to submit eval feedback: {e}")
            return False

    async def submit_trace_feedback(
        self,
        trace_id: str,
        rating: str,
        comment: str | None = None,
        user_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """
        Submit feedback on a trace (thumbs up/down, rating).

        Args:
            trace_id: ID of the trace
            rating: Feedback rating (positive, negative, neutral, or 1-5 scale)
            comment: Optional user comment
            user_id: ID of the user providing feedback
            metadata: Additional metadata

        Returns:
            True if feedback was queued successfully
        """
        if not self._buffer:
            logger.warning("No buffer available, feedback not submitted")
            return False

        from .buffer import EventType

        # Normalize rating
        normalized_rating = self._normalize_rating(rating)

        payload = {
            "trace_id": trace_id,
            "rating": rating,
            "normalized_score": normalized_rating,
            "comment": comment,
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "feedback_type": "trace",
            "metadata": metadata or {},
        }

        try:
            await self._buffer.add(EventType.EVAL_FEEDBACK, payload)
            self._stats["trace_feedbacks_submitted"] += 1
            logger.debug(f"Trace feedback submitted for {trace_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to submit trace feedback: {e}")
            return False

    async def submit_span_feedback(
        self,
        span_id: str,
        trace_id: str,
        rating: str,
        comment: str | None = None,
        user_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """
        Submit feedback on a specific span within a trace.

        Useful for pinpointing which step in a workflow was good or bad.

        Args:
            span_id: ID of the span
            trace_id: ID of the parent trace
            rating: Feedback rating (positive, negative, neutral, or 1-5 scale)
            comment: Optional user comment
            user_id: ID of the user providing feedback
            metadata: Additional metadata

        Returns:
            True if feedback was queued successfully
        """
        if not self._buffer:
            logger.warning("No buffer available, feedback not submitted")
            return False

        from .buffer import EventType

        # Normalize rating
        normalized_rating = self._normalize_rating(rating)

        payload = {
            "span_id": span_id,
            "trace_id": trace_id,
            "rating": rating,
            "normalized_score": normalized_rating,
            "comment": comment,
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "feedback_type": "span",
            "metadata": metadata or {},
        }

        try:
            await self._buffer.add(EventType.EVAL_FEEDBACK, payload)
            self._stats["span_feedbacks_submitted"] += 1
            logger.debug(f"Span feedback submitted for {span_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to submit span feedback: {e}")
            return False

    async def submit_remediation_feedback(
        self,
        trace_id: str,
        strategy: str,
        was_helpful: bool,
        comment: str | None = None,
        user_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """
        Submit feedback on a remediation attempt.

        Helps train better remediation strategies.

        Args:
            trace_id: ID of the trace where remediation was applied
            strategy: Remediation strategy used (retry, fallback, etc.)
            was_helpful: Whether the remediation helped
            comment: Optional user comment
            user_id: ID of the user providing feedback
            metadata: Additional metadata

        Returns:
            True if feedback was queued successfully
        """
        if not self._buffer:
            logger.warning("No buffer available, feedback not submitted")
            return False

        from .buffer import EventType

        payload = {
            "trace_id": trace_id,
            "strategy": strategy,
            "human_feedback": "thumbs_up" if was_helpful else "thumbs_down",
            "comment": comment,
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }

        try:
            await self._buffer.add(EventType.REMEDIATION_RESULT, payload)
            logger.debug(f"Remediation feedback submitted for {trace_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to submit remediation feedback: {e}")
            return False

    def _normalize_rating(self, rating: str) -> float:
        """
        Normalize various rating formats to a 0-1 scale.

        Args:
            rating: Rating in various formats

        Returns:
            Normalized score between 0 and 1
        """
        # Handle string ratings
        rating_lower = rating.lower().strip()

        if rating_lower in ("positive", "good", "thumbs_up", "like"):
            return 1.0
        if rating_lower in ("negative", "bad", "thumbs_down", "dislike"):
            return 0.0
        if rating_lower in ("neutral", "okay", "mixed"):
            return 0.5

        # Handle numeric ratings
        try:
            numeric = float(rating)
            # Handle 1-5 scale
            if 1 <= numeric <= 5:
                return (numeric - 1) / 4
            # Handle 0-10 scale
            if 0 <= numeric <= 10:
                return numeric / 10
            # Handle 0-100 scale
            if 0 <= numeric <= 100:
                return numeric / 100
            # Handle 0-1 scale
            if 0 <= numeric <= 1:
                return numeric
        except ValueError:
            pass

        # Default to neutral
        logger.warning(f"Unknown rating format: {rating}, defaulting to 0.5")
        return 0.5

    def get_stats(self) -> dict[str, Any]:
        """Get feedback collection statistics."""
        return {
            "eval_feedbacks_submitted": self._stats["eval_feedbacks_submitted"],
            "trace_feedbacks_submitted": self._stats["trace_feedbacks_submitted"],
            "span_feedbacks_submitted": self._stats["span_feedbacks_submitted"],
            "total_feedbacks": sum(self._stats.values()),
        }
