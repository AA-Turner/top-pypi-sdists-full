"""
Kaggle competition reward function.
"""
from dslighting.training.rewards.base import MetricBasedReward


class KaggleReward(MetricBasedReward):
    """
    Kaggle competition reward.

    Uses different metrics depending on task type.
    """

    def __init__(self, task_type: str = "auto"):
        """
        Parameters
        ----------
        task_type : str
            Task type: "classification", "regression", "auto".
        """
        self.task_type = task_type

    def evaluate(self, result, task) -> float:
        # Auto-detect task type.
        if self.task_type == "auto":
            metric_name = self._detect_metric(task)
            higher_is_better = self._is_higher_better(metric_name)
        else:
            metric_name, higher_is_better = self._get_metric_for_type(self.task_type)

        # Create a temporary evaluator.
        evaluator = MetricBasedReward(
            metric_name=metric_name,
            higher_is_better=higher_is_better,
        )
        return evaluator.evaluate(result, task)

    def _detect_metric(self, task):
        """Detect metric based on task metadata."""
        eval_metric = task.get("metadata", {}).get("eval_metric")
        if eval_metric:
            return eval_metric
        return "accuracy"  # Default.

    def _is_higher_better(self, metric_name):
        """Check whether a metric is higher-is-better."""
        higher_better_metrics = {
            "accuracy", "f1", "precision", "recall",
            "auc", "r2", "roc_auc"
        }
        return metric_name in higher_better_metrics

    def _get_metric_for_type(self, task_type):
        """Return metric for a given task type."""
        if task_type == "classification":
            return "accuracy", True
        elif task_type == "regression":
            return "rmse", False
        else:
            return "accuracy", True


__all__ = ["KaggleReward"]
