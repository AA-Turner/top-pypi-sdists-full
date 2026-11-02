"""Keyring backend contract for CLI password storage."""

from __future__ import annotations

from typing import Protocol


class KeyringBackend(Protocol):
    """Password store behind the OS keyring or an in-memory double."""

    def get_keyring(self) -> object:
        """Return the active backend or fail when unavailable."""

    def set_password(self, service: str, username: str, password: str) -> None:
        """Store a password."""

    def get_password(self, service: str, username: str) -> str | None:
        """Load a password, returning None when absent."""

    def delete_password(self, service: str, username: str) -> None:
        """Forget a stored password."""
