"""A training process's background work on the Probe service (plan Q5).

The SDK forks detached processes beside a training loop (the outbox's
drainer, the box watcher) and POSTs telemetry from a thread. With a service
running it hands each to the service instead; without one it does what it
always did. What these hold:

  * hand-off: `outbox_worker.maybe_spawn` gives the drain to a running service,
    whose child (this interpreter, the stored login) delivers every op in
    order with no fork here; `box.spawn.maybe_spawn` the watcher; the
    telemetry sender a batch;
  * fallback: no service, an older one (no such method), a refusal (a caller
    in a sandbox, a folder failing at its start), an environment credential,
    a credential queue: the SDK forks or POSTs as before;
  * never blocking: a service that does not answer costs one budget, then
    is not asked again for a while;
  * a service stopped mid-drain leaves its child delivering: nothing lost or
    sent twice, and the next service takes the next drain;
  * two processes on one outbox: one drainer at a time, every op once;
  * the service side never takes a credential in a child's environment.
"""

from __future__ import annotations

import contextlib
import json
import os
import signal
import socket
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from probe.box import spawn as box_spawn
from probe.sdk import outbox_worker, service_handoff
from probe.sdk.journal import CREDENTIAL_NAMESPACE, Journal
from probe.service import background, client, paths, protocol
from probe.service.protocol import BackgroundRefusal, BackgroundState, ErrorCode, Method
from tests.service_harness import pid_running, service_home, wait_for  # noqa: F401 -- a fixture

#: What a caller's wait may run past its handoff budget (thread start, the
#: socket's folder check). macos-14 runners overran 0.1 s by 14-49 ms in four
#: agent-ci runs (2026-10-23). The bugs these bounds catch cost far more: an
#: unbudgeted key wait plus folder check is 0.59 s, a hung home mount 5 s.
SLACK_S = 0.25

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the service is POSIX-only")

TOKEN = "probe_pat_q5_stored_login"


@pytest.fixture(autouse=True)
def _fresh_backoffs():
    service_handoff.reset(wait=6.0)  # no request thread of an earlier test still out
    yield
    service_handoff.reset(wait=6.0)


# -- a loopback API that counts what arrives, and how many at once -------------


class _Api(BaseHTTPRequestHandler):
    def _respond(self, status: int, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        server = self.server
        with server.lock:
            server.inflight += 1
            server.max_inflight = max(server.max_inflight, server.inflight)
        try:
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b""
            with server.lock:
                server.arrived += 1
            server.gate.wait(60)  # a test holds the API here while it stops the service
            if server.delay:
                time.sleep(server.delay)
            with server.lock:
                server.records.append((self.path, json.loads(raw) if raw else None, self.headers.get("Authorization")))
            self._respond(200, b"{}")
        finally:
            with server.lock:
                server.inflight -= 1

    def do_GET(self) -> None:  # noqa: N802
        self._respond(200, b'{"id": "r-q5", "tags": []}')

    def log_message(self, *args) -> None:
        pass


@pytest.fixture
def api():
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Api)
    server.daemon_threads = True
    server.records, server.lock = [], threading.Lock()
    server.inflight = server.max_inflight = server.arrived = 0
    server.delay = 0.0
    server.gate = threading.Event()
    server.gate.set()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    server.url = f"http://127.0.0.1:{server.server_port}"
    try:
        yield server
    finally:
        server.gate.set()
        server.shutdown()
        server.server_close()


def _children_of(home: Path) -> list[int]:
    """Live drainer / watcher processes whose HOME is `home` (Linux /proc)."""
    found = []
    proc = Path("/proc")
    if not proc.is_dir():
        return found
    for entry in proc.iterdir():
        if not entry.name.isdigit():
            continue
        try:
            argv = (entry / "cmdline").read_bytes().split(b"\0")
            env = (entry / "environ").read_bytes().split(b"\0")
        except OSError:
            continue
        if (b"probe.sdk.outbox_worker" in argv or b"probe.box" in argv) and f"HOME={home}".encode() in env:
            found.append(int(entry.name))
    return found


@pytest.fixture
def service(service_home, monkeypatch):
    """A real service; a generous hand-off budget (what these tests check is
    where the work goes, not a loaded runner's timing: the budget's own test
    is below); and no drainer or watcher left behind, whatever happened."""
    monkeypatch.setattr(client, "HANDOFF_BUDGET_S", 10.0)
    try:
        yield service_home
    finally:
        for pid in _children_of(service_home.home):
            with contextlib.suppress(OSError):
                os.kill(pid, signal.SIGKILL)


def _received(server) -> list:
    with server.lock:
        return list(server.records)


@pytest.fixture
def stored_login(monkeypatch, tmp_path, api):
    """This machine's CLI config holds the login (no credential in the
    environment), aimed at the loopback API: what the service's children use."""
    config = tmp_path / "config" / "probe.json"
    config.parent.mkdir(parents=True)
    config.write_text(json.dumps({
        "version": 2, "current_context": "default",
        "contexts": {"default": {"base_url": api.url, "token": TOKEN}},
    }))
    config.chmod(0o600)
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(config))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    _no_credentials(monkeypatch)
    for name in ("PROBE_BASE_URL", "PROBE_OUTBOX_DIR", "PROBE_ASYNC", "PROBE_OUTBOX_WORKER"):
        monkeypatch.delenv(name, raising=False)
    return api.url


def _no_credentials(monkeypatch) -> None:
    """Nothing credential-like in the environment (the suite sets
    PROBE_MCP_VERIFY_TOKEN, a switch, which reads as one and keeps the fork)."""
    for name in [n for n in os.environ if protocol.secret_env(n)]:
        monkeypatch.delenv(name, raising=False)


def _journal(tmp_path, url: str, name: str = "outbox") -> Journal:
    return Journal(tmp_path / name, context={"name": None, "base_url": url})


def _steps(server) -> list:
    return [p["step_index"] for path, body, _ in _received(server) if path.endswith("/metrics") for p in body["points"]]


class _NoFork:
    """Stands in for `subprocess.Popen` where the SDK must NOT fork."""

    calls = 0

    def __init__(self, *args, **kwargs) -> None:
        type(self).calls += 1
        raise AssertionError("the SDK forked its own drainer although the service took it")


def _no_fork_in(monkeypatch, module, popen) -> None:
    """`module`'s own `subprocess.Popen` (and only its: the harness still
    starts real services) becomes `popen`."""
    import types

    monkeypatch.setattr(module, "subprocess", types.SimpleNamespace(
        Popen=popen, DEVNULL=subprocess.DEVNULL, PIPE=subprocess.PIPE))


class _FakeChild:
    """A forked drainer that is (for `_spawn_took`) alive."""

    def __init__(self, argv, **kwargs) -> None:
        self.argv = argv
        self.returncode = None
        _FakeChild.made.append(argv)

    def poll(self):
        return None


@pytest.fixture
def fake_fork(monkeypatch):
    _FakeChild.made = []
    _no_fork_in(monkeypatch, outbox_worker, _FakeChild)
    return _FakeChild.made


# -- what crosses the socket ---------------------------------------------------


def test_the_childs_environment_never_carries_a_credential(monkeypatch):
    for name, value in {
        "PROBE_TOKEN": "t", "PROBE_HMAC_SECRET": "s", "PROBE_INGEST_TOKEN": "i", "AWS_SECRET_ACCESS_KEY": "a",
        "PROBE_RUN_ID": "r-1", "PYTHONPATH": "/x", "HTTPS_PROXY": "http://proxy:3128", "LD_LIBRARY_PATH": "/lib",
    }.items():
        monkeypatch.setenv(name, value)
    env = service_handoff.runtime_env()
    assert {"PROBE_RUN_ID", "PYTHONPATH", "HTTPS_PROXY", "LD_LIBRARY_PATH"} <= set(env)
    assert not {"PROBE_TOKEN", "PROBE_HMAC_SECRET", "PROBE_INGEST_TOKEN", "AWS_SECRET_ACCESS_KEY", "HOME"} & set(env)
    assert service_handoff.env_credential() is True


