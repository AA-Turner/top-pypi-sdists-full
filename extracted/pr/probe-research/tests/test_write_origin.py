"""A run process's writes say so (swarm friction R41).

A training script, a sweep or a job a launcher started inherits its agent's
session from the environment, so its writes carry that session -- and a
background job that keeps filing runs while the agent sits idle at its prompt
read as the agent working (1.5 h of the Fourier branch's 3.0 h wall time). A
process that opens a run for itself (`probe.init()`, `Client.run()` in a
script, a job joining `PROBE_RUN_ID`) and `probe exec`'s launcher are marked
(`PROBE_RUN_PROCESS`, naming the session they run as); their writes, and those
of what they start as the same session, send `X-Probe-Write-Origin: run`. The
agent's own `probe` commands never do. A queued op records its origin and is
sent with it whichever process drains it.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from types import SimpleNamespace

import httpx
import pytest

from probe.sdk import agent_session
from probe.sdk import journal as jm
from probe.sdk import outbox_worker, service_handoff
from probe.sdk import transport as transport_mod
from probe.sdk.agent_session import (
    AGENT_SESSION_HEADER,
    EVENT_AT_ENV,
    RUN_PROCESS_ENV,
    WRITE_ORIGIN_HEADER,
)
from probe.sdk.client import Client
from probe.sdk.config import Settings
from probe.sdk.journal import Journal, drain
from probe.sdk.surface import Surface
from probe.sdk.transport import Transport
from tests.conftest import make_client, open_run
from tests.served_fake_app import child_env, serve

SESSION = "643ce138-4801-4409-b69c-ca30ab7605bc"
OTHER = "5f0c1d2e-bbbb-4a10-9f3e-00000000000b"
AS_SESSION = f"claude_code:{SESSION}"
SETTINGS = Settings(base_url="http://test", token="test-token")


@pytest.fixture(autouse=True)
def under_claude_code(monkeypatch, tmp_path):
    """A Claude Code session, and an unmarked process whose mark, when a test
    makes one, is undone after it (`mark_run_process` writes `os.environ`)."""
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_ATTRIBUTION", raising=False)
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SESSION)
    monkeypatch.setenv(RUN_PROCESS_ENV, "registered for undo")
    monkeypatch.delenv(RUN_PROCESS_ENV)


def _client(seen: list[httpx.Request], *, surface: str = Surface.SDK.value, **kwargs) -> Client:
    def handle(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"id": "r1"})

    http = httpx.Client(base_url="http://test", transport=httpx.MockTransport(handle))
    transport = Transport(SETTINGS, client=http, surface=surface)
    return Client(settings=SETTINGS, transport=transport, auto_drain=False, **kwargs)


def _origins(requests) -> set[str | None]:
    """The origin of every request that named the session."""
    return {r.headers.get(WRITE_ORIGIN_HEADER) for r in requests if r.headers.get(AGENT_SESSION_HEADER)}


def test_a_script_opening_a_run_is_that_runs_process(app):
    """`Client.run()` from a script marks the process before its create, so
    the create, its writes and everything after go as the run's (what the
    script wrote before opening a run, `open_run`'s experiment here, did not)."""
    client = make_client(app)
    run = open_run(client, experiment="e1", name="sweep", heartbeat=False)
    run.log({"loss": 0.5}, step=1)
    run.finish()
    client.close()
    assert agent_session.run_write_origin(AS_SESSION) == "run"
    [create] = [i for i, r in enumerate(app.requests) if r.method == "POST" and r.url.path.endswith("/runs")]
    assert _origins(app.requests[create:]) == {"run"}
    assert any(r.method == "PATCH" for r in app.requests[create:])


def test_the_agents_own_cli_commands_never_send_it(app):
    """A `probe` command's run is one write its agent made: a CLI client marks
    nothing, and in an unmarked process no request carries an origin."""
    httpx_client = httpx.Client(base_url="http://test", transport=httpx.MockTransport(app.handler))
    settings = Settings(base_url="http://test", token="ros_pat_deadbeef", workspace="mine")
    cli = Client(
        settings=settings,
        transport=Transport(settings, client=httpx_client, surface=Surface.CLI.value),
        async_writes=False,
    )
    app.seed_experiment("e1")
    cli.run(experiment="e1", name="typed", heartbeat=False, snapshot=False, capture_outputs=False)
    cli.close()
    assert RUN_PROCESS_ENV not in os.environ
    assert app.requests and _origins(app.requests) == {None}


class Stop(Exception):
    pass


def _stop(*_a, **_kw):
    raise Stop


