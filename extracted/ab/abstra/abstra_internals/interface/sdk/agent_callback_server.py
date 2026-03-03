from __future__ import annotations

import json
import logging
import secrets
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable, Dict, Tuple

logger = logging.getLogger(__name__)

_MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB


def _make_handler(
    functions: Dict[str, Callable],
    expected_secret: str,
) -> type:
    """Create a request handler class bound to the given function registry."""

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            if self.path != "/execute":
                self._send_json(404, {"error": "Not found"})
                return

            provided_secret = self.headers.get("X-Callback-Secret")
            if provided_secret != expected_secret:
                self._send_json(403, {"error": "Forbidden"})
                return

            try:
                body = self._read_body()
            except Exception:
                self._send_json(400, {"error": "Invalid request body"})
                return

            tool_name = body.get("toolName")
            tool_input = body.get("input", {})

            if not isinstance(tool_name, str) or not tool_name:
                self._send_json(400, {"error": "Missing or invalid 'toolName' field"})
                return

            func = functions.get(tool_name)
            if func is None:
                self._send_json(
                    404,
                    {"error": f"Tool not found: {tool_name}"},
                )
                return

            if not isinstance(tool_input, dict):
                self._send_json(400, {"error": "'input' must be an object"})
                return

            try:
                result = func(**tool_input)
                self._send_json(200, {"result": result})
            except Exception:
                logger.exception("Tool '%s' raised an exception", tool_name)
                self._send_json(
                    500,
                    {"error": "Tool execution failed"},
                )

        def _read_body(self) -> Dict[str, Any]:
            length = int(self.headers.get("Content-Length", 0))
            if length <= 0 or length > _MAX_BODY_SIZE:
                raise ValueError(f"Invalid Content-Length: {length}")
            raw = self.rfile.read(length)
            return json.loads(raw)

        def _send_json(self, status: int, data: Dict[str, Any]) -> None:
            payload = json.dumps(data).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, format: str, *args: Any) -> None:
            # Suppress default stderr logging
            pass

    return CallbackHandler


class AgentCallbackServer:
    """Lightweight HTTP server for executing custom agent tool callbacks.

    Runs in a background thread and dispatches POST /execute requests
    to the registered Python functions.
    """

    def __init__(self, functions: Dict[str, Callable]) -> None:
        if not functions:
            raise ValueError("At least one function must be registered")
        self._functions = dict(functions)  # defensive copy
        self._secret = secrets.token_hex(32)
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    def start(self) -> Tuple[str, str]:
        """Start the callback server on a random port.

        Returns a tuple of (base_url, secret) where base_url is e.g.
        http://127.0.0.1:12345 and secret is the shared authentication token.
        """
        handler_class = _make_handler(self._functions, self._secret)
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), handler_class)
        port = self._server.server_address[1]

        self._thread = threading.Thread(
            target=self._server.serve_forever,
            daemon=True,
        )
        self._thread.start()

        return f"http://127.0.0.1:{port}", self._secret

    def stop(self) -> None:
        """Shut down the callback server."""
        if self._server is not None:
            self._server.shutdown()
            self._server = None
        if self._thread is not None:
            self._thread.join(timeout=5)
            self._thread = None