@pytest.mark.parametrize("name", ["PROBE_TOKEN", "PROBE_SERVICE_TOKEN", "PROBE_HMAC_SECRET", "AWS_ACCESS_KEY_ID", "HOME"])
def test_the_service_refuses_any_other_variable(name):
    with pytest.raises(protocol.RpcError) as raised:
        protocol.need_background({"dir": "/tmp/x", "python": "/usr/bin/python3", "env": {name: "v"}}, directory=True)
    assert raised.value.code == ErrorCode.INVALID_PARAMS


def test_the_service_takes_the_runtime_variables_and_absolute_paths_only():
    ok = protocol.need_background(
        {"dir": "/tmp/x", "python": "/usr/bin/python3", "env": {"PROBE_RUN_ID": "r", "XDG_CONFIG_HOME": "/c"}},
        directory=True,
    )
    assert ok == {
        "dir": "/tmp/x", "python": "/usr/bin/python3", "cwd": None,
        "env": {"PROBE_RUN_ID": "r", "XDG_CONFIG_HOME": "/c"},
    }
    for bad in (
        {"dir": "rel", "python": "/p"}, {"dir": "/d", "python": "python3"}, {"dir": "/d"},
        {"dir": "/d", "python": "/p", "cwd": "rel"},
    ):
        with pytest.raises(protocol.RpcError):
            protocol.need_background(bad, directory=True)
    with pytest.raises(protocol.RpcError):  # box.watch names its registry
        protocol.need_background({"python": "/p", "env": {}}, directory=False)
    with pytest.raises(protocol.RpcError):
        protocol.need_telemetry({"entries": [{"no": "event"}]})


def test_a_process_holding_a_credential_never_asks_the_service(monkeypatch, tmp_path):
    asked = []
    monkeypatch.setattr(client, "drain_outbox", lambda *a, **k: asked.append(a) or {"accepted": True})
    monkeypatch.setattr(client, "watch_box", lambda *a, **k: asked.append(a) or {"accepted": True})
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_env")
    assert service_handoff.drain(str(tmp_path)) is None
    assert service_handoff.box_watch(str(tmp_path)) is None
    assert asked == []


def test_a_credential_queue_never_goes_to_the_service(monkeypatch, tmp_path):
    asked = []
    monkeypatch.setattr(service_handoff, "drain", lambda d: asked.append(d) or BackgroundState.STARTED)
    queue = Journal(tmp_path / "outbox" / CREDENTIAL_NAMESPACE / "abcdef0123456789")
    queue._ensure()
    assert outbox_worker._hand_to_service(queue) is None
    inner = Journal(queue.dir / "delivery-v1")  # a folder inside one (its receipts')
    inner._ensure()
    assert outbox_worker._hand_to_service(inner) is None
    assert asked == []


def test_telemetry_behind_a_proxy_is_sent_by_this_process(monkeypatch):
    asked = []
    monkeypatch.setattr(client, "send_telemetry", lambda *a, **k: asked.append(a) or {"accepted": True})
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy:3128")
    assert service_handoff.telemetry([{"event": "e", "distinct_id": "d", "properties": {}}]) is False
    assert asked == []


def test_the_telemetry_sender_posts_itself_only_when_the_service_did_not_take_it(monkeypatch):
    from probe._shared import telemetry

    posted = []
    monkeypatch.setattr(telemetry.core, "post_batch", lambda entries, **kw: posted.append(entries))
    monkeypatch.setattr(service_handoff, "telemetry", lambda entries: True)
    telemetry._post_batch([{"event": "a"}])
    assert posted == []
    monkeypatch.setattr(service_handoff, "telemetry", lambda entries: False)
    telemetry._post_batch([{"event": "b"}])
    ((only,),) = posted
    assert only["event"] == "b" and len(only["uuid"]) == 36, "stamped: a copy the service sent too collapses"


def test_the_box_spawner_hands_off_and_falls_back(monkeypatch, tmp_path):
    monkeypatch.setenv("PROBE_BOX", "1")
    forks = []
    _no_fork_in(monkeypatch, box_spawn, lambda argv, **kw: forks.append(argv))
    monkeypatch.setattr(service_handoff, "box_watch", lambda directory=None: BackgroundState.STARTED)
    assert box_spawn.maybe_spawn(tmp_path / "box") is True
    monkeypatch.setattr(service_handoff, "box_watch", lambda directory=None: BackgroundState.RUNNING)
    assert box_spawn.maybe_spawn(tmp_path / "box") is False
    assert forks == []
    monkeypatch.setattr(service_handoff, "box_watch", lambda directory=None: None)
    assert box_spawn.maybe_spawn(tmp_path / "box") is True
    assert forks and forks[0][1:] == ["-m", "probe.box"]


def test_a_running_answer_is_no_spawn_for_the_kick_throttle(tmp_path, fake_fork, monkeypatch):
    """STARTED arms the writer's kick throttle like a fork; RUNNING (a drainer
    at the lease) does not, as when this process finds the lease held."""
    _no_credentials(monkeypatch)
    journal = _journal(tmp_path, "https://api.example")
    journal.append_http("POST", "/v1/runs/r-q5/metrics", {"points": [{"step_index": 1}]})
    monkeypatch.setattr(service_handoff, "drain", lambda d: BackgroundState.STARTED)
    assert outbox_worker.maybe_spawn(str(journal.dir)) is True
    monkeypatch.setattr(service_handoff, "drain", lambda d: BackgroundState.RUNNING)
    assert outbox_worker.maybe_spawn(str(journal.dir)) is False
    assert fake_fork == []


def test_the_leases_the_service_reads_are_the_childrens(tmp_path):
    journal = _journal(tmp_path, "https://api.example")
    journal._ensure()
    assert Path(outbox_worker._lease_path(journal)).name == background.DRAIN_LEASE
    assert box_spawn.lock_path(tmp_path / "box" / "runs") == tmp_path / "box" / background.BOX_LEASE


# -- no service, an older one, a silent one: the old fork, quickly ------------


def test_with_no_service_the_sdk_forks_as_before(tmp_path, fake_fork, monkeypatch):
    _no_credentials(monkeypatch)
    journal = _journal(tmp_path, "https://api.example")
    journal.append_http("POST", "/v1/runs/r-q5/metrics", {"points": [{"step_index": 1}]})
    started = time.monotonic()
    assert outbox_worker.maybe_spawn(str(journal.dir)) is True
    assert time.monotonic() - started < 1.0
    assert len(fake_fork) == 1 and fake_fork[0][1:3] == ["-m", "probe.sdk.outbox_worker"]


class _FakeService:
    """A socket at this machine's service path. Each connection, in turn,
    takes the next of `script` (the last one repeats):

        "older"   hello, then `-32601` (a service from before Q5)
        "silent"  reads the request, never answers (a wedged one)
        "eof"     reads the request, closes the connection unanswered
        a dict    hello, then that result

    `requests` keeps every request's params, in order."""

    def __init__(self, *, silent: bool = False, script: list | None = None) -> None:
        self.script = list(script or (["silent"] if silent else ["older"]))
        self.connections = 0
        self.requests: list = []
        path = paths.ensure_dirs()
        with contextlib.suppress(FileNotFoundError):
            path.unlink()
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(str(path))
        self.sock.listen(8)
        self._held: list = []
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def _serve(self) -> None:
        while True:
            try:
                conn, _ = self.sock.accept()
            except OSError:
                return
            step = self.script[min(self.connections, len(self.script) - 1)]
            self.connections += 1
            self._held.append(conn)
            data = b""
            with contextlib.suppress(OSError):
                conn.settimeout(5)
                while data.count(b"\n") < 2:
                    chunk = conn.recv(65536)
                    if not chunk:
                        break
                    data += chunk
                lines = [json.loads(line) for line in data.splitlines() if line.strip()]
                self.requests += [req.get("params") for req in lines if req.get("method") != Method.HELLO]
                if step == "silent":
                    continue
                if step == "eof":
                    conn.close()
                    continue
                for req in lines:
                    if req["method"] == Method.HELLO:
                        conn.sendall(protocol.encode(protocol.result(req["id"], {"api": 1})))
                    elif step == "older":
                        conn.sendall(protocol.encode(protocol.error(
                            req["id"], protocol.RpcError(ErrorCode.UNKNOWN_METHOD, "unknown method"))))
                    else:
                        conn.sendall(protocol.encode(protocol.result(req["id"], step)))

    def close(self) -> None:
        self.sock.close()
        for conn in self._held:
            with contextlib.suppress(OSError):
                conn.close()