@pytest.mark.parametrize("surface, origin", [(Surface.SDK.value, "run"), (Surface.CLI.value, None)])
def test_joining_a_run_marks_a_script_and_never_a_command(monkeypatch, surface, origin):
    """`attach_run()` marks like `run()`: a job joining its run (the rank-lease
    and Lightning paths) is the run's process; `probe` attaching for one write
    (CLI surface) is its agent's."""
    monkeypatch.setattr(Client, "get_run", _stop)
    with _client([], surface=surface, async_writes=False) as client, pytest.raises(Stop):
        client.attach_run("r1")
    assert agent_session.run_write_origin(AS_SESSION) == origin


@pytest.mark.parametrize("command", ["import_local", "import_hosted"])
def test_a_wandb_import_is_the_agents_own_command(monkeypatch, tmp_path, command):
    """`probe wandb import-*` opens runs through the W&B connector's
    `client.run()`: its client is the CLI's, so the command never marks itself a
    run process and its writes stay the agent's."""
    from probe.cli import wandb_import
    from probe.connectors import wandb as wb

    used = []

    def importer(client, *_a, **_kw):
        used.append(client.transport.surface)
        with pytest.raises(Stop):
            client.run(experiment="e")
        return SimpleNamespace(wandb_run_id="w", probe_run_id=None, tier=SimpleNamespace(value="t"),
                               metrics_written=0, points_written=0, requests=0, warnings=[])

    monkeypatch.setattr(Client, "_run_impl", _stop)
    monkeypatch.setattr(wb, "import_local_runs", lambda *a, **kw: [importer(*a, **kw)])
    monkeypatch.setattr(wb, "fetch_hosted_runs", lambda *_a, **_kw: [object()])
    monkeypatch.setattr(wb, "import_wandb_run", importer)
    monkeypatch.setenv("PROBE_TOKEN", "ros_pat_deadbeef")
    if command == "import_local":
        wandb_import.import_local(root=str(tmp_path), project="p", dry_run=True)
    else:
        wandb_import.import_hosted(entity="e", wandb_project="w", project="p", run_id=None, dry_run=True)
    assert used == [Surface.CLI.value]
    assert agent_session.run_write_origin(AS_SESSION) is None


def test_init_marks_the_process_in_every_mode_that_writes(monkeypatch):
    """`probe.init()` marks before it opens anything, offline included; a
    disabled run writes nothing and marks nothing."""
    from probe.sdk import fluent

    monkeypatch.setattr(fluent, "_replace_previous", _stop)
    with pytest.raises(Stop):
        fluent.init(mode="disabled")
    assert agent_session.run_write_origin(AS_SESSION) is None
    with pytest.raises(Stop):
        fluent.init(mode="offline", project="p")
    assert agent_session.run_write_origin(AS_SESSION) == "run"


def test_what_a_run_starts_is_the_runs_only_as_the_same_session(monkeypatch):
    """A `probe` command the training script runs inherits the mark and goes as
    the run's; a coding agent started beneath the run (an eval harness,
    `probe exec -- claude`) has a session of its own and is its own writer."""
    monkeypatch.setenv(RUN_PROCESS_ENV, AS_SESSION)
    seen: list[httpx.Request] = []
    with _client(seen, surface=Surface.CLI.value, async_writes=False) as child:
        child.transport.post("/v1/projects", {"name": "from the script"})
        monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", OTHER)
        child.transport.post("/v1/projects", {"name": "from an agent it started"})
    assert [r.headers.get(WRITE_ORIGIN_HEADER) for r in seen] == ["run", None]
    assert seen[1].headers[AGENT_SESSION_HEADER] == OTHER


def test_no_session_no_mark_and_no_header(monkeypatch):
    monkeypatch.delenv("CLAUDECODE")
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID")
    agent_session.mark_run_process()
    assert RUN_PROCESS_ENV not in os.environ


def _queue_one(spool) -> tuple:
    producer = Client(settings=SETTINGS, spool_dir=spool, async_writes=True, auto_drain=False)
    producer.write("POST", "/v1/projects", {"name": "queued"})
    [(path, op)] = producer.journal.pending()
    producer.transport.close()
    return path, op


def _drained(spool) -> list[httpx.Request]:
    seen: list[httpx.Request] = []
    assert drain(Journal(spool), client_factory=lambda _ctx: _client(seen, spool_dir=spool)).delivered == 1
    return seen


def test_a_runs_queued_write_stays_the_runs_whoever_drains_it(monkeypatch, tmp_path):
    monkeypatch.setenv(RUN_PROCESS_ENV, AS_SESSION)
    _, op = _queue_one(tmp_path / "a")
    assert op["write_origin"] == "run"
    monkeypatch.delenv(RUN_PROCESS_ENV)  # an outbox worker: drains, opens no run
    [sent] = _drained(tmp_path / "a")
    assert sent.headers[WRITE_ORIGIN_HEADER] == "run"
    assert sent.headers[AGENT_SESSION_HEADER] == SESSION


