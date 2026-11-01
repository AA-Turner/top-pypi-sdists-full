"""Pins that an outbox TODAY's SDK wrote still drains: every queued op delivered, status.json's shape kept.

`baselines/journal_fixture/` is frozen (UPDATE=1 never touches it): rebuild it only with
PROBE_SAFETY_NET=1 PROBE_SAFETY_NET_RECORD_JOURNAL=1, and NEVER during the restructure.
"""

from __future__ import annotations

import json
import os
import shutil
import socket
from pathlib import Path

import httpx
import pytest

import probe

from tests.conftest import FakeApp, make_client
from tests.safety_net.sdk.sdk_session import SESSION, child_env, cli, close_open_runs, run_session
from tests.safety_net.sdk.wire_recording import recording
from tests.served_fake_app import serve

RECORD = os.environ.get("PROBE_SAFETY_NET_RECORD_JOURNAL") == "1"
FIXTURE = Path(__file__).resolve().parent / "baselines" / "journal_fixture"
FIXTURE_HOST, FIXTURE_PID = "fixture-host", "4242"
#: Placeholders the fixture carries where the recording machine's values were.
RUN_ID, BASE_URL, FILES, OUTBOX = "<RUN_ID>", "<BASE_URL>", "<FILES>", "<OUTBOX>"
#: Runtime flock sidecars: recreated on demand, never state.
_SIDECARS = (".append.lock", ".drain.lock", ".drain.want", ".promote.lock", ".run-locks")


@pytest.fixture(autouse=True)
def _no_bound_run(monkeypatch):
    monkeypatch.delenv("PROBE_RUN_ID", raising=False)
    close_open_runs()
    yield
    close_open_runs()


def _frozen(text: str, swaps: dict[str, str]) -> str:
    for old, new in sorted(swaps.items(), key=lambda kv: -len(kv[0])):
        text = text.replace(old, new)
    return text


def _record_fixture(tmp_path: Path) -> None:
    """Run the session against a server that fails every write, then freeze the outbox."""
    app = FakeApp()
    serve_up = app.handler
    run: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        if run:  # the run is open: from here on the server answers 503
            app.requests.append(request)
            return httpx.Response(503, json={"detail": "down"})
        return serve_up(request)

    def outage() -> None:
        run["id"] = probe.active_run().id

    app.handler = handler
    outbox, files = tmp_path / "outbox", tmp_path / "files"
    client = make_client(app, tmp_spool=outbox, async_writes=True)
    run_session(files, big=False, client=client, after_init=outage)
    pid = str(os.getpid())
    swaps = {
        run["id"]: RUN_ID, "http://test": BASE_URL, str(files): FILES, str(outbox): OUTBOX,
        socket.gethostname(): FIXTURE_HOST, f":{pid}:": f":{FIXTURE_PID}:", f"_{pid}_": f"_{FIXTURE_PID}_",
    }
    shutil.rmtree(FIXTURE, ignore_errors=True)
    for path in sorted(outbox.rglob("*")):
        relative = path.relative_to(outbox)
        if not path.is_file() or relative.parts[0] in _SIDECARS:
            continue
        target = FIXTURE / _frozen(str(relative), swaps)
        target.parent.mkdir(parents=True, exist_ok=True)
        if relative.parts[0] == "blobs":
            target.write_bytes(path.read_bytes())
        else:
            target.write_text(_frozen(path.read_text(encoding="utf-8"), swaps), encoding="utf-8")


def test_journal_fixture_is_frozen_and_machine_free(tmp_path):
    leaks = ["/tmp/", "pytest-of-"]
    if RECORD:
        _record_fixture(tmp_path)
        leaks += [str(tmp_path.parent), socket.gethostname()]  # only the recorder knows its own
    ops = sorted((FIXTURE / "ops").glob("*.json"))
    assert ops and (FIXTURE / "status.json").is_file(), f"no fixture at {FIXTURE}"
    for path in FIXTURE.rglob("*"):
        if path.is_file() and "blobs" not in path.parts:
            text = path.read_text(encoding="utf-8")
            assert not [leak for leak in leaks if leak in text], f"{path} names the recording machine"


def _thaw(outbox: Path, swaps: dict[str, str]) -> None:
    for path in FIXTURE.rglob("*"):
        if not path.is_file():
            continue
        target = outbox / path.relative_to(FIXTURE)
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        if "blobs" in path.relative_to(FIXTURE).parts:
            target.write_bytes(path.read_bytes())
        else:
            target.write_text(_frozen(path.read_text(encoding="utf-8"), swaps), encoding="utf-8")
        target.chmod(0o600)


def _shape(value):
    if isinstance(value, dict):
        return {k: _shape(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_shape(value[0])] if value else []
    return "null" if value is None else type(value).__name__


def test_frozen_outbox_drains_every_op(tmp_path, baseline, monkeypatch):
    app = FakeApp()
    seed = make_client(app)
    run = seed.run(**SESSION, heartbeat=False)  # the run the frozen ops were queued for
    app.requests.clear()
    outbox, files = tmp_path / "outbox", tmp_path / "files"
    files.mkdir()
    (files / "notes.txt").write_text("eval notes\n", encoding="utf-8")
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(outbox))
    with serve(app) as url:
        app.upload_base = url
        _thaw(outbox, {RUN_ID: run.id, BASE_URL: url, FILES: str(files), OUTBOX: str(outbox)})
        queued = len(list((outbox / "ops").glob("*.json")))
        done = cli(["outbox", "drain"], child_env(url, tmp_path), tmp_path)
        requests = list(app.requests)
    assert done.returncode == 0, done.stdout + done.stderr
    assert f"delivered {queued};" in done.stdout and "0 remaining" in done.stdout, done.stdout
    assert not list((outbox / "ops").glob("*.json")) and not list((outbox / "failed").glob("*")), "op left behind"
    assert app.runs[run.id]["status"] == "completed", "the queued close landed"
    baseline("journal_drain", recording(requests, {url: "<server>", str(tmp_path): "<tmp_path>"}))
    status = json.loads((outbox / "status.json").read_text(encoding="utf-8"))
    baseline("journal_status_shape", _shape(status))
