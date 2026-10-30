"""Daemon reads answered inside the daemon host, never as a process (R38, T22).

The parity cases run each moved read twice against one fake backend over a
socket: once as the REAL `probe` executable the daemon spawned until now
(`tools._attempt`, the session's environment), once in the host
(`tools._in_host`, the CLI command's own body in `probe.cli.reads`), and
compare exit code, stdout and stderr byte for byte -- and the headers of the
requests each one sent.
"""

from __future__ import annotations

import asyncio
import os
import subprocess
import sys
import threading
import time

import httpx
import pytest

from probe.daemon import approvals as appr
from probe.daemon import host_reads, lease, probe_api, runctx, tools
from probe.daemon.store import Store
from probe.sdk.agent_session import AGENT_SESSION_HEADER, EVENT_AT_ENV, FORWARDED_SESSION_ENV
from tests.conftest import FakeApp
from tests.served_fake_app import serve

SID = "11111111-2222-3333-4444-555555555555"
SID_B = "66666666-7777-4888-8999-aaaaaaaaaaaa"
TOKEN = "ros_pat_deadbeef"
TOKEN_B = "ros_pat_feedface"
#: The watched coding-agent session each daemon session's commands carry (`worker.forwarded_session`).
WATCHED = "aaaaaaaa-0000-4000-8000-00000000000a"
WATCHED_B = "bbbbbbbb-0000-4000-8000-00000000000b"
#: A header a request carries only per call: never part of a comparison.
_PER_CALL = frozenset({"host", "content-length", "connection", "accept-encoding"})


