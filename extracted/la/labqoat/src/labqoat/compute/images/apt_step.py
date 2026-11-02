"""Exact system packages installed against the managed Debian snapshot."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AptStep:
    """Retain version-qualified Debian package requests in their authored order."""

    packages: tuple[str, ...]