def test_a_run_process_draining_lends_no_op_its_origin(monkeypatch, tmp_path):
    """The agent's own queued command, and an op an older SDK queued, go with
    no origin even when the process draining them is a run's."""
    _, agent_op = _queue_one(tmp_path / "a")
    assert "write_origin" not in agent_op
    path, old = _queue_one(tmp_path / "b")
    del old["agent_session"]
    path.write_text(json.dumps(old))
    monkeypatch.setenv(RUN_PROCESS_ENV, AS_SESSION)
    for spool in ("a", "b"):
        [sent] = _drained(tmp_path / spool)
        assert sent.headers[AGENT_SESSION_HEADER] == SESSION
        assert WRITE_ORIGIN_HEADER not in sent.headers, spool


def test_an_upload_request_carries_one_origin(monkeypatch, tmp_path):
    """A window's uploads share a request only with one origin: a run's files
    and the agent's own go apart."""
    from test_outbox_run_upload_window import Server, upload

    monkeypatch.setattr(jm, "MIN_FREE_BYTES", 0)
    monkeypatch.delenv("PROBE_UPLOAD_WORKERS", raising=False)
    monkeypatch.delenv("PROBE_UPLOAD_MANY", raising=False)
    monkeypatch.setattr(jm, "queued_session", lambda: AS_SESSION)
    queue = Journal(tmp_path / "outbox")
    for i in range(4):
        upload(queue, tmp_path, f"out/file{i}.txt")
    for i, (path, op) in enumerate(queue.pending()):
        stamped = {**op, "enqueued_at": "2026-10-29T10:00:30+00:00"}
        if i % 2:
            stamped["write_origin"] = "run"
        path.write_text(json.dumps(stamped))

    asked: list[tuple] = []

    class Recording(Server):
        def presign_run_uploads(self, run_id, items, *, direct=False):
            asked.append((transport_mod._queued_origin.get(), len(items)))
            return super().presign_run_uploads(run_id, items, direct=direct)

    assert drain(queue, client_factory=lambda _context: Recording()).delivered == 4
    assert sorted(asked, key=lambda a: a[0] or "") == [(None, 2), ("run", 2)]


def test_a_drainer_never_inherits_the_mark(monkeypatch):
    """A drainer sends every writer's ops, each with its own origin and date,
    whether this process forks it or the Probe service starts it."""
    monkeypatch.setenv(RUN_PROCESS_ENV, AS_SESSION)
    monkeypatch.setenv(EVENT_AT_ENV, "2026-10-29T01:00:00+00:00")
    assert RUN_PROCESS_ENV not in outbox_worker._worker_env()
    assert RUN_PROCESS_ENV not in outbox_worker._rescuer_env()

    handed: dict = {}

    class Service:
        def drain_outbox(self, path, executable, env, **_kw):
            handed.update(env)

    monkeypatch.setattr(service_handoff, "_background_env", lambda: {
        RUN_PROCESS_ENV: AS_SESSION, EVENT_AT_ENV: "2026-10-29T01:00:00+00:00", "PROBE_BASE_URL": "http://test",
    })
    monkeypatch.setattr(service_handoff, "_ask", lambda _m, send, **_kw: (send(Service(), 0.0, None), (None, None))[1])
    service_handoff.drain("/tmp/outbox")
    assert handed == {"PROBE_BASE_URL": "http://test"}


# -- end to end, real processes on the served fake ------------------------------


def test_probe_exec_and_its_job_are_the_run_and_the_agents_command_is_not(app, tmp_path):
    """Under a Claude Code session: `probe exec` wrapping a job that calls
    `probe.init()` sends every write as the run's -- the launcher's create and
    close, the job's attach and points; the agent's own `probe run start`
    sends none."""
    app.seed_experiment("e1")
    child = tmp_path / "train.py"
    child.write_text("import probe\nprobe.init()\nprobe.log({'loss': 0.5}, step=1)\n")
    env = child_env("", CLAUDECODE="1", CLAUDE_CODE_SESSION_ID=SESSION)
    env.pop(RUN_PROCESS_ENV, None)
    with serve(app) as url:
        env["PROBE_BASE_URL"] = url
        wrapped = subprocess.run(
            [sys.executable, "-m", "probe.cli", "exec", "--experiment", "e1", "--", sys.executable, str(child)],
            env=env, cwd=tmp_path, capture_output=True, text=True, timeout=120,
        )
        assert wrapped.returncode == 0, wrapped.stderr[-2000:]
        launched = list(app.requests)
        typed = subprocess.run(
            [sys.executable, "-m", "probe.cli", "run", "start", "--experiment", "e1", "--name", "typed"],
            env=env, cwd=tmp_path, capture_output=True, text=True, timeout=120,
        )
        assert typed.returncode == 0, typed.stderr[-2000:]
    commanded = app.requests[len(launched):]
    assert any(r.method == "PATCH" for r in launched) and _origins(launched) == {"run"}
    assert commanded and _origins(commanded) == {None}
