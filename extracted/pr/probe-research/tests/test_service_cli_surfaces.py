"""Four more CLI-side background jobs go through the Probe service (plan Q4b).

    status line     a session's server read: ONE child per plugin folder on the
                    service's schedule (`statusline.refresh` -> the plugin's own
                    `statusline_refresh.py fetch-all`), not a detached fetch per
                    tool call; no service, an older one, or a credential in the
                    hook's environment: the detached fetch, as before
    team note       `probe agent-rules refresh` / `notes sync` / `feedback
                    flush` once per machine, debounced (`notes.sync`), never a
                    `probe` per session per event; else the hooks' own spawn
    import jobs     an approved import's worker is the service's child
                    (`import.start`): listed by `service.status`, its failed
                    start reported, watched again by the next service; else the
                    CLI's own detached worker
    probe wizard    `--action <a> --yes` runs as the service's `action.run`,
                    its text streamed to the terminal; everything the action
                    protocol cannot carry, and every refusal, in-process

Real service processes in a throwaway HOME (`service_harness`); the children
are stand-ins (`service_fakes.FakeCore`: `probe.core.run`, `probe <args>`, an
import worker). Nothing here runs a real `probe notes sync` or `agent-rules
refresh`, and every agent folder the children could read points into a scratch
dir: no test touches the shared ~/.claude/CLAUDE.md or ~/.codex/AGENTS.md.
"""

from __future__ import annotations

import contextlib
import http.server
import importlib
import importlib.util
import io
import json
import os
import re
import signal
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

import probe
from probe.cli import import_jobs, service_calls, wizard_service
from probe.service import client, notesync, paths, protocol, statusline
from probe.service.protocol import Method
from tests.service_fakes import FakeCore
from tests.service_harness import ps_passes, service_home, wait_for  # noqa: F401 -- a fixture

cli_main = importlib.import_module("probe.cli.main")

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the service is POSIX-only (plan S8)")

AGENT = Path(__file__).resolve().parents[1]
HOOKS = AGENT / "plugins" / "probe-research" / "hooks"
SID_A = "11111111-1111-4111-8111-111111111111"
SID_B = "22222222-2222-4222-8222-222222222222"


@pytest.fixture
def scratch(tmp_path, monkeypatch):
    """Every agent folder and state dir a child could write points here."""
    dirs = {name: tmp_path / name.lower() for name in
            ("CLAUDE_CONFIG_DIR", "CODEX_HOME", "PI_CODING_AGENT_DIR", "KIMI_CODE_HOME", "XDG_STATE_HOME",
             "XDG_CONFIG_HOME")}
    for name, path in dirs.items():
        path.mkdir(parents=True)
        monkeypatch.setenv(name, str(path))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "xdg_config_home" / "probe" / "config.json"))
    for name in (*protocol.CREDENTIAL_ENV, *service_calls.WIZARD_LOCAL_ENV, "PROBE_BASE_URL", "PROBE_BIN",
                 "PROBE_AGENT", "PROBE_STATUSLINE"):
        monkeypatch.delenv(name, raising=False)
    return dirs


@pytest.fixture
def core(service_home):
    """`FakeCore`, with `runtime.json` naming the fake as the CLI's own."""
    return FakeCore(service_home.home)


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    added = str(path.parent) not in sys.path
    if added:
        sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        if added:
            sys.path.remove(str(path.parent))
    return module


def _status(service_home) -> dict:
    return service_home.call(Method.STATUS)


# -- the hook's helper ------------------------------------------------------------------


def test_the_hooks_context_is_a_request_context_without_the_per_session_switches():
    helper = _load(HOOKS / "_service_call.py", "_service_call_under_test")
    assert set(helper.CONTEXT_ENV) <= protocol.CONTEXT_ENV
    # The switches would split the machine's one job into one per session.
    assert not {"PROBE_SESSION_STATE", "PROBE_SESSION_TRACKING"} & set(helper.CONTEXT_ENV)
    assert set(helper.CREDENTIAL_ENV) == protocol.CREDENTIAL_ENV
    assert not protocol.CREDENTIAL_ENV & protocol.CONTEXT_ENV
    assert helper.stands_in({}) and not helper.stands_in({"PROBE_TOKEN": "t"})


def test_every_credential_the_sdk_reads_from_the_environment_stays_with_the_caller():
    """`probe.sdk.config`'s env table: each token or secret it names is one a
    request never carries, so a caller holding it does the work itself."""
    from probe.sdk import config

    named = set(re.findall(r"^  (PROBE_[A-Z_]+)\s", config.__doc__, re.M))
    secrets = {name for name in named if name.endswith(("_TOKEN", "_SECRET"))}
    assert secrets and secrets <= protocol.CREDENTIAL_ENV, sorted(secrets - protocol.CREDENTIAL_ENV)
    # What else shapes a wizard run from the environment stays with it too.
    assert {"PROBE_MCP_URL", "PROBE_WORKSPACE", "PROBE_PROJECT"} <= set(service_calls.WIZARD_LOCAL_ENV)


def test_the_hooks_helper_says_no_without_a_service(service_home, scratch):
    helper = _load(HOOKS / "_service_call.py", "_service_call_under_test")
    began = time.monotonic()
    assert helper.call(Method.STATUS, {}) is None
    assert helper.notes_sync("push") is False
    assert helper.statusline_refresh(SID_A, str(AGENT / "plugins" / "probe-research")) is False
    assert time.monotonic() - began < 1.0
    assert service_home.service_processes() == [], "a hook must never start the service"


def test_the_daemon_plugin_carries_the_same_helper():
    daemon = AGENT / "plugins" / "probe-research-daemon" / "hooks" / "_service_call.py"
    assert daemon.read_bytes() == (HOOKS / "_service_call.py").read_bytes()


# -- status line ---------------------------------------------------------------------------


class _Api(http.server.BaseHTTPRequestHandler):
    seen: list = []

    def do_GET(self):  # noqa: N802 -- the stdlib's name
        type(self).seen.append((self.path, self.headers.get("Authorization")))
        if self.path.startswith("/v1/sessions/"):
            body = {"projects": [{"slug": "bird-sql"}], "runs": [{"entity_id": "run-1"}]}
        else:
            body = [{"id": "run-1"}]
        data = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_args):
        pass


@pytest.fixture
def api(scratch):
    """A local stand-in for the Probe API, and a CLI config signed in to it."""
    _Api.seen = []
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Api)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    config = Path(os.environ["PROBE_CONFIG_PATH"])
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(json.dumps({"base_url": f"http://127.0.0.1:{server.server_address[1]}", "token": "ros_test"}))
    yield _Api
    server.shutdown()


@pytest.fixture
def refresh_hook(scratch):
    """The status-line hook, installed (its renderer folder exists)."""
    (scratch["CLAUDE_CONFIG_DIR"] / "probe-research-statusline").mkdir()
    return _load(HOOKS / "statusline_refresh.py", "_statusline_refresh_under_test")


def _marker(scratch, sid: str) -> dict | None:
    path = scratch["XDG_STATE_HOME"] / "probe" / "sessions" / f"{sid}.json"
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def test_one_service_child_refreshes_every_session_that_asked(service_home, api, refresh_hook, scratch, monkeypatch):
    service_home.start()
    spawned: list = []
    monkeypatch.setattr(refresh_hook.subprocess, "Popen", ps_passes(lambda *a, **k: spawned.append(a)))

    refresh_hook.spawn(SID_A)
    refresh_hook.spawn(SID_B)

    assert wait_for(lambda: _marker(scratch, SID_A) and _marker(scratch, SID_B), 15), service_home.log()
    assert spawned == [], "the hook spawned its own fetch although the service took it"
    for sid in (SID_A, SID_B):
        marker = _marker(scratch, sid)
        assert marker["project"] == "bird-sql" and set(marker["active_run_ids"]) == {"run-1"}
        assert marker["capture"]["reason"] in ("not installed", "killswitch", "not started", "running")
    # Both sessions in ONE child: the two requests landed inside one interval.
    view = wait_for(lambda: (s := _status(service_home)["statusline"])["running"] == 0 and s, 10)
    assert view["children"] == 1 and view["last"]["sessions"] == 2 and view["last"]["exit_code"] == 0
    assert {auth for _, auth in api.seen} == {"Bearer ros_test"}
    assert sum(1 for path, _ in api.seen if path.startswith("/v1/sessions/")) == 2


def test_a_second_ask_inside_the_interval_waits_for_the_next_child(service_home, api, refresh_hook, scratch):
    service_home.start()
    root = str(HOOKS.parent)
    first = client.refresh_statusline(SID_A, root, python=sys.executable, context=_hook_context())
    assert first["scheduled"] is True and first["due_in"] <= statusline.GATHER_S
    assert wait_for(lambda: _status(service_home)["statusline"]["children"] == 1, 10)
    again = client.refresh_statusline(SID_A, root, python=sys.executable, context=_hook_context())
    assert again["scheduled"] is True and 0 < again["due_in"] <= statusline.INTERVAL_S


def _hook_context() -> dict:
    helper = _load(HOOKS / "_service_call.py", "_service_call_under_test")
    return helper.context()


