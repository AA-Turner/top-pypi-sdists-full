"""
Reward function for regression tasks.
"""
from dslighting.training.rewards.base import MetricBasedReward


class RegressionReward(MetricBasedReward):
    """
    Regression reward (uses RMSE; lower is better).
    """

    def __init__(self):
        super().__init__(
            metric_name="rmse",
            higher_is_better=False,
        )


__all__ = ["RegressionReward"]
