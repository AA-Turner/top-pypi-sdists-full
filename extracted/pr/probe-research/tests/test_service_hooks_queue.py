"""`hooks.queue`: a hook event's record-keeping routes, run once by the service (plan D36).

What these hold:
  * an event is stored whole and private, once per id (a second send, or one
    already taken, is a duplicate), and refused past MAX_QUEUED;
  * the queue runs its events oldest first, each once (taken before it runs:
    a service stopped mid-run never runs it again), with the event's own
    environment and folder, its harness's root variable included, and only
    the lane's record-keeping routes (`--record-keeping`);
  * an event of a folder that is no complete Probe plugin, or that marks no
    record-keeping route on its lane, is dropped, never run;
  * at start the queue says which service drains it (`drained-by`), and runs
    what waited while no service ran; marks and leftovers are pruned;
  * over the socket: bad params are -32602, a caller in a sandbox is refused,
    queued events hold the service until they ran, `service.status` shows them;
  * the dispatcher and the service agree on every shared constant.
"""

from __future__ import annotations

import asyncio
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

from probe.service import client, hookhosts, hookqueue, paths, protocol
from probe.service.protocol import ErrorCode, Method
from probe.service.registry import Registry
from probe.service.server import Service, _bind
from tests.service_harness import service_home, wait_for  # noqa: F401 -- a fixture

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the service and the hooks are POSIX-only")

AGENT = Path(__file__).resolve().parents[1]
HOOKS = AGENT / "plugins" / "probe-research" / "hooks"

#: Writes `<root var>|<PWD>|<PROBE_TEST_VALUE>|<its stdin's session_id>` to $PROBE_TEST_MARK.
KEEPS = ("/bin/bash -c 'P=\"$(cat)\"; printf \"%s|%s|%s|%s|%s\\n\" \"${PLUGIN_ROOT:-claude:$CLAUDE_PLUGIN_ROOT}\" "
         "\"$PWD\" \"$PROBE_TEST_VALUE\" \"$P\" \"${PROBE_AGENT:-}\" >> \"$PROBE_TEST_MARK\"'")
WAITS = "/bin/bash -c 'cat >/dev/null; echo waits >> \"$PROBE_TEST_MARK\"'"


def _plugin(tmp_path: Path, *, keeps: bool = True, name: str = "probe-research") -> Path:
    root = tmp_path / f"plugin-{len(list(tmp_path.glob('plugin-*')))}"
    hooks = root / "hooks"
    hooks.mkdir(parents=True)
    for file in ("dispatch.py", "dispatch.sh", "zygote.py", "_service_paths.py", "_session_marker.py"):
        shutil.copy2(HOOKS / file, hooks / file)
    kept = {"type": "command", "command": KEEPS}
    if keeps:
        kept["record_keeping"] = True
    routes = {"hooks": {"Stop": [{"lane": "stop", "hooks": [{"type": "command", "command": WAITS}, kept]}]}}
    (hooks / "routes.json").write_text(json.dumps(routes))
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": name}))
    return root


def _item(root: Path, tmp_path: Path, *, event_id: str | None = None, at: float | None = None, **env) -> dict:
    return protocol.need_hook_queue({
        "id": event_id or os.urandom(16).hex(),
        "plugin_root": str(root),
        "lane": "stop",
        "payload": json.dumps({"session_id": env.pop("sid", "s1"), "hook_event_name": "Stop"}),
        "env": {"PATH": os.environ["PATH"], "HOME": os.environ["HOME"], "PROBE_TEST_MARK": str(tmp_path / "mark"),
                "PROBE_TEST_VALUE": "event-env", "CLAUDE_PLUGIN_ROOT": str(root), **env},
        "cwd": str(tmp_path),
        "at": at if at is not None else time.time(),
    })


def _marks(tmp_path: Path) -> list:
    mark = tmp_path / "mark"
    return mark.read_text().splitlines() if mark.exists() else []


@pytest.fixture
def queue(tmp_path):
    made = []

    def make(*, start: bool = True, version: str = "1.2.3") -> hookqueue.HookQueue:
        logs: list = []
        q = hookqueue.HookQueue(logs.append, folder=tmp_path / "queue", version=version)
        q.logs = logs
        if start:
            q.start()
        made.append(q)
        return q

    yield make
    for q in made:
        q.close()


