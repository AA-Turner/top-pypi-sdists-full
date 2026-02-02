# dslighting/benchmark/grader/task.py

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any

import yaml

logger = logging.getLogger(__name__)

@dataclass
class Task:
    """
    Represents a single benchmark task configuration.

    Automatically loads configuration from config.yaml and infers column names.
    """
    task_id: str
    metric: str
    id_column: str
    target_column: str
    answers_file: Path
    description: str

    @classmethod
    def from_registry(cls, registry_dir: Path, task_id: str, data_dir: Path) -> Optional["Task"]:
        """
        Loads a Task from its registry directory.

        Automatically reads config.yaml and infers column names from the answers file.

        Args:
            registry_dir: The parent directory containing all task registries
            task_id: The ID of the task to load
            data_dir: The parent data directory (e.g., 'data/competitions')

        Returns:
            A Task instance, or None if loading fails
        """
        task_registry_path = registry_dir / task_id
        if not task_registry_path.is_dir():
            logger.warning(f"Task registry directory not found: {task_registry_path}")
            return None

        config_path = task_registry_path / "config.yaml"
        if not config_path.exists():
            logger.warning(f"Task config.yaml not found in: {task_registry_path}")
            return None

        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)

            # Read grading info from config
            grader_config = config.get("grader", {})
            metric = grader_config.get("name")
            grade_fn = grader_config.get("grade_fn")
            if not metric:
                if grade_fn:
                    metric = "custom"
                else:
                    raise ValueError("'name' not specified in grader config.")

            # Read dataset info from config
            dataset_config = config.get("dataset", {})
            answers_file_rel = dataset_config.get("answers")
            if not answers_file_rel:
                raise ValueError("'answers' not specified in dataset config.")

            # Resolve answers_file path relative to data_dir
            answers_file_abs = (data_dir / answers_file_rel).resolve()
            if not answers_file_abs.exists():
                # Fallback to standard pattern
                answers_file_abs = (data_dir / task_id / "prepared" / "private" / "test_answer.csv").resolve()
                if not answers_file_abs.exists():
                    raise FileNotFoundError(f"Could not find answers file for task '{task_id}'")

            # Auto-detect ID and target columns
            id_column, target_column = cls._infer_columns(answers_file_abs)

            return cls(
                task_id=task_id,
                metric=metric,
                id_column=id_column,
                target_column=target_column,
                answers_file=answers_file_abs,
                description=config.get("description", f"A competition task: {task_id}")
            )

        except (ValueError, FileNotFoundError, KeyError) as e:
            logger.error(f"Failed to load task '{task_id}': {e}")
            return None

    @staticmethod
    def _infer_columns(answers_file: Path) -> (str, str):
        """
        Auto-detects ID and target columns from an answers CSV file.

        Strategy:
        1. Look for a column with 'id' in its name (case-insensitive)
        2. If not found, assume first column is ID and second is target
        """
        import pandas as pd
        df = pd.read_csv(answers_file, nrows=1)
        columns = df.columns.tolist()

        if len(columns) < 2:
            raise ValueError("Answers file must have at least an ID and a target column.")

        # Try to find ID column
        id_col = next((c for c in columns if 'id' in c.lower()), None)

        if id_col:
            # Target is the other column
            target_col = next((c for c in columns if c != id_col), None)
            if target_col:
                return id_col, target_col

        # Fallback: first column is ID, second is target
        logger.warning("Could not detect ID column. Assuming first column is ID and second is target.")
        return columns[0], columns[1]
