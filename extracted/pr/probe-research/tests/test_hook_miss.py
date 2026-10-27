"""An event no warm host takes: the dispatcher's miss (plan D35, D36).

What these hold, through the real `dispatch.sh`:
  * on a miss only what the agent waits on runs here (a decision, context, a
    message); the record-keeping routes (routes.json `"record_keeping": true`)
    go to the Probe service, which runs them once, by the event's id, with the
    event's own environment and folder (`hooks.queue`);
  * with no service answering they are written straight into its queue, but
    only when the service the CLI starts next drains it (its `drained-by`
    stamp); that service, started by the miss itself (the CLI's own
    `client.ensure`, detached, at most every ENSURE_EVERY_S), runs them;
  * whatever the service cannot take (an older service, a refusal, a full
    queue, an event too big, a session set off, no CLI at all) runs here, as
    before; a session set off never starts the service;
  * an unanswered `hooks.queue` is written beside it, and the one id runs once;
  * the miss asks for the folder's warm host only once it reached a service.
"""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from probe import __version__
from probe.service import client, hookqueue, paths, protocol
from tests.service_harness import service_home, wait_for  # noqa: F401 -- a fixture

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the hooks and the service are POSIX-only")

AGENT = Path(__file__).resolve().parents[1]
HOOKS = AGENT / "plugins" / "probe-research" / "hooks"
SID = "0199f0a2-6b1c-7d3e-8f40-5a6b7c8d9e10"
CONTEXT = {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "waited on"}}
#: A route the agent waits on: its context.
WAITS = {"type": "command", "command": "/bin/bash -c 'cat >/dev/null; echo \"$X_CONTEXT\"'", "timeout": 5}
#: A record-keeping route: it writes what it was given where PROBE_TEST_MARK says, and
#: where it ran: here (`||`), in a host (`1|`), in the service's fresh dispatcher (`|off`).
KEEPS = {
    "type": "command",
    "command": "/bin/bash -c 'cat > \"$PROBE_TEST_MARK.payload\"; printf \"%s|%s|%s|%s\\n\" \"$PROBE_TEST_VALUE\" \"$PWD\" \"${PROBE_HOOK_HOSTED:-}\" \"${PROBE_HOOK_HOST:-}\" >> \"$PROBE_TEST_MARK\"'",
    "timeout": 5,
    "record_keeping": True,
}
ROUTES = {"hooks": {"UserPromptSubmit": [{"lane": "prompt", "hooks": [WAITS, KEEPS]}]}}
#: For a test whose stand-in service ANSWERS `hooks.queue`: the dispatcher's
#: wait for it (`dispatch.QUEUE_WAIT_ENV`), long enough that a loaded runner
#: scheduling the stand-in's thread late never turns its answer into no answer
#: (agent-ci 3.11: `['service.hello']` only, the event queued instead). The
#: hook still returns the moment the answer comes. Tests of a late or missing
#: answer keep the real 0.3 s.
ANSWERED = {"PROBE_HOOK_QUEUE_WAIT_S": "10"}


def _plugin(tmp_path: Path, routes: dict = ROUTES) -> Path:
    root = tmp_path / "plugin"
    hooks = root / "hooks"
    hooks.mkdir(parents=True)
    for name in ("dispatch.py", "dispatch.sh", "zygote.py", "_service_paths.py", "_session_marker.py"):
        shutil.copy2(HOOKS / name, hooks / name)
    (hooks / "routes.json").write_text(json.dumps(routes))
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": "probe-research"}))
    return root


def _env(tmp_path: Path, root: Path, **extra) -> dict:
    env = {
        "PATH": os.environ["PATH"],
        "HOME": os.environ["HOME"],
        "XDG_STATE_HOME": str(tmp_path / "xdg"),
        "CLAUDE_PLUGIN_ROOT": str(root),
        "X_CONTEXT": json.dumps(CONTEXT),
        "PROBE_TEST_MARK": str(tmp_path / "kept"),
        "PROBE_TEST_VALUE": "from-the-event",
        "PROBE_TELEMETRY": "off",
    }
    env.update(extra)
    return env


