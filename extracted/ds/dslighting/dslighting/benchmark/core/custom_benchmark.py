"""
Custom Benchmark

Benchmark for user-defined task lists.
"""

import logging
from typing import Dict, List

from dslighting.benchmark.core.benchmark import BaseBenchmark
from dsat.models.task import TaskDefinition

logger = logging.getLogger(__name__)


class CustomBenchmark(BaseBenchmark):
    """
    Custom benchmark based on a provided list of tasks.

    Use this when you want full control over tasks and evaluation.

    Example:
        >>> tasks = [task1, task2, task3]
        >>> benchmark = CustomBenchmark("my-benchmark", tasks)
        >>> results = await benchmark.run_evaluation(eval_fn)
        >>> stats = benchmark.get_statistics()
    """

    def __init__(
        self,
        name: str,
        tasks: List[TaskDefinition],
        log_path: str = "runs/benchmarks/custom",
    ):
        """
        Initialize the custom benchmark.

        Args:
            name: Benchmark name.
            tasks: Tasklist
            log_path: Output log directory.
        """
        super().__init__(name, tasks, log_path)

        logger.debug(f"✓ Custom Benchmark initialized: {name}")
        logger.info(f"  Tasks: {len(tasks)}")

    async def run_evaluation(self, eval_fn, **kwargs) -> List[Dict]:
        """
        Run evaluation for all tasks.

        Uses BaseBenchmark logic but allows custom eval_fn.
        """
        return await super().run_evaluation(eval_fn, **kwargs)
