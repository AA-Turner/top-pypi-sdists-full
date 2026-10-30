"""API v1 on the wire: hello first, closed method set, checked params, pinned shapes.

Against a real service process (what a client meets), plus the socket's and
folder's permissions and the peer-uid check (SO_PEERCRED on Linux,
LOCAL_PEERCRED on macOS).
"""

from __future__ import annotations

import json
import os
import socket
import stat
import sys

import pytest

from probe.service import client, paths, protocol
from probe.service.protocol import ErrorCode, Method, Mode
from probe.service.server import peer_uid
from tests.service_harness import service_home  # noqa: F401 -- a fixture

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")


def _raw(sh, *lines: bytes) -> list[dict]:
    """Send raw lines on one connection; the answers, one per line."""
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.settimeout(3.0)
        sock.connect(str(paths.socket_path()))
        sock.sendall(b"".join(lines))
        buffer = b""
        while buffer.count(b"\n") < len(lines):
            chunk = sock.recv(65536)
            if not chunk:
                break
            buffer += chunk
    return [json.loads(line) for line in buffer.splitlines() if line.strip()]


def _req(id_, method, params=None) -> bytes:
    return protocol.encode(protocol.request(id_, method, params))


HELLO = _req(0, Method.HELLO, {"client": "cli", "client_version": "test", "api": 1})


def test_hello_is_required_first(service_home):
    service_home.start()
    first, hello, then = _raw(service_home, _req(1, Method.STATUS), HELLO, _req(2, Method.STATUS))
    assert first["id"] == 1 and first["error"]["code"] == ErrorCode.HELLO_REQUIRED == -32002
    assert hello["result"]["api"] == 1
    assert then["id"] == 2 and "result" in then


@pytest.mark.parametrize("method", ["action.nope", "update.now", "no.such"])
def test_unknown_methods_are_32601(service_home, method):
    service_home.start()
    _, answer = _raw(service_home, HELLO, _req(5, method, {}))
    assert answer["id"] == 5 and answer["error"]["code"] == ErrorCode.UNKNOWN_METHOD == -32601


@pytest.mark.parametrize(
    "params",
    [
        {"harness": "h", "mode": "inline", "owner": None, "generation": 1},  # no sid
        {"sid": "s", "harness": "h", "mode": "bogus", "owner": None, "generation": 1},
        {"sid": "s", "harness": "h", "mode": "inline", "owner": None, "generation": "1"},
        {"sid": "s", "harness": "h", "mode": "inline", "owner": None, "generation": -1},
        {"sid": "s", "harness": "h", "mode": "inline", "generation": 1},  # owner missing
        {"sid": "s", "harness": "h", "mode": "inline", "owner": {"pid": 1, "start_time": "x"}, "generation": 1},
        {"sid": "s", "harness": "h", "mode": "inline", "owner": {"pid": 9}, "generation": 1},
        {"sid": "", "harness": "h", "mode": "inline", "owner": None, "generation": 1},
    ],
)
def test_register_checks_its_params(service_home, params):
    service_home.start()
    _, answer = _raw(service_home, HELLO, _req(3, Method.SESSION_REGISTER, params))
    assert answer["error"]["code"] == ErrorCode.INVALID_PARAMS == -32602


@pytest.mark.parametrize(
    ("method", "params"),
    [
        (Method.HELLO, {"client": "browser", "client_version": "1", "api": 1}),
        (Method.HELLO, {"client": "app", "api": 1}),
        (Method.HELLO, {"client": "app", "client_version": "1", "api": 1, "keepalive": "yes"}),
        (Method.EVENTS_SUBSCRIBE, {"topics": ["no.such.topic"]}),
        (Method.EVENTS_SUBSCRIBE, {"topics": []}),
        (Method.STATUS_GET, {"refresh": "yes"}),
        (Method.SESSION_END, {"sid": "s"}),
        (Method.RECORDERS_FINISH, {}),
        (Method.RECORDERS_FINISH, {"harness": "claude_code", "wait": -1}),
        (Method.RECORDERS_FINISH, {"harness": "claude_code", "wait": 61}),
        (Method.RECORDERS_FINISH, {"harness": "claude_code", "wait": True}),
        (Method.RUN_HOLD, {"run": "r"}),
        (Method.RUN_HOLD, {"run": "r", "owner": None}),
        (Method.RUN_HOLD, {"run": "r", "owner": {"pid": 1, "start_time": "x"}}),
        (Method.RUN_HOLD, {"owner": {"pid": 4242, "start_time": "x"}}),
        (Method.RUN_HOLD, {"run": "r" * 257, "owner": {"pid": 4242, "start_time": "x"}}),
        (Method.RUN_RELEASE, {}),
        (Method.RUN_RELEASE, {"run": "r", "owner": {"pid": "4242"}}),
        (Method.MANIFEST_REFRESH, {"wait": "soon"}),
        (Method.MANIFEST_REFRESH, {"context": {"PROBE_TOKEN": "x"}}),
        (Method.MANIFEST_REFRESH, {"context": {"PROBE_BASE_URL": "http://api.example.test"}}),
    ],
)
def test_other_methods_check_their_params(service_home, method, params):
    service_home.start()
    _, answer = _raw(service_home, HELLO, _req(4, method, params))
    assert answer["error"]["code"] == ErrorCode.INVALID_PARAMS


