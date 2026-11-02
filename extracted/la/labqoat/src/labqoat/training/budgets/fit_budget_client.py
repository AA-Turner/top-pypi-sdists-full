"""Typed worker-only fit grants and exact usage-report replay."""

import time
from dataclasses import dataclass

from labqoat.training.budgets.fit_grant import FitGrant
from labqoat.training.budgets.fit_report import FitReport
from labqoat.worker.replay_request import ReplayRequest
from labqoat.worker.scoped_api import ScopedApi


@dataclass(frozen=True)
class FitBudgetClient:
    """Bind every fit interval to one immutable run, attempt and fence."""

    api: ScopedApi
    run_id: str
    attempt_id: str
    fence: int

    def grant(self, key: str, duration_ms: int = 30_000) -> FitGrant:
        """Preserve the first request time through retries so response loss cannot extend local expiry."""
        if not isinstance(key, str) or not 1 <= len(key.encode()) <= 200:
            raise ValueError("Fit grant key must contain 1 to 200 bytes")
        if type(duration_ms) is not int or not 1 <= duration_ms <= 30_000:
            raise ValueError("Fit grant duration must be between 1 and 30000 milliseconds")
        requested_at = time.monotonic()
        response = ReplayRequest(self.api).send("/api/v1/worker/fit/grants", {"key": key, "duration_ms": duration_ms})
        grant = FitGrant.capture(response, requested_at, time.monotonic())
        self._authorize(grant)
        return grant

    def report(self, grant: FitGrant, report: FitReport) -> str:
        """Replay one sequence exactly and verify the returned durable receipt before advancing."""
        self._authorize(grant)
        body = report.to_dict()
        receipt = ReplayRequest(self.api).send(f"/api/v1/worker/fit/grants/{grant.id}/reports", dict(body))
        expected = body | {"grant_id": grant.id}
        if any(receipt.get(key) != value for key, value in expected.items()):
            raise ValueError("Fit usage receipt does not match the submitted report")
        return FitGrant._identity(receipt, "id")

    def _authorize(self, grant: FitGrant) -> None:
        """Reject a confused or stale response even when the transport authenticated successfully."""
        if (grant.run_id, grant.attempt_id, grant.fence) != (self.run_id, self.attempt_id, self.fence):
            raise ValueError("Fit grant belongs to a different execution generation")
