"""
cvc.agent.sandbox — Filesystem sandboxing for CVC Agent.

Restricts file operations to allowed paths. Configurable via settings.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.agent.sandbox")


class Sandbox:
    """Filesystem sandbox that validates paths against allow/deny rules."""

    def __init__(
        self,
        workspace: str | Path,
        allowed_write_paths: list[str] | None = None,
        denied_paths: list[str] | None = None,
    ) -> None:
        self.workspace = Path(workspace).resolve()
        self._allowed_write: list[Path] = []
        self._denied: list[Path] = []

        if allowed_write_paths:
            self._allowed_write = [
                (self.workspace / p).resolve() if not Path(p).is_absolute() else Path(p).resolve()
                for p in allowed_write_paths
            ]

        if denied_paths:
            self._denied = [
                (self.workspace / p).resolve() if not Path(p).is_absolute() else Path(p).resolve()
                for p in denied_paths
            ]

    def can_read(self, path: str | Path) -> bool:
        """Check if a path can be read."""
        resolved = self._resolve(path)
        if not resolved:
            return False
        return not self._is_denied(resolved)

    def can_write(self, path: str | Path) -> bool:
        """Check if a path can be written to."""
        resolved = self._resolve(path)
        if not resolved:
            return False
        if self._is_denied(resolved):
            return False
        # If allowed_write list is configured, path must be under one
        if self._allowed_write:
            return any(
                resolved == allowed or self._is_under(resolved, allowed)
                for allowed in self._allowed_write
            )
        # Default: allow writes within workspace
        return self._is_under(resolved, self.workspace)

    def validate_read(self, path: str | Path) -> str | None:
        """Return error string if read is denied, None if OK."""
        if not self.can_read(path):
            return f"Sandbox: read access denied for {path}"
        return None

    def validate_write(self, path: str | Path) -> str | None:
        """Return error string if write is denied, None if OK."""
        if not self.can_write(path):
            return f"Sandbox: write access denied for {path}"
        return None

    def _resolve(self, path: str | Path) -> Path | None:
        """Resolve a path, returning None if it escapes workspace."""
        try:
            p = Path(path)
            if not p.is_absolute():
                p = self.workspace / p
            return p.resolve()
        except Exception:
            return None

    def _is_under(self, path: Path, parent: Path) -> bool:
        """Check if path is under parent directory."""
        try:
            path.relative_to(parent)
            return True
        except ValueError:
            return False

    def _is_denied(self, path: Path) -> bool:
        """Check if path matches any denied pattern."""
        return any(
            path == denied or self._is_under(path, denied)
            for denied in self._denied
        )
