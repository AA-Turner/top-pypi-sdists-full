"""Recover large retained publications and arguments using current assignment authority."""

from dataclasses import dataclass

from labqoat.json_document import JsonDocument
from labqoat.schemas.identity import Identity
from labqoat.worker.worker_api import WorkerApi
from labqoat.worker.worker_api_error import WorkerApiError
from labqoat.worker.replay_request import ReplayRequest


@dataclass(frozen=True)
class RetainedInputs:
    """Recover executable inputs outside process environment limits and verify their accepted identity."""

    api: WorkerApi

    def capture(self, context: JsonDocument) -> JsonDocument:
        """Fetch the fenced manifest and match the service-injected Run, fence and execution digest."""
        claimed = context.get("worker_protocol", 1) == 2
        response = (
            ReplayRequest(self.api).send(
                "/api/v1/worker/assignments/begin",
                {"recovery_protocol": 1, "distributed_recovery_protocol": 1, "workflow_replay_protocol": 1},
            )
            if claimed
            else self.api.json("GET", "/api/v1/worker/assignments/inputs")
        )
        self.api.capabilities = frozenset(
            JsonDocument.expect_scalar(item, str) for item in JsonDocument.expect_list(response.get("capabilities", []))
        )
        manifest = JsonDocument.expect_dict(response["manifest"])
        if (
            response["run_id"] != context["run_id"]
            or response["fence"] != context["fence"]
            or Identity.digest(manifest) != context["execution_digest"]
        ):
            raise WorkerApiError("Assignment inputs changed the accepted execution identity")
        captured = JsonDocument(context)
        self.api.attempt_id = JsonDocument.expect_scalar(context["attempt_id"], str)
        captured["claimed"] = claimed
        captured["compute"] = manifest["compute"]
        arguments = response.get("arguments")
        captured["args"] = manifest["args"] if arguments is None else arguments
        captured["recovery"] = response.get("recovery")
        return captured
