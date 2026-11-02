"""Typed terminal execution failure retaining the authoritative Run and its diagnostics."""

from labqoat._generated.run import Run
from labqoat.errors.api_error import ApiError


class RunFailedError(ApiError):
    """Keep failed, cancelled and partially failed execution evidence available to SDK callers."""

    def __init__(self, run: Run) -> None:
        """Describe the terminal state while preserving its full generated resource record."""
        failure = run.failure_detail or {}
        detail = failure.get("detail") or failure.get("reason")
        stage = f" while {failure['stage']}" if failure.get("stage") and not failure.get("detail") else ""
        cause = f" {detail}{stage}" if isinstance(detail, str) and detail else ""
        super().__init__(f"Run {run.id} ended with status {run.status}.{cause}")
        self.run = run
