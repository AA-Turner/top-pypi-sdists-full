"""
Training dataset converter.
"""
from typing import List, Dict, Any
import pandas as pd
from pathlib import Path


class DatasetConverter:
    """
    Convert DSLighting tasks into Agent-Lightning training format.

    Output format:
    [
        {
            "task_id": "bike-sharing-demand",
            "data_dir": "/path/to/data",
            "metadata": {...}
        },
        ...
    ]
    """

    def __init__(
        self,
        data_parent_dir: str,
        registry_parent_dir: str,
    ):
        self.data_parent_dir = Path(data_parent_dir)
        self.registry_parent_dir = Path(registry_parent_dir)

    def from_task_list(
        self,
        task_ids: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Create a training dataset from a list of task IDs.

        Parameters
        ----------
        task_ids : List[str]
            List of task IDs.

        Returns
        -------
        List[Dict[str, Any]]
            Training dataset.
        """
        dataset = []

        for task_id in task_ids:
            task_entry = {
                "task_id": task_id,
                "data_dir": str(self.data_parent_dir / task_id),
                "metadata": self._load_task_metadata(task_id),
            }
            dataset.append(task_entry)

        return dataset

    def from_registry(self) -> List[Dict[str, Any]]:
        """
        Load all tasks from the registry directory.

        Returns
        -------
        List[Dict[str, Any]]
            Training dataset for all tasks.
        """
        task_dirs = [d for d in self.registry_parent_dir.iterdir() if d.is_dir()]
        task_ids = [d.name for d in task_dirs]
        return self.from_task_list(task_ids)

    def from_parquet(
        self,
        parquet_path: str,
    ) -> List[Dict[str, Any]]:
        """
        Load a training dataset from a Parquet file.

        Parameters
        ----------
        parquet_path : str
            Path to Parquet file.

        Returns
        -------
        List[Dict[str, Any]]
            Training dataset.
        """
        df = pd.read_parquet(parquet_path)
        return df.to_dict("records")

    def _load_task_metadata(self, task_id: str) -> Dict[str, Any]:
        """Load task metadata."""
        import yaml

        config_path = self.registry_parent_dir / task_id / "config.yaml"

        if config_path.exists():
            with open(config_path) as f:
                return yaml.safe_load(f)
        else:
            return {}


__all__ = ["DatasetConverter"]
