"""Typed JSON boundary for management endpoints used by the CLI."""

from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import TYPE_CHECKING
from urllib.parse import urlencode

from labqoat._generated.response_registry import ResponseRegistry
from labqoat.base_client import BaseClient
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.runs_client import RunsClient
from labqoat.sse_client import SseClient

if TYPE_CHECKING:
    from labqoat.net.response import Response


class ManagementClient(BaseClient):
    """Send explicit management requests and return validated JSON objects."""

    @property
    def runs(self) -> RunsClient:
        """Share the explicit-credential transport with typed execution waiting and result retrieval."""
        return RunsClient(self._transport)

    def get(self, path: str, query: Mapping[str, object]) -> JsonDocument:
        """Read one management document."""
        target = ManagementClient.target(path, query)
        return self.decode_response("GET", target)

    def delete(self, path: str, query: Mapping[str, object]) -> JsonDocument:
        """Delete one management resource."""
        target = ManagementClient.target(path, query)
        return self.decode_response("DELETE", target)

    def post(
        self,
        path: str,
        query: Mapping[str, object],
        payload: JsonValue | Mapping[str, JsonValue],
        *,
        idempotency_key: str | None = None,
    ) -> JsonDocument:
        """Create or mutate one management resource."""
        target = ManagementClient.target(path, query)
        response = self.send_json("POST", target, payload, idempotency_key=idempotency_key)
        return ManagementClient.validate_response("POST", target, response)

    def stream(self, path: str, query: Mapping[str, object]) -> Generator[JsonDocument]:
        """Yield validated server-sent events as bytes arrive."""
        target = ManagementClient.target(path, query)
        if path.startswith("/api/v1/runs/") and path.endswith("/logs"):
            from labqoat.runs.run_log_stream import RunLogStream

            yield from RunLogStream(self, target).entries()
            return
        with self.stream_response("GET", target, event_stream=True) as response:
            yield from SseClient.parse_stream(response.iter_bytes())

    def decode_response(self, method: str, target: str) -> JsonDocument:
        """Read and validate a JSON response against its generated model."""
        return ManagementClient.validate_response(method, target, self.send(method, target))

    def stream_events(self, path: str, query: Mapping[str, object]) -> Generator[JsonDocument]:
        """Yield SSE metadata and raw data while owning one closable response."""
        target = ManagementClient.target(path, query)
        with self.stream_response("GET", target, event_stream=True) as response:
            yield from SseClient.parse_events(response.iter_bytes())

    @staticmethod
    def validate_response(method: str, target: str, response: Response) -> JsonDocument:
        """Decode one response object and convert shape failures to API errors."""
        from labqoat.errors.api_error import ApiError

        try:
            value = response.json()
            return ResponseRegistry.validate(method, target, value)
        except (AttributeError, KeyError, TypeError, ValueError) as error:
            raise ApiError(f"Malformed response from {target}: {error}") from error

    @staticmethod
    def target(path: str, query: Mapping[str, object]) -> str:
        """Bind explicit path placeholders and append remaining non-null query values with safe escaping."""
        selected = {name: value for name, value in query.items() if value is not None}
        for segment in path.split("/"):
            if segment.startswith("{") and segment.endswith("}"):
                value = selected.pop(segment[1:-1], None)
                if not isinstance(value, str) or not value:
                    raise ValueError("Path parameters require nonempty string identities")
                path = path.replace(segment, BaseClient.encode_ref(value))
        encoded = urlencode(selected, doseq=True)
        return path if not encoded else f"{path}?{encoded}"