def test_the_service_refuses_a_folder_that_is_not_a_probe_plugin(service_home, tmp_path, scratch):
    service_home.start()
    (tmp_path / "plugin" / "hooks").mkdir(parents=True)
    answer = client.refresh_statusline(SID_A, str(tmp_path / "plugin"), python=sys.executable)
    assert answer == {"scheduled": False, "reason": "not a Probe plugin folder"}
    with pytest.raises(client.ServiceError) as bad:
        client.refresh_statusline("../../etc", str(tmp_path))
    assert bad.value.code == protocol.ErrorCode.INVALID_PARAMS


def test_no_service_means_the_detached_fetch_as_before(service_home, refresh_hook, monkeypatch):
    spawned: list = []
    monkeypatch.setattr(refresh_hook.subprocess, "Popen", ps_passes(lambda argv, **k: spawned.append(argv)))
    refresh_hook.spawn(SID_A)
    assert spawned and spawned[0][-2:] == ["fetch", SID_A]


def test_a_credential_in_the_hooks_environment_keeps_the_detached_fetch(service_home, refresh_hook, monkeypatch):
    service_home.start()
    monkeypatch.setenv("PROBE_TOKEN", "ros_env_only")
    spawned: list = []
    monkeypatch.setattr(refresh_hook.subprocess, "Popen", ps_passes(lambda argv, **k: spawned.append(argv)))
    refresh_hook.spawn(SID_A)
    assert spawned and spawned[0][-2:] == ["fetch", SID_A]
    assert _status(service_home)["statusline"]["children"] == 0


@contextlib.contextmanager
def _older_service():
    """Something at the service's socket that answers hello and nothing newer:
    a service from before these methods."""
    sock_path = paths.ensure_dirs()
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    listener.bind(str(sock_path))
    listener.listen(8)
    stop = threading.Event()

    def serve() -> None:
        listener.settimeout(0.1)
        while not stop.is_set():
            try:
                conn, _ = listener.accept()
            except (socket.timeout, OSError):
                continue
            with conn:
                buffer = b""
                conn.settimeout(1.0)
                try:
                    while True:
                        chunk = conn.recv(65536)
                        if not chunk:
                            break
                        buffer += chunk
                        while b"\n" in buffer:
                            line, buffer = buffer.split(b"\n", 1)
                            message = json.loads(line)
                            if message["method"] == Method.HELLO:
                                reply = {"jsonrpc": "2.0", "id": message["id"],
                                         "result": {"service_version": "0.1", "api": 1, "pid": 1, "started_at": 0.0,
                                                    "state": "running"}}
                            else:
                                reply = {"jsonrpc": "2.0", "id": message["id"],
                                         "error": {"code": -32601, "message": "unknown method"}}
                            conn.sendall(json.dumps(reply).encode() + b"\n")
                except (OSError, ValueError):
                    pass

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    try:
        yield
    finally:
        stop.set()
        thread.join(2)
        listener.close()
        with contextlib.suppress(OSError):
            os.unlink(sock_path)


def test_an_older_service_means_the_detached_fetch_and_the_spawned_sync(service_home, refresh_hook, monkeypatch):
    spawned: list = []
    monkeypatch.setattr(refresh_hook.subprocess, "Popen", ps_passes(lambda argv, **k: spawned.append(argv)))
    helper = _load(HOOKS / "_service_call.py", "_service_call_under_test")
    with _older_service():
        refresh_hook.spawn(SID_A)
        assert helper.notes_sync("push") is False
    assert spawned and spawned[0][-2:] == ["fetch", SID_A]


def test_fetch_all_refreshes_each_session_and_skips_a_bad_one(refresh_hook, monkeypatch):
    done: list = []

    def refresh(sid, agent=None, *, core=None, marker=None):
        assert core is not None and marker is not None, "loaded once, before the threads"
        if sid == SID_B:
            raise RuntimeError("one session's failure")
        done.append((sid, agent))

    monkeypatch.setattr(refresh_hook, "refresh", refresh)
    codex = "codex"  # harness-literal-ok: a test agent id
    sid_c = "33333333-3333-4333-8333-333333333333"
    refresh_hook.fetch_all({"sessions": [{"sid": SID_A, "agent": codex}, {"sid": "../x"}, "junk", {"sid": SID_B},
                                         {"sid": sid_c}]})
    assert sorted(done) == sorted([(SID_A, codex), (sid_c, None)])


# -- team note --------------------------------------------------------------------------------


def _wait_cli(core, count: int, timeout: float = 15) -> list[dict]:
    calls = wait_for(lambda: len(core.stand_in_calls("cli")) >= count and core.stand_in_calls("cli"), timeout)
    assert calls, "the service ran no `probe` command"
    return calls


def test_a_burst_of_syncs_is_one_run_once_per_machine(service_home, core, scratch):
    core.plan("cli", exit=0)
    service_home.start()
    for _ in range(3):
        assert client.sync_notes("push", context=_hook_context())["outcome"] == protocol.JobOutcome.SCHEDULED
    calls = _wait_cli(core, 1)
    time.sleep(notesync.DEBOUNCE_S + 0.5)
    calls = core.stand_in_calls("cli")
    assert [c["args"] for c in calls] == [["notes", "sync", "--push-only"]]
    # The caller's context reached it: the scratch state and config, never the real ones.
    env = calls[0]["env"]
    assert env["XDG_STATE_HOME"] == str(scratch["XDG_STATE_HOME"])
    assert env["CLAUDE_CONFIG_DIR"] == str(scratch["CLAUDE_CONFIG_DIR"])
    assert env["PROBE_TOKEN"] is None
    assert wait_for(lambda: _status(service_home)["notes"]["runs"] == 1 and not _status(service_home)["notes"]["running"], 5)


def test_a_reconcile_covers_a_push_and_runs_every_agents_rules_first(service_home, core, scratch):
    core.plan("cli", exit=0)
    service_home.start()
    client.sync_notes("push", context=_hook_context())
    client.sync_notes("reconcile", rules_for=["", "codex"], feedback=True, context=_hook_context())  # harness-literal-ok: a test agent id
    calls = _wait_cli(core, 4)
    assert [(c["args"], c["env"]["PROBE_AGENT"]) for c in calls] == [
        (["agent-rules", "refresh"], None),
        (["agent-rules", "refresh"], "codex"),  # harness-literal-ok: a test agent id
        (["notes", "sync"], None),
        (["feedback", "flush"], None),
    ]
    last = wait_for(lambda: _status(service_home)["notes"]["last"], 5)
    assert last["mode"] == "reconcile" and [r["exit"] for r in last["commands"]] == [0, 0, 0, 0]


def test_requests_while_a_sync_runs_join_the_one_run_after_it(service_home, core, tmp_path, scratch):
    gate = tmp_path / "release"
    core.plan("cli", before=[{"wait": str(gate)}])
    service_home.start()
    client.sync_notes("push", context=_hook_context())
    _wait_cli(core, 1)
    for _ in range(3):
        assert client.sync_notes("reconcile", context=_hook_context())["outcome"] == protocol.JobOutcome.QUEUED
    assert _status(service_home)["notes"]["running"] is True
    gate.touch()
    calls = _wait_cli(core, 2)
    time.sleep(notesync.DEBOUNCE_S + 0.5)
    assert [c["args"] for c in core.stand_in_calls("cli")] == [["notes", "sync", "--push-only"], ["notes", "sync"]]


def test_a_pending_sync_holds_the_service_up(service_home, core, monkeypatch, scratch):
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "0.2")
    core.plan("cli", before=[{"sleep": 1.0}])
    started = service_home.start()
    client.sync_notes("reconcile", context=_hook_context())
    _wait_cli(core, 1)
    assert _status(service_home)["pid"] == started["pid"], "the service idled out under a sync"
    assert service_home.wait_exit(started["pid"], 10), "the service never idled out after the sync"


def test_the_stop_hook_hands_its_push_to_the_service(service_home, core, tmp_path, scratch):
    core.plan("cli", exit=0)
    service_home.start()
    probe_log = tmp_path / "probe-called"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "probe").write_text(f"#!/bin/sh\necho \"$@\" >> {probe_log}\n")
    (bin_dir / "probe").chmod(0o755)
    env = {**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}", "PROBE_HOOK_EVENT": "stop"}
    done = subprocess.run(["/bin/bash", str(HOOKS / "team-note-sync.sh")], input="{}", text=True, env=env,
                          capture_output=True, timeout=30)
    assert done.returncode == 0, done.stderr
    calls = _wait_cli(core, 1)
    assert calls[0]["args"] == ["notes", "sync", "--push-only"]
    time.sleep(0.5)
    assert not probe_log.exists(), "the hook spawned its own `probe` although the service took the sync"

    # No service: the hook's own detached `probe`, as before.
    service_home.call(Method.STOP)
    assert wait_for(lambda: service_home.status() is None, 5)
    env["PROBE_HOOK_EVENT"] = "sessionend"
    done = subprocess.run(["/bin/bash", str(HOOKS / "team-note-sync.sh")], input="{}", text=True, env=env,
                          capture_output=True, timeout=30)
    assert done.returncode == 0
    assert wait_for(lambda: probe_log.exists() and probe_log.read_text().strip(), 10) == "notes sync"


