"""
DSLighting Base Benchmark

Base benchmark implementation for running evaluations across tasks.
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import pandas as pd

from dsat.models.task import TaskDefinition

logger = logging.getLogger(__name__)


class BaseBenchmark:
    """
    Base benchmark that evaluates a list of tasks.

    - Runs an async eval_fn for each task.
    - Collects results and computes summary statistics.
    - Saves results to CSV and stats to JSON.

    Example:
        >>> tasks = [task1, task2, task3]
        >>> benchmark = BaseBenchmark("my-benchmark", tasks)
        >>> results = await benchmark.run_evaluation(eval_fn)
        >>> stats = benchmark.get_statistics()
    """

    def __init__(
        self,
        name: str,
        tasks: List[TaskDefinition],
        log_path: str = "runs/benchmarks",
    ):
        """
        Initialize Benchmark

        Args:
            name: Benchmark name.
            tasks: Tasklist（TaskDefinition objectlist）
            log_path: Output directory for logs/results.
        """
        self.name = name
        self.tasks = tasks
        self.log_path = Path(log_path)
        self.results = []

        # Ensure log directory exists.
        self.log_path.mkdir(parents=True, exist_ok=True)

        # resultFilePath
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_path = self.log_path / f"{self.name}_results_{timestamp}.csv"
        self.stats_path = self.log_path / f"{self.name}_stats_{timestamp}.json"

        logger.debug(f"✓ Benchmark initialized: {self.name}")
        logger.info(f"  Tasks: {len(self.tasks)}")
        logger.info(f"  Log path: {self.log_path}")

    async def run_evaluation(self, eval_fn: Callable, **kwargs) -> List[Dict[str, Any]]:
        """
        Run evaluation over all tasks.

        Args:
            eval_fn: Async evaluation function.
            **kwargs: Extra parameters passed to eval_fn.

        Returns:
            Evaluation result list.

        Example:
            >>> async def my_eval_fn(task):
            ...     result = await run_task(task)
            ...     return {"score": result.score, "cost": result.cost}
            >>> results = await benchmark.run_evaluation(my_eval_fn)
        """
        if not self.tasks:
            logger.warning(f"No tasks to evaluate in benchmark '{self.name}'")
            return []

        logger.info(f"Starting evaluation for benchmark '{self.name}' with {len(self.tasks)} tasks")

        results = []
        completed = 0
        failed = 0

        # Iterate tasks sequentially.
        for i, task in enumerate(self.tasks, 1):
            try:
                logger.info(f"[{i}/{len(self.tasks)}] Evaluating task: {task.task_id}")

                # Execute evaluation function.
                result = await eval_fn(task, **kwargs)

                # Validate and record result.
                if isinstance(result, dict):
                    result["task_id"] = task.task_id
                    results.append(result)
                    completed += 1
                else:
                    logger.warning(f"  Invalid result type: {type(result)}")
                    failed += 1

            except Exception as e:
                logger.error(f"  Task '{task.task_id}' failed: {e}")
                failed += 1
                # Record failure.
                results.append({
                    "task_id": task.task_id,
                    "score": None,
                    "error": str(e),
                })

        # Save results and stats.
        self.results = results
        self._save_results(results, **kwargs)

        logger.info(f"Evaluation complete: {completed} succeeded, {failed} failed")

        return results

    def get_statistics(self, results: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Compute summary statistics for results.

        Args:
            results: Optional results list (defaults to self.results).

        Returns:
            Statistics dict (scores, costs, durations, success rate).
        """
        if results is None:
            results = self.results

        if not results:
            return {}

        stats = {
            "total_tasks": len(results),
            "successful_tasks": 0,
            "failed_tasks": 0,
        }

        # Collect metrics.
        scores = []
        costs = []
        durations = []

        for result in results:
            if result.get("score") is not None:
                scores.append(float(result["score"]))
                stats["successful_tasks"] += 1
            else:
                stats["failed_tasks"] += 1

            if result.get("cost") is not None:
                costs.append(float(result["cost"]))

            if result.get("duration") is not None:
                durations.append(float(result["duration"]))

        # Score statistics.
        if scores:
            import numpy as np
            stats["avg_score"] = float(np.mean(scores))
            stats["median_score"] = float(np.median(scores))
            stats["std_score"] = float(np.std(scores))
            stats["min_score"] = float(np.min(scores))
            stats["max_score"] = float(np.max(scores))

        # Cost statistics.
        if costs:
            import numpy as np
            stats["avg_cost"] = float(np.mean(costs))
            stats["total_cost"] = float(np.sum(costs))

        # Duration statistics.
        if durations:
            import numpy as np
            stats["avg_duration"] = float(np.mean(durations))
            stats["total_duration"] = float(np.sum(durations))

        # Success rate.
        stats["success_rate"] = stats["successful_tasks"] / stats["total_tasks"]

        return stats

    def _save_results(self, results: List[Dict], **kwargs):
        """
        Save results and statistics to disk.

        Args:
            results: Evaluateresultlist
            **kwargs: Extra metadata (e.g., model_name).
        """
        try:
            # Convert results to DataFrame.
            df = pd.DataFrame(results)

            # Write CSV.
            df.to_csv(self.results_path, index=False)
            logger.info(f"✓ Results saved to: {self.results_path}")

            # Compute stats.
            stats = self.get_statistics(results)

            # Add metadata.
            stats["benchmark_name"] = self.name
            stats["timestamp"] = datetime.now().isoformat()
            stats["model_name"] = kwargs.get("model_name", "unknown")

            # Write JSON.
            import json
            with open(self.stats_path, "w") as f:
                json.dump(stats, f, indent=2)
            logger.info(f"✓ Statistics saved to: {self.stats_path}")

        except Exception as e:
            logger.error(f"Failed to save results: {e}")

    @classmethod
    def from_config(
        cls,
        name: str,
        config: Dict[str, Any],
        registry_dir: Path,
        data_dir: Path,
    ) -> "BaseBenchmark":
        """
        Create a benchmark from config.

        Args:
            name: Benchmark name.
            config: Configdict/dictionary
            registry_dir: Registry directory.
            data_dir: data directory

        Returns:
            BaseBenchmark instance

        Example:
            >>> config = {
            ...     "tasks": [
            ...         {"task_id": "bike-sharing-demand"},
            ...         {"task_id": "titanic"},
            ...     ]
            ... }
            >>> benchmark = BaseBenchmark.from_config("my-bench", config, registry_dir, data_dir)
        """
        from dslighting.core.data_loader import load_data

        tasks = []

        for task_config in config.get("tasks", []):
            task_id = task_config.get("task_id") or task_config.get("id")

            if not task_id:
                logger.warning(f"Skipping task without task_id: {task_config}")
                continue

            try:
                # LoadData
                loaded_data = load_data(
                    task_id=task_id,
                    registry_parent_dir=str(registry_dir),
                    data_parent_dir=str(data_dir),
                )

                # Create TaskDefinition
                task = TaskDefinition(
                    task_id=task_id,
                    task_type=loaded_data.get_task_type(),
                    payload={
                        "description": loaded_data.description or "",
                        "data_dir": str(loaded_data.data_dir) if loaded_data.data_dir else None,
                    }
                )

                tasks.append(task)

            except Exception as e:
                logger.warning(f"Failed to load task '{task_id}': {e}")
                continue

        logger.info(f"Loaded {len(tasks)} tasks from config")

        return cls(name, tasks)