@pytest.fixture(autouse=True)
def _state(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.setattr(probe_api, "_features", None)


class Backend(FakeApp):
    """The fake API, plus a refused key, optionally slow run reads, and every
    request's headers."""

    refused_token = "ros_pat_refused"

    def __init__(self) -> None:
        super().__init__()
        self.seen: list[tuple[str, str, str | None]] = []
        self.headers: list[dict[str, str]] = []
        self.seen_lock = threading.Lock()
        self.slow: float = 0.0

    def latency(self, request: httpx.Request) -> float:
        return self.slow if request.url.path.startswith("/v1/runs/") else 0.0

    def handler(self, request: httpx.Request) -> httpx.Response:
        with self.seen_lock:
            self.seen.append((request.headers.get("authorization", ""), request.url.path,
                              request.headers.get(AGENT_SESSION_HEADER)))
            self.headers.append({k.lower(): v for k, v in request.headers.items() if k.lower() not in _PER_CALL})
        if request.headers.get("authorization") == f"Bearer {self.refused_token}":
            return httpx.Response(401, json={"detail": "invalid token"})
        return super().handler(request)


def _post(app: FakeApp, method: str, path: str, body: dict) -> dict:
    response = app.handler(httpx.Request(method, f"http://test{path}", json=body,
                                         headers={"authorization": f"Bearer {TOKEN}"}))
    assert response.status_code < 300, (path, response.status_code, response.text)
    return response.json() if response.content else {}


def _seed(app: Backend) -> dict:
    project = _post(app, "POST", "/v1/projects", {"name": "Parity", "slug": "parity",
                                                  "workspace_id": "11111111-1111-1111-1111-111111111111"})
    _post(app, "PATCH", f"/v1/projects/{project['id']}",
          {"notes": "# Plan\n\nalpha comes first.\n\n## Later\n\nbeta, then alpha again.\n"})
    _post(app, "POST", f"/v1/projects/{project['id']}/sub-notes",
          {"title": "Ideas", "body": "beta is the idea.\n\ngamma is not.\n"})
    experiment = app.seed_experiment("exp-a", project_id=project["id"])
    run = _post(app, "POST", "/v1/runs", {"name": "first run ‮", "slug": "first-run"})
    with app.seen_lock:
        app.seen.clear()  # the seeding is not a read under test
        app.headers.clear()
    return {"project": project, "experiment": experiment, "run": run}


def _deps(tmp_path, base_url: str, *, token: str = TOKEN, sid: str = SID, watched: str = WATCHED) -> tools.Deps:
    work = tmp_path / f"work-{sid[:4]}"
    work.mkdir(parents=True, exist_ok=True)
    # As the worker builds it (`worker.probe_env`, `forwarded_session`, `event_at_env`).
    env = {"PROBE_BASE_URL": base_url, "PROBE_TOKEN": token, "PROBE_DAEMON_SESSION": sid,
           FORWARDED_SESSION_ENV: f"claude_code:{watched}", EVENT_AT_ENV: "2026-10-29T10:00:00+00:00",
           "PROBE_OUTBOX_DIR": str(tmp_path / f"outbox-{sid[:4]}"), "PROBE_AUTO_SNAPSHOT": "0"}
    lease.sessions_dir().mkdir(parents=True, exist_ok=True)
    (lease.sessions_dir() / f"{sid}.state").write_text("daemon")
    assert lease.renew(sid)
    return tools.Deps(store=Store(tmp_path / f"s-{sid[:4]}.sqlite", clock=time.time),
                      board=appr.Board(tmp_path / "appr"), session_id=sid, cwd=work, workdirs=[work],
                      home=tmp_path, write_dirs=[], probe_env=env, bypass=False, mode_known=True, bite_id=1,
                      replay=None)


def _env(deps: tools.Deps) -> dict[str, str]:
    """What `run_probe_process` hands a command: the spawned CLI's environment."""
    return {**tools._base_env(), **deps.probe_env, "PROBE_IDEMPOTENCY_KEY": "op", "PROBE_ASYNC": "0",
            "NO_COLOR": "1", "COLUMNS": "200"}


def _both(deps: tools.Deps, argv: list[str]) -> tuple[tools.ProbeResult, tools.ProbeResult]:
    """`(spawned, in the host)` for one command."""
    where = host_reads.route(argv)
    assert where.call is not None, argv

    async def go():
        spawned = await tools._attempt(deps, argv, _env(deps), 60.0, deps.cwd)
        hosted = await tools._in_host(deps, where.call, _env(deps), 60.0)
        return spawned, hosted

    return asyncio.run(go())


def _cases(seeded: dict) -> list[list[str]]:
    run, project = seeded["run"], seeded["project"]
    return [
        ["run", "get", run["id"]],
        ["run", "get", "first-run", "--fields", "id,name"],
        ["run", "get", run["id"], "--fields", "nope"],  # a usage error the body raises
        ["run", "get", "no-such-run"],
        ["run", "check", run["id"]],  # exit 2: incomplete
        ["run", "check", "no-such-run"],
        ["run", "reproduce", run["id"]],
        ["project", "get", "parity"],
        ["project", "get", f"id:{project['id']}", "--fields", "slug,name"],
        ["project", "get", "no-such-project"],
        ["experiment", "get", "exp-a"],
        ["notes", "find", "--project", "parity", "alpha"],
        ["notes", "find", "--project", "parity", "--note", "Ideas", "beta"],
        ["notes", "find", "--project", "parity", "--note", "Missing", "beta"],  # stderr, exit 1
        ["notes", "find", "--run", run["id"], "x"],  # no notes: a stderr line, exit 0
        ["notes", "find", "--project", "parity", "--run", run["id"], "x"],  # two targets
        ["outbox", "status"],
        ["outbox", "status", "--verbose", "--run", run["id"]],
    ]


def test_in_process_read_output_matches_the_cli_byte_for_byte(tmp_path):
    """Each moved read: the host's answer is the spawned CLI's, exit code,
    stdout and stderr, on the same fake answers."""
    app = Backend()
    seeded = _seed(app)
    with serve(app) as url:
        deps = _deps(tmp_path, url)
        for argv in _cases(seeded):
            spawned, hosted = _both(deps, argv)
            assert (hosted.code, hosted.stdout, hosted.stderr) == (spawned.code, spawned.stdout, spawned.stderr), argv


def test_in_process_reads_send_what_the_cli_sent(tmp_path, monkeypatch):
    """The requests too: key, client identity, surface, the watched session the
    worker forwards and the time of the work -- never the coding agent's own
    session from the process's environment."""
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "99999999-9999-4999-8999-999999999999")
    app = Backend()
    seeded = _seed(app)
    with serve(app) as url:
        deps = _deps(tmp_path, url)
        for argv in (["run", "get", seeded["run"]["id"]], ["experiment", "get", "exp-a"]):
            where = host_reads.route(argv)
            asyncio.run(tools._attempt(deps, argv, _env(deps), 60.0, deps.cwd))
            with app.seen_lock:
                spawned, app.headers[:] = list(app.headers), []
            asyncio.run(tools._in_host(deps, where.call, _env(deps), 60.0))
            with app.seen_lock:
                hosted, app.headers[:] = list(app.headers), []
            assert hosted == spawned, argv
            assert {h.get(AGENT_SESSION_HEADER.lower()) for h in hosted} == {WATCHED}, hosted


