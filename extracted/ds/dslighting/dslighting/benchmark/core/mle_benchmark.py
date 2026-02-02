"""
MLE-Bench Lite Benchmark

Lightweight benchmark built on top of MLE-Bench.
"""

import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import yaml

from dslighting.benchmark.core.benchmark import BaseBenchmark
from dsat.models.task import TaskDefinition

logger = logging.getLogger(__name__)


class MLELiteBenchmark(BaseBenchmark):
    """
    MLE-Bench Lite benchmark.

    Combines:
    1. BaseBenchmark (DSLighting):
       - Task list and evaluation loop.
       - Result aggregation and stats.
       - CSV/JSON output.

    2. MLE-Bench (optional):
       - Task loading from registry.
       - Dataset preparation checks.
       - Optional grading integration.

    Example:
        >>> # Default competitions
        >>> benchmark = MLELiteBenchmark()
        >>> results = await benchmark.run_evaluation(eval_fn)
        >>>
        >>> # Custom competitions
        >>> benchmark = MLELiteBenchmark(
        ...     competitions=["bike-sharing-demand", "titanic"]
        ... )
        >>> results = await benchmark.run_evaluation(eval_fn)
    """

    # Default competition list.
    DEFAULT_COMPETITIONS = [
        "bike-sharing-demand",
        "titanic",
        "house-prices",
        "new-york-city-taxi-fare-prediction",
        "tabular-playground-series-dec-2021",
        "histopathologic-cancer-detection",
        "aptos2019-blindness-detection",
        "spooky-author-identification",
        "us-patent-phrase-to-phrase-matching",
        "google-quest-challenge",
    ]

    def __init__(
        self,
        competitions: Optional[List[str]] = None,
        name: str = "mle-lite",
        log_path: str = "runs/benchmarks/mle-lite",
        data_dir: Optional[Path] = None,
    ):
        """
        Initialize MLE-Bench Lite

        Args:
            competitions: List of competition IDs.
            name: Benchmark name.
            log_path: Output directory.
            data_dir: data directory
        """
        # Use default competitions if none provided.
        self.competitions = competitions or self.DEFAULT_COMPETITIONS

        # data directory
        if data_dir is None:
            data_dir = Path("data/competitions")

        self.data_dir = Path(data_dir)

        # Initialize MLE-Bench integration (if available).
        self._init_mlebench()

        # Convert competitions to TaskDefinition list.
        tasks = self._convert_to_task_definitions()

        # Initialize BaseBenchmark.
        super().__init__(name, tasks, log_path)

        logger.debug(f"✓ MLE-Lite Benchmark initialized")
        logger.info(f"  Competitions: {len(self.competitions)}")
        logger.info(f"  Data dir: {self.data_dir}")

    def _init_mlebench(self):
        """
        Initialize MLE-Bench integration if available.
        """
        try:
            # Add benchmarks path to sys.path.
            import sys
            benchmarks_path = Path(__file__).parent.parent.parent / "benchmarks"
            if benchmarks_path.exists():
                if str(benchmarks_path) not in sys.path:
                    sys.path.insert(0, str(benchmarks_path))

            # Provide compatibility module name if needed.
            if "mlebench" not in sys.modules:
                try:
                    mod = __import__("benchmarks.mlebench", fromlist=["*"])
                    sys.modules["mlebench"] = mod
                    sys.modules["mlebench.competitions"] = mod.competitions
                except ImportError:
                    pass

            # Import MLE-Bench registry and helpers.
            from mlebench.registry import Registry
            from mlebench.data import is_dataset_prepared

            self.mle_registry = Registry()
            self.mle_registry = self.mle_registry.set_data_dir(self.data_dir)

            self.is_dataset_prepared = is_dataset_prepared

            logger.info(f"✓ MLE-Bench capabilities loaded")

        except ImportError as e:
            logger.warning(f"⚠️  MLE-Bench import failed: {e}")
            logger.warning(f"   Will run without MLE-Bench integration")
            self.mle_registry = None
            self.is_dataset_prepared = None

    def _convert_to_task_definitions(self) -> List[TaskDefinition]:
        """
        Convert competition IDs to TaskDefinition objects.

        Returns:
            TaskDefinition list
        """
        tasks = []

        for comp_id in self.competitions:
            try:
                # Try to load competition metadata from MLE registry.
                if self.mle_registry:
                    try:
                        competition = self.mle_registry.get_competition(comp_id)
                        description = competition.description if hasattr(competition, 'description') else f"Competition: {comp_id}"

                        # GetDataPath
                        public_dir = competition.public_dir if hasattr(competition, 'public_dir') else None
                        private_dir = competition.private_dir if hasattr(competition, 'private_dir') else None

                    except Exception as e:
                        logger.warning(f"  Competition '{comp_id}' not found in MLE registry: {e}")
                        # Fallback to basic metadata.
                        description = f"Competition: {comp_id}"
                        public_dir = None
                        private_dir = None
                else:
                    # No registry available; use basic metadata.
                    description = f"Competition: {comp_id}"
                    public_dir = None
                    private_dir = None

                # Create TaskDefinition
                task = TaskDefinition(
                    task_id=comp_id,
                    task_type="kaggle",
                    payload={
                        "description": description,
                        "data_dir": str(self.data_dir / comp_id),
                        "public_data_dir": str(public_dir) if public_dir else str(self.data_dir / comp_id / "prepared" / "public"),
                        "output_submission_path": str(self.data_dir / comp_id / "submission.csv"),
                    }
                )

                tasks.append(task)

            except Exception as e:
                logger.warning(f"Failed to convert competition '{comp_id}': {e}")
                continue

        logger.info(f"✓ Converted {len(tasks)} competitions to TaskDefinition")

        return tasks

    async def run_evaluation(self, eval_fn: Callable, **kwargs) -> List[Dict[str, Any]]:
        """
        Run evaluation for all competitions.

        Args:
            eval_fn: Evaluatefunction
            **kwargs: Extra parameters for eval_fn.

        Returns:
            Evaluation result list.
        """
        logger.info(f"Running MLE-Lite evaluation with {len(self.tasks)} tasks")

        # Delegate to BaseBenchmark.
        results = await super().run_evaluation(eval_fn, **kwargs)

        # Add MLE-Lite specific post-processing here if needed.

        return results

    def grade_submission(
        self,
        task_id: str,
        submission_path: Path,
    ) -> Optional[float]:
        """
        Grade a submission using MLE-Bench.

        Args:
            task_id: Task ID
            submission_path: Path to submission file.

        Returns:
            Score if available, else None.
        """
        if not self.mle_registry:
            logger.warning("MLE-Bench not available, cannot grade submission")
            return None

        try:
            from mlebench.grade import grade_csv

            # Get competition from registry.
            competition = self.mle_registry.get_competition(task_id)

            # Grading
            report = grade_csv(submission_path, competition)

            return report.score if report.score is not None else None

        except Exception as e:
            logger.error(f"Grading failed for '{task_id}': {e}")
            return None

    @classmethod
    def get_default_competitions(cls) -> List[str]:
        """
        Return default competition list.

        Returns:
            List of competition IDs.
        """
        return cls.DEFAULT_COMPETITIONS.copy()

    @classmethod
    def list_available_competitions(
        cls,
        data_dir: Optional[Path] = None,
    ) -> List[str]:
        """
        List available competitions from a data directory.

        Args:
            data_dir: data directory

        Returns:
            List of competition IDs.
        """
        if data_dir is None:
            data_dir = Path("data/competitions")

        competitions = []

        # Discover competitions with prepared data.
        for comp_dir in data_dir.iterdir():
            if comp_dir.is_dir() and (comp_dir / "prepared").exists():
                competitions.append(comp_dir.name)

        return sorted(competitions)