# -- storing -------------------------------------------------------------------------


def test_an_event_is_stored_whole_private_and_once_per_id(tmp_path, queue):
    q = queue(start=False)
    q.folder = paths.private_dir(tmp_path / "queue")
    item = _item(_plugin(tmp_path), tmp_path)
    assert q.store(item) == {"queued": True, "duplicate": False}
    stored = q.folder / f"{item['id']}.json"
    assert stored.stat().st_mode & 0o777 == 0o600
    assert json.loads(stored.read_text()) == item
    assert q.store(item) == {"queued": True, "duplicate": True}
    stored.rename(q.folder / f"{item['id']}.done")
    assert q.store(item) == {"queued": True, "duplicate": True}, "taken already: never again"
    assert not stored.exists()


def test_past_max_queued_it_is_refused(tmp_path, queue, monkeypatch):
    monkeypatch.setattr(hookqueue, "MAX_QUEUED", 2)
    q = queue(start=False)
    q.folder = paths.private_dir(tmp_path / "queue")
    root = _plugin(tmp_path)
    assert q.store(_item(root, tmp_path))["queued"] and q.store(_item(root, tmp_path))["queued"]
    assert "refused" in q.store(_item(root, tmp_path))
    assert q.pending() == 2


def test_with_no_folder_it_is_refused(tmp_path, queue):
    q = queue(start=False)
    q.folder = None
    assert "refused" in q.store(_item(_plugin(tmp_path), tmp_path))


@pytest.mark.parametrize("bad", [
    {"id": "A" * 32}, {"id": "abc"}, {"plugin_root": "relative"}, {"lane": "nope"}, {"payload": {"a": 1}},
    {"env": {"A": 1}}, {"env": {"A=B": "c"}}, {"cwd": "rel"}, {"at": "soon"}, {"at": float("nan")},
    {"payload": "x" * (protocol.MAX_HOOK_QUEUE_ITEM + 1)},
])
def test_bad_params_are_refused(tmp_path, bad):
    good = {"id": "a" * 32, "plugin_root": "/p", "lane": "stop", "payload": "{}", "env": {}, "cwd": "/"}
    with pytest.raises(protocol.RpcError) as caught:
        protocol.need_hook_queue({**good, **bad})
    assert caught.value.code == ErrorCode.INVALID_PARAMS


# -- running ---------------------------------------------------------------------------


def test_what_waited_runs_at_start_oldest_first_once_with_its_own_environment(tmp_path, queue):
    root = _plugin(tmp_path)
    folder = paths.private_dir(tmp_path / "queue")
    first, second = _item(root, tmp_path, sid="first"), _item(root, tmp_path, sid="second")
    for n, item in enumerate((second, first)):  # written newest first...
        path = folder / f"{item['id']}.json"
        path.write_text(json.dumps(item))
        stamp = time.time() - (10 if item is first else 5)  # ...but `first` is older
        os.utime(path, (stamp, stamp))
    q = queue(version="4.5.6")
    assert (folder / paths.HOOK_QUEUE_DRAINER).read_text() == "4.5.6"
    assert wait_for(lambda: len(_marks(tmp_path)) == 2 and q.pending() == 0, 20), q.logs
    real = os.path.realpath(root)
    assert [line.split("|")[0] for line in _marks(tmp_path)] == [f"claude:{real}"] * 2
    assert [json.loads(line.split("|")[3])["session_id"] for line in _marks(tmp_path)] == ["first", "second"]
    assert all(line.split("|")[1:3] == [str(tmp_path), "event-env"] for line in _marks(tmp_path))
    assert "waits" not in _marks(tmp_path), "only the record-keeping routes"
    assert sorted(p.suffix for p in folder.iterdir() if not p.name.startswith(".")) == ["", ".done", ".done"]
    time.sleep(0.3)
    assert len(_marks(tmp_path)) == 2


def test_a_codex_event_runs_with_codex_s_root_variable(tmp_path, queue):
    root = _plugin(tmp_path)
    q = queue()
    q.store(_item(root, tmp_path, PLUGIN_ROOT="/stale/folder"))
    assert wait_for(lambda: _marks(tmp_path), 20), q.logs
    assert _marks(tmp_path)[0].split("|")[0] == os.path.realpath(root)