def _prompt(root: Path, env: dict, cwd: Path, payload: dict | None = None) -> subprocess.CompletedProcess:
    body = json.dumps(payload or {"session_id": SID, "hook_event_name": "UserPromptSubmit", "prompt": "hi"})
    return subprocess.run(["/bin/bash", str(root / "hooks" / "dispatch.sh"), "prompt"], input=body,
                          capture_output=True, text=True, env=env, cwd=str(cwd), timeout=30)


def _kept(tmp_path: Path) -> list:
    mark = tmp_path / "kept"
    return mark.read_text().splitlines() if mark.exists() else []


def _queued() -> list:
    folder = paths.hook_queue_dir()
    return sorted(folder.glob("*.json")) if folder.is_dir() else []


def _drainer(version: str) -> None:
    """A queue a service of `version` drains, and a CLI of `version` installed."""
    folder = paths.private_dir(paths.hook_queue_dir())
    (folder / paths.HOOK_QUEUE_DRAINER).write_text(version)


def _fake_cli(tmp_path: Path, version: str) -> Path:
    """runtime.json naming a stand-in interpreter that records how it was started."""
    calls = tmp_path / "cli-calls.txt"
    python = tmp_path / "bin" / "fake-python"
    python.parent.mkdir(exist_ok=True)
    python.write_text(f'#!/bin/sh\necho "$*" >> {calls}\n')
    python.chmod(0o755)
    paths.ensure_dirs()
    client.write_runtime(str(python), version)
    return calls


def _no_host_asks(root: Path) -> None:
    """Forget a host ask an earlier test of this folder path made (the mark lives in /tmp)."""
    sys.path.insert(0, str(HOOKS))
    try:
        import dispatch
    finally:
        sys.path.pop(0)
    marker = dispatch.host_socket(str(root))[: -len(".sock")] + ".asked"
    Path(marker).unlink(missing_ok=True)


@pytest.fixture
def work(tmp_path):
    folder = tmp_path / "work"
    folder.mkdir()
    return folder


# -- no service ---------------------------------------------------------------------


def test_with_no_cli_at_all_everything_runs_here_as_before(tmp_path, work):
    root = _plugin(tmp_path)
    _no_host_asks(root)
    result = _prompt(root, _env(tmp_path, root), work)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == CONTEXT
    assert _kept(tmp_path) == [f"from-the-event|{work}||"]
    assert not paths.hook_queue_dir().exists(), "nothing queued where nothing drains it"


def test_with_the_service_down_record_keeping_waits_in_its_queue_and_the_miss_starts_it(tmp_path, work):
    root = _plugin(tmp_path)
    _no_host_asks(root)
    calls = _fake_cli(tmp_path, "9.9.9")
    _drainer("9.9.9")
    env = _env(tmp_path, root)
    result = _prompt(root, env, work)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == CONTEXT, "what the agent waits on still runs here"
    assert _kept(tmp_path) == [], "the record-keeping route waits for the service"
    [queued] = _queued()
    assert queued.stat().st_mode & 0o777 == 0o600
    item = json.loads(queued.read_text())
    assert queued.name == f"{item['id']}.json" and len(item["id"]) == 32
    assert item["lane"] == "prompt" and item["plugin_root"] == os.path.realpath(root)
    assert item["cwd"] == str(work) and item["env"]["PROBE_TEST_VALUE"] == "from-the-event"
    assert json.loads(item["payload"])["session_id"] == SID
    assert not {"PROBE_HOOK_HOST", "PROBE_HOOK_HOSTED", "PROBE_HOOK_DEADLINE"} & set(item["env"])
    # The CLI's own client starts the service, detached: once, however many misses.
    assert wait_for(lambda: calls.exists() and calls.read_text().strip(), 5)
    # A miss right after it (DOWN_RETRY_S) does not look for the service
    # again: it runs everything here, as before, and starts nothing.
    assert _prompt(root, env, work).returncode == 0
    time.sleep(0.3)
    assert calls.read_text().splitlines() == ["-I -m probe.service.client ensure"]
    assert len(_queued()) == 1 and _kept(tmp_path) == [f"from-the-event|{work}||"]