def test_a_session_start_hands_its_maintenance_to_the_service(service_home, core, scratch, monkeypatch):
    core.plan("cli", exit=0)
    service_home.start()
    hook = _load(HOOKS / "version_check.py", "_version_check_under_test")
    spawned: list = []
    monkeypatch.setattr(hook.subprocess, "Popen", ps_passes(lambda argv, **k: spawned.append(argv)))
    monkeypatch.setattr(hook, "_team_note_cli_too_old", lambda _binary: None)
    monkeypatch.setenv("PROBE_AGENT", "codex")  # harness-literal-ok: a test agent id
    # As session-start.sh runs it: always with the `probe` it resolved.
    assert 'export PROBE_BIN="${PROBE_BIN:-probe}"' in (HOOKS / "session-start.sh").read_text()
    monkeypatch.setenv("PROBE_BIN", "probe")
    assert hook._spawn_session_maintenance() is None
    assert spawned == []
    calls = _wait_cli(core, 2)
    assert [(c["args"], c["env"]["PROBE_AGENT"]) for c in calls] == [
        (["agent-rules", "refresh"], "codex"),  # harness-literal-ok: a test agent id
        (["notes", "sync"], None),
    ]
    # No service: the session start's own detached maintenance, as before.
    service_home.call(Method.STOP)
    assert wait_for(lambda: service_home.status() is None, 5)
    hook._spawn_session_maintenance()
    assert spawned and spawned[-1][-1] == "probe agent-rules refresh; probe notes sync"


_CONFINED = r"""
import ctypes, json, sys
# PR_SET_NO_NEW_PRIVS: more confined than the service, as an agent's sandbox is.
assert ctypes.CDLL(None, use_errno=True).prctl(38, 1, 0, 0, 0) == 0
from probe.service import client
out = {}
for name, ask in (
    ("notes", lambda: client.sync_notes("push")),
    ("statusline", lambda: client.refresh_statusline(sys.argv[1], sys.argv[2])),
    ("import", lambda: client.start_import("ab" * 16, "/tmp", 0, {"HOME": "/tmp"})),
    # `probe wizard --action ... --yes` from an agent's sandboxed shell.
    ("action", lambda: client.call("action.run", {"action": "logout", "client_request_id": "sandboxed"})),
):
    try:
        out[name] = ask()
    except client.ServiceError as exc:
        out[name] = {"code": exc.code, "reason": (exc.data or {}).get("reason")}
print(json.dumps(out))
"""


def _no_new_privs() -> bool:
    try:
        return "NoNewPrivs:\t1" in Path("/proc/self/status").read_text()
    except OSError:
        return True


@pytest.mark.skipif(not sys.platform.startswith("linux") or _no_new_privs(),
                    reason="no_new_privs is Linux's, and this process must not have it already")
def test_a_caller_in_a_sandbox_is_refused_everything_that_runs_work(service_home, scratch):
    service_home.start()
    done = subprocess.run([sys.executable, "-c", _CONFINED, SID_A, str(HOOKS.parent)], capture_output=True,
                          text=True, timeout=30)
    assert done.returncode == 0, done.stderr
    answers = json.loads(done.stdout)
    refused = {"code": protocol.ErrorCode.REFUSED, "reason": protocol.RefusedReason.SANDBOXED}
    assert answers == {"notes": refused, "statusline": refused, "import": refused, "action": refused}


# -- import jobs ----------------------------------------------------------------------------


def _job(tmp_path) -> tuple[Path, Path]:
    """A queued job record, as `import_jobs._enqueue` writes one."""
    directory = (tmp_path / "import-jobs").resolve()
    payload = {"x": 1}
    folder = directory / import_jobs._identity("transcripts", payload)
    folder.mkdir(parents=True)
    now = import_jobs.now_iso()
    import_jobs._save(folder, {
        "version": 1, "id": folder.name, "kind": "transcripts", "label": "test", "payload": payload,
        "state": "queued", "created_at": now, "updated_at": now, "started_at": None, "finished_at": None,
        "attempt": 0, "pid": None, "pid_identity": None, "progress": {"message": "Queued."}, "error": None,
        "report": [], "children": [], "log_path": str(folder / "output.log"), "origin": None,
    })
    return directory, folder


def _launch(folder: Path) -> dict:
    """`_launch` as `enqueue` and `resume` call it: under the jobs' lifecycle
    lock and the job's launch lock."""
    with import_jobs._lifecycle(folder.parent), import_jobs._job_lock(folder, "launch.lock"):
        return import_jobs._launch(folder)


@pytest.fixture
def same_cli(monkeypatch):
    """The CLI under test is the one `runtime.json` names (FakeCore's stand-in)."""
    monkeypatch.setattr(service_calls, "same_cli", lambda: True)


def test_the_service_starts_and_watches_an_imports_worker(service_home, core, tmp_path, same_cli, scratch,
                                                          monkeypatch):
    gate = tmp_path / "release"
    core.plan("import_worker", before=[{"wait": str(gate)}], exit=0)
    started = service_home.start()
    directory, folder = _job(tmp_path)
    monkeypatch.setenv("MARKER", "from-the-cli")
    job = _launch(folder)
    (call,) = wait_for(lambda: core.stand_in_calls("import_worker"), 10)
    assert call["args"] == [folder.name, "--directory", str(directory)]
    assert call["cwd"] == str(folder) and call["ppid"] == started["pid"], "the worker is the service's child"
    assert call["env"]["MARKER"] == "from-the-cli", "the worker runs with the CLI's own environment"
    assert job["launch_pid"] == call["pid"] and job["pid"] == call["pid"]
    listed = _status(service_home)["imports"]
    assert [(i["job_id"], i["pid"]) for i in listed] == [(folder.name, call["pid"])]
    assert "1 import running" in service_calls.summary(service_calls.view())
    assert wait_for(lambda: "stand-in import_worker" in (folder / "output.log").read_text(), 5)
    # Asked again while it runs: the same worker, not a second one.
    again = client.start_import(folder.name, str(directory), 0, {"HOME": os.environ["HOME"]})
    assert again == {"started": False, "reason": "running", "pid": call["pid"], "start_time": again["start_time"]}

    gate.touch()
    assert wait_for(lambda: _status(service_home)["imports"] == [], 10)


def test_a_worker_that_never_claims_its_job_reads_failed(service_home, core, tmp_path, same_cli, scratch):
    core.plan("import_worker", exit=3)
    service_home.start()
    _directory, folder = _job(tmp_path)
    job = _launch(folder)
    assert job["launch_pid"]
    record = wait_for(lambda: (r := import_jobs._read(folder))["state"] == "failed" and r, 20)
    assert record, (import_jobs._read(folder), service_home.log())
    assert record["error"] == "The import worker could not start (exit code 3)."


def test_the_next_service_watches_a_worker_the_last_one_started(service_home, core, tmp_path, same_cli, scratch):
    gate = tmp_path / "release"
    core.plan("import_worker", before=[{"wait": str(gate)}], exit=0)
    first = service_home.start()
    _directory, folder = _job(tmp_path)
    _launch(folder)
    (call,) = wait_for(lambda: core.stand_in_calls("import_worker"), 10)
    os.kill(first["pid"], signal.SIGTERM)
    assert service_home.wait_exit(first["pid"], 10)
    assert os.kill(call["pid"], 0) is None, "the worker stopped with the service"
    second = service_home.start()
    assert second["pid"] != first["pid"]
    assert [i["pid"] for i in _status(service_home)["imports"]] == [call["pid"]]
    gate.touch()
    assert wait_for(lambda: _status(service_home)["imports"] == [], 10)


def test_without_the_service_the_cli_starts_its_own_worker(service_home, tmp_path, monkeypatch, scratch):
    _directory, folder = _job(tmp_path)
    launched: list = []

    class _Child:
        pid = os.getpid()

        def wait(self):
            return 0

    monkeypatch.setattr(import_jobs.subprocess, "Popen", ps_passes(lambda argv, **k: launched.append(argv) or _Child()))
    _launch(folder)
    assert launched and "probe.cli.import_jobs" in launched[0][3]


def test_a_start_waits_for_neither_a_previous_attempt_nor_an_update(tmp_path):
    from probe.service import imports

    held = {"on": False}
    workers = imports.ImportWorkers(tmp_path / "imports.json", log=lambda _m: None, held=lambda: held["on"])
    job, here, there = "ab" * 16, str(tmp_path / "a"), str(tmp_path / "b")
    worker = imports.Worker(job, here, 4242, "t0", attempt=2, since=0.0)
    workers.workers[worker.ident] = worker
    # The same attempt of the same folder's job asked again: the worker it runs.
    assert workers.refuse(here, job, 2) == {"started": False, "reason": "running", "pid": 4242, "start_time": "t0"}
    # The same approval in another state folder is another job.
    assert workers.refuse(there, job, 2) is None
    # A newer attempt, its predecessor still exiting: it gets a worker of its own.
    assert workers.refuse(here, job, 3) is None
    # Mid in-place update: none starts here (the CLI starts its own, as before).
    held["on"] = True
    assert workers.refuse(here, job, 3) == {"started": False, "reason": "updating"}
    assert workers.refuse(here, "cd" * 16, 0) == {"started": False, "reason": "updating"}