def test_a_stored_event_runs_and_an_id_sent_again_does_not(tmp_path, queue):
    root = _plugin(tmp_path)
    q = queue()
    item = _item(root, tmp_path)
    assert q.store(item) == {"queued": True, "duplicate": False}
    assert wait_for(lambda: _marks(tmp_path) and q.pending() == 0, 20), q.logs
    assert q.store(item) == {"queued": True, "duplicate": True}
    # And one a dispatcher writes beside it after it ran is dropped, unrun.
    (q.folder / f"{item['id']}.json").write_text(json.dumps(item))
    q._wake.set()
    assert wait_for(lambda: not (q.folder / f"{item['id']}.json").exists(), 10)
    time.sleep(0.3)
    assert len(_marks(tmp_path)) == 1


def test_an_event_taken_before_a_stop_never_runs_again(tmp_path, queue):
    root = _plugin(tmp_path)
    folder = paths.private_dir(tmp_path / "queue")
    item = _item(root, tmp_path)
    (folder / f"{item['id']}.done").write_text("")  # taken by a service that stopped
    (folder / f"{item['id']}.json").write_text(json.dumps(item))
    q = queue()
    assert wait_for(lambda: not (folder / f"{item['id']}.json").exists(), 10)
    time.sleep(0.3)
    assert _marks(tmp_path) == [] and q.pending() == 0


@pytest.mark.parametrize("case", ["not-probe", "no-record-keeping", "gone", "unreadable"])
def test_an_event_that_cannot_run_as_queued_is_dropped(tmp_path, queue, case):
    root = _plugin(tmp_path, keeps=case != "no-record-keeping", name="other" if case == "not-probe" else "probe-research")
    item = _item(root, tmp_path)
    if case == "gone":
        shutil.rmtree(root)
    q = queue()
    if case == "unreadable":
        (q.folder / f"{item['id']}.json").write_text("{not json")
        q._wake.set()
    else:
        q.store(item)
    assert wait_for(lambda: q.pending() == 0 and not list(q.folder.glob("*.json")), 20)
    time.sleep(0.3)
    assert _marks(tmp_path) == [], "dropped, never run (a folder that knows no `--record-keeping` runs every route)"
    assert any("dropped" in line for line in q.logs), q.logs


def test_old_marks_and_leftover_temporary_files_are_pruned(tmp_path, queue):
    folder = paths.private_dir(tmp_path / "queue")
    old, fresh, tmp = folder / f"{'a' * 32}.done", folder / f"{'b' * 32}.done", folder / ".x.1.tmp"
    for path in (old, fresh, tmp):
        path.write_text("")
    stamp = time.time() - hookqueue.TOMBSTONE_S - 5
    os.utime(old, (stamp, stamp))
    os.utime(tmp, (stamp, stamp))
    queue()
    assert wait_for(lambda: not old.exists() and not tmp.exists(), 10)
    assert fresh.exists()


# -- over the socket -------------------------------------------------------------------


@pytest.fixture
def service(service_home):  # noqa: F811 -- the fixture above
    path = paths.ensure_dirs().with_name("hooks-queue-test.sock")
    holder: dict = {}

    def start() -> Path:
        listen = _bind(path)
        svc = Service(registry=Registry(paths.service_dir() / "hooks-queue.json"), discovery_s=0, grace_s=60)
        ready = threading.Event()
        loop = asyncio.new_event_loop()
        thread = threading.Thread(target=lambda: loop.run_until_complete(svc.run(listen, on_ready=ready.set)))
        thread.start()
        assert ready.wait(10)
        holder.update(service=svc, loop=loop, thread=thread)
        return path

    start.holder = holder
    yield start
    if holder:
        holder["loop"].call_soon_threadsafe(holder["service"].stop, "test")
        holder["thread"].join(10)
    path.unlink(missing_ok=True)


def _ask(path: Path, method: str, params: dict) -> dict:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.settimeout(30)
        sock.connect(str(path))
        hello = protocol.request(0, Method.HELLO, {"client": "cli", "client_version": "test", "api": 1})
        sock.sendall(protocol.encode(hello) + protocol.encode(protocol.request(1, method, params)))
        buffer = b""
        while buffer.count(b"\n") < 2:
            chunk = sock.recv(65536)
            if not chunk:
                break
            buffer += chunk
    return [json.loads(line) for line in buffer.splitlines() if line.strip()][1]


