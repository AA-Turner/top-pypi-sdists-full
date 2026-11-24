"""The worker's ``/agent/preview/{port}/…`` door: a dev server on the machine's loopback, for a
person AI Dream admitted (port previews). A REAL ``http.server`` answers on a free loopback port;
the door must relay it only with the machine agent token, and never open the machine's own services.
"""

from __future__ import annotations

import functools
import http.server
import socket
import threading
from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from matrx_scraper.cloud_browser.worker import http_app, machine_agent
from matrx_scraper.cloud_browser.worker.errors import WorkerProtocolError


@pytest.fixture
def dev_server(tmp_path):
    (tmp_path / "hello.txt").write_text("hello from the machine")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(tmp_path))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield server.server_address[1]
    server.shutdown()


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _client(monkeypatch: pytest.MonkeyPatch, tmp_path) -> TestClient:
    monkeypatch.setattr(machine_agent, "home_dir", lambda: str(tmp_path))

    def verify(token: str, **_: object) -> None:
        if token != "machine-token":
            raise WorkerProtocolError("bad_token")

    worker = SimpleNamespace(worker_id="w", token_verifier=SimpleNamespace(verify=verify))
    launch = SimpleNamespace(files_token="", files_url="", process_env={})
    app = FastAPI()
    http_app._install_machine_files_and_agent(app, worker, launch)  # type: ignore[arg-type]
    return TestClient(app)


TOKEN = {"x-sandbox-access-token": "machine-token"}


def test_a_dev_server_on_the_machine_is_relayed_with_the_machine_token(monkeypatch, tmp_path, dev_server) -> None:
    client = _client(monkeypatch, tmp_path)
    resp = client.get(f"/agent/preview/{dev_server}/hello.txt", headers=TOKEN)
    assert resp.status_code == 200, resp.text
    assert resp.text == "hello from the machine"
    # The catch-all daemon door did NOT take the call.
    assert client.get(f"/agent/preview/{dev_server}/missing.txt", headers=TOKEN).status_code == 404


def test_no_machine_token_no_preview(monkeypatch, tmp_path, dev_server) -> None:
    client = _client(monkeypatch, tmp_path)
    assert client.get(f"/agent/preview/{dev_server}/hello.txt").status_code == 401
    assert client.get(
        f"/agent/preview/{dev_server}/hello.txt", headers={"x-sandbox-access-token": "forged"}
    ).status_code == 401


@pytest.mark.parametrize("port", [8002, 8080, machine_agent.AGENT_PORT, 0, 70000])
def test_the_machines_own_services_are_never_a_preview(monkeypatch, tmp_path, port) -> None:
    client = _client(monkeypatch, tmp_path)
    resp = client.get(f"/agent/preview/{port}/", headers=TOKEN)
    assert resp.status_code == 403, resp.text


def test_a_port_nobody_listens_on_says_so(monkeypatch, tmp_path) -> None:
    client = _client(monkeypatch, tmp_path)
    port = _free_port()
    resp = client.get(f"/agent/preview/{port}/", headers=TOKEN)
    assert resp.status_code == 502
    assert f"port {port}" in resp.text


def test_this_build_says_it_can_preview_ports() -> None:
    assert "port_preview" in http_app.MACHINE_CAPABILITIES
