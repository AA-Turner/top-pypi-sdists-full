"""A call relayed to a worker's front door waits in that worker's queue as long as the queue needs — no read
deadline — and a caller that hangs up meanwhile is passed on to the worker (operator 2026-11-16: "a 6 hour per call
timeout? what even is this for?"). With a 600 s socket timeout here, 205 calls of a 261-call test fire failed at
exactly 600 s while still queued at the Wrapper, which went on serving them for nobody."""
import json
import select
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from hugpy_core.relay import relay


def _worker(delay_s, hung_up):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_POST(self):
            self.rfile.read(int(self.headers.get("Content-Length") or 0))
            end = time.monotonic() + delay_s
            while time.monotonic() < end:                 # the call waits in the queue
                r, _, _ = select.select([self.connection], [], [], 0.05)
                if r and self.connection.recv(1, socket.MSG_PEEK) == b"":
                    hung_up.set()                         # the relay closed its socket: the caller is gone
                    return
            chunk = {"choices": [{"delta": {"content": "hello"}, "finish_reason": "stop"}]}
            body = f"data: {json.dumps(chunk)}\n\ndata: [DONE]\n\n".encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, {"url": f"http://127.0.0.1:{server.server_address[1]}", "key": "k", "engine": {"name": "fitevict"}}


PAYLOAD = {"model_key": "org/m", "messages": [{"role": "user", "content": "hi"}], "max_new_tokens": 8}


def test_a_queued_call_is_waited_for_past_any_socket_timeout(monkeypatch):
    monkeypatch.setattr(relay, "CONNECT_TIMEOUT_S", 0.3)     # reaching the worker is bounded; its queue is not
    server, worker = _worker(1.2, threading.Event())
    try:
        events = list(relay.worker_stream(worker, PAYLOAD))
    finally:
        server.shutdown()
    assert [e["text"] for e in events if e["type"] == "token"] == ["hello"]
    assert events[-1]["type"] == "done"


def test_a_caller_that_hangs_up_is_passed_on_to_the_worker(monkeypatch):
    monkeypatch.setattr(relay, "CALLER_CHECK_S", 0.05)
    caller, served = socket.socketpair()                     # served: the socket of the request Core is answering
    monkeypatch.setattr(relay, "_caller_socket", lambda: served)
    hung_up = threading.Event()
    server, worker = _worker(30.0, hung_up)
    outcome = {}

    def relay_call():
        try:
            list(relay.worker_stream(worker, PAYLOAD))
        except Exception as exc:  # noqa: BLE001
            outcome["exc"] = exc

    t = threading.Thread(target=relay_call, daemon=True)
    try:
        t.start()
        time.sleep(0.3)
        assert t.is_alive()                                  # the call is waiting at the worker
        caller.close()                                       # the caller hangs up
        t.join(5.0)
        assert not t.is_alive() and isinstance(outcome.get("exc"), relay.CallerGone)
        assert hung_up.wait(5.0)                             # and the worker saw the relay hang up too
    finally:
        served.close()
        server.shutdown()
