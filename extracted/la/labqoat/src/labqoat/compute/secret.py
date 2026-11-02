"""Name-only reference to an environment-scoped platform secret."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Secret:
    """Attach a stored bundle to a run without loading credentials into source or publication metadata."""

    name: str

    def __post_init__(self) -> None:
        """Reject invalid resource names without making a network request."""
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,62}", self.name):
            raise ValueError(
                "Secret names must start with a letter or digit and contain 1-63 letters, digits, underscores or hyphens"
            )

    @classmethod
    def from_name(cls, name: str) -> "Secret":
        """Reference an existing secret in the submitting client's selected environment."""
        return cls(name)