@pytest.fixture
def isolated_home(monkeypatch):
    import shutil
    import tempfile

    home = Path(tempfile.mkdtemp(prefix="pq-", dir="/tmp"))
    monkeypatch.setenv("HOME", str(home))
    yield home
    shutil.rmtree(home, ignore_errors=True)


def test_an_older_service_means_the_old_fork_and_is_not_asked_again(isolated_home, tmp_path, fake_fork, monkeypatch):
    _no_credentials(monkeypatch)
    older = _FakeService(silent=False)
    try:
        journal = _journal(tmp_path, "https://api.example")
        journal.append_http("POST", "/v1/runs/r-q5/metrics", {"points": [{"step_index": 1}]})
        assert outbox_worker.maybe_spawn(str(journal.dir)) is True
        assert len(fake_fork) == 1 and older.connections == 1
        assert outbox_worker.maybe_spawn(str(journal.dir)) is True
        assert len(fake_fork) == 2 and older.connections == 1, "an older service is not asked again at once"
    finally:
        older.close()


def test_a_service_that_does_not_answer_costs_one_budget(isolated_home, tmp_path, monkeypatch):
    _no_credentials(monkeypatch)
    wedged = _FakeService(silent=True)
    try:
        started = time.monotonic()
        assert service_handoff.drain(str(tmp_path)) is None
        first = time.monotonic() - started
        assert first < client.HANDOFF_BUDGET_S + 0.2, f"a silent service held the caller {first:.2f} s"
        started = time.monotonic()
        assert service_handoff.drain(str(tmp_path)) is None
        assert service_handoff.telemetry([{"event": "e"}]) is False
        assert time.monotonic() - started < 0.05 and wedged.connections == 1, "then it is not asked for a while"
    finally:
        wedged.close()


def test_the_budget_covers_the_machine_key_and_the_socket_folder_checks(isolated_home, tmp_path, monkeypatch):
    """Codex P2: the key wait came before the RPC's own budget and
    `Connection.open()` checked the socket's folder outside any timeout (296 ms
    with a 45 ms key and a silent service; 600 ms with a slow folder check).
    One deadline covers all of it now."""
    _no_credentials(monkeypatch)
    wedged = _FakeService(silent=True)
    try:
        real_key, real_check = paths.machine_key, paths.require_private
        monkeypatch.setattr(paths, "_machine_key", None)
        monkeypatch.setattr(paths, "machine_key", lambda: (time.sleep(0.04), real_key())[1])
        monkeypatch.setattr(paths, "require_private", lambda path: (time.sleep(0.3), real_check(path))[1])
        started = time.monotonic()
        assert service_handoff.drain(str(tmp_path)) is None
        elapsed = time.monotonic() - started
        assert elapsed < client.HANDOFF_BUDGET_S + SLACK_S, f"the training thread waited {elapsed:.2f} s"
    finally:
        wedged.close()


def test_a_home_mount_that_hangs_costs_one_budget_and_one_thread(isolated_home, tmp_path, monkeypatch):
    """Codex P2: a stalled home mount blocked the caller without bound. The
    request runs on a thread of its own; the caller waits one budget, and no
    second thread starts while that one is stuck.

    A 1 s budget here, so a second one cannot hide in the slack: the next
    caller may wait out the grace (INFLIGHT_WAIT_S) and no more, and macos-14
    took 0.21 s over that 0.05 s join (a 0.2 s bound, 2026-10-23). A second
    thread, or a wait on the stuck one, costs a whole budget (1 s); the hang
    itself 5 s."""
    _no_credentials(monkeypatch)
    monkeypatch.setattr(client, "HANDOFF_BUDGET_S", 1.0)
    paths.machine_key()
    hung, entered = threading.Event(), []

    def hanging(path):
        entered.append(path)
        hung.wait(5)
        raise PermissionError("released")

    monkeypatch.setattr(paths, "require_private", hanging)
    try:
        started = time.monotonic()
        assert service_handoff.drain(str(tmp_path)) is None
        assert time.monotonic() - started < client.HANDOFF_BUDGET_S + SLACK_S
        service_handoff.reset()  # not even a back-off: the thread still out is what holds it
        started = time.monotonic()
        assert service_handoff.drain(str(tmp_path)) is None
        assert time.monotonic() - started < service_handoff.INFLIGHT_WAIT_S + SLACK_S and len(entered) == 1
    finally:
        hung.set()


def test_a_request_thread_hung_past_its_deadline_backs_off_again_at_once(isolated_home, tmp_path, monkeypatch):
    """Review: once the first back-off ran out, every hand-off waited 50 ms for
    a thread that would never finish, and set no back-off again."""
    _no_credentials(monkeypatch)
    hung = threading.Event()
    monkeypatch.setattr(paths, "_machine_key", None)
    monkeypatch.setattr(paths, "machine_key", lambda: hung.wait(10))
    try:
        assert service_handoff.drain(str(tmp_path)) is None  # the thread now hangs
        service_handoff.reset()  # as if the back-off had run out
        time.sleep(service_handoff.INFLIGHT_WAIT_S)
        started = time.monotonic()
        assert service_handoff.drain(str(tmp_path)) is None
        assert time.monotonic() - started < 0.02, "no wait for a thread past its own deadline"
        assert service_handoff._quieted(protocol.Method.OUTBOX_DRAIN), "and the back-off is set again"
    finally:
        hung.set()


def test_a_request_beside_a_healthy_one_still_out_backs_nothing_off(isolated_home, tmp_path, monkeypatch):
    """Review: a telemetry batch overlapping a drain kick found the other
    request still out (slower than the 50 ms grace, inside its deadline) and
    backed the service off for a minute. It is done here, and that is all.

    The first is held until the end, inside a 5 s budget: healthy for as long
    as the test looks. (A 0.2 s wait on each folder check was 0.4 s with the
    socket's two folders, past a 0.25 s budget: the first request then backed
    off on its own, and macos-14 read that back-off.)"""
    _no_credentials(monkeypatch)
    monkeypatch.setattr(client, "HANDOFF_BUDGET_S", 5.0)
    paths.machine_key()
    slow = threading.Event()
    monkeypatch.setattr(paths, "require_private", lambda path: (slow.wait(5), _raise_missing())[1])
    first = threading.Thread(target=service_handoff.drain, args=(str(tmp_path),), kwargs={})
    try:
        first.start()
        assert wait_for(lambda: service_handoff._inflight is not None and service_handoff._inflight.is_alive(), 2)
        held = service_handoff._inflight
        assert service_handoff.drain(str(tmp_path)) is None  # the one still out holds the way
        assert held.is_alive() and service_handoff._inflight is held, "it overlapped the first, still out"
        assert not service_handoff._quieted(protocol.Method.OUTBOX_DRAIN), "a healthy overlap backs nothing off"
    finally:
        slow.set()
        first.join(5)


def _raise_missing():
    raise FileNotFoundError("no service here")


