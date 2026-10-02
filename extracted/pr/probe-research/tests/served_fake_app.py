"""Serve the in-process ``FakeApp`` over a real loopback socket.

Most SDK tests hand ``FakeApp.handler`` to an ``httpx.MockTransport``, which
only reaches code in THIS interpreter. Exit handling cannot be tested that way:
``sys.exit``, atexit and ``os.fork`` are process-level, so the code under test
has to run in a real child process. This bridge gives that child the same fake
backend -- the same routes, the same state -- over HTTP, so the assertions read
``app.runs`` / ``app.spans`` / ``app.requests`` exactly as the in-process tests do.
"""

from __future__ import annotations

import contextlib
import json
import os
import re
import threading
import time
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import httpx


@contextlib.contextmanager
def serve(app) -> Iterator[str]:
    """Yield a base URL whose every request is answered by ``app.handler``."""
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def _bridge(self) -> None:
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else b""
            request = httpx.Request(
                self.command,
                f"http://127.0.0.1:{self.server.server_port}{self.path}",
                headers=[(k, v) for k, v in self.headers.items()],
                content=body,
            )
            # A test's network latency (``app.latency(request) -> seconds``),
            # spent BEFORE the fake acts, outside the lock so it slows only
            # this request: like a real round trip, a client that dies
            # meanwhile has still sent what it sent, and never reads a reply.
            latency = getattr(app, "latency", None)
            if latency is not None:
                time.sleep(latency(request))
            # The fake is plain dicts and lists; a heartbeat thread and the main
            # thread of the child must not interleave inside it.
            with lock:
                response = app.handler(request)
            payload = response.content
            self.send_response(response.status_code)
            for key, value in response.headers.items():
                if key.lower() in {"content-length", "transfer-encoding", "connection"}:
                    continue
                self.send_header(key, value)
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        do_GET = do_POST = do_PATCH = do_PUT = do_DELETE = _bridge

        def log_message(self, *args) -> None:  # keep pytest output clean
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()


_RUN_PATCH = re.compile(r"/v1/runs/[^/]+")
_RELEASE = re.compile(r"/v1/runs/[^/]+/writers/[^/]+/release")


def close_latency(seconds: float):
    """An ``app.latency`` for :func:`serve` that holds each CLOSE request --
    a run's closing PATCH (``ended_at`` or ``status`` in it) and a lease
    release -- for ``seconds``, as a real network's round trips hold a close.
    Everything else is answered at once."""

    def latency(request: httpx.Request) -> float:
        path = request.url.path
        if request.method == "POST" and _RELEASE.fullmatch(path):
            return seconds
        if request.method == "PATCH" and _RUN_PATCH.fullmatch(path):
            try:
                body = json.loads(request.content or b"{}")
            except ValueError:
                return 0.0
            if isinstance(body, dict) and ("ended_at" in body or "status" in body):
                return seconds
        return 0.0

    return latency


def child_env(url: str, **extra: str) -> dict[str, str]:
    """The environment a child process needs to reach the served fake.

    Inherits the suite's isolation (HOME, outbox, telemetry off -- the autouse
    fixtures set them in ``os.environ``) and turns off the capture paths a
    child would otherwise run against the fake: snapshot and output capture
    are theirs to test, not an exit test's."""
    return {
        **os.environ,
        "PROBE_BASE_URL": url,
        "PROBE_TOKEN": "ros_pat_deadbeef",
        "PROBE_AUTO_SNAPSHOT": "0",
        "PROBE_CAPTURE_OUTPUTS": "0",
        **extra,
    }
