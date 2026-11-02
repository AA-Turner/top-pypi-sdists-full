"""Verified SHA-256 content identities."""

import re
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, slots=True)
class Sha256:
    """A lowercase SHA-256 hexadecimal digest."""

    value: str

    def __post_init__(self) -> None:
        """Reject ambiguous or malformed digest encodings."""
        if re.fullmatch(r"[0-9a-f]{64}", self.value) is None:
            raise ValueError("Expected 64 lowercase hexadecimal characters")

    @classmethod
    def parse(cls, value: str) -> Self:
        """Parse one immutable digest."""
        return cls(value)

    def __str__(self) -> str:
        """Return the wire representation."""
        return self.value