def test_a_symlinked_box_registry_is_read_at_the_watchers_own_lease(tmp_path):
    """Review: the lease was looked for beside the registry's real folder, the
    watcher takes it beside the folder as named: a live watcher read as none."""
    import fcntl

    host = background.BackgroundHost(log=lambda m: None)
    (tmp_path / "real" / "runs").mkdir(parents=True)
    (tmp_path / "named").mkdir()
    (tmp_path / "named" / "runs").symlink_to(tmp_path / "real" / "runs")
    named = tmp_path / "named" / "runs"
    assert box_spawn.lock_path(named) == tmp_path / "named" / background.BOX_LEASE
    with open(box_spawn.lock_path(named), "a+") as lease:
        fcntl.flock(lease.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)  # a live watcher's
        answer = host.watch_box({"python": sys.executable, "cwd": None, "env": {"PROBE_BOX_DIR": str(named)}})
    assert answer == {"accepted": True, "state": BackgroundState.RUNNING} and host.started == 0


def test_a_caller_with_no_new_privs_like_the_service_counts_as_sandboxed(monkeypatch):
    """Codex P1: with no_new_privs on both sides a caller can add a Landlock
    domain that shows in none of the fields compared, and the service ran its
    work outside it. It cannot be ruled out, so it counts as sandboxed: in
    `caller.sandboxed` (every method that runs or stores work) and in the hook
    host's own copy."""
    if not sys.platform.startswith("linux"):
        pytest.skip("Landlock and no_new_privs are Linux's")
    from probe.service import caller

    both = ("0", "0", "1", "mnt:[4026531841]", "user:[4026531837]")
    monkeypatch.setattr(caller, "confinement", lambda pid: both)
    assert caller.sandboxed(4242) is True
    plain = ("0", "0", "0", "mnt:[4026531841]", "user:[4026531837]")
    monkeypatch.setattr(caller, "confinement", lambda pid: plain)
    assert caller.sandboxed(4242) is False
    import importlib.util

    for plugin in ("probe-research", "probe-research-daemon"):
        path = Path(__file__).resolve().parents[1] / "plugins" / plugin / "hooks" / "zygote.py"
        spec = importlib.util.spec_from_file_location(f"_q5_zygote_{plugin.replace('-', '_')}", path)
        zygote = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(zygote)
        monkeypatch.setattr(zygote, "_peer_pid", lambda conn: 4242)
        monkeypatch.setattr(zygote, "_confinement", lambda pid: both)
        zygote._OWN_CONFINEMENT[:] = []
        assert zygote._sandboxed(None) is True, plugin
        monkeypatch.setattr(zygote, "_confinement", lambda pid: plain)
        zygote._OWN_CONFINEMENT[:] = []
        assert zygote._sandboxed(None) is False, plugin


@pytest.fixture
def plain_network(monkeypatch):
    for name in service_handoff.NETWORK_ENV:
        monkeypatch.delenv(name, raising=False)


def test_a_batch_whose_answer_was_lost_is_resent_under_its_id(isolated_home, plain_network):
    """Codex P2: the service may have taken it (and POSTed it) when the
    connection closed before its answer; the SDK posted it again. Now it asks
    again under the same id, and the service acknowledges what it took."""
    fake = _FakeService(script=["eof", {"accepted": True}])
    try:
        assert service_handoff.telemetry([{"event": "e", "uuid": "0" * 8 + "-0000-4000-8000-" + "0" * 12}]) is True
        assert fake.connections == 2
        first, second = fake.requests
        assert first["id"] == second["id"], "the same batch, the same id"
    finally:
        fake.close()


def test_a_refusal_after_a_timeout_never_loses_the_batch(isolated_home, plain_network):
    """Codex P2: a timeout counted as taken, and the service then refused it
    (a sandbox refusal answered late): the batch was gone. Only an explicit
    `accepted` is taken now; a refusal on the resend means this process
    POSTs it itself."""
    fake = _FakeService(script=["silent", {"accepted": False, "reason": BackgroundRefusal.SANDBOXED}])
    try:
        assert service_handoff.telemetry([{"event": "e", "uuid": "0" * 8 + "-0000-4000-8000-" + "0" * 12}]) is False
        assert fake.connections == 2 and fake.requests[0]["id"] == fake.requests[1]["id"]
    finally:
        fake.close()


def test_a_batch_never_answered_is_posted_here_with_uuids_that_collapse_copies(isolated_home, plain_network):
    fake = _FakeService(silent=True)
    try:
        entries = service_handoff.stamp([{"event": "a"}, {"event": "b", "uuid": "kept"}])
        started = time.monotonic()
        assert service_handoff.telemetry(entries) is False
        assert time.monotonic() - started < service_handoff.TELEMETRY_TRIES * (client.HANDOFF_BUDGET_S + 0.2)
        assert fake.connections == service_handoff.TELEMETRY_TRIES
        assert len({r["id"] for r in fake.requests}) == 1
        assert entries[1]["uuid"] == "kept" and len(entries[0]["uuid"]) == 36
    finally:
        fake.close()


def test_the_service_takes_a_batch_once_and_acknowledges_a_resend_even_when_stopping():
    host = background.BackgroundHost(log=lambda m: None)
    sent, gate = [], threading.Event()
    host.transport = lambda entries: (gate.wait(5), sent.append(entries))
    assert host.send_telemetry([{"event": "a"}], "b1") == {"accepted": True}
    assert host.send_telemetry([{"event": "a"}], "b1") == {"accepted": True}
    host.close()
    assert host.send_telemetry([{"event": "a"}], "b1") == {"accepted": True}, "what was taken stays taken"
    assert host.send_telemetry([{"event": "c"}], "b2")["reason"] == BackgroundRefusal.STOPPING
    gate.set()
    assert wait_for(lambda: sent, 5)
    time.sleep(0.2)
    assert sent == [[{"event": "a"}]], "queued once"


def test_a_stopping_service_flushes_the_telemetry_it_took():
    """Codex P2: `close()` signalled the sender and returned, so a POST in
    flight (or queued) was lost when the service exited. It now waits for
    them, up to the SDK sender's own flush bound."""
    host = background.BackgroundHost(log=lambda m: None)
    sent = []
    host.transport = lambda entries: (time.sleep(0.3), sent.append(entries))
    assert host.send_telemetry([{"event": "a"}], "f1")["accepted"] is True
    assert host.send_telemetry([{"event": "b"}], "f2")["accepted"] is True
    started = time.monotonic()
    host.close(background.FLUSH_S)
    assert sent == [[{"event": "a"}], [{"event": "b"}]]
    assert time.monotonic() - started < background.FLUSH_S


# -- the service's side, without a service -------------------------------------


def _script(tmp_path: Path, name: str, body: str) -> str:
    path = tmp_path / name
    path.write_text("#!/bin/sh\n" + body + "\n")
    path.chmod(0o755)
    return str(path)


def _wait_children_gone(host: background.BackgroundHost, timeout: float = 10.0) -> None:
    assert wait_for(lambda: not host.public()["drains"] and not host.public()["box_watchers"], timeout)


def test_a_child_failing_at_its_start_marks_its_folder_failing(tmp_path):
    host = background.BackgroundHost(log=lambda m: None)
    folder = tmp_path / "q"
    folder.mkdir()
    failing = _script(tmp_path, "broken-python", "exit 1")
    request = {"dir": str(folder), "python": failing, "env": {}}
    assert host.drain(request) == {"accepted": True, "state": BackgroundState.STARTED}
    _wait_children_gone(host)
    assert host.drain(request) == {"accepted": False, "reason": BackgroundRefusal.FAILING}
    # A clean exit (drained, auth-blocked, paused) never does.
    other = tmp_path / "r"
    other.mkdir()
    clean = _script(tmp_path, "auth-blocked-python", "exit 3")
    assert host.drain({"dir": str(other), "python": clean, "env": {}})["accepted"] is True
    _wait_children_gone(host)
    assert host.drain({"dir": str(other), "python": clean, "env": {}})["accepted"] is True
    assert "drainer.log" in os.listdir(folder)