def test_no_secret_of_the_session_reaches_the_queue(tmp_path, work):
    root = _plugin(tmp_path)
    _no_host_asks(root)
    _fake_cli(tmp_path, "9.9.9")
    _drainer("9.9.9")
    secrets = {"ANTHROPIC_API_KEY": "sk-x", "GITHUB_TOKEN": "g", "CLAUDE_CODE_OAUTH_TOKEN": "o", "AWS_SECRET_ACCESS_KEY": "a",
               "PROBE_INGEST_TOKEN": "i", "BASH_ENV": "/evil", "LD_PRELOAD": "/evil.so", "PYTHONPATH": "/evil",
               "SOME_PASSWORD": "p"}
    kept = {"PROBE_TOKEN": "probe's own", "CLAUDE_CODE_SESSION_ID": "s", "HTTPS_PROXY": "http://proxy", "LANG": "C.UTF-8"}
    assert _prompt(root, _env(tmp_path, root, **secrets, **kept), work).returncode == 0
    [queued] = _queued()
    env = json.loads(queued.read_text())["env"]
    assert not set(secrets) & set(env), sorted(set(secrets) & set(env))
    assert {k: env.get(k) for k in kept} == kept


def test_a_queue_another_cli_version_drains_is_not_written_but_the_service_is_still_started(tmp_path, work):
    root = _plugin(tmp_path)
    _no_host_asks(root)
    calls = _fake_cli(tmp_path, "9.9.9")
    _drainer("9.9.8")  # the service that made it is older than the CLI that starts next
    result = _prompt(root, _env(tmp_path, root), work)
    assert result.returncode == 0 and json.loads(result.stdout) == CONTEXT
    assert _kept(tmp_path) == [f"from-the-event|{work}||"] and _queued() == []
    assert wait_for(lambda: calls.exists() and "ensure" in calls.read_text(), 5)


def test_a_session_set_off_never_starts_the_service_and_queues_nothing(tmp_path, work):
    root = _plugin(tmp_path)
    _no_host_asks(root)
    calls = _fake_cli(tmp_path, "9.9.9")
    _drainer("9.9.9")
    result = _prompt(root, _env(tmp_path, root, PROBE_SESSION_STATE="off"), work)
    assert result.returncode == 0 and json.loads(result.stdout) == CONTEXT
    assert _kept(tmp_path) == [f"from-the-event|{work}||"] and _queued() == []
    time.sleep(0.3)
    assert not calls.exists(), "a Probe-off session never starts the service"


def test_a_full_queue_or_an_event_too_big_runs_here(tmp_path, work):
    root = _plugin(tmp_path)
    _no_host_asks(root)
    _fake_cli(tmp_path, "9.9.9")
    _drainer("9.9.9")
    big = {"session_id": SID, "hook_event_name": "UserPromptSubmit", "prompt": "x" * 300_000}
    assert _prompt(root, _env(tmp_path, root), work, big).returncode == 0
    assert len(_kept(tmp_path)) == 1 and _queued() == []
    folder = paths.hook_queue_dir()
    for n in range(hookqueue.MAX_QUEUED):
        (folder / f"{n:032x}.json").write_text("{}")
    assert _prompt(root, _env(tmp_path, root), work).returncode == 0
    assert len(_kept(tmp_path)) == 2 and len(_queued()) == hookqueue.MAX_QUEUED


def test_hosting_off_runs_everything_here(tmp_path, work):
    root = _plugin(tmp_path)
    _no_host_asks(root)
    calls = _fake_cli(tmp_path, "9.9.9")
    _drainer("9.9.9")
    result = _prompt(root, _env(tmp_path, root, PROBE_HOOK_HOST="off"), work)
    assert result.returncode == 0 and json.loads(result.stdout) == CONTEXT
    assert len(_kept(tmp_path)) == 1 and _queued() == []
    time.sleep(0.3)
    assert not calls.exists()


# -- a service that answers ------------------------------------------------------------


