"""Shared helpers for editor WebSocket route tests.

Spin a real Flask app (with a flask_sock blueprint) on a werkzeug server bound
to an ephemeral port and connect real simple_websocket clients to it — the
same stack the editor uses in production (interface/cli/editor.py serves via
werkzeug's make_server with threaded=True).
"""

import threading
import time
from contextlib import contextmanager
from typing import Callable, Iterator, List

import flask
import flask_sock
from werkzeug.serving import make_server

# What the front sends every 30s on every editor WebSocket
# (desktop/src/apps/editor/apis/webSocketService.ts, startKeepalive).
KEEPALIVE_FRAME = '{"type": "keepalive"}'


@contextmanager
def run_ws_app(blueprint: flask.Blueprint, url_prefix: str) -> Iterator[str]:
    """Serve `blueprint` under `url_prefix` and yield the base ws:// URL."""
    app = flask.Flask(__name__)
    app.register_blueprint(blueprint, url_prefix=url_prefix)
    server = make_server("127.0.0.1", 0, app, threaded=True)
    thread = threading.Thread(
        target=server.serve_forever, daemon=True, name="WsTestServer"
    )
    thread.start()
    try:
        yield f"ws://127.0.0.1:{server.server_port}{url_prefix}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


def wait_until(
    predicate: Callable[[], bool], timeout: float = 5.0, interval: float = 0.02
) -> bool:
    """Poll `predicate` until it returns True; False if `timeout` elapses."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(interval)
    return predicate()


@contextmanager
def isolated_listeners(registry) -> Iterator[List[flask_sock.Server]]:
    """Snapshot and restore a controller's class-level `listeners` list.

    The broadcast controllers keep listeners as class state shared across the
    process; tests must not leak registrations into each other. Mutates the
    list in place because the controllers hold a reference to it.
    """
    original = list(registry.listeners)
    registry.listeners.clear()
    try:
        yield registry.listeners
    finally:
        registry.listeners[:] = original
