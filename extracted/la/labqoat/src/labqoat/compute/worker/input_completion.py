"""Negotiate one replayable result transaction while retaining legacy worker completion."""

from dataclasses import dataclass

from labqoat.json_document import JsonValue
from labqoat.worker.worker_api import WorkerApi
from labqoat.worker.replay_request import ReplayRequest


@dataclass(frozen=True)
class InputCompletion:
    """Use assignment-owned result authority without releasing a still-running physical process."""

    api: WorkerApi

    def finish(self, result: dict[str, JsonValue]) -> None:
        """Keep typed output and terminal acknowledgement indivisible on negotiated servers."""
        if "atomic_lifecycle" in self.api.capabilities:
            ReplayRequest(self.api).send("/api/v1/worker/assignments/finish", result)
        else:
            self.api.json("POST", "/api/v1/worker/assignments/output", result)
            self.api.json("POST", "/api/v1/worker/assignments/complete", {})