class StandIn:
    """A stand-in service on this HOME's socket: answers `hooks.queue` as told
    (a result, "error", or None: never), `delay` seconds late, and records
    every request."""

    def __init__(self, answer, delay: float = 0.0) -> None:
        self.answer = answer
        self.delay = delay
        #: Called with each `hooks.queue` request's params, before any answer.
        self.on_queue = None
        self.requests: list = []
        path = paths.ensure_dirs()
        path.unlink(missing_ok=True)
        self.path = path
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.bind(str(path))
        self.server.listen(8)
        self.server.settimeout(0.2)
        self.stop = False
        self.thread = threading.Thread(target=self._serve, daemon=True)
        self.thread.start()

    def _serve(self) -> None:
        while not self.stop:
            try:
                conn, _ = self.server.accept()
            except OSError:
                continue
            threading.Thread(target=self._talk, args=(conn,), daemon=True).start()

    def _talk(self, conn) -> None:
        buffer = b""
        conn.settimeout(5)
        try:
            while True:
                chunk = conn.recv(65536)
                if not chunk:
                    return
                buffer += chunk
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    request = json.loads(line)
                    self.requests.append(request)
                    method = request["method"]
                    if method == "service.hello":
                        reply = {"jsonrpc": "2.0", "id": request["id"], "result": {"api": 1}}
                    elif method == "hooks.queue":
                        if self.on_queue is not None:
                            self.on_queue(request["params"])
                        answer = self.answer
                        if answer is None:
                            continue
                        time.sleep(self.delay)
                        reply = ({"jsonrpc": "2.0", "id": request["id"], "error": {"code": -32601, "message": "unknown"}}
                                 if answer == "error" else {"jsonrpc": "2.0", "id": request["id"], "result": answer})
                    else:
                        continue
                    conn.sendall(json.dumps(reply).encode() + b"\n")
        except OSError:
            return
        finally:
            conn.close()

    def methods(self) -> list:
        return [r["method"] for r in self.requests]

    def close(self) -> None:
        self.stop = True
        self.server.close()
        self.thread.join(2)
        self.path.unlink(missing_ok=True)


@pytest.fixture
def stand_in():
    made = []

    def start(answer, delay: float = 0.0):
        made.append(StandIn(answer, delay))
        return made[-1]

    yield start
    for one in made:
        one.close()


def test_a_service_that_takes_them_runs_them_and_is_asked_for_a_host(tmp_path, work, stand_in):
    root = _plugin(tmp_path)
    _no_host_asks(root)
    calls = _fake_cli(tmp_path, "9.9.9")
    service = stand_in({"queued": True, "duplicate": False})
    result = _prompt(root, _env(tmp_path, root, **ANSWERED), work)
    assert result.returncode == 0 and json.loads(result.stdout) == CONTEXT
    assert _kept(tmp_path) == []
    assert wait_for(lambda: "hooks.host" in service.methods(), 5)
    assert service.methods() == ["service.hello", "hooks.queue", "hooks.host"]
    [queued] = [r["params"] for r in service.requests if r["method"] == "hooks.queue"]
    assert queued["env"]["PROBE_TEST_VALUE"] == "from-the-event" and queued["cwd"] == str(work)
    host = [r["params"] for r in service.requests if r["method"] == "hooks.host"][0]
    assert host["root"] == os.path.realpath(root)
    # The ask is marked once made: the next miss within ASK_EVERY_S does not ask again.
    assert _prompt(root, _env(tmp_path, root, **ANSWERED), work).returncode == 0
    time.sleep(0.2)
    assert service.methods().count("hooks.host") == 1
    assert not calls.exists(), "a service answered: nothing to start"


@pytest.mark.parametrize("answer", ["error", {"refused": "the hook queue is full"}])
def test_an_older_service_or_a_refusal_runs_them_here(tmp_path, work, stand_in, answer):
    root = _plugin(tmp_path)
    _no_host_asks(root)
    _fake_cli(tmp_path, __version__)
    _drainer(__version__)
    service = stand_in(answer)
    result = _prompt(root, _env(tmp_path, root, **ANSWERED), work)
    assert result.returncode == 0 and json.loads(result.stdout) == CONTEXT
    assert "hooks.queue" in service.methods()
    assert _kept(tmp_path) == [f"from-the-event|{work}||"] and _queued() == []


