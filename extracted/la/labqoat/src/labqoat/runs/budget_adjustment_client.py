"""Bounded interval history and evidence-backed corrections of conservative fit charges."""

from urllib.parse import urlencode
from uuid import uuid4

from labqoat._generated.budget_adjustment import BudgetAdjustment
from labqoat._generated.budget_adjustment_request import BudgetAdjustmentRequest
from labqoat._generated.fit_budget_intervals import FitBudgetIntervals
from labqoat.base_client import BaseClient
from labqoat.errors.api_error import ApiError
from labqoat.errors.transport_error import TransportError
from labqoat.json_document import JsonDocument


class BudgetAdjustmentClient(BaseClient):
    """Preserve immutable original reports and retry the exact reviewed correction at most three times."""

    def intervals(self, run_id: str, *, cursor: str | None = None) -> FitBudgetIntervals:
        """Read at most fifty original grants and their separately recorded correction receipts."""
        path = self._path(run_id) + "/intervals"
        if cursor is not None:
            path += "?" + urlencode({"cursor": cursor})
        page = self.decode(self.send("GET", path), path, FitBudgetIntervals.from_dict)
        if page.run_id != run_id:
            raise ApiError("Fit interval history identity mismatch")
        return page

    def adjust(
        self, run_id: str, request: BudgetAdjustmentRequest, *, operation_key: str | None = None
    ) -> BudgetAdjustment:
        """Establish actual consumption of one expired interval without refunding confirmed usage."""
        key = operation_key if operation_key is not None else request.operation_key or str(uuid4())
        if not 1 <= len(key.encode()) <= 200:
            raise ValueError("operation_key must contain 1 to 200 bytes")
        path = self._path(run_id) + "/adjustments?" + urlencode({"operation_key": key})
        body = request.to_dict()
        body.pop("operation_key", None)
        receipt = self._submit(path, body)
        if receipt.run_id != run_id or receipt.request_key != key or receipt.request != body:
            raise ApiError("Fit adjustment receipt does not match the requested correction")
        return receipt

    def _submit(self, path: str, body: JsonDocument) -> BudgetAdjustment:
        """Never mint another mutation key when the first response is lost."""
        attempt = 0
        while True:
            try:
                return self.decode(self.send_json("POST", path, body), path, BudgetAdjustment.from_dict)
            except TransportError:
                if attempt == 2:
                    raise
                attempt += 1

    @staticmethod
    def _path(run_id: str) -> str:
        """Quote the complete run selector before composing an owned REST resource."""
        return f"/api/v1/runs/{BaseClient.encode_ref(run_id)}/fit-budget"
