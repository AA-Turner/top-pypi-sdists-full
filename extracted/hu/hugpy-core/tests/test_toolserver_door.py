"""What Core does with a request under /toolserver/: hand it to its toolserver as the caller sent it."""
import io
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from hugpy_core.config import settings
from hugpy_core.web import toolserver_door


class _Toolserver(BaseHTTPRequestHandler):
    """Stands in for the toolserver: answers 401 without a token, else echoes what arrived."""

    def _answer(self):
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        status = 200 if self.headers.get("X-Operator-Token") or self.headers.get("Authorization") else 401
        reply = json.dumps({"method": self.command, "path": self.path, "body": body.decode(),
                            "headers": {k.lower(): v for k, v in self.headers.items()}}).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(reply)))
        self.end_headers()
        self.wfile.write(reply)

    do_GET = do_POST = _answer

    def log_message(self, *args):
        pass


@pytest.fixture
def toolserver(monkeypatch):
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Toolserver)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    monkeypatch.setattr(settings, "TOOLSERVER_URL", f"http://127.0.0.1:{server.server_port}")
    yield server
    server.shutdown()
    server.server_close()


def _call(app, method, path, query="", body=b"", **headers):
    seen = {}
    environ = {"REQUEST_METHOD": method, "PATH_INFO": path, "QUERY_STRING": query,
               "wsgi.url_scheme": "https", "wsgi.input": io.BytesIO(body), "CONTENT_LENGTH": str(len(body)),
               "REMOTE_ADDR": "203.0.113.9", "HTTP_HOST": "core.example", "SERVER_NAME": "core", "SERVER_PORT": "443"}
    if body:
        environ["CONTENT_TYPE"] = "application/json"
    environ.update({"HTTP_" + name.upper(): value for name, value in headers.items()})
    out = b"".join(app(environ, lambda status, hdrs: seen.update(status=int(status.split()[0]))))
    return seen["status"], json.loads(out)


def _core(environ, start_response):
    start_response("200 OK", [("Content-Type", "application/json")])
    return [b'{"served_by": "core"}']


def test_a_toolserver_call_through_core_arrives_as_the_caller_sent_it(toolserver):
    door = toolserver_door.wrap(_core)

    status, got = _call(door, "POST", "/toolserver/ts/call", query="trace=1",
                        body=b'{"name": "time_now_iso", "arguments": {}}', X_OPERATOR_TOKEN="station-token")
    assert status == 200
    assert (got["method"], got["path"]) == ("POST", "/ts/call?trace=1")
    assert json.loads(got["body"]) == {"name": "time_now_iso", "arguments": {}}
    assert got["headers"]["x-operator-token"] == "station-token"
    # the toolserver must be able to tell a relayed caller from a program on its own box
    assert "203.0.113.9" in got["headers"]["x-forwarded-for"]

    # Core lends no credential: without one the toolserver's own refusal comes back
    status, _ = _call(door, "POST", "/toolserver/ts/list", body=b"{}")
    assert status == 401

    # everything else is still Core's
    assert _call(door, "GET", "/toolserverish/x") == (200, {"served_by": "core"})
    assert _call(door, "GET", "/api/version") == (200, {"served_by": "core"})


def test_core_says_so_when_its_toolserver_is_not_answering(monkeypatch):
    monkeypatch.setattr(settings, "TOOLSERVER_URL", "http://127.0.0.1:9")
    status, got = _call(toolserver_door.wrap(_core), "GET", "/toolserver/healthz")
    assert status == 502
    assert "unreachable" in got["error"]["message"]
