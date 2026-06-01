"""
Base metric classes for reliability evaluation.
"""

from abc import ABC, abstractmethod
from typing import Any

from ..evaluation import EvaluationResult
from .types import MetricContextBase


class BaseMetric(ABC):
    """
    Base class for all reliability metrics.

    Focused on production reliability.

    Usage:
        class MyMetric(BaseMetric):
            async def measure(self, input, output, context=None):
                # Calculate metric
                return EvaluationResult(
                    score=0.85,
                    score_type=ScoreType.CUSTOM,
                    explanation="Metric explanation"
                )
    """

    def __init__(
        self, threshold: float = 0.7, name: str | None = None, description: str | None = None
    ):
        """
        Initialize base metric.

        Args:
            threshold: Minimum score to consider metric successful (0.0-1.0)
            name: Metric name (defaults to class name)
            description: Metric description

        Raises:
            ValueError: If threshold is not between 0.0 and 1.0
        """
        # Validate threshold
        if not isinstance(threshold, (int, float)) or not 0.0 <= threshold <= 1.0:
            raise ValueError(
                f"Threshold must be a number between 0.0 and 1.0, got {threshold} (type: {type(threshold).__name__})"
            )

        self.threshold = float(threshold)
        self.name = name or self.__class__.__name__
        self.description = description
        self.score: float | None = None
        self.reason: str | None = None
        self.metadata: dict[str, Any] = {}

    def _validate_context(
        self, context: dict[str, Any] | None, required_fields: list | None = None
    ) -> dict[str, Any]:
        """
        Validate context parameter type and required fields.

        Args:
            context: Context dictionary to validate
            required_fields: List of required field names

        Returns:
            Validated context dictionary

        Raises:
            TypeError: If context is not a dict
            ValueError: If required fields are missing
        """
        if context is None:
            context = {}

        # Type validation
        if not isinstance(context, dict):
            raise TypeError(f"Context must be a dictionary, got {type(context).__name__}")

        # Required fields validation
        if required_fields:
            missing_fields = [field for field in required_fields if field not in context]
            if missing_fields:
                raise ValueError(f"Missing required context fields: {', '.join(missing_fields)}")

        return context

    @abstractmethod
    async def measure(
        self,
        input: Any,
        output: Any,
        context: dict[str, Any] | MetricContextBase | None = None,
    ) -> EvaluationResult:
        """
        Measure the metric.

        Args:
            input: Input data (function input, span input, etc.)
            output: Output data (function output, span output, etc.)
            context: Optional context (trace data, span data, etc.)
                Must be a dict or MetricContextBase TypedDict

        Returns:
            EvaluationResult with score, explanation, and metadata

        Raises:
            TypeError: If context is not a dict
            ValueError: If required context fields are missing
        """
        pass

    def is_successful(self) -> bool:
        """
        Check if metric passes threshold.

        Returns:
            True if score >= threshold, False otherwise
        """
        return self.score is not None and self.score >= self.threshold

    async def evaluate(
        self,
        input: Any,
        output: Any,
        context: dict[str, Any] | MetricContextBase | None = None,
    ) -> EvaluationResult:
        """
        Evaluate and store results.

        This is a convenience method that calls measure() and stores results.

        Args:
            input: Input data
            output: Output data
            context: Optional context

        Returns:
            EvaluationResult
        """
        result = await self.measure(input, output, context)

        # Validate result score
        if not isinstance(result.score, (int, float)) or not 0.0 <= result.score <= 1.0:
            raise ValueError(
                f"Metric {self.name} returned invalid score: {result.score}. "
                f"Score must be between 0.0 and 1.0."
            )

        self.score = float(result.score)
        self.reason = result.explanation
        self.metadata = result.metadata
        return result
