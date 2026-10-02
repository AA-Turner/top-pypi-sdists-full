"""What the daemon's logbook files a `probe` write as, from the REAL CLI (L14).

A refused write used to exit 0 (the CLI queued the server's refusal and printed
`null`), so the logbook marked it `ran` and the state of the record listed it
under "Recorded". These run the real `probe` executable the daemon runs, with
the daemon's key and session, against the fake backend over a socket (a
refusal), or against a port nobody listens on (no answer).
"""

from __future__ import annotations

import asyncio
import json
import socket
import time

import httpx
import pytest

from probe.daemon import approvals as appr
from probe.daemon import lease, probe_api, tools
from probe.daemon.store import Store
from tests.conftest import FakeApp
from tests.served_fake_app import serve

SID = "11111111-2222-3333-4444-555555555555"
RUN_A = "11111111-1111-4111-8111-111111111111"
RUN_B = "22222222-2222-4222-8222-222222222222"
EDGE = ["edge", "add", "--source", f"run:{RUN_B}", "--relation", "derived_from", "--target", f"run:{RUN_A}",
        "--reason", "B was started from A's checkpoint"]


@pytest.fixture(autouse=True)
def _state(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.setattr(probe_api, "_features", None)


class Refusing(FakeApp):
    def handler(self, request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and request.url.path == "/v1/edges":
            return httpx.Response(404, json={"detail": "target endpoint not found"})
        return super().handler(request)


def _deps(tmp_path, base_url: str) -> tools.Deps:
    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    env = {"PROBE_BASE_URL": base_url, "PROBE_TOKEN": "ros_pat_deadbeef", "PROBE_DAEMON_SESSION": SID,
           "PROBE_OUTBOX_DIR": str(tmp_path / "outbox"), "PROBE_AUTO_SNAPSHOT": "0"}
    lease.sessions_dir().mkdir(parents=True, exist_ok=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")
    assert lease.renew(SID)
    return tools.Deps(store=Store(tmp_path / "s.sqlite", clock=time.time), board=appr.Board(tmp_path / "appr"),
                      session_id=SID, cwd=work, workdirs=[work], home=tmp_path, write_dirs=[], probe_env=env,
                      bypass=False, mode_known=True, bite_id=1, replay=None)


def _statuses(deps: tools.Deps) -> list[str]:
    return [r["status"] for r in deps.store.db.execute("SELECT status FROM writes ORDER BY id")]


def _dead_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]  # closed on exit: nothing listens there


def test_a_refused_link_is_failed_in_the_logbook_never_recorded(tmp_path):
    with serve(Refusing()) as url:
        deps = _deps(tmp_path, url)
        out = asyncio.run(tools.run_probe_command(deps, EDGE, why="B continues A"))
    assert out.startswith("[exit 1]") and "target endpoint not found" in out, out
    assert _statuses(deps) == ["failed"]
    assert deps.store.filed() == []
    assert [r["status"] for r in deps.store.open_failures(bites=10, limit=5)] == ["failed"]


def test_a_link_probe_did_not_answer_is_queued_apart_from_recorded(tmp_path, monkeypatch):
    from probe.daemon import worker as worker_mod

    deps = _deps(tmp_path, f"http://127.0.0.1:{_dead_port()}")
    out = asyncio.run(tools.run_probe_command(deps, EDGE, why="B continues A"))
    assert out.startswith("[exit 0]") and "probe: queued: POST /v1/edges" in out, out
    assert _statuses(deps) == ["queued"]
    assert deps.store.filed() == []  # not "Recorded"
    [row] = deps.store.open_failures(bites=10, limit=5)
    assert row["status"] == "queued"

    # The state of the record (`session` op=status) lists it apart from Recorded.
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(json.dumps({"type": "user", "message": {"content": "go"}, "cwd": str(deps.cwd)}) + "\n")
    worker = worker_mod.Worker(worker_mod.Session(SID, transcript, deps.cwd, "claude_code", home=tmp_path))
    worker.store = deps.store
    state = worker.state_of_record()
    recorded, pending = state.split("Not recorded yet, or waiting for the researcher:")
    assert "edge add" not in recorded and "- nothing yet" in recorded
    assert f"- queued: probe edge add --source run:{RUN_B}" in pending
    assert worker_mod.QUEUED_LINE in pending and "don't run it again" in worker_mod.QUEUED_LINE


def test_a_later_success_of_the_same_link_clears_the_queued_line(tmp_path):
    deps = _deps(tmp_path, "http://unused.test")
    argv = ["probe", *EDGE]
    deps.store.log_write(bite=1, op_id="a", argv=argv, head="edge add", status="failed")
    deps.store.log_write(bite=1, op_id="b", argv=argv, head="edge add", status="queued")
    assert [r["status"] for r in deps.store.open_failures(bites=10, limit=5)] == ["queued"]
    deps.store.log_write(bite=1, op_id="c", argv=argv, head="edge add", status="ran")
    assert deps.store.open_failures(bites=10, limit=5) == []


@pytest.mark.parametrize("code, stderr, status", [
    (0, "", "ran"),
    (0, "probe: queued: POST /v1/edges was not delivered (ConnectError)", "queued"),
    (0, 'a warning quotes "probe: queued: " mid-line', "ran"),
    (1, "error: target endpoint not found", "failed"),
    (None, "", "failed"),
])
def test_the_logbook_status_of_a_write(code, stderr, status):
    assert tools.write_status(code, stderr) == status


def test_the_queued_line_counts_on_stderr_only(tmp_path, monkeypatch):
    """stdout is the record the command printed: a note or a reason quoting the
    CLI's line at the start of one of its lines must not file the write as queued."""
    async def run(deps, argv, op_id, *, cwd=None):
        return tools.ProbeResult(0, '{"reason": "x"}\nprobe: queued: POST /v1/edges was not delivered\n', "")

    monkeypatch.setattr(tools, "run_probe_process", run)
    deps = _deps(tmp_path, "http://unused.test")
    asyncio.run(tools.run_probe_command(deps, EDGE))
    assert _statuses(deps) == ["ran"]
