"""Non-secret CLI profile settings."""

from __future__ import annotations

from dataclasses import dataclass, replace
import math
import re


@dataclass(frozen=True)
class Profile:
    """Named selection of API origin, user, and timeouts."""

    name: str
    base_url: str
    username: str
    timeout_seconds: float = 30.0
    environment: str = "default"

    def __post_init__(self) -> None:
        """Reject invalid deadlines and nonportable environment identifiers before requests."""
        if not math.isfinite(self.timeout_seconds) or self.timeout_seconds <= 0:
            raise ValueError("Request timeout must be a positive finite number")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", self.environment):
            raise ValueError("Environment must contain 1-128 letters, digits, dots, underscores or hyphens")

    @staticmethod
    def default_base_url() -> str:
        """Return the public production endpoint."""
        return "https://app.labqoat.com"

    def with_base_url(self, base_url: str | None) -> Profile:
        """Override the base URL when a flag provides one."""
        if base_url is None:
            return self
        return replace(self, base_url=base_url)
