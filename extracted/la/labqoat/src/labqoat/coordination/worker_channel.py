"""Dict and queue requests under a run's own credentials."""

import json
from collections.abc import Mapping

from labqoat.coordination.store_reply import StoreReply
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.worker.worker_api import WorkerApi
from labqoat.worker.worker_api_error import WorkerApiError


class WorkerChannel:
    """Reach the dicts and queues of the run's own project; the credentials decide which project that is."""

    PREFIX = "/api/v1/worker"

    def __init__(self, api: WorkerApi) -> None:
        """Share the run's worker API and its pooled connections."""
        self._api = api

    def send(
        self, method: str, path: str, document: Mapping[str, JsonValue] | None = None, wait: float = 0.0
    ) -> StoreReply:
        """Send one request; the worker API's own deadline outlasts any wait the service may hold it for."""
        body = None
        if document is not None:
            body = json.dumps(document, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()
        try:
            raw = self._api.request(method, self.PREFIX + path, body, "application/json")
        except WorkerApiError as error:
            if error.status in (404, 409):
                return StoreReply(error.status)
            raise
        return StoreReply(200, JsonDocument.expect_dict(json.loads(raw)) if raw else JsonDocument())
