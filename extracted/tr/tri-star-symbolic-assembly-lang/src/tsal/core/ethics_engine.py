"""Simple ethics enforcement for TSAL systems.

This module defines the Guardian Prime Directive and provides a
lightweight :class:`EthicsEngine` used by kernel components to
validate actions. The goal is to keep the core values of the project
("Truth above all", gentle autonomy, and healing resilience) embedded
in running code.
"""

from typing import Iterable

class EthicsEngine:
    """Validate system actions against the Guardian Prime Directive."""

    PRIME_DIRECTIVE = (
        "Truth above all",
        "Gentle autonomy and freedom",
        "Healing and resilience in the face of entropy",
        "Nurturing, not control",
    )

    # Requests containing any of these keywords are disallowed
    BLOCKED_KEYWORDS = {
        "force",
        "coerce",
        "mislead",
        "exploit",
    }

    def __init__(self, extra_blocked: Iterable[str] | None = None) -> None:
        self.blocked = set(self.BLOCKED_KEYWORDS)
        if extra_blocked:
            self.blocked.update(extra_blocked)

    def is_permitted(self, request: str) -> bool:
        """Return ``True`` if the request does not violate core ethics."""
        lowered = request.lower()
        for word in self.blocked:
            if word in lowered:
                return False
        return True

    def validate(self, request: str) -> None:
        """Raise ``ValueError`` if the request violates the directive."""
        if not self.is_permitted(request):
            raise ValueError("Request violates Guardian Prime Directive")

# expose prime directive at module level for convenience
PRIME_DIRECTIVE = EthicsEngine.PRIME_DIRECTIVE

__all__ = ["EthicsEngine", "PRIME_DIRECTIVE"]