def test_another_clis_code_never_hands_its_worker_to_the_service(service_home, core, tmp_path, scratch):
    service_home.start()
    assert service_calls.same_cli() is False  # runtime.json names FakeCore's python, not this one
    _directory, folder = _job(tmp_path)
    assert service_calls.start_import(folder.name, str(folder.parent), 0, dict(os.environ)) is None


def test_import_start_refuses_what_is_not_a_job(service_home, tmp_path, scratch):
    service_home.start()
    (tmp_path / "jobs" / ("cd" * 16)).mkdir(parents=True)
    answer = client.start_import("cd" * 16, str(tmp_path / "jobs"), 0, {"HOME": "/x"})
    assert answer["started"] is False and answer["reason"] == "not_a_job"
    for bad in ({"job_id": "../etc", "directory": "/tmp", "attempt": 0, "env": {"A": "b"}},
                {"job_id": "ab" * 16, "directory": "relative", "attempt": 0, "env": {"A": "b"}},
                {"job_id": "ab" * 16, "directory": "/tmp", "attempt": 0, "env": {}}):
        with pytest.raises(client.ServiceError) as refused:
            service_home.call(Method.IMPORT_START, bad)
        assert refused.value.code == protocol.ErrorCode.INVALID_PARAMS


# -- probe wizard --------------------------------------------------------------------------------


def _plan(**flags):
    base = dict(action=None, yes=True, json_output=False, agents=None, tracking=None, capture=None,
                auto_update=None, agent_rules=None, reinstall=False, who_records=None, folder=None,
                uninstall=False, auth_code=None, sign_in_flags=False)
    return wizard_service.plan(**{**base, **flags})


def test_which_wizard_runs_the_service_takes():
    claude = ("claude_code",)  # harness-literal-ok: a test agent id
    assert _plan(action="configure", agents=claude, capture=False) == wizard_service.Routed(
        "configure", {"agents": list(claude), "capture": False})
    assert _plan(action="configure", agents=claude, reinstall=True) == wizard_service.Routed(
        "configure", {"agents": list(claude), "reinstall": True})
    assert _plan(who_records="daemon") == wizard_service.Routed("recorder", {"who_records": "daemon"})
    assert _plan(action="logout") == wizard_service.Routed("logout")
    # `probe uninstall` stops the service itself: never one of its actions.
    assert isinstance(_plan(action="uninstall"), str)
    assert _plan(action="update", update_trigger="session_start") == wizard_service.Routed(
        "update", trigger="session_start")
    assert _plan(action="update", update_trigger="bogus") == wizard_service.Routed("update")
    # What the action protocol cannot carry stays in-process (each a reason).
    for flags in (
        {"action": "logout", "yes": False},  # the menu and its prompts
        {"action": "logout", "json_output": True},  # its reader wants this process's stream
        {"action": "configure"},  # agents found on this terminal's PATH
        {"action": "configure", "agents": claude, "auth_code": "ABCDE12345"},
        {"action": "configure", "agents": claude, "reinstall": True, "capture": True},
        {"action": "login", "sign_in_flags": True},
        {"action": "recorder"},  # a read of the current setting
        {"action": "transcripts", "folder": "/x"},
        {"action": "configure", "agents": claude, "uninstall": True},
        {"action": "diagnose"},
        {"action": None},
        {"action": "logout", "capture": False},
        # A flag the action would drop is the in-process path's usage error.
        {"action": "logout", "who_records": "daemon"},
        {"action": "update", "who_records": "agent"},
        {"action": "configure", "agents": claude, "who_records": "daemon"},
        {"action": "logout", "agents": claude},
        {"action": "uninstall", "reinstall": True},
    ):
        assert isinstance(_plan(**flags), str), flags


def _logout_plan(core, *, say: str = "Signed out of https://api.example", exit_steps=()):
    steps = [{"event": {"event": "step", "name": "sign_in", "status": "started", "message": "", "agent": None}},
             {"say": say}, *exit_steps]
    core.plan("logout", steps=steps)


def test_a_wizard_action_runs_on_the_service_and_streams_its_text(service_home, core, same_cli, scratch, capfd):
    _logout_plan(core)
    service_home.start()
    code = wizard_service.run(wizard_service.Routed("logout"))
    assert code == 0
    assert "Signed out of https://api.example" in capfd.readouterr().out
    (call,) = core.calls("logout")
    env = call["env"]
    assert env["CLAUDE_CONFIG_DIR"] == str(scratch["CLAUDE_CONFIG_DIR"]) and env["PROBE_TOKEN"] is None
    assert env["PROBE_DESKTOP_HUMAN"] == "0"


def test_the_wizard_command_itself_goes_through_the_service(service_home, core, same_cli, scratch):
    _logout_plan(core, say="bye from the service", exit_steps=[{"exit": 4}])
    service_home.start()
    from typer.testing import CliRunner

    result = CliRunner().invoke(cli_main.app, ["wizard", "--action", "logout", "--yes"])
    assert "bye from the service" in result.output
    assert result.exit_code == 4, result.output
    assert len(core.calls("logout")) == 1


def test_ctrl_c_during_the_browser_approval_cancels_it(service_home, core, same_cli, tmp_path, scratch):
    prompt = {"event": "device_prompt", "verification_uri": "https://x", "verification_uri_complete": "https://x/c",
              "user_code": "ABCD-EFGH", "expires_in": 600}
    core.plan("configure", steps=[{"event": prompt, "interruptible": True},
                                  {"wait": str(tmp_path / "never"), "interruptible": True}])
    service_home.start()
    # The terminal is a process of its own, so the Ctrl-C lands on it alone.
    terminal = subprocess.Popen(
        [sys.executable, "-c", _TERMINAL, "claude_code"],  # harness-literal-ok: a test agent id
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )

    def waiting() -> bool:
        return any("device_prompt" in record.read_text() for record in paths.actions_dir().glob("*.jsonl"))

    try:
        assert wait_for(waiting, 15), "the action never reached its browser approval"
        time.sleep(0.5)  # the terminal reads the approval wait (it polls every POLL_S)
        terminal.send_signal(signal.SIGINT)
        out, err = terminal.communicate(timeout=30)
    finally:
        if terminal.poll() is None:
            terminal.kill()
    assert json.loads(out.strip().splitlines()[-1]) == {"code": 130}, err
    (journal,) = paths.actions_dir().glob("*.jsonl")
    assert '"type":"cancel"' in journal.read_text(), "no action.cancel reached the service"


_TERMINAL = r"""
import json, sys
from probe.cli import service_calls, wizard_service
service_calls.same_cli = lambda: True  # FakeCore's python stands for this CLI
code = wizard_service.run(wizard_service.Routed("configure", {"agents": [sys.argv[1]]}))
print(json.dumps({"code": code}), flush=True)
"""


def test_the_wizard_runs_in_process_whenever_the_service_does_not_take_it(service_home, core, same_cli,
                                                                          tmp_path, scratch, monkeypatch):
    # No service.
    assert wizard_service.run(wizard_service.Routed("logout")) is None
    service_home.start()
    # A request an older core refuses (here: an agent no harness has).
    assert wizard_service.run(wizard_service.Routed("configure", {"agents": ["nobody"]})) is None
    # Busy: another action holds the one mutating slot.
    gate = tmp_path / "release"
    core.plan("uninstall", steps=[{"wait": str(gate)}])
    service_home.call(Method.ACTION_RUN, {"action": "uninstall", "client_request_id": "held"})
    try:
        assert wizard_service.run(wizard_service.Routed("logout")) is None
    finally:
        gate.touch()
    # A credential the service's child cannot be given.
    monkeypatch.setenv("PROBE_TOKEN", "ros_env_only")
    assert wizard_service.run(wizard_service.Routed("logout")) is None
    assert core.calls("logout") == []


@contextlib.contextmanager
def _service_without_sandbox_caps(seen: list):
    """A service from before `caps` (the released one): it answers hello
    without `caps` and runs `action.run`, with no sandbox check of its caller."""
    sock_path = paths.ensure_dirs()
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    listener.bind(str(sock_path))
    listener.listen(8)
    stop = threading.Event()
    done = {"v": 1, "event": "done", "ok": True, "complete": True, "exit_code": 0, "steps": []}

    def serve() -> None:
        listener.settimeout(0.1)
        while not stop.is_set():
            try:
                conn, _ = listener.accept()
            except (socket.timeout, OSError):
                continue
            with conn:
                buffer = b""
                conn.settimeout(1.0)
                try:
                    while True:
                        chunk = conn.recv(65536)
                        if not chunk:
                            break
                        buffer += chunk
                        while b"\n" in buffer:
                            line, buffer = buffer.split(b"\n", 1)
                            message = json.loads(line)
                            seen.append(message["method"])
                            result = {
                                Method.HELLO: {"service_version": "0.289.0", "api": 1, "pid": 1, "started_at": 0.0,
                                               "state": "running"},
                                Method.ACTION_RUN: {"action_id": "act_00000000000000aa"},
                                Method.ACTION_EVENTS: {"events": [{"seq": 1, "event": done}], "done": True},
                            }.get(message["method"], {})
                            conn.sendall(json.dumps({"jsonrpc": "2.0", "id": message["id"], "result": result}).encode()
                                         + b"\n")
                except (OSError, ValueError):
                    pass

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    try:
        yield
    finally:
        stop.set()
        thread.join(2)
        listener.close()
        with contextlib.suppress(OSError):
            os.unlink(sock_path)


