"""Daemon TTL caches and long-lived HTTP connection pool."""

from __future__ import annotations

import threading
import time
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import httpx
import pytest

from runlayer_cli import mdm_config
from runlayer_cli.daemon import runtime
from runlayer_cli.hook import relay


@pytest.fixture(autouse=True)
def _reset_daemon_seams() -> Iterator[None]:
    relay.set_shared_http_client_provider(None)
    relay.set_credential_cache(None)
    relay.set_deferred_event_sender(None)
    mdm_config.set_managed_config_provider(None)
    yield
    relay.set_shared_http_client_provider(None)
    relay.set_credential_cache(None)
    relay.set_deferred_event_sender(None)
    mdm_config.set_managed_config_provider(None)


def test_managed_config_cache_refreshes_after_ttl_and_returns_copies() -> None:
    now = [0.0]
    loads: list[int] = []

    def load() -> mdm_config.ManagedConfig:
        loads.append(len(loads))
        return {
            "org_api_key": "rl_org_test",
            "daemon_enabled": len(loads) == 1,
        }

    cache = runtime.ManagedConfigCache(load, ttl=30.0, clock=lambda: now[0])

    first = cache.get()
    first["daemon_enabled"] = False
    assert cache.get()["daemon_enabled"] is True
    assert len(loads) == 1

    now[0] = 30.0
    assert cache.get()["daemon_enabled"] is False
    assert len(loads) == 2


def test_credential_cache_refreshes_on_ttl_and_invalidation() -> None:
    now = [0.0]
    managed_loads: list[int] = []
    credential_loads: list[int] = []
    managed = runtime.ManagedConfigCache(
        lambda: managed_loads.append(1) or {},
        ttl=30.0,
        clock=lambda: now[0],
    )
    cache = runtime.CredentialCache(
        managed,
        ttl=30.0,
        clock=lambda: now[0],
    )

    def load_credentials() -> tuple[str, str]:
        credential_loads.append(1)
        return "https://example.com", f"secret-{len(credential_loads)}"

    assert cache.get(load_credentials)[1] == "secret-1"
    assert cache.get(load_credentials)[1] == "secret-1"
    now[0] = 30.0
    assert cache.get(load_credentials)[1] == "secret-2"

    managed.get()
    cache.invalidate()
    assert cache.get(load_credentials)[1] == "secret-3"
    managed.get()
    assert len(managed_loads) == 2


def test_401_invalidates_cached_credentials(monkeypatch) -> None:
    managed = runtime.ManagedConfigCache(lambda: {})
    credentials = runtime.CredentialCache(managed)
    loads: list[int] = []

    def load_credentials() -> tuple[str, str]:
        loads.append(1)
        return "https://api.example.com", f"secret-{len(loads)}"

    monkeypatch.setattr(relay, "_load_credentials_uncached", load_credentials)
    monkeypatch.setattr(relay, "_maybe_attach_device", lambda payload: payload)
    client = httpx.Client(
        transport=httpx.MockTransport(
            lambda _request: httpx.Response(401, text="unauthorized")
        )
    )
    relay.set_credential_cache(credentials)
    relay.set_shared_http_client_provider(lambda: client)
    try:
        assert relay._load_credentials()[1] == "secret-1"
        with pytest.raises(relay.RelayError, match="HTTP 401"):
            relay._post(
                "https://api.example.com",
                "secret-1",
                "{}",
                target="enforce",
            )
        assert relay._load_credentials()[1] == "secret-2"
    finally:
        client.close()

    assert len(loads) == 2


class _CountingHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _KeepAliveHandler)
        self.accept_count = 0

    def get_request(self):
        request, address = super().get_request()
        self.accept_count += 1
        return request, address


class _KeepAliveHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", "0"))
        self.rfile.read(content_length)
        body = b'{"ok":true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format: str, *_args: object) -> None:
        pass


def test_sequential_hook_posts_reuse_one_tcp_connection(monkeypatch) -> None:
    server = _CountingHTTPServer()
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    host = f"http://127.0.0.1:{server.server_port}"
    pooled = httpx.Client(
        limits=httpx.Limits(
            max_keepalive_connections=8,
            max_connections=32,
            keepalive_expiry=90.0,
        )
    )
    monkeypatch.setattr(relay, "_maybe_attach_device", lambda payload: payload)
    relay.set_shared_http_client_provider(lambda: pooled)
    try:
        relay._post(host, "rl_org_test", "{}", target="enforce")
        relay._post(host, "rl_org_test", "{}", target="enforce")
    finally:
        pooled.close()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    assert not thread.is_alive()
    assert server.accept_count == 1