def test_the_parity_cases_reach_every_outcome(tmp_path):
    """The parity corpus is not all one shape: success, exit 1 and exit 2, a
    usage error worded against the command, a stderr-only answer."""
    app = Backend()
    seeded = _seed(app)
    with serve(app) as url:
        deps = _deps(tmp_path, url)
        results = {tuple(argv): asyncio.run(tools._in_host(deps, host_reads.route(argv).call, _env(deps), 60.0))
                   for argv in _cases(seeded)}
    codes = {r.code for r in results.values()}
    assert codes == {0, 1, 2}, codes
    run_id = seeded["run"]["id"]
    usage = results[("run", "get", run_id, "--fields", "nope")]
    assert usage.code == 2 and usage.stderr.startswith("Usage: probe run get [OPTIONS] "), usage
    assert "\\u202e" in results[("run", "get", run_id)].stdout  # display controls escaped, compact JSON
    assert results[("notes", "find", "--run", run_id, "x")].stderr.endswith("has no notes yet\n")
    assert '2 of 4 paragraphs mention "alpha"' in results[("notes", "find", "--project", "parity", "alpha")].stdout


def test_a_refused_key_reads_as_refused_in_the_host_too(tmp_path):
    """A 401 on an in-host read prints the CLI's `KEY_REFUSED_LINE`, so the
    daemon stops and hands the session back exactly as after a spawned one."""
    app = Backend()
    seeded = _seed(app)
    with serve(app) as url:
        deps = _deps(tmp_path, url, token=Backend.refused_token)
        argv = ["run", "get", seeded["run"]["id"]]
        spawned, hosted = _both(deps, argv)
        assert (hosted.code, hosted.stdout, hosted.stderr) == (spawned.code, spawned.stdout, spawned.stderr)
        assert tools._key_refused(hosted)
        out = asyncio.run(tools.run_probe_command(deps, argv))
    assert deps.key_refused and deps.stopped == "Probe refused the daemon's key", out