def test_with_no_cli_a_miss_asks_nothing_of_a_service(tmp_path, work, stand_in):
    """No CLI, no service of this machine's to ask (the socket here is a
    stand-in's): a plugin-only machine pays two stats per miss, nothing more."""
    root = _plugin(tmp_path)
    _no_host_asks(root)
    service = stand_in({"queued": True, "duplicate": False})
    result = _prompt(root, _env(tmp_path, root), work)
    assert result.returncode == 0 and json.loads(result.stdout) == CONTEXT
    assert _kept(tmp_path) == [f"from-the-event|{work}||"]
    time.sleep(0.2)
    assert service.requests == []


def test_an_unanswered_queue_request_is_written_beside_it(tmp_path, work, stand_in):
    root = _plugin(tmp_path)
    _no_host_asks(root)
    _fake_cli(tmp_path, "9.9.9")
    _drainer("another version: a running service took the request")
    service = stand_in(None)
    started = time.monotonic()
    result = _prompt(root, _env(tmp_path, root), work)
    assert result.returncode == 0 and json.loads(result.stdout) == CONTEXT
    assert time.monotonic() - started < 3
    assert _kept(tmp_path) == []
    [queued] = _queued()
    sent = [r["params"] for r in service.requests if r["method"] == "hooks.queue"][0]
    assert queued.name == f"{sent['id']}.json", "the same id: it runs once"


# -- the real service -------------------------------------------------------------------


def test_the_service_runs_the_queued_routes_once_with_the_events_own_environment(tmp_path, work, service_home):  # noqa: F811
    root = _plugin(tmp_path)
    _no_host_asks(root)
    service_home.start()
    result = _prompt(root, _env(tmp_path, root), work)
    assert result.returncode == 0 and json.loads(result.stdout) == CONTEXT
    assert wait_for(lambda: _kept(tmp_path), 20), service_home.log()
    assert _kept(tmp_path) == [f"from-the-event|{work}||off"], "run by the service, not here"
    assert json.loads((tmp_path / "kept.payload").read_text())["prompt"] == "hi"
    taken = list(paths.hook_queue_dir().glob("*.done"))
    assert len(taken) == 1 and taken[0].stat().st_size == 0
    assert wait_for(lambda: (service_home.status() or {}).get("hook_queue") == {"pending": 0}, 10)
    # The miss asked for the folder's host; the next miss-free event is hosted,
    # and its record-keeping route runs there with the rest.
    sys.path.insert(0, str(HOOKS))
    try:
        import dispatch
    finally:
        sys.path.pop(0)
    assert wait_for(lambda: os.path.exists(dispatch.host_socket(str(root))), 20), service_home.log()
    assert _prompt(root, _env(tmp_path, root), work).returncode == 0
    assert wait_for(lambda: len(_kept(tmp_path)) == 2, 10)
    assert _kept(tmp_path)[1] == f"from-the-event|{work}|1|"
    time.sleep(0.5)
    assert len(_kept(tmp_path)) == 2, "each event's routes ran once"


def test_what_waited_while_no_service_ran_runs_when_the_miss_starts_one(tmp_path, work, service_home):  # noqa: F811
    root = _plugin(tmp_path)
    _no_host_asks(root)
    status = service_home.start()  # a service of this CLI made the queue and stamped it
    service_home.call("service.stop")
    assert service_home.wait_exit(status["pid"], 10)
    assert (paths.hook_queue_dir() / paths.HOOK_QUEUE_DRAINER).read_text() == __version__
    client.write_runtime(sys.executable, __version__)  # the CLI that starts next is that one
    result = _prompt(root, _env(tmp_path, root), work)
    assert result.returncode == 0 and json.loads(result.stdout) == CONTEXT
    assert wait_for(lambda: _kept(tmp_path), 30), service_home.log()
    assert _kept(tmp_path) == [f"from-the-event|{work}||off"], "run by the service the miss started"
    assert service_home.status(), "the miss started the service"


# -- review fixes (R2: Codex) ------------------------------------------------------------