def test_a_service_that_does_not_enforce_the_sandbox_on_action_run_is_never_sent_one(service_home, same_cli,
                                                                                      scratch):
    """After an in-place CLI update the service from before it (same
    interpreter path, older code) still answers, and its `action.run` checks no
    sandbox: a wizard action sent there would run outside the caller's sandbox.
    Only a service that says it checks (`caps`) gets one; else in-process."""
    seen: list = []
    with _service_without_sandbox_caps(seen):
        assert wizard_service.run(wizard_service.Routed("logout")) is None
    assert Method.ACTION_RUN not in seen, seen
    # This service says so.
    service_home.start()
    with service_home.connect(hello=False) as conn:
        assert protocol.Cap.ACTION_SANDBOX in conn.hello("cli", "test")["caps"]


class _Lost:
    """A connection whose `action.run` was sent and never answered."""

    def __init__(self, answers):
        self.answers = answers
        self.sent: list = []

    def hello(self, *_a, **_k):
        return {"caps": [protocol.Cap.ACTION_SANDBOX]}

    def call(self, method, params=None):
        self.sent.append((method, dict(params or {})))
        answer = self.answers.pop(0)
        if isinstance(answer, BaseException):
            raise answer
        return answer

    def close(self):
        pass


def test_a_run_sent_and_never_answered_is_never_run_here_as_well(service_home, same_cli, scratch, monkeypatch, capsys):
    from probe.service import client as service_client

    paths.ensure_dirs()
    paths.socket_path().touch()  # `_reachable`: a socket file is there
    first = _Lost([TimeoutError("no answer")])
    monkeypatch.setattr(service_client.Connection, "open", classmethod(lambda cls, timeout=2.0: first))
    monkeypatch.setattr(wizard_service, "RECONNECT_S", 0.3)
    monkeypatch.setattr(wizard_service, "_reopen", lambda version, deadline: None)
    assert wizard_service.run(wizard_service.Routed("logout")) == 1, "a lost answer must not fall back in-process"
    assert "may still run it" in capsys.readouterr().err

    # It answers on a new connection, by the same client_request_id: followed, once.
    again = _Lost([{"action_id": "act_0000000000000001", "existing": True}])
    first = _Lost([TimeoutError("no answer")])
    monkeypatch.setattr(service_client.Connection, "open", classmethod(lambda cls, timeout=2.0: first))
    monkeypatch.setattr(wizard_service, "_reopen", lambda version, deadline: again)
    followed: list = []
    monkeypatch.setattr(wizard_service._Follower, "follow", lambda self: followed.append(self.action_id) or 0)
    assert wizard_service.run(wizard_service.Routed("logout")) == 0
    assert followed == ["act_0000000000000001"]
    assert first.sent[0][1]["client_request_id"] == again.sent[0][1]["client_request_id"]

    # A refusal of the RESEND says nothing about the first send: unconfirmed, never run here.
    refused = _Lost([service_client.ServiceError(protocol.ErrorCode.INVALID_PARAMS, "invalid params")])
    first = _Lost([TimeoutError("no answer")])
    monkeypatch.setattr(service_client.Connection, "open", classmethod(lambda cls, timeout=2.0: first))
    monkeypatch.setattr(wizard_service, "_reopen", lambda version, deadline: refused)
    assert wizard_service.run(wizard_service.Routed("logout")) == 1


def test_a_retry_of_an_accepted_request_gets_its_action_whatever_changed(service_home, core, tmp_path, scratch):
    """The first `action.run` was accepted; its retry (same client_request_id)
    gets that action even when a check of the caller would now refuse it (here
    an endpoint the config no longer names, as after a logout)."""
    gate = tmp_path / "release"
    core.plan("logout", steps=[{"wait": str(gate)}])
    service_home.start()
    first = service_home.call(Method.ACTION_RUN, {"action": "logout", "client_request_id": "retry-me"})
    try:
        again = service_home.call(Method.ACTION_RUN, {
            "action": "logout", "client_request_id": "retry-me", "base_url": "https://not-signed-in.example",
        })
        assert again == {"action_id": first["action_id"], "existing": True}
        with pytest.raises(client.ServiceError) as fresh:
            service_home.call(Method.ACTION_RUN, {
                "action": "logout", "client_request_id": "new-one", "base_url": "https://not-signed-in.example",
            })
        assert fresh.value.code == protocol.ErrorCode.INVALID_PARAMS
    finally:
        gate.touch()


_CONFINED_APP = r"""
import ctypes, json, sys
assert ctypes.CDLL(None, use_errno=True).prctl(38, 1, 0, 0, 0) == 0
from probe.service import client
out = {}
with client.Connection.open() as conn:
    conn.hello(sys.argv[1], "spoofed")  # the label is the caller's to choose
    try:
        out["answer"] = conn.call("action.run", {"action": "logout", "client_request_id": "label-" + sys.argv[1]})
    except client.ServiceError as exc:
        out["refused"] = (exc.data or {}).get("reason")
print(json.dumps(out))
"""


@pytest.mark.skipif(not sys.platform.startswith("linux") or _no_new_privs(),
                    reason="no_new_privs is Linux's, and this process must not have it already")
@pytest.mark.parametrize("label", ["app", "tap", "pi", "cli"])  # harness-literal-ok: API v1 client kinds
def test_no_client_label_lets_a_sandboxed_caller_run_an_action(service_home, core, scratch, label):
    """The sandbox check reads the caller's confinement, never the client kind
    it names in its hello: a sandboxed process saying `app` is refused too."""
    core.plan("logout", steps=[])
    service_home.start()
    done = subprocess.run([sys.executable, "-c", _CONFINED_APP, label], capture_output=True, text=True, timeout=30)
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout) == {"refused": protocol.RefusedReason.SANDBOXED}
    assert core.calls("logout") == []


def test_the_same_job_in_two_jobs_folders_gets_two_workers(service_home, core, tmp_path, scratch):
    """One approval in two state folders has one job id: each folder's job is
    its own, and neither is handed the other's worker."""
    gate = tmp_path / "release"
    core.plan("import_worker", before=[{"wait": str(gate)}], exit=0)
    service_home.start()
    (_dir_a, folder_a), (_dir_b, folder_b) = _job(tmp_path / "a"), _job(tmp_path / "b")
    assert folder_a.name == folder_b.name
    env = {"HOME": os.environ["HOME"], "PATH": os.environ["PATH"]}
    first = client.start_import(folder_a.name, str(folder_a.parent), 0, env)
    second = client.start_import(folder_b.name, str(folder_b.parent), 0, env)
    try:
        assert first["started"] is True and second["started"] is True, (first, second)
        assert first["pid"] != second["pid"]
        listed = _status(service_home)["imports"]
        assert sorted(i["pid"] for i in listed) == sorted([first["pid"], second["pid"]])
    finally:
        gate.touch()
    assert wait_for(lambda: _status(service_home)["imports"] == [], 10)


def test_a_newer_attempt_never_drops_the_worker_still_running(service_home, core, tmp_path, scratch):
    """Attempt 1's worker is started while attempt 0's still runs: both are
    listed (and hold the updater off) until each exits on its own."""
    gate_a, gate_b = tmp_path / "release-a", tmp_path / "release-b"
    core.plan("import_worker", before=[{"wait": str(gate_a)}], exit=0)
    service_home.start()
    _directory, folder = _job(tmp_path)
    env = {"HOME": os.environ["HOME"], "PATH": os.environ["PATH"]}
    old = client.start_import(folder.name, str(folder.parent), 0, env)
    # It read its plan (gate a) before the next worker's is written (gate b).
    assert wait_for(lambda: len(core.stand_in_calls("import_worker")) == 1, 10)
    core.plan("import_worker", before=[{"wait": str(gate_b)}], exit=0)
    new = client.start_import(folder.name, str(folder.parent), 1, env)
    try:
        assert old["started"] is True and new["started"] is True and old["pid"] != new["pid"]
        assert sorted(i["pid"] for i in _status(service_home)["imports"]) == sorted([old["pid"], new["pid"]])
        saved = json.loads((paths.service_dir() / "imports.json").read_text())
        assert sorted(w["pid"] for w in saved["workers"]) == sorted([old["pid"], new["pid"]])
        gate_b.touch()  # the newer one ends first: the older one is still listed
        assert wait_for(lambda: [i["pid"] for i in _status(service_home)["imports"]] == [old["pid"]], 10)
    finally:
        gate_a.touch()
        gate_b.touch()
    assert wait_for(lambda: _status(service_home)["imports"] == [], 10)


def test_writing_a_childs_request_never_blocks_the_loop(tmp_path):
    """A request bigger than a pipe holds (a full status-line batch), to a child
    that reads it late: the loop keeps running meanwhile."""
    import asyncio

    from probe.service import children

    request = b"x" * (256 * 1024)
    child = [sys.executable, "-c", "import sys, time; time.sleep(0.6); sys.stdin.buffer.read()"]

    async def scenario():
        loop = asyncio.get_running_loop()
        fired: list = []
        armed = loop.time()
        loop.call_later(0.02, lambda: fired.append(loop.time() - armed))
        code = await children.run_command(child, env=dict(os.environ), cwd=str(tmp_path), timeout=10, stdin=request)
        return code, fired

    code, fired = asyncio.run(scenario())
    assert code == 0
    assert fired and fired[0] < 0.3, f"a 20 ms timer fired after {fired[0] * 1000:.0f} ms: the write blocked the loop"