def test_over_the_socket_an_event_is_queued_run_and_holds_the_service_till_then(tmp_path, service):
    path = service()
    svc = service.holder["service"]
    root = _plugin(tmp_path)
    item = _item(root, tmp_path)
    item.pop("at")
    answer = _ask(path, Method.HOOKS_QUEUE, item)
    assert answer["result"] == {"queued": True, "duplicate": False}
    assert svc.holds() or _marks(tmp_path), "a queued event holds the service until it ran"
    assert wait_for(lambda: _marks(tmp_path), 20)
    assert wait_for(lambda: svc.hook_queue.pending() == 0, 10)
    assert _ask(path, Method.HOOKS_QUEUE, item)["result"]["duplicate"] is True
    assert _ask(path, Method.STATUS, {})["result"]["hook_queue"] == {"pending": 0}
    assert _ask(path, Method.HOOKS_QUEUE, {**item, "id": "nothex"})["error"]["code"] == ErrorCode.INVALID_PARAMS


def test_a_caller_in_a_sandbox_is_refused(tmp_path, service):
    if not sys.platform.startswith("linux"):
        pytest.skip("no-new-privs is Linux's")
    path = service()
    item = _item(_plugin(tmp_path), tmp_path)
    script = (
        "import ctypes, json, socket, sys\n"
        "assert ctypes.CDLL(None, use_errno=True).prctl(38, 1, 0, 0, 0) == 0\n"  # PR_SET_NO_NEW_PRIVS
        "s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); s.settimeout(10); s.connect(sys.argv[1])\n"
        "hello = {'jsonrpc': '2.0', 'id': 0, 'method': 'service.hello', 'params': {'client': 'cli', 'client_version': 't', 'api': 1}}\n"
        "ask = {'jsonrpc': '2.0', 'id': 1, 'method': 'hooks.queue', 'params': json.loads(sys.argv[2])}\n"
        "s.sendall((json.dumps(hello) + '\\n' + json.dumps(ask) + '\\n').encode())\n"
        "buf = b''\n"
        "while buf.count(b'\\n') < 2:\n"
        "    buf += s.recv(65536)\n"
        "print(buf.splitlines()[1].decode())\n"
    )
    done = subprocess.run([sys.executable, "-c", script, str(path), json.dumps(item)], capture_output=True, text=True,
                          timeout=30)
    assert "refused" in json.loads(done.stdout)["result"], done.stderr
    time.sleep(0.3)
    assert _marks(tmp_path) == []


# -- one contract ----------------------------------------------------------------------


def _dispatch():
    sys.path.insert(0, str(HOOKS))
    try:
        import dispatch
    finally:
        sys.path.pop(0)
    return dispatch


def test_the_dispatcher_and_the_service_agree():
    dispatch = _dispatch()
    assert dispatch.RECORD_KEEPING == hookqueue.RECORD_KEEPING
    assert dispatch.MAX_QUEUED == hookqueue.MAX_QUEUED
    assert dispatch.MAX_QUEUED_BYTES == protocol.MAX_HOOK_QUEUE_ITEM
    assert dispatch.UNHOSTED_LANES == hookhosts.UNHOSTED_LANES == frozenset({"session-end"})
    assert Method.HOOKS_QUEUE == "hooks.queue" and Method.HOOKS_QUEUE in protocol.METHODS
    # One event's item is what hooks.queue takes, as the dispatcher builds it.
    item, data = dispatch.queued_item(str(HOOKS.parent), "post-tool", b'{"tool_name": "Bash", "x": "\xff"}')
    checked = protocol.need_hook_queue(json.loads(data))
    assert checked["payload"].encode("utf-8", "surrogateescape") == b'{"tool_name": "Bash", "x": "\xff"}'
    assert len(checked["id"]) == protocol.HOOK_EVENT_ID_LEN