def test_a_late_refusal_with_nowhere_to_write_runs_them_here(tmp_path, work, stand_in):
    """An older service's unknown-method answer, past the 300 ms wait, and no
    queue folder to write the event in: neither the service nor the disk took
    it, so it runs here (Codex P2: it was dropped because the request had been
    sent)."""
    root = _plugin(tmp_path)
    _no_host_asks(root)
    _fake_cli(tmp_path, "9.9.9")
    service = stand_in("error", delay=0.6)
    result = _prompt(root, _env(tmp_path, root), work)
    assert result.returncode == 0 and json.loads(result.stdout) == CONTEXT
    assert "hooks.queue" in service.methods()
    assert not paths.hook_queue_dir().exists()
    assert _kept(tmp_path) == [f"from-the-event|{work}||"]


@pytest.mark.parametrize("name", ["HTTPS_PROXY", "http_proxy", "ALL_PROXY"])
def test_an_event_behind_a_proxy_with_credentials_runs_here_and_is_never_stored(tmp_path, work, name):
    """A proxy URL carrying a user and password is a credential: it never
    reaches a queue file, and its event, which needs the proxy, runs here."""
    root = _plugin(tmp_path)
    _no_host_asks(root)
    _fake_cli(tmp_path, "9.9.9")
    _drainer("9.9.9")
    env = _env(tmp_path, root, **{name: "http://user:password@proxy.example:8080"})
    result = _prompt(root, env, work)
    assert result.returncode == 0 and json.loads(result.stdout) == CONTEXT
    assert _queued() == []
    assert _kept(tmp_path) == [f"from-the-event|{work}||"]


def test_a_queued_run_never_hands_over_to_another_installed_copy(tmp_path, work):
    """`--record-keeping` is the folder's own: run where it was queued, never
    in the copy the install ledger names (a rollback's older dispatcher knows
    no `--record-keeping` and would run every route, claiming daemon messages
    and audit lines nobody sees). Without the service's own hand-over mark too."""
    cache = tmp_path / "claude" / "plugins" / "cache" / "mkt" / "probe-research"
    new = cache / "0.2.0"
    _plugin(tmp_path)
    shutil.copytree(tmp_path / "plugin", new)
    old = cache / "0.1.0"
    shutil.copytree(tmp_path / "plugin", old)
    ran_old = tmp_path / "old-ran"
    (old / "hooks" / "dispatch.py").write_text(
        f"import sys\n\ndef run(argv):\n    open({str(ran_old)!r}, 'a').write(' '.join(argv) + '\\n')\n    sys.exit(0)\n")
    ledger = tmp_path / "claude" / "plugins" / "installed_plugins.json"
    ledger.write_text(json.dumps({"plugins": {"probe-research@mkt": [{"scope": "user", "installPath": str(old)}]}}))
    env = _env(tmp_path, new, CLAUDE_CONFIG_DIR=str(tmp_path / "claude"), PROBE_HOOK_HOST="off")
    body = json.dumps({"session_id": SID, "hook_event_name": "UserPromptSubmit", "prompt": "hi"})
    # The event itself does hand over (the ledger names 0.1.0): the test's own control.
    subprocess.run(["/bin/bash", str(new / "hooks" / "dispatch.sh"), "prompt"], input=body, capture_output=True,
                   text=True, env=env, cwd=str(work), timeout=30)
    assert ran_old.read_text().split() == ["prompt"]
    queued = subprocess.run(["/bin/bash", str(new / "hooks" / "dispatch.sh"), "prompt", "--record-keeping"],
                            input=body, capture_output=True, text=True, env=env, cwd=str(work), timeout=30)
    assert queued.returncode == 0, queued.stderr
    assert ran_old.read_text().split() == ["prompt"], "the queued run went to the older copy"
    assert _kept(tmp_path) == [f"from-the-event|{work}||off"]
    assert queued.stdout == "", "only the record-keeping route ran"



def _full_queue() -> Path:
    folder = paths.private_dir(paths.hook_queue_dir())
    for n in range(hookqueue.MAX_QUEUED):
        (folder / f"{n:032x}.json").write_text("{}")
    return folder