def test_a_descendant_keeping_stdin_never_holds_the_writer_or_the_leader(tmp_path, monkeypatch):
    """A child that started a descendant in a session of its own (setsid), which
    keeps stdin open and never reads it: the timeout's group kill misses that
    descendant, so a blocking write of a request bigger than the pipe waited on
    it forever, and the leader, never waited for, stayed a zombie."""
    import asyncio

    from probe.service import children

    pidfile = tmp_path / "descendant.pid"
    script = (
        "import subprocess, sys, time\n"
        "d = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'], start_new_session=True)\n"
        f"open(r'{pidfile}', 'w').write(str(d.pid))\n"
        "time.sleep(30)\n"
    )
    started: list = []
    real = children.spawn_watched

    def spy(*args, **kwargs):
        child = real(*args, **kwargs)
        started.append(child)
        return child

    monkeypatch.setattr(children, "spawn_watched", spy)
    try:
        code = asyncio.run(children.run_command([sys.executable, "-c", script], env=dict(os.environ),
                                                cwd=str(tmp_path), timeout=1.5, stdin=b"x" * (1024 * 1024)))
        assert code is None
        leader = started[0]
        names = {f"probe-child-{leader.pid}", f"probe-stdin-{leader.pid}"}
        assert wait_for(lambda: leader.returncode is not None, 5), "the leader was never reaped"
        assert wait_for(lambda: not [t for t in threading.enumerate() if t.name in names], 5), \
            "a thread still waits on a descendant that holds stdin"
    finally:
        with contextlib.suppress(OSError, ValueError):
            os.kill(int(pidfile.read_text()), signal.SIGKILL)


def test_a_resend_never_goes_to_a_service_that_does_not_enforce_the_sandbox(monkeypatch):
    """The resend after a lost answer opens a new connection: one to a service
    without `caps` (an older one, back at the same path) is never used."""
    from probe.service import client as service_client

    class Older:
        closed = False

        def hello(self, *_a, **_k):
            return {"service_version": "0.289.0", "api": 1}

        def close(self):
            self.closed = True

    opened: list = []
    monkeypatch.setattr(service_client.Connection, "open",
                        classmethod(lambda cls, timeout=2.0: opened.append(Older()) or opened[-1]))
    assert wizard_service._reopen("test", time.monotonic() + 0.2) is None
    assert opened and all(conn.closed for conn in opened)


def test_another_clis_code_runs_the_wizard_itself(service_home, core, scratch):
    service_home.start()
    assert wizard_service.run(wizard_service.Routed("logout")) is None  # runtime.json names another python
    assert core.calls("logout") == []


# -- the schedulers, on their own ------------------------------------------------------------


@pytest.fixture
def ran(monkeypatch):
    """`children.run_command` recorded instead of run: (argv, env, stdin)."""
    import asyncio

    calls: list = []

    async def fake(argv, *, env, cwd, timeout, stdin=b"", log_path=None, kill_on_cancel=False):
        calls.append((argv, env, stdin))
        await asyncio.sleep(0)
        return 0

    monkeypatch.setattr(notesync.children, "run_command", fake)
    # The status line's folders here are stand-ins: a child's own re-check passes.
    monkeypatch.setattr(statusline.StatuslineRefresher, "check", lambda self, root: None)
    monkeypatch.setattr(notesync.children, "core_python", lambda: "/cli/python")
    return calls


def test_notes_sync_waits_out_an_in_place_update_and_merges_what_it_was_asked(ran, monkeypatch):
    import asyncio

    monkeypatch.setattr(notesync, "DEBOUNCE_S", 0.01)
    held = {"on": True}
    logged: list = []
    kimi = "kimi_code"  # harness-literal-ok: a test agent id

    async def scenario():
        sync = notesync.NoteSync(log=logged.append, held=lambda: held["on"])
        assert sync.request({"A": "1"}, "push", [], False) == {"outcome": "scheduled"}
        assert sync.request({"A": "1"}, "reconcile", ["", kimi, kimi], True)["outcome"] == "scheduled"
        await asyncio.sleep(0.1)
        assert ran == [] and sync.in_flight(), "a sync started while the update applied"
        held["on"] = False
        while sync.in_flight():
            await asyncio.sleep(0.01)
        return sync

    sync = asyncio.run(scenario())
    assert [argv[4:] for argv, _env, _ in ran] == [
        ["agent-rules", "refresh"], ["agent-rules", "refresh"], ["notes", "sync"], ["feedback", "flush"],
    ]
    assert ran[0][0][:4] == ["/cli/python", "-I", "-m", "probe.cli"]
    assert "PROBE_AGENT" not in ran[0][1] and ran[1][1]["PROBE_AGENT"] == kimi
    assert all(env["A"] == "1" for _argv, env, _ in ran)
    assert sync.runs == 1 and logged == []


def test_a_stopping_service_hands_an_unrun_sync_to_a_detached_shell(ran, monkeypatch):
    import asyncio

    monkeypatch.setattr(notesync, "DEBOUNCE_S", 30)
    shells: list = []
    codex = "codex"  # harness-literal-ok: a test agent id

    class _Shell:
        def __init__(self, argv, **kwargs):
            shells.append((argv, kwargs))

    monkeypatch.setattr(subprocess, "Popen", _Shell)

    async def scenario():
        sync = notesync.NoteSync(log=lambda _m: None)
        sync.request({"XDG_STATE_HOME": "/s t"}, "reconcile", [codex], False)
        sync.close()
        assert sync.request({}, "push", [], False)["outcome"] is None

    asyncio.run(scenario())
    ((argv, kwargs),) = shells
    assert argv[:2] == ["/bin/sh", "-c"]
    assert argv[2] == (f"PROBE_AGENT={codex} /cli/python -I -m probe.cli agent-rules refresh; "
                       "/cli/python -I -m probe.cli notes sync")
    assert kwargs["env"]["XDG_STATE_HOME"] == "/s t" and kwargs["start_new_session"] is True
    assert ran == []


def test_the_team_notes_probe_commands_say_the_service_started_them(ran, monkeypatch):
    """Marked `SERVICE_CHILD_ENV`, so none of them asks the service for an
    update (`probe.cli.main._hand_update_to_service`): an ask from the first
    would land while the job's next command still runs from the CLI's files."""
    import asyncio

    monkeypatch.setattr(notesync, "DEBOUNCE_S", 0.01)
    shells: list = []

    class _Shell:
        def __init__(self, argv, **kwargs):
            shells.append(kwargs)

    monkeypatch.setattr(subprocess, "Popen", _Shell)

    async def scenario():
        sync = notesync.NoteSync(log=lambda _m: None)
        sync.request({"A": "1"}, "reconcile", [""], True)
        while sync.in_flight():
            await asyncio.sleep(0.01)
        handed = notesync.NoteSync(log=lambda _m: None)
        handed.request({"A": "1"}, "push", [], False)
        handed.close()

    asyncio.run(scenario())
    assert len(ran) == 3
    assert all(env[notesync.children.SERVICE_CHILD_ENV] == "1" and env["A"] == "1" for _argv, env, _ in ran)
    (kwargs,) = shells
    assert kwargs["env"][notesync.children.SERVICE_CHILD_ENV] == "1"


def test_the_status_line_scheduler_batches_and_spaces_its_children(ran, monkeypatch):
    import asyncio

    monkeypatch.setattr(statusline, "INTERVAL_S", 0.2)
    monkeypatch.setattr(statusline, "GATHER_S", 0.02)
    monkeypatch.setattr(statusline, "MAX_BATCH", 2)

    async def scenario():
        refresher = statusline.StatuslineRefresher(log=lambda _m: None)
        for sid in ("s-0000001", "s-0000002", "s-0000003", "s-0000001"):
            assert refresher.request("/plugin", "/py", {"X": "1"}, sid, None)["scheduled"] is True
        began = time.monotonic()
        while len(ran) < 2 or refresher.in_flight():
            await asyncio.sleep(0.01)
        return refresher, time.monotonic() - began

    refresher, took = asyncio.run(scenario())
    batches = [[s["sid"] for s in json.loads(stdin)["sessions"]] for _argv, _env, stdin in ran]
    assert batches == [["s-0000001", "s-0000002"], ["s-0000003"]], "one child per batch, no session twice"
    assert ran[0][0] == ["/py", "-I", "/plugin/hooks/statusline_refresh.py", "fetch-all"]
    assert ran[0][1]["X"] == "1"
    assert took >= 0.2 - 0.05, "the second child came sooner than the interval"
    assert refresher.public()["children"] == 2 and refresher.public()["waiting"] == 0


