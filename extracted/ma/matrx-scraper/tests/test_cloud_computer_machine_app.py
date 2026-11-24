"""The Cloud Computer's supervised app and its ``/app`` door (machines plan 4b part 2 item 3).

The host names one app (argv, folder in the home, loopback port, exact env); the worker
starts it with ONLY that env on a minimal base (never the worker's launch env, which holds
the machine files token), restarts it when it exits, logs into the home, stops it on
request or worker shutdown, and relays ``/app/{path}`` to it behind the machine agent token.
"""

from __future__ import annotations

import asyncio
import json
import sys
from types import SimpleNamespace

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from matrx_scraper.cloud_browser.worker import http_app, machine_agent
from matrx_scraper.cloud_browser.worker.errors import WorkerProtocolError
from matrx_scraper.cloud_browser.worker.machine_app import (
    AppSpec,
    AppSpecError,
    MachineApp,
    parse_spec,
)

# A child that records its environment and exits 3 (so the supervisor must restart it).
_RECORD_AND_EXIT = (
    "import json, os, sys; p = sys.argv[1]; "
    "n = len(open(p).read().splitlines()) if os.path.exists(p) else 0; "
    "open(p, 'a').write(json.dumps(dict(os.environ)) + '\\n'); "
    "print('ran', n, flush=True); sys.exit(3)"
)