def test_an_event_run_here_after_an_unanswered_request_is_never_stored_late(tmp_path, work, stand_in):
    """Codex R3 P2: the service's store is slow and the queue is full when the
    hook stops waiting, so the hook runs the routes itself; once room frees,
    the still-pending store must not run the same event again. The hook claims
    the event (`<id>.claim`) before it runs it, and the store honors the claim."""
    root = _plugin(tmp_path)
    _no_host_asks(root)
    _fake_cli(tmp_path, "9.9.9")
    folder = _full_queue()
    service = stand_in(None)  # takes the request, never answers: a slow store
    result = _prompt(root, _env(tmp_path, root), work)
    assert result.returncode == 0 and json.loads(result.stdout) == CONTEXT
    assert _kept(tmp_path) == [f"from-the-event|{work}||"], "the queue was full: it ran here"
    [sent] = [r["params"] for r in service.requests if r["method"] == "hooks.queue"]
    for path in folder.glob("0*.json"):
        path.unlink()  # room again
    late = hookqueue.HookQueue(lambda message: None, folder=folder)
    answer = late.store(protocol.need_hook_queue(sent))
    assert "refused" in answer, answer
    assert not (folder / f"{sent['id']}.json").exists(), "stored late: it would run twice"


def test_an_event_no_claim_could_be_made_for_is_never_run_here_too(tmp_path, work, stand_in):
    """#3300 review: the queue is full and the claim cannot be made (here a
    folder the hook cannot write; a full disk alike): running it here without
    a claim could run it twice once a late store gets room. At most once: it
    is left to the service."""
    root = _plugin(tmp_path)
    _no_host_asks(root)
    _fake_cli(tmp_path, "9.9.9")
    folder = _full_queue()
    service = stand_in(None)
    folder.chmod(0o500)
    try:
        result = _prompt(root, _env(tmp_path, root), work)
    finally:
        folder.chmod(0o700)
    assert result.returncode == 0 and json.loads(result.stdout) == CONTEXT, "what the agent waits on still ran"
    assert _kept(tmp_path) == [], "no claim: never run here as well"
    assert [r for r in service.requests if r["method"] == "hooks.queue"], "it was offered to the service"


def test_an_event_the_service_claimed_first_is_never_run_here(tmp_path, work, stand_in):
    """The other order: the slow store claimed the event before the hook
    stopped waiting (so it will run there), and the queue is full: the hook
    leaves it to the service instead of running it too."""
    root = _plugin(tmp_path)
    _no_host_asks(root)
    _fake_cli(tmp_path, "9.9.9")
    folder = _full_queue()
    service = stand_in(None)
    service.on_queue = lambda params: (folder / f"{params['id']}.claim").write_text("")
    result = _prompt(root, _env(tmp_path, root), work)
    assert result.returncode == 0 and json.loads(result.stdout) == CONTEXT
    assert _kept(tmp_path) == [], "the service holds it: never here too"


# -- the lifeboat at a session's start (plan fool-proof-updates B4) -------------------

#: A SessionStart route the agent waits on: nothing to say.
QUIET = {"type": "command", "command": "/bin/bash -c 'cat >/dev/null'", "timeout": 5}
SESSION_ROUTES = {"hooks": {"SessionStart": [{"lane": "session-start", "hooks": [QUIET]}],
                            "UserPromptSubmit": [{"lane": "prompt", "hooks": [WAITS]}]}}


def _start(root: Path, env: dict, cwd: Path) -> subprocess.CompletedProcess:
    body = json.dumps({"session_id": SID, "hook_event_name": "SessionStart", "source": "startup"})
    return subprocess.run(["/bin/bash", str(root / "hooks" / "dispatch.sh"), "session-start"], input=body,
                          capture_output=True, text=True, env=env, cwd=str(cwd), timeout=30)


def _fake_lifeboat(tmp_path: Path) -> Path:
    """The lifeboat's folder with a wrapper that records how it was started."""
    from probe.service import lifeboat

    folder = paths.private_dir(lifeboat.root())
    mark = tmp_path / "lifeboat-ran"
    wrapper = lifeboat.wrapper_path()
    wrapper.write_text(f'#!/bin/sh\necho "$* $PPID" >> {mark}\n')
    assert folder == Path(os.environ["HOME"]) / ".local" / "state" / "probe" / "lifeboat"
    return mark