def test_one_child_per_folder_and_at_most_max_drains(tmp_path):
    host = background.BackgroundHost(log=lambda m: None, max_drains=2)
    sleeper = _script(tmp_path, "slow-python", "exec sleep 30")
    folders = []
    for name in "abc":
        (tmp_path / name).mkdir()
        folders.append({"dir": str(tmp_path / name), "python": sleeper, "env": {"PROBE_RUN_ID": name}})
    try:
        assert host.drain(folders[0])["state"] == BackgroundState.STARTED
        assert host.drain(folders[0])["state"] == BackgroundState.RUNNING
        assert host.drain(folders[1])["state"] == BackgroundState.STARTED
        assert host.drain(folders[2]) == {"accepted": False, "reason": BackgroundRefusal.BUSY}
        assert len(host.public()["drains"]) == 2
        host.close()
        assert host.drain(folders[2]) == {"accepted": False, "reason": BackgroundRefusal.STOPPING}
        pids = [d["pid"] for d in host.public()["drains"]]
        assert all(pid_running(pid) for pid in pids), "closing never stops a child: the outbox is its own"
    finally:
        for drain in host.public()["drains"]:
            with contextlib.suppress(OSError):
                os.kill(drain["pid"], signal.SIGKILL)


def test_a_child_that_let_its_lease_go_is_replaced_and_a_held_lease_is_running(tmp_path, monkeypatch):
    """A worker lets its lease go a moment before its process ends: an op
    queued then must get a new drainer, never a "running" for the old one
    (review: the writer's last op waited for the next `probe` command). And a
    lease someone holds is RUNNING, nothing started."""
    import fcntl

    monkeypatch.setattr(background, "STARTUP_S", 0.2)
    host = background.BackgroundHost(log=lambda m: None)
    folder = tmp_path / "q"
    folder.mkdir()
    lingering = _script(tmp_path, "lingering-python", "exec sleep 30")  # alive, no lease taken
    request = {"dir": str(folder), "python": lingering, "env": {}}
    pids = []
    try:
        assert host.drain(request)["state"] == BackgroundState.STARTED
        pids += [d["pid"] for d in host.public()["drains"]]
        assert host.drain(request)["state"] == BackgroundState.RUNNING, "still starting"
        time.sleep(0.3)
        assert host.drain(request)["state"] == BackgroundState.STARTED, "its lease is free: a new drainer"
        pids = [d["pid"] for d in host.public()["drains"]]
        assert host.started == 2 and len(set(pids)) == 2, "the one it replaced still counts until reaped"
        time.sleep(0.3)
        with open(folder / background.DRAIN_LEASE, "a+") as lease:
            fcntl.flock(lease.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)  # a live worker's
            assert host.drain(request) == {"accepted": True, "state": BackgroundState.RUNNING}
        assert host.started == 2
    finally:
        for pid in pids:
            with contextlib.suppress(OSError):
                os.kill(pid, signal.SIGKILL)


def test_children_that_never_take_their_lease_stay_bounded_and_are_stopped(tmp_path, monkeypatch):
    """Codex P2: past STARTUP_S a live child still importing (no lease yet) was
    replaced in the bookkeeping while its process and waiter lived on, so
    kicks during stalled imports made children without bound (6 live against a
    limit of 2). Every live child counts now, and one that never takes its
    lease in STALL_S is stopped.

    STALL_S stays long while the six kicks run and is cut to 1 s only after
    them, so no kick can take the first look: on macos-14 the kicks (0.5 s of
    sleeps after the first child's start) ran past a 1 s STALL_S, the last one
    took the first look, and the "not yet" look below was the second
    (stopped == 1, 2026-10-23)."""
    monkeypatch.setattr(background, "STARTUP_S", 0.05)
    monkeypatch.setattr(background, "STALL_S", 60.0, raising=False)
    monkeypatch.setattr(background, "STALL_CONFIRM_S", 0.3, raising=False)
    host = background.BackgroundHost(log=lambda m: None, max_drains=2)
    folder = tmp_path / "q"
    folder.mkdir()
    marks = tmp_path / "pids"
    stalled = _script(tmp_path, "stalled-python", f'echo $$ >> "{marks}"; exec sleep 30')
    request = {"dir": str(folder), "python": stalled, "env": {}}

    def alive() -> list[int]:
        try:
            listed = [int(p) for p in marks.read_text().split()]
        except OSError:
            return []
        return [p for p in listed if pid_running(p)]

    try:
        answers = []
        for _ in range(6):
            answers.append(host.drain(request))
            time.sleep(0.1)
        assert wait_for(lambda: marks.exists() and len(marks.read_text().split()) >= host.started, 5)
        assert len(alive()) <= 2, (answers, alive())  # background.MAX_PER_KEY
        assert {"accepted": False, "reason": BackgroundRefusal.BUSY} in answers, "past the bound: the caller forks"
        # Past STALL_S, the lease free on one look: not yet (a long drainer
        # lets it go a moment before it exits, its last report to send) ...
        monkeypatch.setattr(background, "STALL_S", 1.0)
        time.sleep(1.1)
        host.drain(request)
        assert host.stopped == 0
        # ... free again STALL_CONFIRM_S later: the stalled ones are stopped.
        time.sleep(0.4)
        host.drain(request)
        assert wait_for(lambda: len(alive()) <= 1, 10), alive()
        assert host.stopped >= 1
    finally:
        for pid in alive():
            with contextlib.suppress(OSError):
                os.kill(pid, signal.SIGKILL)


def test_a_child_whose_waiter_will_not_start_is_killed_not_forgotten(tmp_path, monkeypatch):
    """Codex P2 (round 4): when the waiter thread would not start, the running
    child was dropped from the books: six requests got six children at a
    limit of one. It is killed and reaped now, and the caller forks its own."""
    import types

    host = background.BackgroundHost(log=lambda m: None, max_drains=1)

    class NoThread:
        def __init__(self, *a, **k):
            pass

        def start(self):
            raise RuntimeError("can't start new thread")

    monkeypatch.setattr(background, "threading", types.SimpleNamespace(Thread=NoThread, Lock=threading.Lock))
    marks = tmp_path / "pids"
    slow = _script(tmp_path, "slow-python", f'echo $$ >> "{marks}"; exec sleep 30')

    def alive() -> list[int]:
        try:
            return [p for p in (int(x) for x in marks.read_text().split()) if pid_running(p)]
        except OSError:
            return []

    try:
        answers = []
        for name in "abcdef":
            (tmp_path / name).mkdir()
            answers.append(host.drain({"dir": str(tmp_path / name), "python": slow, "env": {}}))
        assert answers == [{"accepted": False, "reason": BackgroundRefusal.UNUSABLE}] * 6
        assert host.public()["drains"] == []
        assert wait_for(lambda: not alive(), 5), alive()
    finally:
        for pid in alive():
            with contextlib.suppress(OSError):
                os.kill(pid, signal.SIGKILL)


def test_a_child_runs_in_the_callers_folder(tmp_path):
    """As the caller's own fork did: `-m` reads modules from the working folder."""
    host = background.BackgroundHost(log=lambda m: None)
    folder, work = tmp_path / "q", tmp_path / "project"
    folder.mkdir()
    work.mkdir()
    where = _script(tmp_path, "where-python", f'pwd > "{folder}/cwd.txt"')
    assert host.drain({"dir": str(folder), "python": where, "env": {}, "cwd": str(work)})["accepted"] is True
    assert wait_for(lambda: (folder / "cwd.txt").exists() and (folder / "cwd.txt").read_text().strip(), 10)
    assert os.path.realpath((folder / "cwd.txt").read_text().strip()) == os.path.realpath(work)


def test_a_folder_or_interpreter_not_this_users_is_refused(tmp_path):
    host = background.BackgroundHost(log=lambda m: None)
    assert host.drain({"dir": str(tmp_path / "missing"), "python": sys.executable, "env": {}})["reason"] == (
        BackgroundRefusal.UNUSABLE
    )
    assert host.drain({"dir": str(tmp_path), "python": str(tmp_path / "nope"), "env": {}})["reason"] == (
        BackgroundRefusal.UNUSABLE
    )


