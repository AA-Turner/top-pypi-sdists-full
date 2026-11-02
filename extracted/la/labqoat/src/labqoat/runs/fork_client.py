"""Typed changed-work submission and immutable source/checkpoint/usage lineage."""

from urllib.parse import urlencode
from uuid import uuid4

from labqoat._generated.fork_lineage import ForkLineage
from labqoat._generated.fork_page import ForkPage
from labqoat._generated.fork_request import ForkRequest
from labqoat.base_client import BaseClient
from labqoat.errors.api_error import ApiError
from labqoat.errors.transport_error import TransportError


class ForkClient(BaseClient):
    """Accept a new run without reopening the source or hiding inherited scientific consumption."""

    def create(self, run_id: str, request: ForkRequest, *, operation_key: str | None = None) -> ForkLineage:
        """Freeze one key and request body for at most three transport attempts."""
        key = operation_key if operation_key is not None else request.operation_key or str(uuid4())
        if not 1 <= len(key.encode()) <= 200:
            raise ValueError("operation_key must contain 1 to 200 bytes")
        path = self._path(run_id, "forks") + "?" + urlencode({"operation_key": key})
        body = request.to_dict()
        body.pop("operation_key", None)
        attempt = 0
        while True:
            try:
                result = self.decode(self.send_json("POST", path, body), path, ForkLineage.from_dict)
                if result.source_run_id != run_id or result.run_id == run_id or result.id != result.run_id:
                    raise ApiError("Fork lineage identity mismatch")
                return result
            except TransportError:
                if attempt == 2:
                    raise
                attempt += 1

    def get(self, run_id: str) -> ForkLineage:
        """Read a fork's immutable ancestry; a source without fork lineage returns the API's not-found error."""
        path = self._path(run_id, "lineage")
        result = self.decode(self.send("GET", path), path, ForkLineage.from_dict)
        if result.run_id != run_id or result.id != run_id:
            raise ApiError("Fork lineage identity mismatch")
        return result

    def list(self, run_id: str, *, limit: int = 50, cursor: str | None = None) -> ForkPage:
        """Read one bounded page of new runs forked from this source."""
        query = {"limit": str(limit)}
        if cursor is not None:
            query["cursor"] = cursor
        path = self._path(run_id, "forks") + "?" + urlencode(query)
        return self.decode(self.send("GET", path), path, ForkPage.from_dict)

    @staticmethod
    def _path(run_id: str, suffix: str) -> str:
        """Keep user run references encoded independently of route structure."""
        return f"/api/v1/runs/{BaseClient.encode_ref(run_id)}/{suffix}"
