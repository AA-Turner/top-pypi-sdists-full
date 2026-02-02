"""
Evaluator and grading utilities.

Supports registry-based graders and metric-based grading.
Provides async and sync evaluation APIs.
"""

import importlib.util
import logging
import math
import numbers
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

import pandas as pd

from dslighting.benchmark.core.evaluator import BaseBenchmarkEvaluator
from dslighting.benchmark.grading.task import Task
from dslighting.benchmark.grading.metrics import grade_submission

logger = logging.getLogger(__name__)


def _load_registry_grade_fn(
    registry_dir: Path,
    grade_fn_str: Optional[str],
) -> Optional[Callable[..., Any]]:
    if not grade_fn_str:
        return None

    grade_py = registry_dir / "grade.py"
    if not grade_py.exists():
        return None

    func_name = "grade"
    if ":" in grade_fn_str:
        _, func_name = grade_fn_str.split(":", 1)
        func_name = func_name.strip() or "grade"
    else:
        func_name = grade_fn_str.strip() or "grade"

    spec = importlib.util.spec_from_file_location("registry_grade_module", str(grade_py))
    if spec is None or spec.loader is None:
        return None

    grade_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(grade_module)

    if not hasattr(grade_module, func_name):
        return None

    return getattr(grade_module, func_name)


def _normalize_score(result: Any) -> float:
    if isinstance(result, numbers.Number):
        value = float(result)
        try:
            if math.isnan(value):
                raise ValueError(
                    "Grade returned NaN. This usually means submission and answers "
                    "do not align (e.g., no matching IDs)."
                )
        except TypeError:
            pass
        return value

    if isinstance(result, dict):
        for key in ("score", "accuracy", "metric"):
            if key in result and isinstance(result[key], numbers.Number):
                return float(result[key])
        for value in result.values():
            if isinstance(value, numbers.Number):
                return float(value)

    raise ValueError(f"Unsupported grade result type: {type(result).__name__}")


def call_registry_grade_fn(
    grade_fn: Callable[..., Any],
    submission_path: Path,
    answers_path: Path,
) -> float:
    """
    Call a registry grade function with DataFrames only.
    Supports return values as float or dict.
    """
    submission_df = pd.read_csv(submission_path)
    answers_df = pd.read_csv(answers_path)
    try:
        result = grade_fn(submission_df, answers_df)
    except TypeError as exc:
        raise TypeError(
            "grade() must accept (submission_df, answers_df). "
            "Update the registry grader signature."
        ) from exc
    return _normalize_score(result)


