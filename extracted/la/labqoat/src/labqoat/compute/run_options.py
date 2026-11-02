"""Explicit submission configuration independent of the captured authored callable."""

from dataclasses import dataclass

from labqoat.authoring.resources import Resources


@dataclass(frozen=True)
class RunOptions:
    """Capture repeatable host operation identity, numerical seed and environment resource selection."""

    key: str | None = None
    seed: int = 0
    resources: Resources | None = None
    location: str | None = None

    def __post_init__(self) -> None:
        """Reject invalid options before source capture or network effects."""
        if self.key is not None and not 1 <= len(self.key.encode()) <= 200:
            raise ValueError("Run operation keys must contain 1..200 UTF-8 bytes")
        if type(self.seed) is not int or not 0 <= self.seed < 2**32:
            raise ValueError("Run seeds must be unsigned 32-bit integers")