@pytest.mark.parametrize("case", ["runtime", "fallback", "none"])
def test_the_dispatcher_finds_the_interpreter_client_ensure_starts(tmp_path, case):
    dispatch = _dispatch()
    sys.path.insert(0, str(HOOKS))
    try:
        import _service_paths
    finally:
        sys.path.pop(0)
    python = tmp_path / "python"
    python.write_text("#!/bin/sh\n")
    python.chmod(0o755)
    if case == "runtime":
        paths.ensure_dirs()
        client.write_runtime(str(python), "1.0.0")
    elif case == "fallback":
        fallback = paths.fallback_python()
        fallback.parent.mkdir(parents=True)
        fallback.symlink_to(python)
    assert dispatch.runtime_python(_service_paths) == client.runtime_python()
    assert (client.runtime_python() is None) == (case == "none")


@pytest.mark.parametrize("case", ["idle", "idle-long-ago", "stop", "none", "idle-then-another-started",
                                  "idle-lock-unchanged"])
def test_a_miss_does_not_restart_a_service_that_just_went_idle(tmp_path, monkeypatch, case):
    """A service that exited idle had nothing to keep it: a session whose tap
    never asks it to record (a 0.9.x tap, after an update) only made every hook
    miss start it again, and it quit 20 s later, every minute (live test G).
    Within IDLE_RETRY_S of an idle exit a miss starts none; the session's own
    tap starts one when it has something to record."""
    from probe.service import guard

    dispatch = _dispatch()
    sys.path.insert(0, str(HOOKS))
    try:
        import _service_paths
    finally:
        sys.path.pop(0)
    python = tmp_path / "python"
    python.write_text("#!/bin/sh\necho started >> " + str(tmp_path / "spawned") + "\n")
    python.chmod(0o755)
    paths.ensure_dirs()
    client.write_runtime(str(python), "1.0.0")
    at = {"idle": time.time() - 5, "idle-long-ago": time.time() - getattr(dispatch, "IDLE_RETRY_S", 600) - 5,
          "stop": time.time() - 5}.get(case, time.time() - 5 if case.startswith("idle-") else None)
    if at is not None:
        reason = "stop" if case == "stop" else "idle"
        (paths.service_dir() / guard.LAST_STOP_NAME).write_text(
            json.dumps({"pid": 999999, "start": "111", "reason": reason, "at": at}))
    if case == "idle-then-another-started":
        # A service started since the idle exit (a tap's `tap record`) and then
        # crashed: its lock names it, not the one that went idle.
        paths.lock_path().write_text("424242 222\n")
    elif case == "idle-lock-unchanged":
        paths.lock_path().write_text("999999 111\n")
    monkeypatch.setattr(dispatch, "service_mark", lambda kind: str(tmp_path / f"mark.{kind}"))
    dispatch.ensure_service(_service_paths, lambda: True)
    started = wait_for(lambda: (tmp_path / "spawned").exists(), 2.0)
    assert bool(started) == (case not in ("idle", "idle-lock-unchanged")), case
    # The service's own names for what it writes there.
    assert dispatch.LAST_STOP_NAME == guard.LAST_STOP_NAME and dispatch.IDLE_STOP == protocol.StopReason.IDLE


@pytest.mark.parametrize("idle", [True, False])
def test_a_miss_after_an_idle_exit_runs_its_record_keeping_routes_itself(tmp_path, monkeypatch, idle):
    """No service is coming to drain the queue soon after an idle exit (a miss
    starts none then), so the record-keeping routes run in the hook, never
    left in a queue nobody drains."""
    from probe.service import guard

    dispatch = _dispatch()
    paths.ensure_dirs()
    if idle:
        (paths.service_dir() / guard.LAST_STOP_NAME).write_text(json.dumps({"reason": "idle", "at": time.time()}))
    written = []
    monkeypatch.setattr(dispatch, "queue_folder", lambda sp, any_drainer: str(tmp_path))
    monkeypatch.setattr(dispatch, "write_queued", lambda folder, item, data: written.append(item) or True)
    miss = dispatch.Miss(str(HOOKS.parent), b'{"session_id": "s"}', time.monotonic())
    monkeypatch.setattr(miss, "connect", lambda: dispatch.Miss.DOWN)
    monkeypatch.setattr(miss, "_session_off", lambda: False)
    queued = miss.queue("post-tool", b'{"session_id": "s", "tool_name": "Bash"}', {"session_id": "s"})
    assert queued is (not idle) and bool(written) is (not idle)


