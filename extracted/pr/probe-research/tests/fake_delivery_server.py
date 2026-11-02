"""A loopback HTTP server standing in for the Probe API's telemetry routes, for delivery tests
that run a REAL detached worker: counts POSTs per route, adds latency, answers 503 on demand."""

from __future__ import annotations

import json
import threading
import time
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class _Handler(BaseHTTPRequestHandler):
    def _respond(self, status: int, body: dict, headers: dict | None = None) -> None:
        raw = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802 -- http.server's name
        server = self.server
        if self.path.startswith("/v1/server/features"):
            self._respond(200, {"features": sorted(server.features)})
            return
        self._respond(200, {"id": "r-fake", "tags": []})

    def do_POST(self) -> None:  # noqa: N802
        server = self.server
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        if server.latency:
            time.sleep(server.latency)
        try:
            body = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            body = None
        with server.lock:
            server.requests.append((self.command, self.path, body, time.monotonic()))
        if server.unavailable:
            self._respond(503, {"detail": "unavailable"}, {"Retry-After": "1"})
            return
        for marker, retry_after in server.refusing.items():
            if marker in self.path:
                self._respond(503, {"detail": "unavailable"}, {"Retry-After": retry_after})
                return
        if self.path.endswith("/steps/batch"):
            if "steps_batch" not in server.features:
                self._respond(404, {"detail": "Not Found"})
                return
            steps = (body or {}).get("steps") or []
            self._respond(201, {"written": len(steps), "unchanged": 0})
            return
        self._respond(200, {})

    do_PATCH = do_POST

    def log_message(self, *args) -> None:  # noqa: D102 -- keep test output clean
        pass


class FakeDeliveryServer:
    """The server and what it saw. ``latency`` seconds per write; ``unavailable`` answers 503;
    ``refusing`` (path fragment -> Retry-After seconds) answers 503 to the writes it names;
    ``features`` is what `GET /v1/server/features` lists."""

    def __init__(self, *, latency: float = 0.0, features: tuple = ()) -> None:
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        self._server.daemon_threads = True
        self._server.requests = []
        self._server.lock = threading.Lock()
        self._server.latency = latency
        self._server.unavailable = False
        self._server.refusing = {}
        self._server.features = set(features)
        self.url = f"http://127.0.0.1:{self._server.server_port}"
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    @property
    def unavailable(self) -> bool:
        return self._server.unavailable

    @unavailable.setter
    def unavailable(self, value: bool) -> None:
        self._server.unavailable = value

    @property
    def refusing(self) -> dict:
        return self._server.refusing

    @property
    def features(self) -> set:
        return self._server.features

    def requests(self) -> list:
        """(method, path, body, monotonic time) per write, in arrival order."""
        with self._server.lock:
            return list(self._server.requests)

    def count(self, suffix: str) -> int:
        return sum(1 for _, path, _, _ in self.requests() if path.endswith(suffix))

    def start(self) -> "FakeDeliveryServer":
        self._thread.start()
        return self

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()


@contextmanager
def running_server(**kw):
    server = FakeDeliveryServer(**kw).start()
    try:
        yield server
    finally:
        server.stop()


def wait_for(predicate, timeout: float, every: float = 0.05) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(every)
    return bool(predicate())


def point_values(server: FakeDeliveryServer) -> list:
    """Every metric value the server received, in arrival order."""
    values = []
    for _, path, body, _ in server.requests():
        if path.endswith("/metrics"):
            values.extend(point.get("value") for point in (body or {}).get("points") or [])
    return values