def test_two_sessions_with_different_tokens_in_one_host_never_cross(tmp_path, monkeypatch):
    """~40 sessions share one host: each read carries ITS session's key, URL and
    watched session -- never the other's, never one from the process's or the
    run's environment -- with both sessions reading at the same moment, each
    against a server of its own."""
    app_a, app_b = Backend(), Backend()
    seeded = {"a": _seed(app_a), "b": _seed(app_b)}
    # The process's own environment names another key and a coding agent's
    # session: an in-host read must take neither.
    monkeypatch.setenv("PROBE_TOKEN", "ros_pat_process")
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "99999999-9999-4999-8999-999999999999")
    results: dict[str, list[str]] = {}
    counts: dict[str, dict] = {}
    with serve(app_a) as url_a, serve(app_b) as url_b:
        runctx.install()
        try:
            barrier = threading.Barrier(2, timeout=30)
            base = dict(os.environ.copy())

            def session(name: str, base_url: str, token: str, sid: str, watched: str) -> None:
                # Each run's thread owns its session's store, as in the host.
                deps = _deps(tmp_path, base_url, token=token, sid=sid, watched=watched)
                # The run's own environment (what `os.environ` answers inside it)
                # names yet another key: the read takes the session's, passed in.
                run = runctx.Run(session_id=deps.session_id, env={**base, "PROBE_TOKEN": f"ros_pat_run_{name}"})
                run_id = seeded[name]["run"]["id"]
                with runctx.enter(run):
                    assert lease.renew(deps.session_id)  # the lease is the run's own (its token)
                    barrier.wait()

                    async def reads():
                        return await asyncio.gather(*(
                            tools.run_probe_command(deps, argv) for argv in
                            (["run", "get", run_id], ["project", "get", "parity"],
                             ["experiment", "get", "exp-a"], ["run", "check", run_id]) * 2))

                    results[name] = asyncio.run(reads())
                    counts[name] = deps.store.fact(tools.PROBE_READS_FACT)

            threads = [threading.Thread(target=session, args=("a", url_a, TOKEN, SID, WATCHED), daemon=True),
                       threading.Thread(target=session, args=("b", url_b, TOKEN_B, SID_B, WATCHED_B), daemon=True)]
            for t in threads:
                t.start()
            for t in threads:
                t.join(60)
                assert not t.is_alive()
        finally:
            runctx.uninstall()
    assert set(results) == {"a", "b"}
    for outs in results.values():
        assert all(out.startswith(("[exit 0]", "[exit 2]")) for out in outs), outs
    for app, token, watched in ((app_a, TOKEN, WATCHED), (app_b, TOKEN_B, WATCHED_B)):
        assert app.seen and {(auth, session) for auth, _path, session in app.seen} == {(f"Bearer {token}", watched)}
    # And none was answered by spawning a CLI.
    for count in counts.values():
        assert "spawned" not in count and sum(count["in_host"].values()) == 8, count


def test_a_moved_read_starts_no_process_and_an_unmoved_one_spawns_and_is_counted(tmp_path, monkeypatch, caplog):
    started: list[list[str]] = []
    real = tools.probe_executable

    def counted():
        started.append(["probe"])
        return real()

    monkeypatch.setattr(tools, "probe_executable", counted)
    app = Backend()
    seeded = _seed(app)
    with serve(app) as url:
        deps = _deps(tmp_path, url)
        out = asyncio.run(tools.run_probe_command(deps, ["run", "get", seeded["run"]["id"]]))
        assert out.startswith("[exit 0]") and started == [], out
        with caplog.at_level("INFO", logger="probe.daemon.tools"):
            out = asyncio.run(tools.run_probe_command(deps, ["project", "list"]))
        assert out.startswith("[exit 0]") and len(started) == 1, out
        # Help still goes to the CLI too.
        asyncio.run(tools.run_probe_command(deps, ["run", "get", "--help"]))
    assert len(started) == 2
    assert deps.store.fact(tools.PROBE_READS_FACT) == {"in_host": {"run get": 1},
                                                       "spawned": {"project list": 1, "run get": 1}}
    assert "probe read spawned a CLI process (not answered in the daemon host): probe project list" in caplog.text


@pytest.mark.parametrize("why", ["no slot", "a large outbox", "a bug in the body"])
def test_a_read_the_host_hands_back_is_answered_by_the_cli(tmp_path, monkeypatch, why):
    """A full in-flight slot, an outbox too large to parse in the host, or a
    bug: the CLI answers (its real output), and the read counts as spawned."""
    from probe.cli import reads

    app = Backend()
    seeded = _seed(app)
    argv = ["outbox", "status"] if why == "a large outbox" else ["run", "get", seeded["run"]["id"]]
    if why == "no slot":
        monkeypatch.setattr(host_reads, "_IN_FLIGHT", threading.BoundedSemaphore(1))
        assert host_reads._IN_FLIGHT.acquire(blocking=False)
    elif why == "a large outbox":
        monkeypatch.setattr(host_reads, "OUTBOX_HOST_OPS", 0)
        monkeypatch.setattr(host_reads, "_queued_more_than", lambda journal, limit: True)
    else:
        monkeypatch.setattr(reads, "run_get", lambda *a, **k: 1 / 0)
    with serve(app) as url:
        deps = _deps(tmp_path, url)
        spawned = asyncio.run(tools._attempt(deps, argv, _env(deps), 60.0, deps.cwd))
        out = asyncio.run(tools.run_probe_command(deps, argv))
    assert out.startswith(f"[exit {spawned.code}]") and spawned.stdout.strip() in out, out
    assert deps.store.fact(tools.PROBE_READS_FACT) == {"spawned": {" ".join(argv[:2]): 1}}


