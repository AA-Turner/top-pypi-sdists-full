"""Callable-owned warm container bounds independent of per-input resource requests."""

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Scaling:
    """Bound demand scaling from zero and retain idle containers for an explicit window."""

    max_containers: int = 10
    buffer_containers: int = 0
    scaledown_window: int = 60

    def __post_init__(self) -> None:
        """Reject impossible or unbounded fleet declarations before publication."""
        values = (self.max_containers, self.buffer_containers, self.scaledown_window)
        if any(type(value) is not int for value in values):
            raise ValueError("Scaling values must be integers")
        if not 0 <= self.max_containers <= 1000:
            raise ValueError("Scaling requires 0 <= max_containers <= 1000")
        if not 0 <= self.buffer_containers <= self.max_containers or not 0 <= self.scaledown_window <= 86400:
            raise ValueError("Scaling buffer and idle window exceed their bounds")
