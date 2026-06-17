"""
Evaluation System for Aigie SDK.

Provides online evaluation scoring with:
- Score attachment to traces/spans
- Feedback collection (thumbs up/down)
- LLM-as-judge evaluators
- Custom evaluator functions
- Score aggregation and analysis
"""

import asyncio
import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

logger = logging.getLogger(__name__)


class ScoreType(str, Enum):
    """Types of evaluation scores."""

    ACCURACY = "accuracy"
    RELEVANCE = "relevance"
    COHERENCE = "coherence"
    FLUENCY = "fluency"
    GROUNDEDNESS = "groundedness"
    HALLUCINATION = "hallucination"
    TOXICITY = "toxicity"
    HELPFULNESS = "helpfulness"
    HARMFULNESS = "harmfulness"
    FEEDBACK = "feedback"  # User feedback scores
    CUSTOM = "custom"


class ScoreDataType(str, Enum):
    """Data type of the score value."""

    NUMERIC = "numeric"  # 0-1 float
    CATEGORICAL = "categorical"  # String categories
    BOOLEAN = "boolean"  # True/False


@dataclass
class Score:
    """
    A score attached to a trace or span.

    This is the primary way to record evaluations, feedback, and ratings.

    Usage:
        # Numeric score
        score = Score(
            name="accuracy",
            value=0.95,
            trace_id="trace-123"
        )

        # Categorical score (user feedback)
        feedback = Score(
            name="user_feedback",
            value="positive",
            data_type=ScoreDataType.CATEGORICAL,
            trace_id="trace-123",
            comment="Great response!"
        )

        # Boolean score
        passed = Score(
            name="passed_test",
            value=True,
            data_type=ScoreDataType.BOOLEAN,
            trace_id="trace-123"
        )
    """

    name: str
    value: float | str | bool
    trace_id: str
    span_id: str | None = None
    data_type: ScoreDataType = ScoreDataType.NUMERIC
    comment: str | None = None
    source: str = "sdk"  # "sdk", "api", "user", "llm-as-judge"
    config_id: str | None = None  # For linking to evaluation configs
    id: str | None = None
    created_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.id = self.id or str(uuid4())
        self.created_at = self.created_at or datetime.utcnow()

        # Auto-detect data type
        if self.data_type == ScoreDataType.NUMERIC and isinstance(self.value, bool):
            self.data_type = ScoreDataType.BOOLEAN
        elif self.data_type == ScoreDataType.NUMERIC and isinstance(self.value, str):
            self.data_type = ScoreDataType.CATEGORICAL

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API."""
        return {
            "id": self.id,
            "name": self.name,
            "value": self.value,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "data_type": self.data_type.value,
            "comment": self.comment,
            "source": self.source,
            "config_id": self.config_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Score":
        """Create from dictionary."""
        return cls(
            id=data.get("id"),
            name=data["name"],
            value=data["value"],
            trace_id=data["trace_id"],
            span_id=data.get("span_id"),
            data_type=ScoreDataType(data.get("data_type", "numeric")),
            comment=data.get("comment"),
            source=data.get("source", "sdk"),
            config_id=data.get("config_id"),
            created_at=datetime.fromisoformat(data["created_at"])
            if data.get("created_at")
            else None,
            metadata=data.get("metadata", {}),
        )


@dataclass
class EvaluationResult:
    """Result of an evaluation."""

    score: float
    score_type: ScoreType
    metadata: dict[str, Any] = field(default_factory=dict)
    explanation: str | None = None
    source: str = "evaluator"

    def to_score(self, name: str, trace_id: str, span_id: str | None = None) -> Score:
        """Convert to a Score object for API submission."""
        return Score(
            name=name,
            value=self.score,
            trace_id=trace_id,
            span_id=span_id,
            data_type=ScoreDataType.NUMERIC,
            comment=self.explanation,
            source=self.source,
            metadata=self.metadata,
        )


class Evaluator:
    """
    Base class for evaluators.

    Usage:
        class MyEvaluator(Evaluator):
            async def evaluate(self, expected, actual) -> EvaluationResult:
                score = 1.0 if expected == actual else 0.0
                return EvaluationResult(
                    score=score,
                    score_type=ScoreType.ACCURACY
                )
    """

    async def evaluate(
        self, expected: Any, actual: Any, context: dict[str, Any] | None = None
    ) -> EvaluationResult:
        """
        Evaluate expected vs actual.

        Args:
            expected: Expected value
            actual: Actual value
            context: Optional context data

        Returns:
            EvaluationResult
        """
        raise NotImplementedError


class EvaluationHook:
    """
    Hook for automatically running evaluations on traces/spans.

    Usage:
        async def accuracy_evaluator(expected, actual):
            return EvaluationResult(
                score=1.0 if expected == actual else 0.0,
                score_type=ScoreType.ACCURACY
            )

        hook = EvaluationHook(
            name="accuracy",
            evaluator=accuracy_evaluator,
            score_type=ScoreType.ACCURACY
        )

        # Register with trace
        async with aigie.trace("workflow") as trace:
            trace.add_evaluation_hook(hook)
            # Evaluation runs automatically on completion
    """

    def __init__(
        self,
        name: str,
        evaluator: Callable | Evaluator,
        score_type: ScoreType = ScoreType.CUSTOM,
        run_on: str = "trace",  # "trace" or "span"
    ):
        """
        Initialize evaluation hook.

        Args:
            name: Hook name
            evaluator: Evaluator function or Evaluator instance
            score_type: Type of score
            run_on: When to run ("trace" or "span")
        """
        self.name = name
        self.evaluator = evaluator
        self.score_type = score_type
        self.run_on = run_on

    async def run(
        self, expected: Any, actual: Any, context: dict[str, Any] | None = None
    ) -> EvaluationResult:
        """
        Run the evaluation.

        Args:
            expected: Expected value
            actual: Actual value
            context: Optional context

        Returns:
            EvaluationResult
        """
        if isinstance(self.evaluator, Evaluator):
            return await self.evaluator.evaluate(expected, actual, context)
        # Assume it's a callable
        if asyncio.iscoroutinefunction(self.evaluator):
            result = await self.evaluator(expected, actual, context)
        else:
            result = self.evaluator(expected, actual, context)

        # Convert to EvaluationResult if needed
        if isinstance(result, EvaluationResult):
            return result
        if isinstance(result, (int, float)):
            return EvaluationResult(score=float(result), score_type=self.score_type)
        return EvaluationResult(score=1.0 if result else 0.0, score_type=self.score_type)


class EvaluationRegistry:
    """Registry for managing evaluations."""

    def __init__(self):
        self._hooks: dict[str, EvaluationHook] = {}

    def register(self, hook: EvaluationHook) -> None:
        """Register an evaluation hook."""
        self._hooks[hook.name] = hook

    def get(self, name: str) -> EvaluationHook | None:
        """Get evaluation hook by name."""
        return self._hooks.get(name)

    def list(self) -> list[EvaluationHook]:
        """List all registered hooks."""
        return list(self._hooks.values())


class ScoreManager:
    """
    Manager for online scoring of traces and spans.

    Provides a simple API for attaching scores to traces.

    Usage:
        manager = ScoreManager(aigie_client)

        # Score a trace
        await manager.score(
            trace_id="trace-123",
            name="accuracy",
            value=0.95,
            comment="High accuracy on factual claims"
        )

        # Record user feedback
        await manager.feedback(
            trace_id="trace-123",
            positive=True,
            comment="User liked the response"
        )

        # LLM-as-judge evaluation
        await manager.llm_evaluate(
            trace_id="trace-123",
            input="What is 2+2?",
            output="4",
            criteria="correctness"
        )
    """

    def __init__(self, aigie_client=None):
        """
        Initialize score manager.

        Args:
            aigie_client: Optional Aigie client instance for API calls
        """
        self.aigie = aigie_client
        self._local_scores: list[Score] = []

    async def score(
        self,
        trace_id: str,
        name: str,
        value: float | str | bool,
        span_id: str | None = None,
        comment: str | None = None,
        source: str = "sdk",
        metadata: dict[str, Any] | None = None,
    ) -> Score:
        """
        Attach a score to a trace or span.

        Args:
            trace_id: ID of the trace to score
            name: Score name (e.g., "accuracy", "relevance")
            value: Score value (float 0-1, string category, or bool)
            span_id: Optional span ID for span-level scoring
            comment: Optional explanation/comment
            source: Score source (sdk, api, user, llm-as-judge)
            metadata: Optional additional metadata

        Returns:
            Score object
        """
        score = Score(
            name=name,
            value=value,
            trace_id=trace_id,
            span_id=span_id,
            comment=comment,
            source=source,
            metadata=metadata or {},
        )

        self._local_scores.append(score)

        # Send to platform if client available
        if self.aigie:
            try:
                await self._send_score(score)
            except Exception as e:
                logger.warning(f"Failed to send score to platform: {e}")

        return score

    async def feedback(
        self,
        trace_id: str,
        positive: bool,
        comment: str | None = None,
        span_id: str | None = None,
        user_id: str | None = None,
    ) -> Score:
        """
        Record user feedback (thumbs up/down).

        Args:
            trace_id: ID of the trace
            positive: True for positive feedback, False for negative
            comment: Optional user comment
            span_id: Optional span ID
            user_id: Optional user ID who provided feedback

        Returns:
            Score object
        """
        return await self.score(
            trace_id=trace_id,
            name="user_feedback",
            value="positive" if positive else "negative",
            span_id=span_id,
            comment=comment,
            source="user",
            metadata={"user_id": user_id} if user_id else {},
        )

    async def thumbs_up(self, trace_id: str, comment: str | None = None) -> Score:
        """Record positive feedback."""
        return await self.feedback(trace_id, positive=True, comment=comment)

    async def thumbs_down(self, trace_id: str, comment: str | None = None) -> Score:
        """Record negative feedback."""
        return await self.feedback(trace_id, positive=False, comment=comment)

    async def rate(
        self, trace_id: str, rating: int, max_rating: int = 5, comment: str | None = None
    ) -> Score:
        """
        Record a numeric rating (e.g., 1-5 stars).

        Args:
            trace_id: ID of the trace
            rating: Rating value (1 to max_rating)
            max_rating: Maximum rating value (default 5)
            comment: Optional comment

        Returns:
            Score object
        """
        # Normalize to 0-1 scale
        normalized = (rating - 1) / (max_rating - 1) if max_rating > 1 else 1.0

        return await self.score(
            trace_id=trace_id,
            name="rating",
            value=normalized,
            comment=comment,
            source="user",
            metadata={"raw_rating": rating, "max_rating": max_rating},
        )

    async def evaluate(
        self,
        trace_id: str,
        evaluator: Callable | Evaluator,
        input_data: Any,
        output_data: Any,
        expected: Any | None = None,
        name: str | None = None,
        span_id: str | None = None,
    ) -> Score:
        """
        Run an evaluator and record the result as a score.

        Args:
            trace_id: ID of the trace
            evaluator: Evaluator function or Evaluator instance
            input_data: Input to the operation being evaluated
            output_data: Output of the operation
            expected: Optional expected output
            name: Optional score name (defaults to evaluator name)
            span_id: Optional span ID

        Returns:
            Score object
        """
        context = {"input": input_data, "output": output_data, "expected": expected}

        if isinstance(evaluator, Evaluator):
            result = await evaluator.evaluate(expected, output_data, context)
            eval_name = name or evaluator.__class__.__name__
        else:
            # Callable evaluator
            if asyncio.iscoroutinefunction(evaluator):
                result = await evaluator(expected, output_data, context)
            else:
                result = evaluator(expected, output_data, context)

            eval_name = name or getattr(evaluator, "__name__", "custom_evaluator")

            # Convert to EvaluationResult if needed
            if not isinstance(result, EvaluationResult):
                if isinstance(result, (int, float)):
                    result = EvaluationResult(score=float(result), score_type=ScoreType.CUSTOM)
                else:
                    result = EvaluationResult(
                        score=1.0 if result else 0.0, score_type=ScoreType.CUSTOM
                    )

        return await self.score(
            trace_id=trace_id,
            name=eval_name,
            value=result.score,
            span_id=span_id,
            comment=result.explanation,
            source="evaluator",
            metadata=result.metadata,
        )

    async def llm_evaluate(
        self,
        trace_id: str,
        input_data: str,
        output_data: str,
        criteria: str = "relevance",
        model: str = "gpt-4o-mini",
        span_id: str | None = None,
    ) -> Score:
        """
        Use LLM-as-judge to evaluate an output.

        Args:
            trace_id: ID of the trace
            input_data: The input/question
            output_data: The output/response to evaluate
            criteria: Evaluation criteria (relevance, accuracy, etc.)
            model: Model to use for evaluation
            span_id: Optional span ID

        Returns:
            Score object
        """
        # TODO: Implement actual LLM call when OpenAI client is available
        # For now, return a placeholder
        logger.warning("LLM evaluation requires OpenAI client - returning placeholder")

        return await self.score(
            trace_id=trace_id,
            name=f"llm_{criteria}",
            value=0.0,
            span_id=span_id,
            comment="LLM evaluation not configured",
            source="llm-as-judge",
            metadata={"model": model, "criteria": criteria},
        )

    async def _send_score(self, score: Score) -> None:
        """Record a score locally.

        Scores are not part of the single-immutable-span taxonomy and have no
        wire event type — the prior ``SCORE_CREATE`` emit referenced a
        non-existent enum member (dead/broken). Scores live in
        ``self._local_scores`` and are read back via ``get_scores``.
        """
        if not self.aigie:
            return
        logger.debug("Score recorded locally (no wire emit): %s", score.name)

    def get_scores(self, trace_id: str | None = None) -> list[Score]:
        """Get locally stored scores, optionally filtered by trace ID."""
        if trace_id:
            return [s for s in self._local_scores if s.trace_id == trace_id]
        return self._local_scores.copy()

    def clear(self) -> None:
        """Clear local score cache."""
        self._local_scores.clear()


# Global score manager instance
_global_score_manager: ScoreManager | None = None


def get_score_manager(aigie_client=None) -> ScoreManager:
    """Get the global score manager."""
    global _global_score_manager
    if _global_score_manager is None:
        _global_score_manager = ScoreManager(aigie_client)
    elif aigie_client and not _global_score_manager.aigie:
        _global_score_manager.aigie = aigie_client
    return _global_score_manager


async def score(trace_id: str, name: str, value: float | str | bool, **kwargs) -> Score:
    """
    Quick function to score a trace.

    Usage:
        from aigie import score

        await score("trace-123", "accuracy", 0.95)
    """
    return await get_score_manager().score(trace_id, name, value, **kwargs)


async def feedback(trace_id: str, positive: bool, **kwargs) -> Score:
    """Quick function to record feedback."""
    return await get_score_manager().feedback(trace_id, positive, **kwargs)