@pytest.mark.parametrize("argv, why", [
    (["run", "reproduce", "r1", "--export", "x.json"], "writes a file"),
    (["run", "check", "r1", "--verify"], "runs git on this machine"),
    (["--base-url", "http://elsewhere.test", "run", "get", "r1"], "a root option"),
    (["run", "get"], "click refuses it: the CLI words the usage error"),
    (["run", "get", "r1", "--nope"], "an unknown option"),
    (["run", "list"], "not moved yet"),
    (["run", "tag", "r1", "x"], "a write"),
])
def test_what_the_host_leaves_to_the_cli(argv, why):
    assert host_reads.route(argv).call is None, why


def test_the_moved_reads_parse_with_their_defaults():
    call = host_reads.route(["notes", "find", "a", "b", "--project", "p"]).call
    assert call.path == "notes find" and call.params == {"words": ("a", "b"), "project": "p", "experiment": None,
                                                         "run": None, "note": None}
    assert host_reads.route(["outbox", "status"]).call.params == {"verbose": False, "run": None}
    assert host_reads.route(["run", "reproduce", "r1"]).call.params["export"] is None
    assert host_reads.route(["run", "check", "r1"]).call.params["verify"] is False
    assert host_reads.route(["run", "check", "r1", "--verify"]).read == "run check"
    assert host_reads.MOVED == {"run get", "run check", "notes find", "outbox status", "run reproduce",
                                "project get", "experiment get"}


def _read_threads() -> list[threading.Thread]:
    """The in-host reads' threads (`host_reads.start` names each `... probe-read <command>`),
    never another thread a test in this worker left behind (the SDK's `probe-reads-hasher`)."""
    return [t for t in threading.enumerate() if "probe-read " in t.name]


def test_a_slow_read_stops_at_its_timeout_and_its_thread_ends(tmp_path):
    """The caller's stop is what the model reads, and the read's own thread --
    its request bounded by `transport.deadline_scope` -- ends a moment later,
    long before the server would have answered."""
    app = Backend()
    seeded = _seed(app)
    app.slow = 8.0
    with serve(app) as url:
        deps = _deps(tmp_path, url)
        call = host_reads.route(["run", "get", seeded["run"]["id"]]).call
        started = time.monotonic()
        result = asyncio.run(tools._in_host(deps, call, _env(deps), 1.0))
        assert (result.code, result.stdout, result.stderr) == (None, "", "stopped after 1s")
        while _read_threads() and time.monotonic() - started < 6.0:
            time.sleep(0.05)
        assert not _read_threads(), "the read outlived its deadline"


def test_a_slow_read_is_stopped_when_the_lease_is_lost(tmp_path):
    app = Backend()
    seeded = _seed(app)
    app.slow = 8.0
    with serve(app) as url:
        deps = _deps(tmp_path, url)
        call = host_reads.route(["run", "get", seeded["run"]["id"]]).call

        async def go():
            task = asyncio.ensure_future(tools._in_host(deps, call, _env(deps), 60.0))
            await asyncio.sleep(0.3)
            lease.release(SID, "a test")
            return await task

        started = time.monotonic()
        result = asyncio.run(go())
        took = time.monotonic() - started
    assert result.code is None and result.stderr.startswith("stopped while it ran ("), result
    assert took < 6.0, took  # the server would have taken 8 s


