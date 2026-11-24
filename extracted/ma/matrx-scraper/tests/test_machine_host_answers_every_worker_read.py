"""The multi-browser host answers every read the HTTP layer makes (2026-11-02 P0).

Break this catches: on machine image 297821e6 every ``/agent`` door (exec, fs, git,
search, processes, ports), ``/machine/vault-env`` and the terminal answered 503 "no
token verifier". ``server.py`` hands ``create_worker_app`` a ``MachineBrowsers`` host
when ``MATRX_CLOUD_COMPUTER=1``, and ``http_app`` read ``getattr(worker, "_verifier",
None)`` — a private attribute only the one-browser ``BrowserWorker`` had, hidden behind
a default. Both tests here failed on that code:

* the app is built EXACTLY as ``server.py`` builds it on a Cloud Computer, and a
  real ES256 machine agent token reaches ``/agent/exec`` and ``/agent/pty``;
* every attribute ``http_app`` reads off its worker is found by AST and must exist on
  BOTH host classes, and no read may hide a missing one behind ``getattr``/``hasattr``.
"""

from __future__ import annotations

import ast
import asyncio
import importlib
import sys
from pathlib import Path

import httpx
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient
from matrx_connect import ScopedTokenIssuer
from matrx_scraper.cloud_browser.worker import cloud_computer_launch, http_app, machine_agent
from matrx_scraper.cloud_browser.worker.machine_browsers import MachineBrowsers
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker
from matrx_utils.source_guard import stable_source
from starlette.websockets import WebSocketDisconnect

WORKER_ID = "44444444-4444-8444-8444-444444444444"
ISSUER = "matrx-broker"


def _issuer() -> ScopedTokenIssuer:
    pem = ec.generate_private_key(ec.SECP256R1()).private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
    ).decode()
    return ScopedTokenIssuer(issuer=ISSUER, private_key_pem=pem)


def _agent_token(issuer: ScopedTokenIssuer) -> str:
    """The token AI Dream's relay sends (``cloud_computer_files.mint_agent_token``)."""
    token, _ = issuer.mint(
        user_id=f"machine:{WORKER_ID}",
        audience=f"worker:{WORKER_ID}",
        tier_policy="none",
        ttl_seconds=600,
        extra_claims={"mtx_op": machine_agent.AGENT_OP},
    )
    return token


class _FakeDaemonPty:
    def __init__(self) -> None:
        self._out: asyncio.Queue[object] = asyncio.Queue()
        self._out.put_nowait(b"$ ")

    async def __aenter__(self) -> _FakeDaemonPty:
        return self

    async def __aexit__(self, *exc: object) -> None:
        return None

    async def send(self, message: object) -> None:
        await self._out.put(None if message == "exit\n" else b"echo:" + str(message).encode())

    def __aiter__(self) -> _FakeDaemonPty:
        return self

    async def __anext__(self) -> object:
        item = await self._out.get()
        if item is None:
            raise StopAsyncIteration
        return item


