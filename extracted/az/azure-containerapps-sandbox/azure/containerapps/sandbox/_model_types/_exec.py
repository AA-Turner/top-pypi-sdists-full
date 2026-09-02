"""Exec result model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecResult:
    """Result of executing a command in a sandbox."""
    exit_code: int = 0
    stdout: str = ""
    stderr: str = ""

    @classmethod
    def _from_dict(cls, d: dict) -> ExecResult:
        return cls(
            exit_code=d.get("exitCode", 0),
            stdout=d.get("stdout", ""),
            stderr=d.get("stderr", ""),
        )
