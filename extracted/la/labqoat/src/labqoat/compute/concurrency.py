"""Hard input slots and demand targets for one reusable worker process."""

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Concurrency:
    """Multiplex synchronous inputs on threads and asynchronous inputs on one event loop."""

    max_inputs: int = 1
    target_inputs: int = 1

    def __post_init__(self) -> None:
        """Keep a positive scaling target within the hard input-slot limit."""
        if type(self.max_inputs) is not int or type(self.target_inputs) is not int:
            raise ValueError("Concurrency values must be integers")
        if not 1 <= self.target_inputs <= self.max_inputs <= 256:
            raise ValueError("Concurrency requires 1 <= target_inputs <= max_inputs <= 256")