class TestDeferredEventQueue:
    def test_sends_run_in_fifo_order(self) -> None:
        queue = runtime.DeferredEventQueue()
        done = threading.Event()
        order: list[int] = []

        gate = threading.Event()

        def make_send(index: int):
            def send() -> None:
                gate.wait(timeout=5)
                order.append(index)
                if index == 2:
                    done.set()

            return send

        # Enqueue everything before releasing the worker so ordering is
        # decided by the queue, not by enqueue/drain interleaving.
        assert queue.enqueue(make_send(0)) is True
        assert queue.enqueue(make_send(1)) is True
        assert queue.enqueue(make_send(2)) is True
        gate.set()
        assert done.wait(timeout=5)
        assert queue.flush_and_stop() is True
        assert order == [0, 1, 2]

    def test_overflow_drops_oldest(self) -> None:
        queue = runtime.DeferredEventQueue(max_size=2)
        gate = threading.Event()
        ran: list[str] = []

        def blocker() -> None:
            gate.wait(timeout=5)
            ran.append("blocker")

        def make_send(name: str):
            def send() -> None:
                ran.append(name)

            return send

        assert queue.enqueue(blocker) is True
        # Worker picks up `blocker` and parks; fill the queue behind it.
        for _ in range(50):
            with queue._cond:
                blocked = queue._inflight == 1 and not queue._items
            if blocked:
                break
            time.sleep(0.01)
        assert queue.enqueue(make_send("a")) is True
        assert queue.enqueue(make_send("b")) is True
        assert queue.enqueue(make_send("c")) is True  # drops "a"
        gate.set()
        assert queue.flush_and_stop() is True
        assert ran == ["blocker", "b", "c"]

    def test_flush_drains_pending_sends_and_closes(self) -> None:
        queue = runtime.DeferredEventQueue()
        ran: list[int] = []
        for index in range(5):
            assert queue.enqueue(lambda index=index: ran.append(index)) is True

        assert queue.flush_and_stop() is True
        assert ran == [0, 1, 2, 3, 4]
        assert queue.enqueue(lambda: ran.append(99)) is False
        assert ran == [0, 1, 2, 3, 4]

    def test_flush_times_out_on_stuck_send(self) -> None:
        queue = runtime.DeferredEventQueue()
        release = threading.Event()
        assert queue.enqueue(lambda: release.wait(timeout=10)) is True

        started = time.monotonic()
        assert queue.flush_and_stop(timeout=0.2) is False
        assert time.monotonic() - started < 5
        release.set()

    def test_send_exception_does_not_kill_worker(self) -> None:
        queue = runtime.DeferredEventQueue()
        ran: list[str] = []

        def boom() -> None:
            raise RuntimeError("send failed")

        assert queue.enqueue(boom) is True
        assert queue.enqueue(lambda: ran.append("after")) is True
        assert queue.flush_and_stop() is True
        assert ran == ["after"]

    def test_flush_on_empty_queue_is_immediate(self) -> None:
        queue = runtime.DeferredEventQueue()
        assert queue.flush_and_stop(timeout=0.1) is True
        assert queue.enqueue(lambda: None) is False


class TestRuntimeDeferredEvents:
    def test_install_defers_forward_event_and_close_flushes(self, monkeypatch) -> None:
        sent: list[httpx.Request] = []
        release = threading.Event()

        def respond(request: httpx.Request) -> httpx.Response:
            release.wait(timeout=5)
            sent.append(request)
            return httpx.Response(200)

        client = httpx.Client(transport=httpx.MockTransport(respond))
        daemon_runtime = runtime.DaemonRuntime(client=client)
        monkeypatch.setattr(
            relay,
            "_load_credentials",
            lambda: ("https://api.example.com", "rl_org_test"),
        )
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda payload: payload)
        daemon_runtime.install()
        try:
            relay.forward_event("claude_code", "PreToolUse", {"tool_name": "Bash"})
            # The POST is queued, not inline: nothing sent until released.
            assert sent == []
            release.set()
        finally:
            daemon_runtime.close()

        # close() flushed the queue before closing the pooled client.
        assert len(sent) == 1
        assert sent[0].url.path == "/api/v1/hooks/events"

    def test_close_clears_deferred_seam(self, monkeypatch) -> None:
        client = httpx.Client(
            transport=httpx.MockTransport(lambda _request: httpx.Response(200))
        )
        daemon_runtime = runtime.DaemonRuntime(client=client)
        daemon_runtime.install()
        daemon_runtime.close()
        assert relay._deferred_event_sender is None


def test_prewarm_runs_on_start_and_first_hook_after_idle(monkeypatch) -> None:
    now = [0.0]
    requests: list[httpx.Request] = []
    request_sent = threading.Event()

    def send(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        request_sent.set()
        return httpx.Response(200)

    client = httpx.Client(transport=httpx.MockTransport(send))
    daemon_runtime = runtime.DaemonRuntime(clock=lambda: now[0], client=client)
    monkeypatch.setattr(
        relay,
        "_load_credentials",
        lambda: ("https://api.example.com", "rl_org_test"),
    )
    try:
        daemon_runtime.prewarm(force=True)
        request_sent.clear()
        now[0] = 10.0
        daemon_runtime.before_hook()
        now[0] = 101.0
        daemon_runtime.before_hook()
        assert request_sent.wait(timeout=5)
    finally:
        daemon_runtime.close()

    assert [request.method for request in requests] == ["HEAD", "HEAD"]