def test_a_newer_api_is_unsupported(service_home):
    service_home.start()
    (answer,) = _raw(service_home, _req(1, Method.HELLO, {"client": "app", "client_version": "9", "api": 2}))
    assert answer["error"]["code"] == ErrorCode.UNSUPPORTED_API == -32013
    assert answer["error"]["data"] == {"supported": [1]}


def test_lines_that_are_not_requests_are_32600(service_home):
    service_home.start()
    answers = _raw(
        service_home,
        b"not json\n",
        b"[1, 2]\n",
        b'{"jsonrpc": "2.0", "method": "service.status"}\n',  # no id
        b'{"jsonrpc": "1.0", "id": 7, "method": "service.status"}\n',
    )
    assert [a["error"]["code"] for a in answers] == [ErrorCode.INVALID_REQUEST] * 4
    assert answers[0]["id"] is None and answers[3]["id"] == 7


def test_a_line_over_one_mebibyte_is_refused(service_home):
    service_home.start()
    (answer,) = _raw(service_home, b'{"x": "' + b"a" * (protocol.MAX_LINE_BYTES + 10) + b'"}\n')
    assert answer["error"]["code"] == ErrorCode.INVALID_REQUEST


def test_response_shapes(service_home):
    service_home.start()
    with service_home.connect() as conn:
        hello = conn.hello("app", "1.2.3")
        assert set(hello) == {"service_version", "api", "pid", "started_at", "state", "caps", "env"}
        assert hello["caps"] == sorted(protocol.CAPS) and protocol.Cap.ACTION_SANDBOX in hello["caps"]
        assert hello["api"] == 1 and isinstance(hello["pid"], int) and isinstance(hello["started_at"], float)
        assert hello["state"] in ("discovering", "running", "grace")
        status = conn.call(Method.STATUS)
        assert set(status) == {
            "service_version", "pid", "started_at", "state", "sessions", "app_clients", "update",
            "actions", "discovering_until", "hook_hosts", "hook_queue", "recorders", "workers", "runs",
            "watched", "background", "imports", "statusline", "notes", "watch", "daemon_host", "codex_trust",
        }
        assert status["runs"] == [] and status["workers"] == [] and status["imports"] == []
        # The daemon host (plan daemon-in-service): none until a session's daemon starts.
        assert status["daemon_host"]["pid"] is None and status["daemon_host"]["runs"] == 0
        # What fails here and what was reported (crash-report plan B2): the
        # debug log and `probe doctor` read it.
        assert set(status["watch"]) == {"enabled", "last_scan", "waiting", "reports"}
        assert status["background"] == {
            "drains": [], "box_watchers": [], "started": 0, "telemetry": {"queued": 0, "sent": 0, "dropped": 0},
        }
        assert set(status["statusline"]) == {"folders", "waiting", "running", "children", "followed", "followups", "last"}
        assert set(status["notes"]) == {"running", "waiting", "runs", "last"}
        # Probe's hooks in Codex, kept approved (#3617): nothing of Probe's in this Codex.
        assert set(status["codex_trust"]) == {"state", "asks", "approved", "retry_at", "last"}
        assert set(status["update"]) == {
            "enabled", "last_check", "last_result", "next_check", "in_progress", "cycle_id", "step", "deferred",
            "deferred_since", "guard", "app",
        }
        # The desktop app's update check, which the service decides (#3321): the
        # app reads this to know whether a check is due and why.
        assert set(status["update"]["app"]) == {"due", "reason", "last_check", "listening", "last"}
        assert status["actions"] == {"running": None, "queued": []}
        assert status["app_clients"] == 1
        assert conn.call(
            Method.SESSION_REGISTER,
            {"sid": "s-shape", "harness": "test", "mode": Mode.DAEMON, "owner": None, "generation": 1},
        ) == {"alive": True}
        listing = conn.call(Method.SESSION_LIST)
        assert set(listing) == {"sessions", "harnesses"}
        (listed,) = listing["sessions"]
        assert set(listed) == {"sid", "harness", "mode", "alive", "owner", "generation", "registered_at", "agent_live", "receipts"}
        assert listed["receipts"] is None  # no journal in this HOME
        assert listing["harnesses"] == [{
            "harness": "test", "scope": None, "sessions": 1, "alive": 1, "received_at": None, "pending_bytes": None,
            "pending_lines": None, "pending_batches": 0,
        }]
        # A caller that only counts asks for none: the listing as it always was.
        (bare,) = conn.call(Method.SESSION_LIST, {"receipts": False})["sessions"]
        assert set(bare) == {"sid", "harness", "mode", "alive", "owner", "generation", "registered_at", "agent_live"}
        assert conn.call(Method.EVENTS_SUBSCRIBE, {"topics": sorted(protocol.TOPICS)}) == {}
        assert conn.call(Method.SESSION_END, {"sid": "s-shape", "generation": 1}) == {}
        ended = conn.next_event(2.0)
        assert ended == {"topic": "session.ended", "sid": "s-shape", "generation": 1, "reason": "end"}


