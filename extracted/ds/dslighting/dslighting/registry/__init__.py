"""
DSLighting Registry - Task configuration loader

Load task configuration files (config.yaml) and description files (description.md).
"""

import logging
from pathlib import Path
from typing import Dict, Optional, Any

import yaml

logger = logging.getLogger(__name__)


def load_task_config(task_id: str) -> Dict[str, Any]:
    """
    Load task configuration.

    Args:
        task_id: Task ID (e.g. "bike-sharing-demand").

    Returns:
        Configuration dict containing:
        - data_path: Data directory path.
        - description: Path to description.md.
        - task_description: Task description text (if description.md exists).
        - dataset: Dataset config (sample_submission, answers, etc.).
        - grader: Grader configuration.

    Raises:
        FileNotFoundError: If task config does not exist.
    """
    # Locate registry directory.
    registry_dir = Path(__file__).parent
    task_dir = registry_dir / task_id

    if not task_dir.exists():
        raise FileNotFoundError(f"Task configuration not found: {task_id}")

    # Load config.yaml.
    config_file = task_dir / "config.yaml"
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # Add description.md path.
    description_file = task_dir / "description.md"
    if description_file.exists():
        config["description"] = str(description_file)
        # Also load description contents into task_description.
        with open(description_file, 'r', encoding='utf-8') as f:
            config["task_description"] = f.read()
    else:
        logger.warning(f"Description file not found: {description_file}")
        config["description"] = None
        config["task_description"] = config.get("name", task_id)

    # Add data path.
    # Try multiple possible data directories.
    data_parent_dir = None

    # Candidate parent directories.
    possible_parents = [
        # Current project's data/competitions/
        Path.cwd() / "data" / "competitions",
        # DSLighting package's data/competitions/
        Path(__file__).parent.parent.parent / "data" / "competitions",
        # MLE-Bench competitions/
        Path(__file__).parent.parent.parent / "benchmarks" / "mlebench" / "competitions",
        # Absolute path (local override)
        Path("/Users/liufan/Applications/Github/dslighting/data/competitions"),
    ]

    for parent_dir in possible_parents:
        data_path = parent_dir / task_id
        if data_path.exists():
            data_parent_dir = data_path
            logger.info(f"Found data directory: {data_parent_dir}")
            break

    if data_parent_dir:
        config["data_path"] = str(data_parent_dir)
    else:
        logger.warning(f"Could not find data directory for task: {task_id}")
        config["data_path"] = None

    logger.debug(f"Loaded task config: {task_id}")
    return config


def list_available_tasks() -> list:
    """
    List all available tasks.

    Returns:
        List of task IDs.
    """
    registry_dir = Path(__file__).parent
    task_dirs = [d.name for d in registry_dir.iterdir() if d.is_dir() and not d.name.startswith('_')]
    return sorted(task_dirs)
