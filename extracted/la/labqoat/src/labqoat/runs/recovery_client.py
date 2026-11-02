"""Typed management transport for durable same-run recovery operations."""

from collections.abc import Generator
from uuid import uuid4
from urllib.parse import urlencode

from labqoat._generated.recovery_discovery import RecoveryDiscovery
from labqoat._generated.recovery_operation import RecoveryOperation
from labqoat._generated.recovery_page import RecoveryPage
from labqoat._generated.recovery_request import RecoveryRequest
from labqoat._generated.run_stream_event import RunStreamEvent
from labqoat.base_client import BaseClient
from labqoat.errors.api_error import ApiError
from labqoat.errors.transport_error import TransportError
from labqoat.runs.recovery_handle import RecoveryHandle


class RecoveryClient(BaseClient):
    """Freeze mutation identity before transport retries and keep operation reads independent of current Run state."""

    def discovery(self, run_id: str, *, limit: int = 50, cursor: str | None = None) -> RecoveryDiscovery:
        """Read advisory readiness with a bounded page of retained checkpoint candidates."""
        path = self._path(run_id, "recovery") + self._page(limit, cursor)
        return self.decode(self.send("GET", path), path, RecoveryDiscovery.from_dict)

    def list(self, run_id: str, *, limit: int = 50, cursor: str | None = None) -> RecoveryPage:
        """Read one bounded page of durable recovery operations."""
        path = self._path(run_id, "recoveries") + self._page(limit, cursor)
        return self.decode(self.send("GET", path), path, RecoveryPage.from_dict)

    def get(self, run_id: str, operation_id: str) -> RecoveryOperation:
        """Read admission and the admitted cycle outcome, including subsequent automatic attempts."""
        path = self._path(run_id, "recoveries/" + self.encode_ref(operation_id))
        operation = self.decode(self.send("GET", path), path, RecoveryOperation.from_dict)
        if operation.run_id != run_id or operation.id != operation_id:
            raise ApiError("Recovery operation identity mismatch")
        return operation

    def create(self, run_id: str, request: RecoveryRequest, *, operation_key: str | None = None) -> RecoveryHandle:
        """Accept frozen intent promptly and reuse exactly one key and payload across bounded transport retries."""
        key = str(uuid4()) if operation_key is None else operation_key
        if not 1 <= len(key.encode()) <= 255:
            raise ValueError("operation_key must contain 1 to 255 bytes")
        path = self._path(run_id, "recoveries") + "?" + urlencode({"operation_key": key})
        payload = request.to_dict()
        attempt = 0
        while True:
            try:
                response = self.send_json("POST", path, payload)
                operation = self.decode(response, path, RecoveryOperation.from_dict)
                if operation.run_id != run_id:
                    raise ApiError("Recovery operation identity mismatch")
                return RecoveryHandle(operation, key, self)
            except TransportError:
                if attempt == 2:
                    raise
                attempt += 1

    def cancel(self, run_id: str, operation_id: str) -> RecoveryOperation:
        """Cancel pending admission; an already admitted cycle must be cancelled through its Run."""
        path = self._path(run_id, "recoveries/" + self.encode_ref(operation_id) + "/cancel")
        return self.decode(self.send_json("POST", path, {}), path, RecoveryOperation.from_dict)

    def events(self, run_id: str, operation_id: str, cursor: str | None) -> Generator[RunStreamEvent]:
        """Follow the explicit operation through terminal old projections and its captured cycle."""
        from labqoat.runs_client import RunsClient

        yield from RunsClient(self._transport).events(run_id, cursor=cursor, recovery_operation_id=operation_id)

    @staticmethod
    def _path(run_id: str, suffix: str) -> str:
        """Encode the logical Run identity independently of route structure."""
        return f"/api/v1/runs/{BaseClient.encode_ref(run_id)}/{suffix}"

    @staticmethod
    def _page(limit: int, cursor: str | None) -> str:
        """Retain exact server cursors without changing the requested page view."""
        values = {"limit": str(limit)}
        if cursor is not None:
            values["cursor"] = cursor
        return "?" + urlencode(values)
