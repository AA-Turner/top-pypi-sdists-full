"""Auto-generated stub for module: metric."""
from typing import Any

# Functions
def cat_acc_metric(max_plate_slots: int, vocabulary_size: int) -> Any:
    """
    Categorical accuracy metric.
    """
    ...
def plate_acc_metric(max_plate_slots: int, vocabulary_size: int) -> Any:
    """
    Plate accuracy metric.
    """
    ...
def plate_len_acc_metric(max_plate_slots: int, vocabulary_size: int, pad_token_index: int) -> Any:
    """
    Plate-length accuracy metric.
    """
    ...
def top_3_k_metric(vocabulary_size: int) -> Any:
    """
    Top 3 K categorical accuracy metric.
    """
    ...