@pytest.fixture
def cloud_computer_app(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """``server.build_app()`` with the Cloud Computer image's environment."""
    import websockets.asyncio.client as ws_client

    issuer = _issuer()
    for name, value in {
        "BROWSER_WORKER_ID": WORKER_ID,
        "BROWSER_WORKER_PUBLIC_KEY_PEM": issuer.public_key_pem,
        "BROWSER_WORKER_TOKEN_ISSUER": ISSUER,
        "BROWSER_WORKER_DESKTOP_SESSION": "1",
        "MATRX_CLOUD_COMPUTER": "1",
        "MATRX_CLOUD_FILES_URL": "",
        "HOME": str(tmp_path),
    }.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setattr(cloud_computer_launch, "hide_process_memory", lambda: False)
    monkeypatch.setattr(machine_agent, "home_dir", lambda: str(tmp_path))
    ran: list[dict] = []

    async def fake_exec(_daemon, body, *, timeout):  # noqa: ANN001, ANN202, ASYNC109
        ran.append(body)
        if body.get("cwd") == "/home/agent":  # the daemon refuses a folder the box lacks
            request = httpx.Request("POST", "http://127.0.0.1:8765/exec/stream")
            refused = httpx.Response(400, json={"detail": "Folder not found: /home/agent"}, request=request)
            raise httpx.HTTPStatusError("400 Bad Request", request=request, response=refused)
        return {"exit_code": 0, "stdout": "gate-ok\n", "stderr": ""}

    monkeypatch.setattr(machine_agent, "run_exec", fake_exec)
    monkeypatch.setattr(ws_client, "connect", lambda url, **_: _FakeDaemonPty())
    sys.modules.pop("matrx_scraper.cloud_browser.worker.server", None)
    server = importlib.import_module("matrx_scraper.cloud_browser.worker.server")
    try:
        yield TestClient(server.app), issuer, ran
    finally:
        sys.modules.pop("matrx_scraper.cloud_browser.worker.server", None)


def test_the_agent_door_answers_on_a_cloud_computer_built_like_server_py(cloud_computer_app) -> None:
    client, issuer, ran = cloud_computer_app
    assert client.get("/health").json()["multi_browser"] is True  # the MachineBrowsers host
    reply = client.post(
        "/agent/exec",
        json={"command": "echo gate-ok"},
        headers={"x-sandbox-access-token": _agent_token(issuer)},
    )
    assert reply.status_code == 200, reply.text
    assert reply.json()["stdout"] == "gate-ok\n"
    assert ran == [{"command": "echo gate-ok"}]
    # The verifier really runs: a forged token is refused, not waved through.
    forged = client.post("/agent/exec", json={"command": "id"}, headers={"x-sandbox-access-token": "x"})
    assert forged.status_code == 401
    assert len(ran) == 1


def test_a_command_the_daemon_refuses_keeps_its_status_and_reason(cloud_computer_app) -> None:
    """Live 2026-11-13: a terminal command in a folder the box lacks answered 503 "agent daemon
    exec failed: 500 ..." (reads as the machine being down). The daemon's refusal is relayed."""
    client, issuer, _ran = cloud_computer_app
    reply = client.post(
        "/agent/exec",
        json={"command": "ls", "cwd": "/home/agent"},
        headers={"x-sandbox-access-token": _agent_token(issuer)},
    )
    assert reply.status_code == 400, reply.text
    assert reply.json()["detail"] == "Folder not found: /home/agent"


def test_the_terminal_answers_on_a_cloud_computer_built_like_server_py(cloud_computer_app) -> None:
    client, issuer, _ran = cloud_computer_app
    with client.websocket_connect(
        "/agent/pty?cols=80&rows=24", headers={"x-sandbox-access-token": _agent_token(issuer)}
    ) as ws:
        assert ws.receive_bytes() == b"$ "
        ws.send_text("echo gate-ok\n")
        assert ws.receive_bytes() == b"echo:echo gate-ok\n"
        ws.send_text("exit\n")
    with pytest.raises(WebSocketDisconnect) as closed:
        with client.websocket_connect("/agent/pty", headers={"x-sandbox-access-token": "x"}) as ws:
            ws.receive_bytes()
    assert closed.value.code == 4401


# ── the guard: one surface, two hosts ───────────────────────────────────────


def _worker_reads() -> tuple[set[str], list[str]]:
    """Every ``worker.<name>`` the HTTP layer reads, and every read hidden behind a default."""
    tree = ast.parse(Path(http_app.__file__).read_text())
    names: set[str] = set()
    hidden: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "worker":
            names.add(node.attr)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in {"getattr", "hasattr"}
            and node.args
            and isinstance(node.args[0], ast.Name)
            and node.args[0].id == "worker"
        ):
            hidden.append(f"line {node.lineno}: {node.func.id}(worker, ...)")
    return names, hidden


def test_every_attribute_http_app_reads_exists_on_both_host_classes() -> None:
    names, hidden = _worker_reads()
    assert {"token_verifier", "worker_id", "health"} <= names  # the walk sees the reads
    assert hidden == [], "a worker read hidden behind a default lets one host lack it: " + "; ".join(hidden)
    missing = {
        cls.__name__: sorted(n for n in names if not hasattr(cls, n) and n not in _instance_attrs(cls))
        for cls in (BrowserWorker, MachineBrowsers)
    }
    assert missing == {"BrowserWorker": [], "MachineBrowsers": []}


def _instance_attrs(cls: type) -> set[str]:
    """Attributes ``__init__`` assigns on ``self`` (``self.worker_id = ...``)."""

    tree = ast.parse(stable_source(cls))
    return {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "self"
        and isinstance(node.ctx, ast.Store)
    }


def test_the_memory_door_answers_on_a_cloud_computer_built_like_server_py(
    cloud_computer_app, tmp_path: Path
) -> None:
    """The person's memory push (``POST /machine/memory``) reaches the real app with the real
    machine agent token and lands in the home; no token is a 401."""
    client, issuer, _ = cloud_computer_app
    body = {"source": "personal", "files": [{"path": "about-me.md", "content": "Likes tea."}],
            "rendering": "# Your memory\n"}
    assert client.post("/machine/memory", json=body).status_code == 401
    reply = client.post("/machine/memory", json=body,
                        headers={"X-Sandbox-Access-Token": _agent_token(issuer)})
    assert reply.status_code == 200, reply.text
    assert (tmp_path / ".matrx" / "memory" / "about-me.md").read_text() == "Likes tea."
    assert "person_memory" in client.get("/health").json().get("capabilities", [])
