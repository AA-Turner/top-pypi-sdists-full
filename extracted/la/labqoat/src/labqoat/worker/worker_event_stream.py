"""Small bounded SSE reader for dependency-free worker images."""

from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING, cast

from labqoat.worker.worker_api_error import WorkerApiError

if TYPE_CHECKING:
    from http.client import HTTPResponse


class WorkerEventStream:
    """Read a completion event while enforcing frame and overall wait bounds."""

    _MAX_BYTES = 4_194_304

    @staticmethod
    def complete(response: HTTPResponse, kind: str, deadline: float) -> dict[str, object]:
        """Return the terminal object, preserving explicit server errors."""
        while True:
            event, raw = WorkerEventStream._frame(response, deadline)
            document = WorkerEventStream._document(raw)
            if event == f"{kind}.error":
                raise WorkerApiError(f"{kind} stream failed: {document.get('error')}", code="stream_failed")
            if event == f"{kind}.complete":
                return document

    @staticmethod
    def _frame(response: HTTPResponse, deadline: float) -> tuple[str, bytes]:
        """Collect one SSE frame, ignoring comments and empty heartbeats."""
        event, data = "message", b""
        while True:
            line = WorkerEventStream._line(response, deadline)
            if line in (b"\n", b"\r\n"):
                if data:
                    return event, data
                event = "message"
            elif line.startswith(b"event:"):
                event = line[6:].strip().decode("utf-8")
            elif line.startswith(b"data:"):
                data += line[5:].lstrip()
                if len(data) > WorkerEventStream._MAX_BYTES:
                    raise RuntimeError("worker stream frame is too large")

    @staticmethod
    def _line(response: HTTPResponse, deadline: float) -> bytes:
        """Reject incomplete streams and waits that exceed the worker deadline."""
        if time.monotonic() >= deadline:
            raise RuntimeError("worker stream did not complete before the deadline")
        line = response.readline(WorkerEventStream._MAX_BYTES + 1)
        if not line:
            raise WorkerApiError("worker stream closed before completion")
        if len(line) > WorkerEventStream._MAX_BYTES:
            raise RuntimeError("worker stream line is too large")
        return line

    @staticmethod
    def _document(raw: bytes) -> dict[str, object]:
        """Require one valid JSON object for every non-heartbeat event."""
        try:
            value = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise RuntimeError("worker stream returned invalid JSON") from error
        if not isinstance(value, dict):
            raise RuntimeError("worker stream response must be an object")
        return cast("dict[str, object]", value)