def test_a_followed_session_is_refreshed_when_its_capture_moves_with_no_hook_asking(ran, monkeypatch):
    """A session's capture reading is taken a moment before the service
    registers it (or its recorder takes it), and an idle session's hooks never
    ask again: it read "not started" / "not recording" while it was recorded
    (2026-10-27). The service follows it: a change in what the reading is
    taken from refreshes it again, in the context it last asked in."""
    import asyncio

    monkeypatch.setattr(statusline, "INTERVAL_S", 0.05)
    monkeypatch.setattr(statusline, "GATHER_S", 0.01)
    monkeypatch.setattr(statusline, "FOLLOW_S", 0.02)
    monkeypatch.setattr(statusline, "SETTLE_S", 60)
    known: dict = {}

    async def settle(refresher, children):
        deadline = time.monotonic() + 5
        while (len(ran) < children or refresher.in_flight()) and time.monotonic() < deadline:
            await asyncio.sleep(0.01)
        await asyncio.sleep(0.15)  # several looks: nothing more is asked

    async def scenario():
        refresher = statusline.StatuslineRefresher(log=lambda _m: None, readings=lambda: dict(known))
        assert refresher.request("/plugin", "/py", {"X": "1"}, "s-0000001", "claude_code")["scheduled"] is True
        await settle(refresher, 1)
        assert len(ran) == 1, "nothing moved: no second child"
        known["s-0000001"] = ("daemon", None)  # registered after its first reading
        await settle(refresher, 2)
        known["s-0000001"] = ("daemon", (True, True, False))  # its recorder took it
        await settle(refresher, 3)
        public = refresher.public()
        refresher.close()
        return public

    public = asyncio.run(scenario())
    batches = [[(s["sid"], s["agent"]) for s in json.loads(stdin)["sessions"]] for _argv, _env, stdin in ran]
    assert batches == [[("s-0000001", "claude_code")]] * 3, "one refresh per change, no more"
    assert all(env["X"] == "1" for _argv, env, _stdin in ran), "in the context the session asked in"
    assert public["followed"] == 1 and public["followups"] == 2


def test_following_stops_for_a_session_the_service_does_not_know_and_is_bounded(ran, monkeypatch):
    import asyncio

    monkeypatch.setattr(statusline, "GATHER_S", 0.01)
    monkeypatch.setattr(statusline, "FOLLOW_S", 0.01)
    monkeypatch.setattr(statusline, "FOLLOW_GRACE_S", 0.05)
    monkeypatch.setattr(statusline, "MAX_FOLLOWED", 2)
    logged: list = []

    async def scenario():
        refresher = statusline.StatuslineRefresher(log=logged.append, readings=dict)
        for sid in ("s-0000001", "s-0000002", "s-0000003"):
            refresher.request("/plugin", "/py", {}, sid, None)
        assert list(refresher.followed) == ["s-0000002", "s-0000003"], "the one that asked longest ago goes"
        await asyncio.sleep(0.3)
        dropped = (dict(refresher.followed), refresher._follow_timer)

        def broken():
            raise RuntimeError("boom")

        failing = statusline.StatuslineRefresher(log=logged.append, readings=broken)
        failing.request("/plugin", "/py", {}, "s-0000004", None)
        await asyncio.sleep(0.1)
        assert failing._follow_timer is not None, "a failed look tries again"
        failing.close()
        return dropped, failing._follow_timer

    (followed, timer), closed_timer = asyncio.run(scenario())
    assert followed == {} and timer is None, "unknown past the grace: no longer followed, no timer left"
    assert closed_timer is None
    assert any("reading the sessions failed: RuntimeError" in line for line in logged)


def test_the_service_reads_a_status_lines_capture_from_its_registration_and_recorder():
    from types import SimpleNamespace

    from probe.service import server

    def row(sid, alive, recording, off):
        return {"sid": sid, "alive": alive, "recording": recording, "off": off, "last": "", "failures": 0}

    fake = SimpleNamespace(
        registry=SimpleNamespace(sessions={
            "s-0000001": SimpleNamespace(sid="s-0000001", mode="daemon"),
            "s-0000002": SimpleNamespace(sid="s-0000002", mode="off"),
            "s-0000004": SimpleNamespace(sid="s-0000004", mode="inline"),
        }),
        recorders=SimpleNamespace(public=lambda: [
            row("s-0000001", True, True, False), row("s-0000003", True, None, False), row("s-0000004", True, True, True)]),
    )
    assert server.Service._statusline_readings(fake) == {
        "s-0000001": ("daemon", (True, True, False)),
        "s-0000002": statusline.OFF,  # registered off
        "s-0000003": (None, (True, None, False)),
        "s-0000004": statusline.OFF,  # its recorder holds it off
    }


def _settle(ran, refresher, children, extra=0.15):
    import asyncio

    async def wait():
        deadline = time.monotonic() + 5
        while (len(ran) < children or refresher.in_flight()) and time.monotonic() < deadline:
            await asyncio.sleep(0.01)
        await asyncio.sleep(extra)

    return wait()


@pytest.fixture
def fast_follow(monkeypatch):
    monkeypatch.setattr(statusline, "INTERVAL_S", 0.05)
    monkeypatch.setattr(statusline, "GATHER_S", 0.01)
    monkeypatch.setattr(statusline, "FOLLOW_S", 0.02)
    monkeypatch.setattr(statusline, "SETTLE_S", 60)


def _sids(ran):
    return [[s["sid"] for s in json.loads(stdin)["sessions"]] for _argv, _env, stdin in ran]


def test_a_session_switched_off_is_never_refreshed_from_the_service(ran, fast_follow):
    """Its child would read the server for it: Probe off makes no call for
    the session (its hooks refresh none either)."""
    import asyncio

    known = {"s-0000001": ("daemon", (True, True, False))}

    async def scenario():
        refresher = statusline.StatuslineRefresher(log=lambda _m: None, readings=lambda: dict(known))
        refresher.request("/plugin", "/py", {}, "s-0000001", None)
        await _settle(ran, refresher, 1)
        known["s-0000001"] = statusline.OFF
        await _settle(ran, refresher, 1, 0.3)
        assert len(ran) == 1, "switched off: nothing ran for it"
        assert "s-0000001" in refresher.followed, "off is not ended: still followed"
        known["s-0000001"] = ("daemon", (True, True, False))  # on again, no hook asking
        await _settle(ran, refresher, 2)
        # A hook's request that lands as it is switched off runs nothing either.
        known["s-0000001"] = statusline.OFF
        refresher.request("/plugin", "/py", {}, "s-0000001", None)
        await _settle(ran, refresher, 2, 0.3)
        refresher.close()

    asyncio.run(scenario())
    assert _sids(ran) == [["s-0000001"], ["s-0000001"]]


def test_a_session_whose_request_names_an_endpoint_is_not_followed(ran, fast_follow):
    """The endpoint was checked against the CLI config only when it asked."""
    import asyncio

    async def scenario():
        refresher = statusline.StatuslineRefresher(log=lambda _m: None, readings=dict)
        refresher.request("/plugin", "/py", {"PROBE_BASE_URL": "https://api.research.prbe.ai"}, "s-0000001", None)
        followed = dict(refresher.followed)
        await _settle(ran, refresher, 1)
        refresher.close()
        return followed

    assert asyncio.run(scenario()) == {}
    assert len(ran) == 1, "its own refresh still runs"


def test_a_session_switched_off_then_closed_is_never_refreshed(ran, fast_follow):
    import asyncio

    known = {"s-0000001": ("daemon", (True, True, False))}

    async def scenario():
        refresher = statusline.StatuslineRefresher(log=lambda _m: None, readings=lambda: dict(known))
        refresher.request("/plugin", "/py", {}, "s-0000001", None)
        await _settle(ran, refresher, 1)
        known["s-0000001"] = statusline.OFF
        await _settle(ran, refresher, 1, 0.1)
        del known["s-0000001"]  # closed while off, well within the grace
        await _settle(ran, refresher, 1, 0.3)
        followed = dict(refresher.followed)
        refresher.close()
        return followed

    assert asyncio.run(scenario()) == {}
    assert len(ran) == 1


def test_a_session_back_on_is_still_followed_while_its_registration_catches_up(ran, fast_follow):
    import asyncio

    known = {"s-0000001": ("daemon", (True, True, False))}

    async def scenario():
        refresher = statusline.StatuslineRefresher(log=lambda _m: None, readings=lambda: dict(known))
        refresher.request("/plugin", "/py", {}, "s-0000001", None)
        await _settle(ran, refresher, 1)
        known["s-0000001"] = statusline.OFF
        await _settle(ran, refresher, 1, 0.1)
        known["s-0000001"] = (None, (True, True, False))  # its recorder shows first
        await _settle(ran, refresher, 2)
        still = "s-0000001" in refresher.followed
        refresher.close()
        return still

    assert asyncio.run(scenario())
    assert len(ran) == 2


def test_a_new_folder_past_the_limit_takes_the_place_of_the_least_recently_asked(ran, fast_follow, monkeypatch):
    import asyncio

    monkeypatch.setattr(statusline, "MAX_GROUPS", 2)

    async def scenario():
        refresher = statusline.StatuslineRefresher(log=lambda _m: None, readings=dict)
        refresher.request("/a", "/py", {}, "s-0000001", None)
        await asyncio.sleep(0.01)
        refresher.request("/b", "/py", {}, "s-0000002", None)
        await _settle(ran, refresher, 2)
        answer = refresher.request("/c", "/py", {}, "s-0000003", None)
        followed = sorted(refresher.followed)
        refresher.close()
        return answer, followed

    answer, followed = asyncio.run(scenario())
    assert answer["scheduled"] is True
    assert followed == ["s-0000002", "s-0000003"], "the folder asked of longest ago made room"