def _dispatch():
    sys.path.insert(0, str(HOOKS))
    try:
        import dispatch
    finally:
        sys.path.pop(0)
    return dispatch


def _ran(mark: Path) -> list:
    return [line.split()[0] for line in mark.read_text().splitlines()] if mark.exists() else []


def test_a_session_start_with_no_keeper_runs_the_lifeboat_detached_at_most_hourly(tmp_path, work):
    """A pod with no user scheduler: no keeper unit runs the lifeboat, so a
    session's start does, whatever state the CLI is in."""
    root = _plugin(tmp_path, SESSION_ROUTES)
    mark = _fake_lifeboat(tmp_path)
    env = _env(tmp_path, root)
    assert _start(root, env, work).returncode == 0
    assert wait_for(lambda: _ran(mark) == ["session"], 5), "`/bin/sh lifeboat.sh session`"
    assert _start(root, env, work).returncode == 0
    assert _prompt(root, env, work).returncode == 0
    time.sleep(0.5)
    assert _ran(mark) == ["session"], "once an hour, and only at a session's start"
    stamp = Path(os.environ["HOME"]) / ".local" / "state" / "probe" / "lifeboat" / "session.stamp"
    then = time.time() - 3601
    os.utime(stamp, (then, then))
    assert _start(root, env, work).returncode == 0
    assert wait_for(lambda: _ran(mark) == ["session", "session"], 5)


def test_a_keeper_unit_and_a_service_that_answered_leave_it_to_the_keeper(tmp_path):
    dispatch = _dispatch()
    mark = _fake_lifeboat(tmp_path)
    timer = Path(os.environ["HOME"]) / ".config" / "systemd" / "user" / "probe-service-keeper.timer"
    timer.parent.mkdir(parents=True)
    timer.write_text("[Timer]\n")
    assert dispatch.keeper_installed()
    assert dispatch.launch_lifeboat(answered=True) is False
    assert dispatch.launch_lifeboat(answered=False) is True, "the keeper may not be running: the service is not"
    assert wait_for(lambda: _ran(mark) == ["session"], 5)


def test_a_lifeboat_that_is_missing_or_not_private_is_never_run_and_the_hook_goes_on(tmp_path, work):
    dispatch = _dispatch()
    root = _plugin(tmp_path, SESSION_ROUTES)
    assert _start(root, _env(tmp_path, root), work).returncode == 0
    assert dispatch.launch_lifeboat(answered=False) is False, "none installed"
    mark = _fake_lifeboat(tmp_path)
    folder = Path(os.environ["HOME"]) / ".local" / "state" / "probe" / "lifeboat"
    folder.chmod(0o777)
    try:
        assert dispatch.launch_lifeboat(answered=False) is False, "a folder others can write is not ours to run"
    finally:
        folder.chmod(0o700)
    time.sleep(0.3)
    assert _ran(mark) == []


@pytest.mark.parametrize("value, wait", [(None, 0.3), ("10", 10.0), ("junk", 0.3), ("0", 0.3), ("-2", 0.3)])
def test_the_queue_wait_is_the_real_one_unless_a_test_says_otherwise(monkeypatch, value, wait):
    dispatch = _dispatch()
    if value is None:
        monkeypatch.delenv(dispatch.QUEUE_WAIT_ENV, raising=False)
    else:
        monkeypatch.setenv(dispatch.QUEUE_WAIT_ENV, value)
    assert dispatch.QUEUE_WAIT_S == 0.3 and dispatch.queue_wait_s() == wait


def test_the_dispatcher_names_what_the_service_writes():
    """It imports nothing of Probe, so the lifeboat's and the keeper's paths are spelled twice."""
    from probe.service import keeper, lifeboat

    dispatch = _dispatch()
    home = Path(os.environ["HOME"])
    assert home.joinpath(*dispatch.LIFEBOAT_DIR) == lifeboat.root()
    assert dispatch.LIFEBOAT_WRAPPER == lifeboat.WRAPPER_NAME
    assert dispatch.KEEPER_TIMER[-1] == f"{keeper.NAME}.timer"
    assert home.joinpath(*dispatch.KEEPER_PLIST) == keeper._plist_path()  # noqa: SLF001
