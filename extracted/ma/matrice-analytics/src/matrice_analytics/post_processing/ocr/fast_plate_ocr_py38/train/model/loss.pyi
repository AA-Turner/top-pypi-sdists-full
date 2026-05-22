"""Auto-generated stub for module: loss."""
from typing import Any

# Functions
def cce_loss(vocabulary_size: int, label_smoothing: float = 0.01) -> Any:
    """
    Categorical cross-entropy loss.
    """
    ...
def focal_cce_loss(vocabulary_size: int, alpha: float = 0.25, gamma: float = 2.0, label_smoothing: float = 0.01) -> Any:
    """
    Categorical focal cross-entropy loss.
    """
    ...