def test_a_full_telemetry_queue_is_busy_and_nothing_raises(tmp_path):
    host = background.BackgroundHost(log=lambda m: None)
    gate, sent = threading.Event(), []

    def slow(entries):
        gate.wait(10)
        sent.append(entries)

    host.transport = slow
    answers = [host.send_telemetry([{"event": str(i)}]) for i in range(background.MAX_TELEMETRY_BATCHES + 2)]
    assert answers[0] == {"accepted": True}
    assert answers[-1] == {"accepted": False, "reason": BackgroundRefusal.BUSY}
    gate.set()
    assert wait_for(lambda: len(sent) >= background.MAX_TELEMETRY_BATCHES, 10)
    host.transport = lambda entries: (_ for _ in ()).throw(OSError("PostHog is down"))
    assert host.send_telemetry([{"event": "x"}]) == {"accepted": True}
    assert wait_for(lambda: host.public()["telemetry"]["dropped"] == 1, 5)


# -- a real service -------------------------------------------------------------


def test_a_running_service_drains_the_outbox_for_a_training_process(service, stored_login, api, tmp_path,
                                                                     monkeypatch):
    status = service.start()
    journal = _journal(tmp_path, stored_login)
    for step in (1, 2, 3):
        journal.append_http("POST", "/v1/runs/r-q5/metrics", {"points": [{"step_index": step}]})
    _no_fork_in(monkeypatch, outbox_worker, _NoFork)
    assert outbox_worker.maybe_spawn(str(journal.dir)) is True
    assert wait_for(lambda: not journal.pending(), 30), f"the service's drainer never emptied it:\n{service.log()}"
    assert _steps(api) == [1, 2, 3], "FIFO, across the hand-off"
    assert {auth for _, _, auth in _received(api)} == {f"Bearer {TOKEN}"}, "the stored login, never another"
    assert wait_for(lambda: outbox_worker._lease_is_free(journal), 15)
    assert service.status()["background"]["started"] == 1
    assert f"probe.sdk.outbox_worker started for {os.path.realpath(journal.dir)} (pid" in service.log()
    assert status["pid"] == service.status()["pid"]


def test_an_op_queued_as_the_services_drainer_exits_is_still_delivered(service, stored_login, api, tmp_path):
    """Review: the drainer lets its lease go a moment before its process ends;
    an op queued in that moment was answered "running" and waited for the next
    `probe` command. Now a free lease always gets a drainer."""
    service.start()
    journal = _journal(tmp_path, stored_login)
    journal.append_http("POST", "/v1/runs/r-q5/metrics", {"points": [{"step_index": 1}]})
    first = client.drain_outbox(str(journal.dir), sys.executable, service_handoff.runtime_env(), budget=10.0)
    assert first["state"] == BackgroundState.STARTED
    assert wait_for(lambda: not outbox_worker._lease_is_free(journal), 15)
    deadline = time.monotonic() + 30
    while not outbox_worker._lease_is_free(journal):  # the instant it goes, its process still alive
        assert time.monotonic() < deadline
    journal.append_http("POST", "/v1/runs/r-q5/metrics", {"points": [{"step_index": 2}]})
    outbox_worker.maybe_spawn(str(journal.dir))
    assert wait_for(lambda: not journal.pending(), 30), f"the op stranded:\n{service.log()}"
    assert _steps(api) == [1, 2]


def test_an_environment_credential_keeps_the_local_fork(service, stored_login, api, tmp_path, monkeypatch):
    service.start()
    monkeypatch.setenv("PROBE_TOKEN", TOKEN)
    journal = _journal(tmp_path, stored_login)
    journal.append_http("POST", "/v1/runs/r-q5/metrics", {"points": [{"step_index": 7}]})
    assert outbox_worker.maybe_spawn(str(journal.dir)) is True
    assert wait_for(lambda: not journal.pending(), 30)
    assert _steps(api) == [7]
    assert service.status()["background"]["started"] == 0


def test_an_endpoint_the_config_does_not_name_is_refused(service, stored_login, tmp_path):
    service.start()
    (tmp_path / "q").mkdir()
    env = {"PROBE_BASE_URL": "https://elsewhere.example", "PROBE_CONFIG_PATH": os.environ["PROBE_CONFIG_PATH"]}
    answer = client.drain_outbox(str(tmp_path / "q"), sys.executable, env, budget=5.0)
    assert answer == {"accepted": False, "reason": BackgroundRefusal.UNKNOWN_ENDPOINT}
    with pytest.raises(client.ServiceError) as raised:
        client.drain_outbox(str(tmp_path / "q"), sys.executable, {"PROBE_TOKEN": "x"}, budget=5.0)
    assert raised.value.code == ErrorCode.INVALID_PARAMS


_CONFINED = """
import ctypes, json, sys
assert ctypes.CDLL(None, use_errno=True).prctl(38, 1, 0, 0, 0) == 0  # PR_SET_NO_NEW_PRIVS
from probe.sdk import outbox_worker, service_handoff
from probe.service import client
client.HANDOFF_BUDGET_S = 10.0
answer = client.drain_outbox(sys.argv[1], sys.executable, {}, budget=10.0)
forks = []
class Fork:
    def __init__(self, argv, **kw):
        forks.append(argv)
    def poll(self):
        return None
import types
outbox_worker.subprocess = types.SimpleNamespace(Popen=Fork, DEVNULL=-3, PIPE=-1)
spawned = outbox_worker.maybe_spawn(sys.argv[1])
print(json.dumps({"answer": answer, "spawned": spawned, "forks": len(forks)}))
"""


def test_a_caller_in_a_sandbox_forks_its_own(service, stored_login, tmp_path):
    if not sys.platform.startswith("linux"):
        pytest.skip("no-new-privs is Linux's")
    service.start()
    journal = _journal(tmp_path, stored_login)
    journal.append_http("POST", "/v1/runs/r-q5/metrics", {"points": [{"step_index": 1}]})
    confined = subprocess.run([sys.executable, "-c", _CONFINED, str(journal.dir)], capture_output=True, text=True,
                              timeout=60)
    found = json.loads(confined.stdout)
    assert found["answer"] == {"accepted": False, "reason": BackgroundRefusal.SANDBOXED}, confined.stderr
    assert found["spawned"] is True and found["forks"] == 1, "refused: it forks its own drainer, as before"
    assert service.status()["background"]["started"] == 0


_NO_NEW_PRIVS = "import ctypes\nassert ctypes.CDLL(None, use_errno=True).prctl(38, 1, 0, 0, 0) == 0\n"
#: `python -m probe.service` under no_new_privs, as a hardened container's
#: process tree runs it (`client.ensure` itself no longer starts one from there).
_NNP_SERVICE = _NO_NEW_PRIVS + (
    "import subprocess, sys\n"
    "from probe.service import client, paths\n"
    "paths.ensure_dirs()\n"
    "subprocess.Popen([sys.executable, '-I', '-m', 'probe.service'], env=client._clean_env(),\n"
    "                 cwd=str(paths.service_dir()), start_new_session=True, stdin=subprocess.DEVNULL,\n"
    "                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\n"
)


def _start_service_with_no_new_privs(service) -> dict:
    subprocess.run([sys.executable, "-c", _NNP_SERVICE], check=True, timeout=60)
    status = wait_for(service.status, 10)
    assert status, service.log()
    assert "NoNewPrivs:\t1" in Path(f"/proc/{status['pid']}/status").read_text(), "the test needs it under no_new_privs"
    return status


def _as_nnp_caller(script: str, *args: str) -> dict:
    """`script`'s last line printed as JSON, run with no_new_privs set."""
    done = subprocess.run([sys.executable, "-c", _NO_NEW_PRIVS + script, *args], capture_output=True, text=True,
                          timeout=60)
    assert done.returncode == 0, done.stderr
    return json.loads(done.stdout.strip().splitlines()[-1])