class Evaluator(BaseBenchmarkEvaluator):
    """
    Grading evaluator for submissions.

    Can evaluate using registry-provided grade.py or built-in metrics.

    Example:
        >>> # Config-driven evaluation
        >>> evaluator = Evaluator(
        ...     config={
        ...         "metric": "rmsle",
        ...         "submission_file": "submission.csv",
        ...         "ground_truth_file": "test.csv"
        ...     },
        ...     workspace=workspace,
        ...     benchmark_path=benchmark_path
        ... )
        >>> result = await evaluator.evaluate()
        >>>
        >>> # Registry-based evaluation
        >>> evaluator = Evaluator.from_registry(
        ...     task_id="bike-sharing-demand",
        ...     registry_parent_dir="dslighting/registry",
        ...     data_parent_dir="data/competitions",
        ...     workspace=workspace
        ... )
        >>> result = await evaluator.evaluate()
        >>>
        >>> # Sync evaluation for a submission file
        >>> score = evaluator.evaluate_sync(submission_path)
    """

    def __init__(
        self,
        workspace: Optional[Any] = None,
        benchmark_path: Optional[Path] = None,
        benchmark_config: Optional[Dict[str, Any]] = None,
        task: Optional[Task] = None,
        registry_dir: Optional[Path] = None,
        registry_grade_fn: Optional[Callable[..., Any]] = None,
    ):
        """
        Initialize Evaluator

        Args:
            workspace: Optional workspace (used to resolve artifact paths).
            benchmark_path: Benchmark directory.
            benchmark_config: Benchmark configuration.
            task: Optional Task loaded from registry.
        """
        # Support passing config directly as the first argument.
        # If workspace is a dict and no benchmark_path/task is provided, treat it as config.
        if workspace is not None and isinstance(workspace, dict) and benchmark_path is None and task is None:
            # Backward-compatible: workspace argument is actually config.
            benchmark_config = workspace
            workspace = None

        # Normalize config and initialize base evaluator.
        config = benchmark_config or {}
        super().__init__(
            workspace=workspace,
            benchmark_path=benchmark_path or Path("."),
            benchmark_config=config
        )

        self.task = task
        self.registry_dir = registry_dir
        self.registry_grade_fn = registry_grade_fn

        # Log task initialization.
        if self.task:
            logger.debug(f"Initialized with task: {self.task.task_id}")

    @classmethod
    def from_registry(
        cls,
        task_id: str,
        registry_parent_dir: Union[str, Path],
        data_parent_dir: Union[str, Path],
        workspace: Optional[Any] = None,
    ) -> "Evaluator":
        """
        Create evaluator from registry.

        Args:
            task_id: Task ID
            registry_parent_dir: Registry base directory.
            data_parent_dir: Data base directory.
            workspace: Optional workspace.

        Returns:
            Evaluator instance
        """
        registry_dir = Path(registry_parent_dir) / task_id
        data_dir = Path(data_parent_dir) / task_id

        registry_grade_fn = None
        config_path = registry_dir / "config.yaml"
        if config_path.exists():
            try:
                import yaml
                with open(config_path, "r") as f:
                    config = yaml.safe_load(f)
                grade_fn_str = config.get("grader", {}).get("grade_fn")
                registry_grade_fn = _load_registry_grade_fn(registry_dir, grade_fn_str)
                if registry_grade_fn:
                    logger.info(f"Loaded registry grade function from {registry_dir}")
            except Exception as e:
                logger.debug(f"Failed to load registry grade function: {e}")

        # Load task
        task = Task.from_registry(
            registry_dir=Path(registry_parent_dir),
            task_id=task_id,
            data_dir=Path(data_parent_dir)
        )

        if task is None:
            raise ValueError(f"Could not load task '{task_id}' from registry")

        logger.info(f"Loaded task '{task_id}' from registry")

        # Build evaluator using registry task.
        return cls(
            workspace=workspace,
            benchmark_path=data_dir,
            benchmark_config=None,
            task=task,
            registry_dir=registry_dir,
            registry_grade_fn=registry_grade_fn,
        )

    async def evaluate(self) -> Dict[str, Any]:
        """
        Evaluate the current benchmark task.

        Returns:
            Result dict with score or error.
        """
        # Resolve submission/ground-truth paths and metric.
        if self.task:
            # Use registry task metadata.
            submission_filename = self.config.get("submission_file", "submission.csv")
            submission_path = self._get_submission_path(submission_filename)
            ground_truth_path = self.task.answers_file
            metric = self.task.metric
            id_column = self.task.id_column
            target_column = self.task.target_column
        else:
            # Use config-based metadata.
            submission_filename = self.config.get("submission_file", "submission.csv")
            submission_path = self._get_submission_path(submission_filename)
            ground_truth_filename = self.config.get("ground_truth_file")
            ground_truth_path = self.benchmark_path / ground_truth_filename
            metric = self.config.get("metric", "rmsle")
            id_column = None
            target_column = None

        # Validate files exist.
        if not submission_path.exists():
            logger.error(f"Submission file not found: {submission_path}")
            return {"error": "Submission file not found"}

        if not ground_truth_path.exists():
            logger.error(f"Ground truth file not found: {ground_truth_path}")
            return {"error": "Ground truth file not found"}

        # Perform evaluation.
        try:
            if self.registry_grade_fn and self.task:
                score = call_registry_grade_fn(
                    self.registry_grade_fn,
                    submission_path=submission_path,
                    answers_path=ground_truth_path,
                )
                logger.info(f"Registry evaluation successful. Score: {score:.4f}")
                return {"score": score}

            score = self._evaluate_files(
                submission_path=submission_path,
                ground_truth_path=ground_truth_path,
                metric=metric,
                id_column=id_column,
                target_column=target_column,
            )

            logger.info(f"Evaluation successful. Metric '{metric}': {score:.4f}")
            return {metric: score}

        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            return {"error": str(e)}

    def evaluate_sync(
        self,
        submission_path: Union[str, Path],
    ) -> float:
        """
        Evaluate a submission file synchronously.

        Args:
            submission_path: Path to submission file.

        Returns:
            Score (or 0.0 on failure).
        """
        if not self.task:
            raise RuntimeError("evaluate_sync() requires task loaded from registry. Use from_registry() first.")

        submission_path = Path(submission_path)
        if not submission_path.exists():
            logger.error(f"Submission file not found: {submission_path}")
            return 0.0

        try:
            if self.registry_grade_fn and self.task:
                score = call_registry_grade_fn(
                    self.registry_grade_fn,
                    submission_path=submission_path,
                    answers_path=self.task.answers_file,
                )
                logger.info(f"Registry evaluation successful. Score: {score:.4f}")
                return score

            score = self._evaluate_files(
                submission_path=submission_path,
                ground_truth_path=self.task.answers_file,
                metric=self.task.metric,
                id_column=self.task.id_column,
                target_column=self.task.target_column,
            )
            return score

        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            return 0.0

    def _get_submission_path(self, filename: str) -> Path:
        """Resolve submission path from workspace or local path."""
        if self.workspace:
            return self.workspace.get_path("artifacts") / filename
        else:
            # Fall back to local path.
            return Path(filename)

    def _evaluate_files(
        self,
        submission_path: Path,
        ground_truth_path: Path,
        metric: str,
        id_column: Optional[str] = None,
        target_column: Optional[str] = None,
    ) -> float:
        """
        Evaluate submission and ground-truth files with a metric.

        Args:
            submission_path: Path to submission file.
            ground_truth_path: Path to ground-truth file.
            metric: Metric name.
            id_column: Optional ID column.
            target_column: Optional target column.

        Returns:
            Score value.
        """
        # Load CSV files.
        submission_df = pd.read_csv(submission_path)
        ground_truth_df = pd.read_csv(ground_truth_path)

        # Grade using metric helper.
        return grade_submission(
            submission_df=submission_df,
            ground_truth_df=ground_truth_df,
            metric=metric,
            id_column=id_column,
            target_column=target_column,
        )


# Compatibility alias.
KaggleEvaluator = Evaluator
