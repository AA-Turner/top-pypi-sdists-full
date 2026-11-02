"""Evidence-backed reconciliation of unknown historical scientific usage."""

from __future__ import annotations

from urllib.parse import urlencode
from uuid import uuid4
from typing import TYPE_CHECKING

from labqoat._generated.budget_reconciliation_request import BudgetReconciliationRequest
from labqoat._generated.fit_budget_history import FitBudgetHistory
from labqoat._generated.fit_budget_intervals import FitBudgetIntervals
from labqoat._generated.budget_adjustment import BudgetAdjustment
from labqoat._generated.budget_adjustment_request import BudgetAdjustmentRequest
from labqoat.runs.budget_adjustment_client import BudgetAdjustmentClient
from labqoat.base_client import BaseClient
from labqoat.errors.api_error import ApiError
from labqoat.errors.transport_error import TransportError

if TYPE_CHECKING:
    from labqoat.net.response import Response


class BudgetHistoryClient(BaseClient):
    """Retain original allowances and reuse one mutation identity after transport failures."""

    def intervals(self, run_id: str, *, cursor: str | None = None) -> FitBudgetIntervals:
        """Read bounded original grant evidence and recorded uncertainty adjustments."""
        return BudgetAdjustmentClient(self._transport).intervals(run_id, cursor=cursor)

    def adjust(
        self, run_id: str, request: BudgetAdjustmentRequest, *, operation_key: str | None = None
    ) -> BudgetAdjustment:
        """Correct one conservative expired interval using retained termination evidence."""
        return BudgetAdjustmentClient(self._transport).adjust(run_id, request, operation_key=operation_key)

    def get(self, run_id: str) -> FitBudgetHistory:
        """Read cumulative consumption, uncertainty and the original historical evidence."""
        path = self._path(run_id)
        return self._decode(run_id, path, self.send("GET", path))

    def establish(
        self, run_id: str, request: BudgetReconciliationRequest, *, operation_key: str | None = None
    ) -> FitBudgetHistory:
        """Establish unknown consumption once; never change the retained allowance or known history."""
        key = operation_key if operation_key is not None else request.operation_key or str(uuid4())
        if not 1 <= len(key.encode()) <= 200:
            raise ValueError("operation_key must contain 1 to 200 bytes")
        path = self._path(run_id) + "/history?" + urlencode({"operation_key": key})
        body = request.to_dict()
        body.pop("operation_key", None)
        attempt = 0
        while True:
            try:
                return self._decode(run_id, path, self.send_json("POST", path, body))
            except TransportError:
                if attempt == 2:
                    raise
                attempt += 1

    def _decode(self, run_id: str, path: str, data: Response) -> FitBudgetHistory:
        result = self.decode(data, path, FitBudgetHistory.from_dict)
        if result.run_id != run_id:
            raise ApiError("Fit budget identity mismatch")
        return result

    @staticmethod
    def _path(run_id: str) -> str:
        return f"/api/v1/runs/{BaseClient.encode_ref(run_id)}/fit-budget"
