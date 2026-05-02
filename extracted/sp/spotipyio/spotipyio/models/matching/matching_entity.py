from dataclasses import dataclass, fields
from typing import Optional


@dataclass
class MatchingEntity:
    track: Optional[str] = None
    artist: Optional[str] = None

    def __post_init__(self):
        self._validate_input()

    def _validate_input(self) -> None:
        if all(getattr(self, field.name) is None for field in fields(self)):
            raise ValueError("At least one matching candidate field must be supplied")