_CALL_EACH_CLASS = """
import json
from probe.service import client
from probe.service.protocol import Method
def ask(method, params):
    try:
        return {"result": client.call(method, params, timeout=10)}
    except client.ServiceError as exc:
        return {"error": exc.data}
print(json.dumps({
    "read": ask(Method.STATUS, {}),
    "control": ask(Method.SESSION_END, {"sid": "nobody", "generation": 1}),
    "register": ask(Method.SESSION_REGISTER, {"sid": "s-nnp", "harness": "test", "mode": "inline", "owner": None,
                                              "generation": 1}),
    "action": ask(Method.ACTION_RUN, {"action": "logout", "params": {}, "client_request_id": "nnp"}),
    "check": ask(Method.UPDATE_CHECK_NOW, {"trigger": "cli"}),
    "status": ask(Method.STATUS_GET, {"refresh": True}),
    "finish": ask(Method.SESSION_FINISH, {"sid": "anyone"}),
    "hooks": ask(Method.HOOKS_HOST, {"root": "/nowhere"}),
    "app_result": ask(Method.UPDATE_APP_RESULT, {"result": "current"}),
}))
"""


def test_every_method_has_a_class_and_work_is_refused_to_a_confined_caller(service, stored_login):
    """Codex P1 (round 4): `action.run`, `update.check_now` and
    `session.register` ran for a caller the hand-offs refused. One table
    classifies every method; WORK is refused before its handler, in the
    shape each method's clients read; READ and CONTROL answer as ever."""
    from probe.service import server

    class _Anything:  # stands in for a Service: `_handlers` only names its methods
        def __getattr__(self, name):
            return lambda *a, **k: None

    assert set(server.METHOD_POLICY) == set(protocol.METHODS) | server.LOCAL_METHODS, "every method has a class"
    assert set(server.Service._handlers(_Anything())) == set(protocol.METHODS) | server.LOCAL_METHODS, "and a handler"
    assert set(server.CONFINED_ANSWERS) <= {m for m, p in server.METHOD_POLICY.items() if p == server.Policy.WORK}
    if not sys.platform.startswith("linux"):
        pytest.skip("no-new-privs is Linux's")
    _start_service_with_no_new_privs(service)
    got = _as_nnp_caller(_CALL_EACH_CLASS)
    assert "result" in got["read"] and got["read"]["result"]["sessions"] == 0, got
    assert got["control"] == {"result": {}}, got
    for work in ("action", "check", "status", "app_result"):
        assert got[work] == {"error": {"reason": protocol.RefusedReason.SANDBOXED}}, (work, got)
    # A forged "current" would hold the desktop app's update check off for 6 h.
    assert service.call(Method.UPDATE_STATUS)["app"]["last"] is None, "nothing was recorded"
    # In the shapes their clients read as "not here": a tap never registers
    # again (and never retries every 2 s), nor reads a hosted recorder.
    assert got["register"] == {"result": {"alive": False, "reason": "sandboxed"}}, got
    assert got["finish"] == {"result": {"recording": False, "finished": False}}, got
    assert got["hooks"] == {"result": {"refused": "a caller in a sandbox", "reason": "sandboxed"}}, got
    assert service.status()["sessions"] == 0, "nothing was registered"


def test_the_screen_refuses_a_gone_caller_and_never_pid_1(monkeypatch):
    """Review: a container's entrypoint (pid 1) read as gone to `procid` and
    lost every WORK method."""
    from probe.service import server

    monkeypatch.setattr(server, "confined", lambda pid: False)
    assert server.screen(1, "12345") is None  # its start time known (Linux), as a real peer's is
    gone = subprocess.Popen(["true"])
    gone.wait()
    assert server.screen(gone.pid, None) == protocol.RefusedReason.CALLER_GONE
    assert server.screen(os.getpid(), None) is None
    monkeypatch.setattr(server, "confined", lambda pid: True)
    assert server.screen(os.getpid(), None) == protocol.RefusedReason.SANDBOXED


def test_a_process_with_no_new_privs_starts_no_service(service_home):
    """A service it started would have no_new_privs too and refuse every
    caller's work, then idle out, again at every hook: none is started."""
    if not sys.platform.startswith("linux"):
        pytest.skip("no-new-privs is Linux's")
    got = _as_nnp_caller("import json\nfrom probe.service import client\nprint(json.dumps(client.ensure(wait=1)))")
    assert got == client.Ensured.CONFINED
    assert service_home.status() is None and not service_home.service_processes()


def test_a_service_with_no_new_privs_refuses_a_caller_with_it_too(service, stored_login, tmp_path):
    """Codex P1, for real: the service started under no_new_privs (a hardened
    container, a sandboxed agent's own process tree) and a caller with it too
    compare equal on every field; the caller may hold a Landlock domain. The
    hand-off is refused and nothing starts."""
    if not sys.platform.startswith("linux"):
        pytest.skip("no-new-privs is Linux's")
    _start_service_with_no_new_privs(service)
    journal = _journal(tmp_path, stored_login)
    journal.append_http("POST", "/v1/runs/r-q5/metrics", {"points": [{"step_index": 1}]})
    asked = subprocess.run(
        [sys.executable, "-c", _NO_NEW_PRIVS + "import json, sys\nfrom probe.service import client\n"
         "print(json.dumps(client.drain_outbox(sys.argv[1], sys.executable, {}, budget=10.0)))", str(journal.dir)],
        capture_output=True, text=True, timeout=60,
    )
    assert json.loads(asked.stdout) == {"accepted": False, "reason": BackgroundRefusal.SANDBOXED}, asked.stderr
    assert service.status()["background"]["started"] == 0


class _SlowPostHog(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(length))
        time.sleep(0.5)
        self.server.batches.append(body)
        self.send_response(200)
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"{}")

    def log_message(self, *args) -> None:
        pass


def test_a_service_that_stops_still_sends_the_telemetry_it_took(service, monkeypatch):
    """Codex P2: the service's sender was a daemon thread nobody waited for: a
    batch still queued (or being POSTed) when the service stopped was lost.
    The stop now gives it the SDK sender's own flush bound."""
    posthog = ThreadingHTTPServer(("127.0.0.1", 0), _SlowPostHog)
    posthog.daemon_threads = True
    posthog.batches = []
    threading.Thread(target=posthog.serve_forever, daemon=True).start()
    try:
        monkeypatch.setenv(background.TELEMETRY_HOST_ENV, f"http://127.0.0.1:{posthog.server_port}")
        for name in service_handoff.NETWORK_ENV:
            monkeypatch.delenv(name, raising=False)
        status = service.start()
        from probe._shared import telemetry

        telemetry._post_batch([{"event": "q5.first", "distinct_id": "machine:test", "properties": {}}])
        telemetry._post_batch([{"event": "q5.second", "distinct_id": "machine:test", "properties": {}}])
        service.call(Method.STOP)
        assert service.wait_exit(status["pid"], 10)
        assert wait_for(lambda: len(posthog.batches) == 2, 5), posthog.batches
        assert [b["batch"][0]["event"] for b in posthog.batches] == ["q5.first", "q5.second"]
    finally:
        posthog.shutdown()
        posthog.server_close()


