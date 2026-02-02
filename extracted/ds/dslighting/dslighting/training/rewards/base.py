"""
Reward function base classes.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class RewardEvaluator(ABC):
    """Base class for reward evaluators."""

    @abstractmethod
    def evaluate(
        self,
        result: Any,
        task: Dict[str, Any],
    ) -> float:
        """
        Evaluate results and return a reward value.

        Parameters
        ----------
        result : Any
            Agent execution result.
        task : Dict[str, Any]
            Task information.

        Returns
        -------
        float
            Reward value (typically in [0, 1]).
        """
        pass


class MetricBasedReward(RewardEvaluator):
    """
    Metric-based reward function.

    Normalizes metric values into the [0, 1] range.
    """

    def __init__(
        self,
        metric_name: str,
        higher_is_better: bool = True,
        baseline: float = None,
        target: float = None,
    ):
        """
        Parameters
        ----------
        metric_name : str
            Metric name (e.g., "accuracy", "f1", "rmse").
        higher_is_better : bool
            Whether larger is better.
        baseline : float
            Baseline value for normalization.
        target : float
            Target value for normalization.
        """
        self.metric_name = metric_name
        self.higher_is_better = higher_is_better
        self.baseline = baseline
        self.target = target

    def evaluate(self, result, task) -> float:
        # Get metric value.
        metric_value = result.metadata.get(self.metric_name, 0.0)

        # Normalize into [0, 1].
        if self.higher_is_better:
            if self.target is not None and self.baseline is not None:
                reward = (metric_value - self.baseline) / (self.target - self.baseline)
            else:
                # Simple normalization: assume metric is in [0, 1].
                reward = metric_value
        else:
            # For lower-is-better metrics (e.g., RMSE).
            if self.target is not None and self.baseline is not None:
                reward = (self.baseline - metric_value) / (self.baseline - self.target)
            else:
                reward = 1.0 - metric_value

        return float(max(0.0, min(1.0, reward)))


__all__ = [
    "RewardEvaluator",
    "MetricBasedReward",
]
