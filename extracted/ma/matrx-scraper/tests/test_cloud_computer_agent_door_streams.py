"""The Cloud Computer's ``/agent`` door relays a live command stream as it comes.

``/agent/exec/stream`` was buffered with a 70 s cap: the app's terminal showed
nothing until the command ended and a long build died (review of 23ecc676,
2026-11-01). It now streams with no read deadline, and git calls get 150 s.
"""

from __future__ import annotations

from types import SimpleNamespace

import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient

from matrx_scraper.cloud_browser.worker import http_app, machine_agent

CHUNKS = [b"data: line 1\n\n", b"data: line 2\n\n", b"event: done\ndata: {}\n\n"]


def _app(monkeypatch, tmp_path, seen: list[dict]) -> TestClient:
    monkeypatch.setattr(machine_agent, "home_dir", lambda: str(tmp_path))
    real = httpx.AsyncClient

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/exec/stream":
            return httpx.Response(200, headers={"content-type": "text/event-stream"}, stream=httpx.ByteStream(b"".join(CHUNKS)))
        return httpx.Response(200, json={"ok": True, "path": request.url.path})

    def client(*args, **kwargs):  # noqa: ANN002, ANN003
        seen.append({"timeout": kwargs.get("timeout")})
        return real(transport=httpx.MockTransport(handler), timeout=kwargs.get("timeout"))

    monkeypatch.setattr(httpx, "AsyncClient", client)
    worker = SimpleNamespace(worker_id="w", token_verifier=SimpleNamespace(verify=lambda *a, **k: None))
    launch = SimpleNamespace(files_token="", files_url="", process_env={})
    app = FastAPI()
    http_app._install_machine_files_and_agent(app, worker, launch)  # type: ignore[arg-type]
    return TestClient(app)


def test_exec_stream_is_relayed_without_a_read_deadline(monkeypatch, tmp_path) -> None:
    seen: list[dict] = []
    client = _app(monkeypatch, tmp_path, seen)
    resp = client.post("/agent/exec/stream", json={"command": "make"}, headers={"x-sandbox-access-token": "t"})
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/event-stream")
    assert resp.content == b"".join(CHUNKS)
    assert seen[-1]["timeout"].read is None


def test_a_git_call_outlasts_the_default_limit(monkeypatch, tmp_path) -> None:
    seen: list[dict] = []
    client = _app(monkeypatch, tmp_path, seen)
    assert client.get("/agent/git/repos", headers={"x-sandbox-access-token": "t"}).json()["path"] == "/git/repos"
    assert seen[-1]["timeout"] == 150.0
    client.get("/agent/fs/list", headers={"x-sandbox-access-token": "t"})
    assert seen[-1]["timeout"] == 70.0


def test_the_first_agent_call_waits_for_the_daemon_to_bind(monkeypatch, tmp_path) -> None:
    """A wake's first exec arrived 0.2 s after /health, before the daemon bound,
    and got 503 (task 06d55a36, 2026-11-01). The door now waits for the bind."""
    import asyncio
    import socket

    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    daemon = machine_agent.AgentDaemon(str(tmp_path), launch_env={}, port=port)
    monkeypatch.setattr(machine_agent.AgentDaemon, "available", property(lambda self: True))

    async def scenario() -> tuple[bool, bool]:
        early = await daemon.wait_listening(0.2)  # nothing bound yet
        server_box: list[asyncio.AbstractServer] = []

        async def bind_later() -> None:
            await asyncio.sleep(0.5)
            server_box.append(await asyncio.start_server(lambda r, w: w.close(), "127.0.0.1", port))

        binder = asyncio.create_task(bind_later())
        late = await daemon.wait_listening(5.0)
        await binder
        server_box[0].close()
        await server_box[0].wait_closed()
        return early, late

    early, late = asyncio.run(scenario())
    assert early is False
    assert late is True


def test_the_agent_door_refuses_honestly_while_the_daemon_never_binds(monkeypatch, tmp_path) -> None:
    seen: list[dict] = []
    monkeypatch.setattr(machine_agent.AgentDaemon, "available", property(lambda self: True))

    async def never(self, timeout: float) -> bool:  # noqa: ANN001
        return False

    monkeypatch.setattr(machine_agent.AgentDaemon, "wait_listening", never)
    client = _app(monkeypatch, tmp_path, seen)
    resp = client.post("/agent/exec", json={"command": "true"}, headers={"x-sandbox-access-token": "t"})
    assert resp.status_code == 503
    assert resp.json()["detail"] == "agent daemon is not listening yet"
    assert seen == []  # nothing was forwarded into the gap