def test_a_cancelled_bite_stops_waiting_for_a_read_at_once(tmp_path):
    app = Backend()
    seeded = _seed(app)
    app.slow = 8.0
    with serve(app) as url:
        deps = _deps(tmp_path, url)

        async def go():
            task = asyncio.ensure_future(tools.run_probe_command(deps, ["run", "get", seeded["run"]["id"]]))
            await asyncio.sleep(0.3)
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task

        started = time.monotonic()
        asyncio.run(go())
        assert time.monotonic() - started < 6.0  # the server would have taken 8 s


def test_the_read_runs_as_the_sessions_run(tmp_path, monkeypatch):
    """The read's thread carries the run it was asked from (its logs, its
    state), and nothing of it is left on the process."""
    seen = []

    def answer(call, env, deadline):
        seen.append((runctx.current(), env["PROBE_TOKEN"], threading.current_thread().name))
        return 0, "{}\n", ""

    app = Backend()
    with serve(app) as url:
        deps = _deps(tmp_path, url)
        run = runctx.Run(session_id=SID)
        monkeypatch.setattr(host_reads, "answer", answer)
        with runctx.enter(run):
            assert lease.renew(SID)
            out = asyncio.run(tools.run_probe_command(deps, ["run", "get", "r1"]))
    assert out == "[exit 0]\n{}\n"
    assert seen == [(run, TOKEN, f"run-{SID[:12]} probe-read run get")]
    assert runctx.current() is None


def test_the_host_never_loads_the_whole_cli():
    """Plan M1: the daemon host imports the read bodies, never `probe.cli.main`."""
    code = ("import sys\n"
            "from probe.daemon import host_reads\n"
            "import probe.cli.reads\n"
            "assert host_reads.route(['run', 'get', 'r1']).call is not None\n"
            "print('probe.cli.main' in sys.modules)\n")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)
    assert out.returncode == 0 and out.stdout.strip() == "False", out.stderr


def test_the_cli_still_lays_out_json_for_a_terminal(app, tmp_path, monkeypatch, capsys):
    """A moved read's CLI command prints indented JSON on a terminal and compact
    JSON on a pipe, as `_print_json` does."""
    from probe import cli
    from tests.conftest import make_client

    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    app.seed_experiment("lr-sweep")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    assert cli.main(["experiment", "get", "lr-sweep"]) == 0
    assert capsys.readouterr().out.startswith('{\n  "id": ')
    monkeypatch.setattr(sys.stdout, "isatty", lambda: False)
    assert cli.main(["experiment", "get", "lr-sweep"]) == 0
    assert capsys.readouterr().out.startswith('{"id":')


def test_held_credentials_are_judged_by_the_sessions_environment(monkeypatch):
    """`outbox status` in the host says whose writes wait by the session's CLI's
    credentials, never the process's."""
    from probe.cli import reads
    from probe.sdk.journal import credential_fingerprint

    monkeypatch.setenv("PROBE_TOKEN", "ros_pat_process")
    here = reads.credentials_here(None, {"PROBE_TOKEN": "ros_pat_session"})
    assert credential_fingerprint("ros_pat_session", None) in here
    assert credential_fingerprint("ros_pat_process", None) not in here


def test_other_outboxes_are_found_under_the_sessions_tmpdir(tmp_path, monkeypatch):
    """The host's `tempfile` keeps the first TMPDIR it saw; a session's
    `outbox status` lists the fallback queues under ITS TMPDIR."""
    from probe.sdk.journal import Journal, _uid

    mine, other = tmp_path / "mine", tmp_path / "other"
    for base in (mine, other):
        queue = base / f"probe-outbox-{_uid()}"
        (queue / "ops").mkdir(parents=True)
        queue.chmod(0o700)
    monkeypatch.setenv("TMPDIR", str(other))
    found = Journal.discover({"TMPDIR": str(mine), "XDG_STATE_HOME": str(tmp_path / "state")})
    assert mine / f"probe-outbox-{_uid()}" in found and other / f"probe-outbox-{_uid()}" not in found
