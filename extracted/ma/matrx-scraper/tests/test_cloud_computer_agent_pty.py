"""The Cloud Computer's ``/agent/pty`` door: a person's interactive terminal (machines plan 4b).

The worker's ``/agent`` door was HTTP only, so the app's Terminal pane had no way into a
Cloud Computer's shell. The worker now relays a WebSocket to the daemon's ``/pty`` after
checking the same machine agent token every ``/agent`` call carries.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from matrx_scraper.cloud_browser.worker import http_app, machine_agent
from matrx_scraper.cloud_browser.worker.errors import WorkerProtocolError


class _FakeDaemonSocket:
    def __init__(self, url: str, sent: list[object], dialed: list[str]) -> None:
        dialed.append(url)
        self.sent = sent
        self._out: asyncio.Queue[object] = asyncio.Queue()
        self._out.put_nowait(b"$ ")

    async def __aenter__(self) -> _FakeDaemonSocket:
        return self

    async def __aexit__(self, *exc: object) -> None:
        return None

    async def send(self, message: object) -> None:
        self.sent.append(message)
        if message == "exit\n":
            await self._out.put(None)
        else:
            await self._out.put(b"echo:" + (message.encode() if isinstance(message, str) else message))

    def __aiter__(self) -> _FakeDaemonSocket:
        return self

    async def __anext__(self) -> object:
        item = await self._out.get()
        if item is None:
            raise StopAsyncIteration
        return item


def _client(monkeypatch: pytest.MonkeyPatch, tmp_path, *, token_ok: bool) -> tuple[TestClient, list, list]:
    import websockets.asyncio.client as ws_client

    monkeypatch.setattr(machine_agent, "home_dir", lambda: str(tmp_path))
    sent: list[object] = []
    dialed: list[str] = []
    monkeypatch.setattr(ws_client, "connect", lambda url, **_: _FakeDaemonSocket(url, sent, dialed))

    def verify(token: str, **_: object) -> None:
        if not token_ok or token != "machine-token":
            raise WorkerProtocolError("bad_token")

    worker = SimpleNamespace(worker_id="w", token_verifier=SimpleNamespace(verify=verify))
    launch = SimpleNamespace(files_token="", files_url="", process_env={})
    app = FastAPI()
    http_app._install_machine_files_and_agent(app, worker, launch)  # type: ignore[arg-type]
    return TestClient(app), sent, dialed


def test_the_terminal_reaches_the_daemons_pty_with_the_machine_token(monkeypatch, tmp_path) -> None:
    client, sent, dialed = _client(monkeypatch, tmp_path, token_ok=True)
    with client.websocket_connect(
        "/agent/pty?cols=100&rows=40&evil=1", headers={"x-sandbox-access-token": "machine-token"}
    ) as ws:
        assert ws.receive_bytes() == b"$ "
        ws.send_text("ls\n")
        assert ws.receive_bytes() == b"echo:ls\n"
        ws.send_text('{"type":"resize","cols":90,"rows":30}')
        assert ws.receive_bytes().startswith(b"echo:{")
        ws.send_text("exit\n")
    assert sent[0] == "ls\n"
    assert len(dialed) == 1
    url = dialed[0]
    assert url.startswith("ws://127.0.0.1:8765/pty?")
    assert "cols=100" in url and "rows=40" in url and "agent_token=" in url
    assert "evil" not in url  # only the size travels; the daemon token is the worker's own


def test_a_terminal_without_the_machine_token_is_refused(monkeypatch, tmp_path) -> None:
    client, _sent, dialed = _client(monkeypatch, tmp_path, token_ok=False)
    with pytest.raises(WebSocketDisconnect) as closed:
        with client.websocket_connect("/agent/pty", headers={"x-sandbox-access-token": "nope"}) as ws:
            ws.receive_bytes()
    assert closed.value.code == 4401
    assert dialed == []
