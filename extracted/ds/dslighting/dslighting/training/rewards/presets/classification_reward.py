"""
Reward function for classification tasks.
"""
from dslighting.training.rewards.base import MetricBasedReward


class ClassificationReward(MetricBasedReward):
    """
    Classification reward (uses accuracy).
    """

    def __init__(self):
        super().__init__(
            metric_name="accuracy",
            higher_is_better=True,
        )


__all__ = ["ClassificationReward"]