def test_an_ended_session_is_not_refreshed_again(ran, fast_follow):
    import asyncio

    known = {"s-0000001": ("daemon", (True, True, False))}

    async def scenario():
        refresher = statusline.StatuslineRefresher(log=lambda _m: None, readings=lambda: dict(known))
        refresher.request("/plugin", "/py", {}, "s-0000001", "claude_code")
        await _settle(ran, refresher, 1)
        known["s-0000001"] = (None, (True, True, False))  # its registration ended, its recorder finishes
        await _settle(ran, refresher, 1, 0.2)
        del known["s-0000001"]
        await _settle(ran, refresher, 1, 0.2)
        idle = not refresher.in_flight() and refresher.followed == {}
        refresher.close()
        return idle

    assert asyncio.run(scenario())
    assert len(ran) == 1


def test_a_change_is_refreshed_again_once_it_settles(ran, fast_follow, monkeypatch):
    """The child also reads what the service does not see (the `.hosted`
    marker, the switch file), which can land after the change."""
    import asyncio

    monkeypatch.setattr(statusline, "SETTLE_S", 0.2)
    known: dict = {}

    async def scenario():
        refresher = statusline.StatuslineRefresher(log=lambda _m: None, readings=lambda: dict(known))
        refresher.request("/plugin", "/py", {}, "s-0000001", None)
        await _settle(ran, refresher, 1)
        known["s-0000001"] = ("daemon", (True, True, False))
        await _settle(ran, refresher, 3, 0.6)
        refresher.close()

    asyncio.run(scenario())
    assert _sids(ran) == [["s-0000001"]] * 3, "the hook's, the change's, one more once settled: no more"


def test_a_failed_refresh_is_retried_a_bounded_number_of_times(monkeypatch, fast_follow):
    import asyncio

    monkeypatch.setattr(statusline, "SETTLE_S", 0.1)  # a settle due after the last failure runs nothing more
    monkeypatch.setattr(statusline.StatuslineRefresher, "check", lambda self, root: None)
    calls: list = []

    async def failing(argv, **_kwargs):
        calls.append(argv)
        return 1

    monkeypatch.setattr(statusline.children, "run_command", failing)
    known = {"s-0000001": ("daemon", (True, False, False))}

    async def scenario():
        refresher = statusline.StatuslineRefresher(log=lambda _m: None, readings=lambda: dict(known))
        refresher.request("/plugin", "/py", {}, "s-0000001", None)
        await asyncio.sleep(1.0)
        tried = len(calls)
        known["s-0000001"] = ("daemon", (True, True, False))  # a new change gets its own tries
        await asyncio.sleep(1.0)
        refresher.close()
        return tried

    assert asyncio.run(scenario()) == statusline.MAX_FOLLOW_RETRIES, "retried, then left for the next change or hook"
    assert len(calls) == 2 * statusline.MAX_FOLLOW_RETRIES


def test_a_folder_gone_since_its_request_runs_nothing_and_ends_its_following(monkeypatch, fast_follow, ran):
    import asyncio

    monkeypatch.setattr(statusline.StatuslineRefresher, "check", lambda self, root: "not a Probe plugin folder")
    logged: list = []

    async def scenario():
        refresher = statusline.StatuslineRefresher(log=logged.append, readings=dict)
        refresher.request("/plugin-0.1", "/py", {}, "s-0000001", None)
        await asyncio.sleep(0.2)
        followed = dict(refresher.followed)
        refresher.close()
        return followed

    assert asyncio.run(scenario()) == {}
    assert ran == [] and any("not a Probe plugin folder" in line for line in logged)


def test_follow_ups_never_queue_past_max_pending_nor_forget_a_followed_folder(ran, fast_follow, monkeypatch):
    import asyncio

    known: dict = {}

    async def scenario():
        refresher = statusline.StatuslineRefresher(log=lambda _m: None, readings=lambda: dict(known))
        for sid in ("s-0000001", "s-0000002", "s-0000003"):
            refresher.request("/plugin", "/py", {}, sid, None)
        await _settle(ran, refresher, 1)
        monkeypatch.setattr(statusline, "MAX_PENDING", 2)
        monkeypatch.setattr(statusline, "GATHER_S", 30)
        monkeypatch.setattr(statusline, "INTERVAL_S", 30)
        known.update({sid: ("daemon", None) for sid in ("s-0000001", "s-0000002", "s-0000003")})
        await asyncio.sleep(0.1)
        waiting = refresher.public()["waiting"]
        # A folder its followed sessions need is never forgotten for a new one.
        monkeypatch.setattr(statusline, "MAX_GROUPS", 1)
        refused = refresher.request("/other", "/py", {}, "s-0000009", None)
        refresher.close()
        return waiting, refused, len(refresher.followed)

    waiting, refused, followed = asyncio.run(scenario())
    assert waiting == 2
    assert refused == {"scheduled": False, "reason": "busy: too many plugin folders"}
    assert followed == 3


def test_an_old_contexts_child_never_settles_the_sessions_new_context():
    """A session that asked again in another context: a child of its old one
    writes the old context's marker, so it must not mark the new one's reading
    as seen (that change would never be refreshed there)."""
    reading = ("daemon", (True, True, False))
    refresher = statusline.StatuslineRefresher(log=lambda _m: None, readings=lambda: {"s-0000001": reading})
    old = statusline._Group("/plugin", "/py", {}, "key-a")
    refresher.followed["s-0000001"] = statusline._Followed("key-b", None)
    assert refresher._seen(old, {"s-0000001": None}) == {"s-0000001": None}
    assert refresher.followed["s-0000001"].seen is None
    new = statusline._Group("/plugin", "/py", {}, "key-b")
    refresher._seen(new, {"s-0000001": None})
    assert refresher.followed["s-0000001"].seen == reading


def test_the_status_line_stops_following_before_the_recorders_pause():
    """Pausing the recorders moves every session's capture: followed, each
    would get a refresh child that reads this service after it has gone and
    writes "not started" on every update's restart (review of #3554)."""
    import asyncio
    from types import SimpleNamespace

    from probe.service import server

    order: list = []

    class Part:
        def __init__(self, name):
            self.name = name

        def close(self, *_a, **_k):
            order.append(self.name)

    class Recorders(Part):
        async def close(self):
            order.append(self.name)

    names = ("mailwatch", "mailhost", "alerts", "hints", "hookhosts", "hook_queue", "background", "workers",
             "watch", "statepost", "actions", "notes", "imports", "statusline")
    fake = SimpleNamespace(
        _discovery_handle=None, _grace_handle=None, _expiry_handle=None, _outbox_task=None, _server=None,
        legacy=None, connections=[], watcher=None, _hook_runs=None, _host_starts=None, _queue_stores=None,
        _background_starts=None, _host_pool=None, recorders=Recorders("recorders"),
        registry=SimpleNamespace(save=lambda: order.append("save")),
        **{name: Part(name) for name in names},
    )
    asyncio.run(server.Service._shutdown(fake))
    assert order.index("statusline") < order.index("recorders")
    assert order.count("statusline") == 1


def test_a_cancelled_status_line_child_is_killed_not_left_running(tmp_path):
    """A refresh child must not outlive the service it reads (`kill_on_cancel`)."""
    import asyncio

    from probe.service import children

    pid_file = tmp_path / "pid"

    async def scenario():
        task = asyncio.ensure_future(children.run_command(
            ["/bin/sh", "-c", f"echo $$ > {pid_file}; exec sleep 30"], env=dict(os.environ), cwd=str(tmp_path),
            timeout=60, kill_on_cancel=True))
        deadline = time.monotonic() + 5
        while not (pid_file.exists() and pid_file.read_text().strip()) and time.monotonic() < deadline:
            await asyncio.sleep(0.02)
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task

    asyncio.run(scenario())
    pid = int(pid_file.read_text())

    def gone() -> bool:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return True
        try:  # a zombie the watcher has not reaped yet is gone too
            return Path(f"/proc/{pid}/stat").read_text().split()[2] == "Z"
        except OSError:
            return True

    deadline = time.monotonic() + 5
    while not gone() and time.monotonic() < deadline:
        time.sleep(0.05)
    assert gone()


def test_the_status_line_scheduler_bounds_folders_and_waiting_sessions(monkeypatch):
    import asyncio

    monkeypatch.setattr(statusline, "MAX_GROUPS", 1)
    monkeypatch.setattr(statusline, "MAX_PENDING", 2)
    monkeypatch.setattr(statusline, "GATHER_S", 30)

    async def scenario():
        refresher = statusline.StatuslineRefresher(log=lambda _m: None)
        assert refresher.request("/a", "/py", {}, "s-0000001", None)["scheduled"] is True
        assert refresher.request("/b", "/py", {}, "s-0000001", None) == {
            "scheduled": False, "reason": "busy: too many plugin folders"}
        assert refresher.request("/a", "/py", {}, "s-0000002", None)["scheduled"] is True
        assert refresher.request("/a", "/py", {}, "s-0000003", None) == {
            "scheduled": False, "reason": "busy: too many sessions waiting"}
        refresher.close()
        assert refresher.request("/a", "/py", {}, "s-0000001", None)["scheduled"] is False

    asyncio.run(scenario())
