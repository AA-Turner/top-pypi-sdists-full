"""Intent-driven metric calculation utilities."""

from dataclasses import dataclass
import time
from typing import Callable, Any, Tuple

@dataclass
class MetricInputs:
    quality: float
    quantity: float
    accuracy: float
    complexity: float

def calculate_idm(
    quality: float,
    quantity: float,
    accuracy: float,
    complexity: float,
    time_taken: float,
) -> float:
    """Compute the intent-driven metric."""
    if complexity <= 0 or time_taken <= 0:
        raise ValueError("complexity and time_taken must be positive")
    info_power = quality * quantity * accuracy
    return info_power / (complexity * time_taken)

def timed_idm(
    inputs: MetricInputs,
    fn: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Tuple[float, Any]:
    """Time a function call and compute IDM using provided inputs."""
    start = time.time()
    result = fn(*args, **kwargs)
    duration = time.time() - start
    score = calculate_idm(
        inputs.quality,
        inputs.quantity,
        inputs.accuracy,
        inputs.complexity,
        duration,
    )
    return score, result