def test_a_service_stopped_mid_drain_loses_nothing(service, stored_login, api, tmp_path, monkeypatch):
    status = service.start()
    journal = _journal(tmp_path, stored_login)
    for step in range(10):
        journal.append_http("POST", "/v1/runs/r-q5/metrics", {"points": [{"step_index": step}]})
    _no_fork_in(monkeypatch, outbox_worker, _NoFork)
    api.gate.clear()  # the drainer's first request is held at the API while the service stops
    assert outbox_worker.maybe_spawn(str(journal.dir)) is True
    assert wait_for(lambda: api.arrived >= 1, 30), service.log()
    service.call(Method.STOP)
    assert service.wait_exit(status["pid"], 10), "the service did not stop"
    assert len(journal.pending()) == 10
    api.gate.set()
    # Its child goes on: the outbox and the lease are its own.
    assert wait_for(lambda: not journal.pending(), 60), "the drain stopped with the service"
    assert _steps(api) == list(range(10)), "every op once, in order, across the stop"
    assert wait_for(lambda: outbox_worker._lease_is_free(journal), 15)
    # The next service takes the next drain.
    service.start()
    journal.append_http("POST", "/v1/runs/r-q5/metrics", {"points": [{"step_index": 10}]})
    assert outbox_worker.maybe_spawn(str(journal.dir)) is True
    assert wait_for(lambda: not journal.pending(), 30)
    assert _steps(api) == list(range(11))
    assert service.status()["background"]["started"] == 1


_WRITER = """
import sys
from probe.sdk import outbox_worker
from probe.sdk.journal import Journal
from probe.service import client
client.HANDOFF_BUDGET_S = 10.0
directory, base_url, writer, count = sys.argv[1:5]
journal = Journal(directory, context={"name": None, "base_url": base_url})
for i in range(int(count)):
    journal.append_http("POST", "/v1/runs/r-q5/metrics", {"points": [{"step_index": i, "writer": writer}]})
    if i % 5 == 0:
        outbox_worker.maybe_spawn(directory)
outbox_worker.maybe_spawn(directory)
"""


def test_two_processes_share_one_outbox_and_one_drainer(service, stored_login, api, tmp_path):
    service.start()
    api.delay = 0.02
    journal = _journal(tmp_path, stored_login)
    journal._ensure()
    writers = [
        subprocess.Popen([sys.executable, "-c", _WRITER, str(journal.dir), stored_login, name, "20"])
        for name in ("a", "b")
    ]
    for proc in writers:
        assert proc.wait(timeout=60) == 0
    assert wait_for(lambda: not journal.pending(), 60), service.log()
    seen = [(p["writer"], p["step_index"]) for path, body, _ in _received(api) for p in body["points"]]
    assert sorted(seen) == sorted((w, i) for w in "ab" for i in range(20)), "every op once"
    for writer in "ab":
        assert [i for w, i in seen if w == writer] == list(range(20)), "each writer's order kept"
    assert api.max_inflight == 1, "one drainer at a time"
    assert service.status()["background"]["started"] >= 1


def test_a_second_caller_finds_the_services_drainer_running(service, stored_login, api, tmp_path):
    service.start()
    api.gate.clear()  # the drainer holds its lease, waiting on the API
    journal = _journal(tmp_path, stored_login)
    for step in range(5):
        journal.append_http("POST", "/v1/runs/r-q5/metrics", {"points": [{"step_index": step}]})
    first = client.drain_outbox(str(journal.dir), sys.executable, service_handoff.runtime_env(), budget=10.0)
    assert first == {"accepted": True, "state": BackgroundState.STARTED}
    assert wait_for(lambda: api.arrived >= 1, 30), service.log()
    again = subprocess.run(
        [sys.executable, "-c", "import json, sys\nfrom probe.service import client\n"
         "print(json.dumps(client.drain_outbox(sys.argv[1], sys.executable, {}, budget=10.0)))", str(journal.dir)],
        capture_output=True, text=True, timeout=60,
    )
    assert json.loads(again.stdout) == {"accepted": True, "state": BackgroundState.RUNNING}, again.stderr
    api.gate.set()
    assert wait_for(lambda: not journal.pending(), 30)
    assert _steps(api) == list(range(5))
    assert service.status()["background"]["started"] == 1


def _box_holder(registry: Path) -> int | None:
    try:
        return int(box_spawn.lock_path(registry).read_text().split()[0])
    except (OSError, ValueError, IndexError):
        return None


def test_the_box_watcher_runs_as_the_services_child_one_per_registry(service, monkeypatch, tmp_path):
    _no_credentials(monkeypatch)
    status = service.start()
    monkeypatch.setenv("PROBE_BOX", "1")
    monkeypatch.setenv("PROBE_BOX_IDLE_EXIT", "3")
    monkeypatch.setenv("PROBE_BOX_INTERVAL", "0.2")
    one, two = tmp_path / "box-a" / "runs", tmp_path / "box-b" / "runs"
    _no_fork_in(monkeypatch, box_spawn, _NoFork)
    assert box_spawn.maybe_spawn(one) is True
    assert box_spawn.maybe_spawn(two) is True, "another registry gets a watcher of its own"
    assert wait_for(lambda: box_spawn.already_running(one) and box_spawn.already_running(two), 30), service.log()
    pids = {_box_holder(one), _box_holder(two)}
    assert None not in pids and len(pids) == 2
    if Path("/proc").is_dir():
        for pid in pids:
            ppid = next(line.split()[1] for line in Path(f"/proc/{pid}/status").read_text().splitlines()
                        if line.startswith("PPid:"))
            assert int(ppid) == status["pid"], "the watcher is the service's child"
    assert {w["pid"] for w in service.status()["background"]["box_watchers"]} == pids
    # Asked directly (the spawner's own lease check answers first otherwise):
    # a held lease is RUNNING, nothing started.
    started = service.status()["background"]["started"]
    env = {**service_handoff.runtime_env(), "PROBE_BOX_DIR": str(one)}
    assert client.watch_box(sys.executable, env, budget=10.0) == {"accepted": True, "state": BackgroundState.RUNNING}
    assert service.status()["background"]["started"] == started
    # Each still exits on its own once its box is quiet, and lets the lease go.
    assert wait_for(lambda: not box_spawn.already_running(one) and not box_spawn.already_running(two), 30)


class _FakePostHog(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        self.server.batches.append(json.loads(self.rfile.read(length)))
        self.send_response(200)
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"{}")

    def log_message(self, *args) -> None:
        pass


def test_a_telemetry_batch_is_posted_by_the_service(service, monkeypatch):
    posthog = ThreadingHTTPServer(("127.0.0.1", 0), _FakePostHog)
    posthog.batches = []
    threading.Thread(target=posthog.serve_forever, daemon=True).start()
    try:
        monkeypatch.setenv(background.TELEMETRY_HOST_ENV, f"http://127.0.0.1:{posthog.server_port}")
        for name in service_handoff.NETWORK_ENV:
            monkeypatch.delenv(name, raising=False)
        service.start()
        from probe._shared import telemetry

        entries = [{"event": "q5.test", "distinct_id": "machine:test", "properties": {"x": 1}}]
        telemetry._post_batch(entries)
        assert wait_for(lambda: posthog.batches, 15), service.log()
        assert posthog.batches[0]["batch"] == entries
        # The fake records the batch BEFORE it answers, and the service counts it
        # sent only once it has read that answer: read once, the count can be 0.
        assert wait_for(lambda: service.status()["background"]["telemetry"]["sent"] == 1, 5), service.status()
    finally:
        posthog.shutdown()
        posthog.server_close()


def test_a_hand_off_to_a_real_service_fits_the_budget(service, stored_login, tmp_path, monkeypatch):
    """The real budget, once the process has found the service: what every
    later kick of a training loop costs."""
    service.start()
    monkeypatch.setattr(client, "HANDOFF_BUDGET_S", 0.25)
    (tmp_path / "q").mkdir()
    service_handoff.drain(str(tmp_path / "q"))  # the first one imports and looks up the machine key
    timings, answers = [], []
    for _ in range(5):
        service_handoff.reset()  # a slow one must show, not back off into instant Nones
        started = time.monotonic()
        answers.append(service_handoff.drain(str(tmp_path / "q")))
        timings.append(time.monotonic() - started)
    assert all(a in (BackgroundState.STARTED, BackgroundState.RUNNING) for a in answers), (answers, timings)
    assert sorted(timings)[len(timings) // 2] < 0.25, timings  # the median: one loaded moment is not the subject
