"""Some common helpers for testing"""

from typing import Generator, Tuple, Sequence, Any
import platform
import tempfile
import random
import http.server
import threading
import logging
import queue


import pytest


RANDOM_PORT = random.randint(25000, 55000)  # nosec
LOGGER = logging.getLogger(__name__)
EchoServerYieldType = Tuple[str, "queue.LifoQueue[Any]"]


def _choose_tmp_path() -> str:
    """Get reasonable tmp path"""
    tempdir = "/tmp" if platform.system() == "Darwin" else tempfile.gettempdir()  # nosec
    return tempdir


@pytest.fixture
def nice_tmpdir() -> Generator[str, None, None]:
    """Return sane tmp path on OSX too"""
    with tempfile.TemporaryDirectory(dir=_choose_tmp_path()) as tmpdir:
        yield str(tmpdir)


@pytest.fixture(scope="module")
def nice_tmpdir_mod() -> Generator[str, None, None]:
    """Return sane tmp path on OSX too, module scoped"""
    with tempfile.TemporaryDirectory(dir=_choose_tmp_path()) as tmpdir:
        yield str(tmpdir)


@pytest.fixture(scope="session")
def nice_tmpdir_ses() -> Generator[str, None, None]:
    """Return sane tmp path on OSX too, session scoped"""
    with tempfile.TemporaryDirectory(dir=_choose_tmp_path()) as tmpdir:
        yield str(tmpdir)


@pytest.fixture(scope="session")
def monkeysession() -> Generator[pytest.MonkeyPatch, None, None]:
    """session scoped monkeypatcher"""
    with pytest.MonkeyPatch.context() as mpatch:
        yield mpatch


@pytest.fixture(scope="module")
def monkeymodule() -> Generator[pytest.MonkeyPatch, None, None]:
    """module scoped monkeypatcher"""
    with pytest.MonkeyPatch.context() as mpatch:
        yield mpatch


class PostEchoHandler(http.server.BaseHTTPRequestHandler):
    """Respond with pong to any get and with the body to any POST"""

    server_queue: "queue.LifoQueue[Any]" = queue.LifoQueue()

    def log_message(self, format: str, *args: Sequence[Any]) -> None:  # pylint: disable=W0622
        """override the default write to stderr as no-op, I use the same argument name as parent
        even though it overrides a built-in name."""

    def _read_request_body(self) -> bytes:
        """read the body based on content-length"""
        if "Content-length" not in self.headers or int(self.headers["Content-length"]) < 1:
            return b""
        request_body = self.rfile.read(int(self.headers["Content-length"]))
        return request_body

    def do_GET(self) -> None:  # pylint: disable=C0103
        """Handle the post"""
        self.close_connection = True  # pylint: disable=W0201
        reply_body = b"Pong"
        self.send_response(http.HTTPStatus.OK)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", str(len(reply_body)))
        self.end_headers()
        self.wfile.write(reply_body)
        self.wfile.flush()
        PostEchoHandler.server_queue.put(
            {"headers": dict(self.headers), "request_body": b"", "reply_body": reply_body}, timeout=1.0
        )

    def do_POST(self) -> None:  # pylint: disable=C0103
        """Handle the post"""
        self.close_connection = True  # pylint: disable=W0201
        request_body = self._read_request_body()
        self.send_response(http.HTTPStatus.OK)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", str(len(request_body)))
        self.end_headers()
        self.wfile.write(request_body)
        self.wfile.flush()
        PostEchoHandler.server_queue.put(
            {"headers": dict(self.headers), "request_body": request_body, "reply_body": request_body},
            timeout=1.0,
        )


@pytest.fixture(scope="session")
def echo_http_server(port: int = RANDOM_PORT) -> Generator[EchoServerYieldType, None, None]:
    """HTTP server echoes the POSTed body"""
    serverlogger = logging.getLogger("http.server")
    serverlogger.setLevel(logging.ERROR)
    server = http.server.HTTPServer(("", port), PostEchoHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    LOGGER.debug("starting server thread")
    server_thread.start()

    yield (f"http://127.0.0.1:{port}/", PostEchoHandler.server_queue)

    # Clear any leftover items from the queue
    while not PostEchoHandler.server_queue.empty():
        _ = PostEchoHandler.server_queue.get(timeout=0.1)
    del serverlogger
    LOGGER.debug("stopping server thread")
    server.shutdown()
    server_thread.join(timeout=1.0)