def test_the_dispatcher_s_cli_marks_are_the_service_s_paths():
    dispatch = _dispatch()
    home = paths.home()
    assert [home.joinpath(*mark) for mark in dispatch.CLI_MARKS] == [paths.runtime_path(), paths.fallback_python()]
    assert dispatch.cli_here() is False
    paths.ensure_dirs()
    client.write_runtime(sys.executable, "1.0.0")
    assert dispatch.cli_here() is True


# -- review fixes (R1: Claude critic) --------------------------------------------------


def test_an_event_its_dispatcher_wrote_beside_an_unanswered_request_runs_at_once(tmp_path, queue):
    """The dispatcher gave up on `hooks.queue`'s answer and wrote the event
    itself; the late store finds that file: it runs now, not at the next rescan."""
    root = _plugin(tmp_path)
    # Idle means its first pass is over: `pending()` is 0 from `start()` on, so
    # waiting on it let the file below land in the middle of that first pass,
    # and a half-written file was read empty and dropped as unreadable
    # (service-macos, 2 of 4 runs). The dispatcher writes it whole (a
    # temporary file renamed into place), so that drop is the test's alone.
    q = queue(start=False)
    idle = threading.Event()
    q.changed = idle.set  # called by a pass that finds nothing waiting
    q.start()
    assert idle.wait(5), q.logs
    item = _item(root, tmp_path)
    # Beside, as the dispatcher writes it.
    assert _dispatch().write_queued(str(q.folder), item, json.dumps(item).encode())
    started = time.monotonic()
    assert q.store(item) == {"queued": True, "duplicate": True}
    assert q.pending() == 1, "it holds the service until it ran"
    assert wait_for(lambda: _marks(tmp_path), 20), q.logs
    assert time.monotonic() - started < hookqueue.RESCAN_S


def test_a_dispatcher_s_file_written_while_the_service_started_is_found(tmp_path, queue, monkeypatch):
    monkeypatch.setattr(hookqueue, "RESCAN_S", 0.2)
    root = _plugin(tmp_path)
    q = queue()
    assert wait_for(lambda: q.pending() == 0, 5)
    item = _item(root, tmp_path)
    # No store, no wake.
    assert _dispatch().write_queued(str(q.folder), item, json.dumps(item).encode())
    assert wait_for(lambda: _marks(tmp_path), 20), q.logs


def test_what_cannot_be_taken_is_left_alone_never_spun_on_nor_held(tmp_path, queue):
    folder = paths.private_dir(tmp_path / "queue")
    (folder / f"{'c' * 32}.json").mkdir()  # a directory in a file's place
    q = queue()
    time.sleep(0.5)
    assert q.pending() == 0, "nothing it cannot run holds the service"
    before = time.process_time()
    time.sleep(1.0)
    assert time.process_time() - before < 0.3, "the runner spins"
    assert any("not a file" in line for line in q.logs)


def test_a_planted_symlink_is_never_followed(tmp_path, queue):
    folder = paths.private_dir(tmp_path / "queue")
    target = tmp_path / "precious"
    target.write_text("keep me")
    (folder / f"{'d' * 32}.json").symlink_to(target)
    q = queue()
    assert wait_for(lambda: not (folder / f"{'d' * 32}.json").is_symlink(), 10)
    time.sleep(0.3)
    assert target.read_text() == "keep me"
    assert q.pending() == 0 and _marks(tmp_path) == []


def test_an_event_that_waited_too_long_is_dropped(tmp_path, queue):
    root = _plugin(tmp_path)
    folder = paths.private_dir(tmp_path / "queue")
    item = _item(root, tmp_path, at=time.time() - hookqueue.EXPIRE_S - 5)
    (folder / f"{item['id']}.json").write_text(json.dumps(item))
    q = queue()
    assert wait_for(lambda: (folder / f"{item['id']}.done").exists(), 10)
    time.sleep(0.3)
    assert _marks(tmp_path) == []
    assert any("waited past" in line for line in q.logs), q.logs


