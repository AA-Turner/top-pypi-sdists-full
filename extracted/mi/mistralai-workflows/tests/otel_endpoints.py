"""In-process OTLP endpoints shared by the telemetry tests (no real network)."""

from __future__ import annotations

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class RecordingTelemetryEndpoint:
    """In-process OTLP endpoint: records request headers and answers with a fixed status."""

    def __init__(self, status_code: int = 200) -> None:
        self.requests: list[dict[str, str]] = []
        endpoint = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:
                length = int(self.headers.get("Content-Length", 0))
                self.rfile.read(length)
                endpoint.requests.append({key.lower(): value for key, value in self.headers.items()})
                self.send_response(status_code)
                self.end_headers()

            def log_message(self, *_args: object) -> None:
                pass

        self._server = HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self._server.serve_forever, daemon=True).start()

    @property
    def url(self) -> str:
        host, port = self._server.server_address[:2]
        return f"http://{host}:{port}/telemetry"

    def bearer_of(self, index: int) -> str | None:
        return self.requests[index].get("authorization")

    def close(self) -> None:
        self._server.shutdown()
        self._server.server_close()
