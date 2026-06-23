"""
Production Reliability Metric.

Overall production reliability score combining all reliability factors.
Production-grade composite metric with weighted scoring.
"""

import logging
from datetime import datetime
from typing import Any

from aigie.evaluation import EvaluationResult, ScoreType
from aigie.metrics.base import BaseMetric
from aigie.metrics.checkpoint import CheckpointValidityMetric
from aigie.metrics.drift import DriftDetectionMetric
from aigie.metrics.nested import NestedAgentHealthMetric
from aigie.metrics.recovery import RecoverySuccessMetric

logger = logging.getLogger(__name__)


class ProductionReliabilityMetric(BaseMetric):
    """
    Composite metric for overall production reliability.

    Combines multiple reliability factors into a single score:
    - Context drift detection
    - Error recovery success
    - Checkpoint validity
    - Nested agent health

    Designed for production use as a comprehensive reliability indicator.

    Usage:
        metric = ProductionReliabilityMetric(threshold=0.75)
        result = await metric.measure(
            input={"workflow": "..."},
            output={"result": "..."},
            context={...}  # Should include all sub-metric contexts
        )
    """

    def __init__(
        self,
        threshold: float = 0.75,
        name: str | None = None,
        description: str | None = None,
        weights: dict[str, float] | None = None,
    ):
        """
        Initialize production reliability metric.

        Args:
            threshold: Minimum score for reliable production (0.0-1.0)
            name: Metric name (defaults to class name)
            description: Metric description
            weights: Custom weights for sub-metrics (defaults to balanced)
        """
        super().__init__(
            threshold=threshold,
            name=name or "ProductionReliability",
            description=description or "Overall production reliability score",
        )

        # Default weights (must sum to 1.0)
        self.weights = weights or {
            "drift": 0.25,  # Context drift detection
            "recovery": 0.30,  # Error recovery (most important)
            "checkpoint": 0.20,  # Checkpoint validity
            "nested": 0.25,  # Nested agent health
        }

        # Normalize weights
        total_weight = sum(self.weights.values())
        if total_weight > 0:
            self.weights = {k: v / total_weight for k, v in self.weights.items()}

        # Initialize sub-metrics
        self.drift_metric = DriftDetectionMetric(threshold=0.7)
        self.recovery_metric = RecoverySuccessMetric(threshold=0.8)
        self.checkpoint_metric = CheckpointValidityMetric(threshold=0.9)
        self.nested_metric = NestedAgentHealthMetric(threshold=0.7)

    async def measure(
        self, input: Any, output: Any, context: dict[str, Any] | None = None
    ) -> EvaluationResult:
        """
        Measure overall production reliability.

        Args:
            input: Workflow/agent input
            output: Workflow/agent output
            context: Context containing data for all sub-metrics:
                - drift: DriftDetectionMetric context
                - recovery: RecoverySuccessMetric context
                - checkpoint: CheckpointValidityMetric context
                - nested: NestedAgentHealthMetric context

        Returns:
            EvaluationResult with composite reliability score

        Raises:
            TypeError: If context is not a dict
            ValueError: If required context fields are missing
        """
        # Validate context type
        context = self._validate_context(context)

        try:
            # Run all sub-metrics
            sub_results = {}
            sub_scores = {}

            # 1. Drift Detection
            if self.weights.get("drift", 0) > 0:
                try:
                    drift_context = context.get("drift", context)
                    drift_result = await self.drift_metric.measure(input, output, drift_context)
                    sub_results["drift"] = drift_result
                    sub_scores["drift"] = drift_result.score
                except Exception as e:
                    logger.warning(f"Drift metric failed: {e}")
                    sub_scores["drift"] = 0.5  # Neutral score on error

            # 2. Recovery Success
            if self.weights.get("recovery", 0) > 0:
                try:
                    recovery_context = context.get("recovery", context)
                    recovery_result = await self.recovery_metric.measure(
                        input, output, recovery_context
                    )
                    sub_results["recovery"] = recovery_result
                    sub_scores["recovery"] = recovery_result.score
                except Exception as e:
                    logger.warning(f"Recovery metric failed: {e}")
                    sub_scores["recovery"] = 0.5

            # 3. Checkpoint Validity
            if self.weights.get("checkpoint", 0) > 0:
                try:
                    checkpoint_context = context.get("checkpoint", context)
                    checkpoint_result = await self.checkpoint_metric.measure(
                        input, output, checkpoint_context
                    )
                    sub_results["checkpoint"] = checkpoint_result
                    sub_scores["checkpoint"] = checkpoint_result.score
                except Exception as e:
                    logger.warning(f"Checkpoint metric failed: {e}")
                    sub_scores["checkpoint"] = 0.5

            # 4. Nested Agent Health
            if self.weights.get("nested", 0) > 0:
                try:
                    nested_context = context.get("nested", context)
                    nested_result = await self.nested_metric.measure(input, output, nested_context)
                    sub_results["nested"] = nested_result
                    sub_scores["nested"] = nested_result.score
                except Exception as e:
                    logger.warning(f"Nested metric failed: {e}")
                    sub_scores["nested"] = 0.5

            # Calculate weighted composite score
            composite_score = sum(
                sub_scores.get(metric, 0.5) * weight for metric, weight in self.weights.items()
            )

            # Determine reliability level
            if composite_score >= 0.9:
                reliability_level = "excellent"
            elif composite_score >= 0.8:
                reliability_level = "good"
            elif composite_score >= 0.7:
                reliability_level = "acceptable"
            elif composite_score >= 0.6:
                reliability_level = "degraded"
            else:
                reliability_level = "poor"

            # Build explanation
            explanation_parts = [
                f"Production reliability: {reliability_level}",
                f"Composite score: {composite_score:.2f}",
            ]
            for metric, score in sub_scores.items():
                explanation_parts.append(f"{metric}: {score:.2f}")

            return EvaluationResult(
                score=composite_score,
                score_type=ScoreType.CUSTOM,
                explanation=" | ".join(explanation_parts),
                metadata={
                    "reliability_level": reliability_level,
                    "composite_score": composite_score,
                    "sub_scores": sub_scores,
                    "weights": self.weights,
                    "sub_results": {
                        k: {"score": v.score, "explanation": v.explanation, "metadata": v.metadata}
                        for k, v in sub_results.items()
                    },
                    "timestamp": datetime.utcnow().isoformat(),
                },
            )

        except Exception as e:
            logger.error(
                f"ProductionReliabilityMetric: Error measuring reliability: {e}", exc_info=True
            )
            return EvaluationResult(
                score=0.5,
                score_type=ScoreType.CUSTOM,
                explanation=f"Error evaluating production reliability: {e!s}",
                metadata={"error": True, "timestamp": datetime.utcnow().isoformat()},
            )
