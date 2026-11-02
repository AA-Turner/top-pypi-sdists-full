"""Explicit replay-sensitive decisions and logical effect identities for retained orchestration."""

from collections.abc import Callable
from dataclasses import dataclass
import re

from labqoat._generated.workflow_decision_receipt import WorkflowDecisionReceipt
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.schemas.identity import Identity
from labqoat.worker.replay_request import ReplayRequest
from labqoat.worker.worker_api import WorkerApi
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass(frozen=True)
class RunWorkflow:
    """Capture external reads, randomness and branch choices before issuing stable child or application effects."""

    api: WorkerApi

    def decide(
        self, key: str, inputs: dict[str, JsonValue], resolve: Callable[[], dict[str, JsonValue]]
    ) -> JsonDocument:
        """Reuse a durable decision without reevaluating its callback; interrupted external reads may repeat."""
        request = self._request("decision/" + key, inputs)
        receipt = self._send(request)
        if not receipt.recorded:
            request["value"] = JsonDocument.expect_dict(resolve())
            receipt = self._send(request)
        return JsonDocument.expect_dict(receipt.value)

    def effect_key(self, key: str, inputs: dict[str, JsonValue]) -> str:
        """Persist an input-bound logical key for an external service that honors idempotency keys."""
        request = self._request("effect/" + key, inputs)
        request["value"] = {}
        return self._send(request).effect_key

    @staticmethod
    def _request(key: str, inputs: dict[str, JsonValue]) -> JsonDocument:
        """Separate decision and effect namespaces while rejecting invalid logical keys locally."""
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,199}", key) is None:
            raise ValueError("Workflow keys must be bounded ASCII logical identifiers")
        return JsonDocument(key=key, input_digest=Identity.digest(inputs))

    def _send(self, request: JsonDocument) -> WorkflowDecisionReceipt:
        """Retry identical bounded bytes and verify that the receipt belongs to the requested decision."""
        if "workflow_decisions" not in self.api.capabilities:
            raise WorkerApiError("Server does not support retained workflow decisions")
        if len(Identity.bytes(request)) > 65536:
            raise ValueError("Workflow decision exceeds 65536 bytes")
        response = ReplayRequest(self.api).send("/api/v1/worker/workflow/decisions", request)
        receipt = WorkflowDecisionReceipt.from_dict(response)
        if receipt.key != request["key"] or receipt.input_digest != request["input_digest"]:
            raise WorkerApiError("Workflow decision receipt changed its logical identity")
        if receipt.recorded and (receipt.id is None or receipt.attempt_id is None or receipt.value is None):
            raise WorkerApiError("Recorded workflow decision is missing durable evidence")
        return receipt
