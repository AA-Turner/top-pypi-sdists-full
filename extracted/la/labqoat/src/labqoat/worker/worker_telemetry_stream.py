"""Acknowledged telemetry pushes with bounded replay over one reusable HTTP connection."""

import http.client
import json
import time
from collections.abc import Callable, Mapping
from threading import RLock

from labqoat.json_document import JsonValue
from labqoat.worker.session.session_telemetry import SessionTelemetry
from labqoat.worker.telemetry_frames import TelemetryFrames
from labqoat.worker.worker_api_error import WorkerApiError


class WorkerTelemetryStream:
    """Confirm every push before returning; send no requests without pending evidence."""

    # Rides out a control-plane restart (about a minute) before surfacing a transient failure to the workload.
    RETRY_DELAYS: tuple[float, ...] = (0.5, 1.0, 2.0, 4.0, 8.0, 15.0, 30.0)

    def __init__(
        self,
        connect: Callable[[], http.client.HTTPConnection],
        path: str,
        headers: Mapping[str, str],
        session: SessionTelemetry | None = None,
    ) -> None:
        """Store an endpoint-validated connection factory without opening a socket."""
        self._connect = connect
        self._session = session
        self._path = path
        self._headers = dict(headers)
        self._connection: http.client.HTTPConnection | None = None
        self._pending: list[bytes] = []
        self._bytes = 0
        self._lock = RLock()
        self._closed = False

    def send(self, kind: str, entries: list[JsonValue]) -> None:
        """Deliver this frame and any retained evidence, bounded to 128 frames or one MiB."""
        frame = TelemetryFrames.encode(kind, entries)
        with self._lock:
            self.stage([frame])
            self.flush()

    def stage(self, frames: list[bytes]) -> None:
        """Take ownership of encoded evidence before delivery, retaining exact bytes until acknowledged."""
        size = sum(map(len, frames))
        if len(frames) > 128 or size > 1_048_580:
            raise ValueError("Telemetry replay window is too large")
        with self._lock:
            if self._closed:
                raise RuntimeError("Worker telemetry is closed")
            if len(self._pending) + len(frames) > 128 or self._bytes + size > 1_048_580:
                self.flush()
            self._pending.extend(frames)
            self._bytes += size

    def flush(self) -> None:
        """Push pending frames and require their durable acknowledgement before releasing them."""
        with self._lock:
            if not self._pending:
                return
            self._retry(self._finish)
            self._pending.clear()
            self._bytes = 0

    def close(self) -> None:
        """Flush outstanding evidence and release the socket even if delivery fails."""
        with self._lock:
            self._closed = True
            try:
                self.flush()
            finally:
                self._disconnect()

    def _open(self) -> None:
        """Reuse the confirmed connection for a new push and replay unacknowledged frames unchanged."""
        if self._connection is None:
            self._connection = self._connect()
        self._connection.putrequest("POST", self._path)
        for name, value in self._headers.items():
            self._connection.putheader(name, value)
        self._connection.putheader("Content-Type", "application/octet-stream")
        self._connection.putheader("Transfer-Encoding", "chunked")
        self._connection.endheaders()
        for frame in self._pending:
            self._chunk(frame)

    def _chunk(self, frame: bytes) -> None:
        """Write an HTTP chunk without creating a new request."""
        assert self._connection is not None
        self._connection.send(f"{len(frame):X}\r\n".encode() + frame + b"\r\n")

    def _finish(self) -> None:
        """A successful bounded response is the durable checkpoint for this replay window."""
        if self._session is not None and self._session.accepts(self._pending):
            self._session.deliver(self._pending)
            return
        self._open()
        assert self._connection is not None
        self._connection.send(b"0\r\n\r\n")
        response = self._connection.getresponse()
        body = response.read(4097)
        if response.status != 200:
            code = self._code(body)
            raise WorkerApiError(f"Worker telemetry returned HTTP {response.status} ({code})", response.status, code)
        self._acknowledge(body)

    @staticmethod
    def _code(body: bytes) -> str:
        """The platform's name for why it refused a push, from its problem document."""
        try:
            document = json.loads(body)
        except ValueError:
            return "unexplained"
        code = document.get("code") if isinstance(document, dict) else None
        return code if isinstance(code, str) else "unexplained"

    @staticmethod
    def _acknowledge(body: bytes) -> None:
        """Validate a bounded JSON acknowledgement without depending on response whitespace."""
        try:
            valid = len(body) <= 4096 and json.loads(body) == {"status": "ok"}
        except ValueError:
            valid = False
        if not valid:
            raise WorkerApiError("Worker telemetry acknowledgement is invalid", 502)

    def _retry(self, operation: Callable[[], None]) -> None:
        """Replay an interrupted window with backoff; permanent rejections never become silent data loss."""
        for delay in self.RETRY_DELAYS:
            try:
                self._attempt(operation)
                return
            except WorkerApiError as error:
                if self._permanent(error):
                    raise
            time.sleep(delay)
        self._attempt(operation)

    @staticmethod
    def _permanent(error: WorkerApiError) -> bool:
        """Never replay redirects, invalid evidence, or rejected assignment authority."""
        return error.status is not None and error.status < 500 and error.status not in {408, 429}

    def _attempt(self, operation: Callable[[], None]) -> None:
        """Drop failed sockets while preserving exact evidence for the next bounded retry."""
        try:
            operation()
        except (OSError, http.client.HTTPException, WorkerApiError) as error:
            self._disconnect()
            status = error.status if isinstance(error, WorkerApiError) else None
            code = error.code if isinstance(error, WorkerApiError) else None
            raise WorkerApiError("Worker telemetry delivery failed", status, code) from error

    def _disconnect(self) -> None:
        """Forget transport state while retaining the replay window until acknowledged."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
