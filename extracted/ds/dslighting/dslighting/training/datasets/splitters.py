"""
Train/validation split utilities.
"""
from typing import List, Dict, Any, Tuple
import random


def train_test_split_tasks(
    tasks: List[Dict[str, Any]],
    test_size: float = 0.2,
    random_state: int = 42,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
    Split task list into train and test sets.

    Parameters
    ----------
    tasks : List[Dict[str, Any]]
        Task list.
    test_size : float
        Test set ratio.
    random_state : int
        Random seed.

    Returns
    -------
    train_tasks : List[Dict[str, Any]]
        Training tasks.
    test_tasks : List[Dict[str, Any]]
        Test tasks.
    """
    random.seed(random_state)
    shuffled = tasks.copy()
    random.shuffle(shuffled)

    split_idx = int(len(shuffled) * (1 - test_size))
    train_tasks = shuffled[:split_idx]
    test_tasks = shuffled[split_idx:]

    return train_tasks, test_tasks


__all__ = ["train_test_split_tasks"]