def test_status_get_runs_probe_status_and_caches_it(service_home):
    service_home.start()
    with service_home.connect() as conn:
        conn.sock.settimeout(60)  # status.get waits for a real `probe.core.run status` child
        first = conn.call(Method.STATUS_GET, {})
        assert isinstance(first, dict) and first, "probe status --json gave nothing"
        second = conn.call(Method.STATUS_GET, {})
        assert second == first  # cached: no second child within 30 s


def test_socket_and_folder_permissions(service_home):
    service_home.start()
    sock = paths.socket_path()
    assert stat.S_ISSOCK(sock.stat().st_mode)
    assert sock.stat().st_mode & 0o777 == 0o600
    assert paths.service_dir().stat().st_mode & 0o777 == 0o700
    assert sock.parent.stat().st_mode & 0o777 == 0o700


def test_a_client_never_trusts_a_socket_in_a_folder_others_could_plant(service_home, monkeypatch):
    """On the /tmp fallback any local user can make `/tmp/probe-<uid>` first and
    listen there; the service refuses to serve in such a folder, and a client
    must refuse to talk to whatever answers in it. Simulated here on the real
    socket: a folder group/other can write to, then one owned by another uid."""
    service_home.start()
    folder = paths.socket_path().parent
    assert client.connect() is not None  # ours, 0700: trusted
    folder.chmod(0o777)
    try:
        with pytest.raises(PermissionError):
            client.Connection.open()
        assert client.connect() is None
    finally:
        folder.chmod(0o700)
    real_uid = os.getuid()
    with monkeypatch.context() as patched:
        patched.setattr(paths.os, "getuid", lambda: real_uid + 1)
        with pytest.raises(PermissionError):
            client.call(Method.STATUS)
        assert client.ensure() == client.Ensured.UNAVAILABLE  # and never spawns beside it
    assert client.connect() is not None


def test_a_long_home_moves_the_socket_to_a_private_tmp_folder(monkeypatch, tmp_path):
    home = tmp_path / ("h" * 120)
    monkeypatch.setenv("HOME", str(home))
    sock = paths.socket_path()
    assert len(str(sock)) <= paths.MAX_SOCKET_PATH
    assert sock.parent == paths.Path("/tmp") / f"probe-{os.getuid()}"
    monkeypatch.setenv("HOME", str(home) + "2")
    assert paths.socket_path() != sock  # a second HOME never shares the socket


def test_peer_uid_is_read_where_the_platform_says():
    left, right = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
    with left, right:
        uid = peer_uid(left)
    if sys.platform.startswith("linux") or sys.platform == "darwin":
        assert uid == os.getuid()
    else:
        assert uid is None


def test_a_peer_of_another_uid_is_refused(service_home, monkeypatch):
    """The server compares the peer's uid to its own; the other uid is faked by
    an in-process server expecting a different one."""
    import asyncio
    import threading

    from probe.service.registry import Registry
    from probe.service.server import Service, _bind

    left, right = socket.socketpair()
    with left, right:
        if peer_uid(left) is None:
            pytest.skip("this platform does not expose the peer's uid")
    path = paths.ensure_dirs().with_name("peer-test.sock")
    listen = _bind(path)
    service = Service(registry=Registry(paths.service_dir() / "peer.json"), discovery_s=0, grace_s=30,
                      expected_uid=os.getuid() + 1)
    ready = threading.Event()
    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=lambda: loop.run_until_complete(service.run(listen, on_ready=ready.set)))
    thread.start()
    try:
        assert ready.wait(5)
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.settimeout(2.0)
            sock.connect(str(path))
            try:
                # The server may close before the hello lands (EPIPE): refused all the same.
                sock.sendall(HELLO)
                answer = sock.recv(100)
            except (BrokenPipeError, ConnectionResetError):
                answer = b""
            assert answer == b""  # closed without an answer
    finally:
        loop.call_soon_threadsafe(service.stop, "test")
        thread.join(5)
        path.unlink(missing_ok=True)


def test_client_errors_carry_the_code(service_home):
    service_home.start()
    with pytest.raises(client.ServiceError) as raised:
        service_home.call("no.such.method", {})
    assert raised.value.code == -32601


def test_workspace_limit_is_a_service_action_and_its_picker_a_read():
    """`action.run workspace_limit` (the app's Settings → Workspace) is a change,
    one at a time like every action; `desktop.request workspaces` (its list) is a read."""
    from probe.core.requests import ActionName
    from probe.service import protocol

    assert protocol.Action.WORKSPACE_LIMIT in protocol.ACTIONS
    assert protocol.ACTIONS <= {a.value for a in ActionName}
    assert protocol.DesktopOp.WORKSPACES in protocol.DESKTOP_READS
