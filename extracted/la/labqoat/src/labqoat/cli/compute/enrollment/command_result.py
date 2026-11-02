"""Captured outcome of one local or remote process."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandResult:
    """Exit status and captured byte streams."""

    returncode: int
    stdout: bytes = b""
    stderr: bytes = b""

    @property
    def ok(self) -> bool:
        """Return whether the process exited successfully."""
        return self.returncode == 0

    @property
    def output(self) -> str:
        """Decode standard output for parsing."""
        return self.stdout.decode(errors="replace").strip()

    def diagnostic(self, limit: int = 600) -> str:
        """Return the tail of standard error, or output when error is empty, for failure messages."""
        text = (self.stderr or self.stdout).decode(errors="replace").strip()
        return text[-limit:] or f"exit status {self.returncode}"
