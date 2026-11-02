"""Structured outcome for the standalone ``--refresh-issue-types`` path.

``RefreshOutcome`` captures the machine-readable result of an ``agdt-setup
--refresh-issue-types`` invocation. It is embedded in the setup report under
``details.refresh_outcome`` so CI pipelines and AI agents can detect the
outcome without parsing stderr.

Nullability rules (FR-007):

- ``success`` => ``reason`` is ``None`` and ``error`` is ``None``.
- ``skipped`` => ``reason`` is a required non-empty string; ``error`` is ``None``.
- ``failed``  => both ``reason`` and ``error`` are required non-empty strings.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

VALID_STATUSES: tuple[str, ...] = ("success", "skipped", "failed")


@dataclass
class RefreshOutcome:
    """Machine-readable outcome of a standalone issue-type refresh.

    Attributes:
        status: One of ``"success"``, ``"skipped"``, or ``"failed"``.
        reason: Machine-readable cause. Required for ``skipped``/``failed``;
            must be ``None`` for ``success``.
        error: Human-readable failure message. Required for ``failed``;
            must be ``None`` for ``success``/``skipped``.
    """

    status: str
    reason: str | None = None
    error: str | None = None

    def __post_init__(self) -> None:
        """Validate the status/reason/error nullability contract."""
        if self.status not in VALID_STATUSES:
            allowed = ", ".join(VALID_STATUSES)
            raise ValueError(f"Invalid refresh outcome status: {self.status!r}. Expected one of: {allowed}")

        if self.status == "success":
            if self.reason is not None:
                raise ValueError("RefreshOutcome with status 'success' must have reason=None")
            if self.error is not None:
                raise ValueError("RefreshOutcome with status 'success' must have error=None")
            return

        if self.status == "skipped":
            if not isinstance(self.reason, str) or not self.reason:
                raise ValueError("RefreshOutcome with status 'skipped' requires a non-empty string reason")
            if self.error is not None:
                raise ValueError("RefreshOutcome with status 'skipped' must have error=None")
            return

        # status == "failed"
        if not isinstance(self.reason, str) or not self.reason:
            raise ValueError("RefreshOutcome with status 'failed' requires a non-empty string reason")
        if not isinstance(self.error, str) or not self.error:
            raise ValueError("RefreshOutcome with status 'failed' requires a non-empty string error")

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict with a stable field order."""
        return {"status": self.status, "reason": self.reason, "error": self.error}

    @classmethod
    def success(cls) -> RefreshOutcome:
        """Build a ``success`` outcome (``reason``/``error`` both ``None``)."""
        return cls(status="success")

    @classmethod
    def skipped(cls, reason: str) -> RefreshOutcome:
        """Build a ``skipped`` outcome with a required *reason*."""
        return cls(status="skipped", reason=reason)

    @classmethod
    def failed(cls, reason: str, error: str) -> RefreshOutcome:
        """Build a ``failed`` outcome with required *reason* and *error*."""
        return cls(status="failed", reason=reason, error=error)