def test_only_what_a_record_keeping_route_reads_of_the_environment_is_kept():
    env = {"HOME": "/h", "PATH": "/p", "PROBE_TOKEN": "probe", "PROBE_INGEST_TOKEN": "x", "CLAUDE_CODE_SESSION_ID": "s",
           "CLAUDE_CODE_OAUTH_TOKEN": "x", "CODEX_THREAD_ID": "t", "XDG_STATE_HOME": "/x", "LC_ALL": "C",
           "HTTPS_PROXY": "p", "ANTHROPIC_API_KEY": "x", "OPENAI_API_KEY": "x", "AWS_SECRET_ACCESS_KEY": "x",
           "GH_TOKEN": "x", "BASH_ENV": "x", "LD_PRELOAD": "x", "PYTHONPATH": "x", "DB_PASSWORD": "x",
           "PROBE_HOOK_DEADLINE": "1", "PROBE_HOOK_HOSTED": "1", "SOMETHING_ELSE": "x"}
    kept = protocol.hook_queue_env(env)
    assert set(kept) == {"HOME", "PATH", "PROBE_TOKEN", "CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID", "XDG_STATE_HOME",
                         "LC_ALL", "HTTPS_PROXY", "PROBE_HOOK_DEADLINE", "PROBE_HOOK_HOSTED"}
    # The dispatcher keeps the same, less what it sets itself.
    dispatch = _dispatch()
    assert dispatch.queue_env(env) == {k: v for k, v in kept.items() if k not in dispatch.OWNED_ENV}
    assert (dispatch.QUEUE_ENV_NAMES, dispatch.QUEUE_ENV_PREFIXES, dispatch.QUEUE_ENV_SECRET,
            dispatch.QUEUE_ENV_CREDENTIAL) == (protocol.HOOK_QUEUE_ENV_NAMES, protocol.HOOK_QUEUE_ENV_PREFIXES,
                                                protocol.HOOK_QUEUE_ENV_SECRET, protocol.HOOK_QUEUE_ENV_CREDENTIAL)
    assert (dispatch.MAX_QUEUED_ENV, dispatch.MAX_QUEUED_PATH) == (protocol.MAX_HOOK_QUEUE_ENV, protocol.MAX_HOOK_PATH)



def test_a_proxy_with_credentials_is_never_stored():
    env = {"HTTPS_PROXY": "http://user:secret@proxy:8080", "http_proxy": "user:secret@proxy:3128",
           "ALL_PROXY": "socks5://u@proxy", "HTTP_PROXY": "http://proxy:8080", "NO_PROXY": "localhost,.internal"}
    kept = protocol.hook_queue_env(env)
    assert kept == {"HTTP_PROXY": "http://proxy:8080", "NO_PROXY": "localhost,.internal"}
    dispatch = _dispatch()
    assert dispatch.queue_env(env) == kept
    assert dispatch.proxy_credentials(env) is True and dispatch.proxy_credentials(kept) is False


class _ServiceFolder:
    """The two paths `idle_recently` asks of `_service_paths`, in a folder of the test's own."""

    def __init__(self, folder: Path):
        self.folder = folder

    def service_dir(self) -> Path:
        return self.folder

    def lock_path(self) -> Path:
        return self.folder / paths.LOCK_NAME


@pytest.mark.parametrize("start", ["123456", "Sat Oct 24 13:52:39 2026"])  # Linux ticks, macOS `ps lstart`
@pytest.mark.parametrize("holder", ["the-idle-one", "another"])
def test_the_idle_record_stands_until_another_service_holds_the_lock(tmp_path, start, holder):
    """The lock keeps `<pid> <start time>` (`server._name_holder`), and on macOS
    the start time is five words: split on every space, it never matched the
    stop record, so every idle exit read as "another service started since"
    there and a miss restarted the service each time. Read as `guard.holder`
    reads it: the pid, then the rest."""
    from probe.service import guard

    dispatch = _dispatch()
    sp = _ServiceFolder(tmp_path)
    (tmp_path / guard.LAST_STOP_NAME).write_text(
        json.dumps({"pid": 4242, "start": start, "reason": dispatch.IDLE_STOP, "at": time.time() - 5}))
    named = f"4242 {start}" if holder == "the-idle-one" else f"5151 {start}"
    sp.lock_path().write_text(named + "\n")
    assert dispatch.idle_recently(sp) is (holder == "the-idle-one")
