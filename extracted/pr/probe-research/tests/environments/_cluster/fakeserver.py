"""Serve the suite's ``FakeApp`` on a UNIX socket, for containers to reach through the relay.

`tests/served_fake_app.serve` listens on 127.0.0.1, which a container cannot reach,
and the box's firewall drops container-to-host TCP. A socket file bind-mounted into
the relay container (``image/relay.py``) crosses the namespace boundary instead.
Same bridge as `serve`: every request goes to ``app.handler`` under one lock.
"""

from __future__ import annotations

import contextlib
import os
import socketserver
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler
from pathlib import Path

import httpx


class _UnixHTTPServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads = True
    allow_reuse_address = True


@contextlib.contextmanager
def serve_unix(app, socket_path: Path, *, host: str = "api") -> Iterator[Path]:
    """Answer every request on ``socket_path`` with ``app.handler``."""
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def address_string(self) -> str:  # a UNIX peer has no (host, port)
            return "relay"

        def _bridge(self) -> None:
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else b""
            request = httpx.Request(
                self.command,
                f"http://{self.headers.get('Host') or host}{self.path}",
                headers=[(k, v) for k, v in self.headers.items()],
                content=body,
            )
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

        do_GET = do_POST = do_PATCH = do_PUT = do_DELETE = do_HEAD = _bridge

        def log_message(self, *args) -> None:
            pass

    socket_path = Path(socket_path)
    with contextlib.suppress(FileNotFoundError):
        socket_path.unlink()
    server = _UnixHTTPServer(str(socket_path), Handler)
    # The relay runs as root in its container; the socket only needs to be
    # connectable by it. 0o777 on a socket inside a 0o700 directory we own.
    os.chmod(socket_path, 0o777)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield socket_path
    finally:
        server.shutdown()
        server.server_close()
        with contextlib.suppress(FileNotFoundError):
            socket_path.unlink()