def test_the_app_gets_only_its_spec_env_restarts_on_exit_and_logs_to_the_home(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("MATRX_CLOUD_FILES_TOKEN", "files-secret")  # the worker's own env
    record = tmp_path / "env.jsonl"
    app = MachineApp(str(tmp_path))
    spec = AppSpec(
        name="aidream", argv=(sys.executable, "-c", _RECORD_AND_EXIT, str(record)),
        cwd=str(tmp_path), port=18001, env={"USER_ID": "u1", "MATRX_TIER": "cloud_computer"},
    )

    async def scenario() -> dict:
        answer = await app.apply(spec)
        for _ in range(100):
            if record.exists() and len(record.read_text().splitlines()) >= 2:
                break
            await asyncio.sleep(0.05)
        again = await app.apply(spec)  # the same spec is a no-op
        await app.stop()
        return {"first": answer, "again": again}

    out = asyncio.run(scenario())
    runs = [json.loads(line) for line in record.read_text().splitlines()]
    assert len(runs) >= 2, "an exited app is restarted"
    env = runs[0]
    assert env["USER_ID"] == "u1" and env["MATRX_TIER"] == "cloud_computer"
    assert env["HOME"] == str(tmp_path)
    assert "MATRX_CLOUD_FILES_TOKEN" not in env, "the worker's launch env never reaches the app"
    # The supervisor hands over only base + spec env. The OS/interpreter itself adds a few vars at
    # exec (macOS injects __CF_USER_TEXT_ENCODING into every child process; Python sets LC_CTYPE/PWD),
    # so those are allowed; anything else would be a leak from the worker's environment.
    os_injected = {"__CF_USER_TEXT_ENCODING", "LC_CTYPE", "PWD"}
    assert set(env) <= {"USER_ID", "MATRX_TIER", "HOME", "PATH", "LANG"} | os_injected
    assert out["first"]["changed"] is True and out["again"]["changed"] is False
    assert app.status()["last_exit"] == 3 and app.status()["restarts"] >= 1
    log = (tmp_path / ".matrx" / "app" / "aidream.log").read_text()
    assert "ran 0" in log and "starting aidream" in log
    assert app.status()["env_names"] == ["MATRX_TIER", "USER_ID"]  # names, never values


def test_stop_ends_a_running_app(tmp_path) -> None:
    app = MachineApp(str(tmp_path))
    spec = AppSpec(name="sleeper", argv=(sys.executable, "-c", "import time; time.sleep(60)"), cwd=str(tmp_path), port=18002)

    async def scenario() -> tuple[bool, bool]:
        await app.apply(spec)
        for _ in range(100):
            if app.running:
                break
            await asyncio.sleep(0.05)
        was = app.running
        await app.stop()
        return was, app.running

    was, after = asyncio.run(scenario())
    assert was is True and after is False


def test_the_spec_is_held_to_the_home_and_off_the_daemon_port(tmp_path) -> None:
    good = {"name": "aidream", "argv": ["python", "run.py"], "cwd": "repos/aidream", "port": 8001, "env": {"A": "b"}}
    spec = parse_spec(good, home=str(tmp_path))
    assert spec.cwd == str((tmp_path / "repos" / "aidream").resolve())
    for bad in (
        {**good, "cwd": "/etc"},
        {**good, "cwd": "../.."},
        {**good, "port": 8765},
        {**good, "port": 80},
        {**good, "argv": []},
        {**good, "env": {"A": 1}},
        {**good, "name": "Bad Name"},
    ):
        with pytest.raises(AppSpecError):
            parse_spec(bad, home=str(tmp_path))


def _client(monkeypatch, tmp_path, seen: list[httpx.Request], *, verify=None) -> tuple[TestClient, FastAPI]:
    monkeypatch.setattr(machine_agent, "home_dir", lambda: str(tmp_path))
    real = httpx.AsyncClient

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(
            200, headers={"content-type": "application/x-ndjson", "x-from": "app"},
            stream=httpx.ByteStream(b'{"a":1}\n{"b":2}\n'),
        )

    def client(*args, **kwargs):  # noqa: ANN002, ANN003
        return real(transport=httpx.MockTransport(handler), timeout=kwargs.get("timeout"))

    monkeypatch.setattr(httpx, "AsyncClient", client)

    async def listening(self, timeout: float) -> bool:  # noqa: ANN001
        return True

    monkeypatch.setattr(MachineApp, "wait_listening", listening)
    worker = SimpleNamespace(worker_id="w", token_verifier=SimpleNamespace(verify=verify or (lambda *a, **k: None)))
    launch = SimpleNamespace(files_token="", files_url="", process_env={})
    app = FastAPI()
    http_app._install_machine_files_and_agent(app, worker, launch)  # type: ignore[arg-type]
    return TestClient(app), app


def test_the_app_door_relays_with_the_persons_jwt_and_consumes_the_machine_token(monkeypatch, tmp_path) -> None:
    seen: list[httpx.Request] = []
    client, app = _client(monkeypatch, tmp_path, seen)
    assert client.get("/app/api/health/version", headers={"x-sandbox-access-token": "t"}).status_code == 409
    app.state.machine_app.spec = AppSpec(name="aidream", argv=("x",), cwd=str(tmp_path), port=18003)
    resp = client.post(
        "/app/api/coding-sessions/claude/stream?account=abc",
        json={"q": 1},
        headers={"x-sandbox-access-token": "t", "authorization": "Bearer person-jwt", "x-organization-id": "o1"},
    )
    assert resp.status_code == 200
    assert resp.content == b'{"a":1}\n{"b":2}\n'
    assert resp.headers["x-from"] == "app"
    upstream = seen[-1]
    assert str(upstream.url) == "http://127.0.0.1:18003/api/coding-sessions/claude/stream?account=abc"
    assert upstream.headers["authorization"] == "Bearer person-jwt"
    assert upstream.headers["x-organization-id"] == "o1"
    assert "x-sandbox-access-token" not in upstream.headers
    assert json.loads(upstream.content) == {"q": 1}


def test_the_app_door_and_its_control_refuse_without_the_machine_token(monkeypatch, tmp_path) -> None:
    def refuse(*_a, **_k):  # noqa: ANN002, ANN003
        raise WorkerProtocolError("bad_token")

    seen: list[httpx.Request] = []
    client, app = _client(monkeypatch, tmp_path, seen, verify=refuse)
    app.state.machine_app.spec = AppSpec(name="aidream", argv=("x",), cwd=str(tmp_path), port=18004)
    assert client.get("/app/api/health/version").status_code == 401
    assert client.put("/machine/app", json={}).status_code == 401
    assert client.get("/machine/app").status_code == 401
    assert seen == []
