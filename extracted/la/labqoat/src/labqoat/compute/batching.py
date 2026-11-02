"""An explicitly named vectorized handler for scalar-typed independently owned inputs."""

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Batching:
    """Call the handler with contexts and named arguments as ordered lists, returning one result per input."""

    handler: str
    max_batch_size: int
    wait_ms: int = 10

    def __post_init__(self) -> None:
        """Require a plain local handler name and bounded batch latency and cardinality."""
        if not self.handler.isidentifier() or self.handler.startswith("_"):
            raise ValueError("Batch handler must be a public Python identifier")
        if type(self.max_batch_size) is not int or not 1 <= self.max_batch_size <= 256:
            raise ValueError("Batch size must be an integer between 1 and 256")
        if type(self.wait_ms) is not int or not 0 <= self.wait_ms <= 60000:
            raise ValueError("Batch wait must be an integer between 0 and 60000 milliseconds")
