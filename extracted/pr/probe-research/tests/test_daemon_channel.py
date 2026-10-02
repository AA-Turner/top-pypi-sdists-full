"""SDK -> Probe daemon channel (daemon v2, R3.1 / T8).

The SDK sends ONE JSON datagram to the session's daemon when a run opens and
when it ends. The contract these tests hold: it lands on a real socket in the
shape the daemon's inbox reader parses; with no listener, no session or a bad
path it returns fast and never raises; the path matches the supervisor's
(`tap/companion_supervisor.py::socket_path`), including the /tmp fallback for a
long state dir, which is refused unless it is this user's private folder.
"""

from __future__ import annotations

import json
import os
import socket
import sys
import time
from pathlib import Path

import pytest

from probe.sdk import agent_session, daemon_channel

SID = "11111111-2222-4333-8444-555555555555"
ENV = {"CLAUDECODE": "1", "CLAUDE_CODE_SESSION_ID": SID}

pytestmark = pytest.mark.skipif(not hasattr(socket, "AF_UNIX"), reason="UNIX sockets only")


@pytest.fixture
def short_state(monkeypatch):
    """A state dir short enough for a UNIX socket path (tmp_path is not)."""
    import tempfile

    root = Path(tempfile.mkdtemp(prefix="ps-", dir="/tmp"))
    monkeypatch.setenv("XDG_STATE_HOME", str(root))
    for key, value in ENV.items():
        monkeypatch.setenv(key, value)
    yield root
    import shutil

    shutil.rmtree(root, ignore_errors=True)


def _listen(path: Path) -> socket.socket:
    path.parent.mkdir(parents=True, exist_ok=True)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.bind(str(path))
    sock.settimeout(2.0)
    return sock


def _recv(sock: socket.socket) -> dict:
    return json.loads(sock.recv(65536).decode("utf-8"))


@pytest.fixture
def supervisor(monkeypatch):
    """The tap's supervisor module, imported off the plugin's own path.

    The plugin's package is named `tap`, like the Codex tap's: whatever `tap`
    modules another test left in `sys.modules` are set aside for this test and
    put back afterwards, and the ones imported here are dropped."""
    tap_root = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap"
    for name in [m for m in list(sys.modules) if m == "tap" or m.startswith("tap.")]:
        monkeypatch.delitem(sys.modules, name)
    monkeypatch.syspath_prepend(str(tap_root))
    from tap import companion_supervisor

    yield companion_supervisor
    for name in [m for m in list(sys.modules) if m == "tap" or m.startswith("tap.")]:
        sys.modules.pop(name, None)


# -- the socket ----------------------------------------------------------------


def test_announce_lands_one_json_datagram_on_a_real_socket(short_state):
    sock = _listen(daemon_channel.socket_path(SID))
    try:
        assert daemon_channel.announce("run ended", run_id="r1", status="completed") is True
        msg = _recv(sock)
    finally:
        sock.close()
    assert msg == {"event": "run ended", "session_id": SID, "run_id": "r1", "status": "completed"}


def test_no_listener_returns_fast_and_false(short_state):
    started = time.monotonic()
    assert daemon_channel.announce("run started", run_id="r1") is False
    assert time.monotonic() - started < 0.2


def test_a_stale_socket_file_with_nobody_bound_is_false_not_an_error(short_state):
    path = daemon_channel.socket_path(SID)
    sock = _listen(path)
    sock.close()  # the file stays; nothing reads it any more
    assert path.exists()
    started = time.monotonic()
    assert daemon_channel.announce("run started", run_id="r1") is False
    assert time.monotonic() - started < 0.5


def test_no_session_is_a_silent_no_op(short_state, monkeypatch):
    for key in ENV:
        monkeypatch.delenv(key)
    assert daemon_channel.current_session_id() is None
    assert daemon_channel.announce("run started", run_id="r1") is False


def test_a_regular_file_where_the_socket_should_be_never_raises(short_state):
    path = daemon_channel.socket_path(SID)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not a socket")
    assert daemon_channel.announce("run started", run_id="r1") is False


def test_announce_swallows_anything_the_path_logic_throws(monkeypatch, short_state):
    def boom(_sid):
        raise RuntimeError("anything")

    monkeypatch.setattr(daemon_channel, "socket_path", boom)
    assert daemon_channel.announce("run started", run_id="r1") is False
    assert daemon_channel.run_started({"id": "r1"}) is False
    assert daemon_channel.run_ended("r1", "completed") is False


def test_the_path_matches_the_supervisors_exactly(short_state, supervisor):
    assert daemon_channel.socket_path(SID) == supervisor.socket_path(SID)
    assert daemon_channel.socket_path(SID) == short_state / "probe" / "sessions" / f"{SID}.sock"


# -- the /tmp fallback ------------------------------------------------------------


@pytest.fixture
def long_state(monkeypatch, tmp_path):
    """A state dir too long for a UNIX socket, and a private fallback root."""
    deep = tmp_path / ("d" * 60) / ("e" * 60)
    deep.mkdir(parents=True)
    monkeypatch.setenv("XDG_STATE_HOME", str(deep))
    for key, value in ENV.items():
        monkeypatch.setenv(key, value)
    import tempfile

    root = Path(tempfile.mkdtemp(prefix="pf-", dir="/tmp"))
    monkeypatch.setattr(daemon_channel, "FALLBACK_ROOT", root)
    yield root
    import shutil

    shutil.rmtree(root, ignore_errors=True)


def test_a_too_long_path_uses_the_private_tmp_folder(long_state):
    folder = long_state / f"probe-{os.getuid()}"
    folder.mkdir(mode=0o700)
    path = daemon_channel.socket_path(SID)
    assert path.parent == folder
    import hashlib

    assert path.name == hashlib.sha256(SID.encode()).hexdigest()[:24] + ".sock"
    assert len(str(daemon_channel._state_base() / "sessions" / f"{SID}.sock").encode()) > 100
    sock = _listen(path)
    try:
        assert daemon_channel.announce("run ended", run_id="r9", status="failed") is True
        assert _recv(sock)["run_id"] == "r9"
    finally:
        sock.close()


def test_the_fallback_matches_the_supervisors_exactly(long_state, supervisor, monkeypatch):
    """Same folder, same hash, same name. The supervisor hardcodes `/tmp` (and
    creates the folder), so its `/tmp` is pointed at this test's root."""
    folder = long_state / f"probe-{os.getuid()}"
    folder.mkdir(mode=0o700)
    real_path = supervisor.Path
    monkeypatch.setattr(
        supervisor, "Path", lambda *parts: long_state if parts == ("/tmp",) else real_path(*parts)
    )
    assert daemon_channel.socket_path(SID) == supervisor.socket_path(SID)
    assert daemon_channel.socket_path(SID).parent == folder


@pytest.mark.parametrize("mode", [0o755, 0o770, 0o701])
def test_a_fallback_folder_others_can_enter_is_refused(long_state, mode):
    folder = long_state / f"probe-{os.getuid()}"
    folder.mkdir()
    folder.chmod(mode)
    with pytest.raises(OSError):
        daemon_channel.socket_path(SID)
    assert daemon_channel.announce("run started", run_id="r1") is False


def test_a_symlinked_fallback_folder_is_refused(long_state, tmp_path):
    real = tmp_path / "elsewhere"
    real.mkdir(mode=0o700)
    (long_state / f"probe-{os.getuid()}").symlink_to(real)
    with pytest.raises(OSError):
        daemon_channel.socket_path(SID)


def test_a_missing_fallback_folder_is_not_created_by_the_sender(long_state):
    with pytest.raises(OSError):
        daemon_channel.socket_path(SID)
    assert not (long_state / f"probe-{os.getuid()}").exists()
    assert daemon_channel.announce("run started", run_id="r1") is False


def test_a_session_id_that_is_not_one_never_becomes_a_path():
    with pytest.raises(ValueError):
        daemon_channel.socket_path("../../etc/passwd")


# -- what a message carries ----------------------------------------------------------


def test_run_started_carries_what_the_run_is(short_state):
    sock = _listen(daemon_channel.socket_path(SID))
    row = {
        "id": "run-1",
        "name": "brave-otter",
        "description": "lr sweep point",
        "tags": ["sweep", "lr"],
        "config": {"lr": 0.001, "seed": 3},
        "metadata": {"intent": "does warmup fix the loss spike"},
        "parent_run_id": "run-0",
        "parent_relation": "retry",
        "project_id": None,
    }
    try:
        with daemon_channel.launch_command(["python", "train.py", "--api-key", "sk-live-1234"]):
            assert daemon_channel.run_started(row) is True
        msg = _recv(sock)
    finally:
        sock.close()
    assert msg["event"] == "run started"
    assert msg["run_id"] == "run-1"
    assert msg["session_id"] == SID
    assert msg["name"] == "brave-otter"
    assert msg["description"] == "lr sweep point"
    assert msg["tags"] == ["sweep", "lr"]
    assert msg["config"] == {"lr": 0.001, "seed": 3}
    assert msg["intent"] == "does warmup fix the loss spike"
    assert msg["parent_run_id"] == "run-0"
    assert msg["relation"] == "retry"
    assert msg["command"].startswith("python train.py --api-key")
    assert "sk-live-1234" not in msg["command"], "the command is scrubbed like the process span"
    assert "config_truncated" not in msg


def test_a_big_config_is_capped_and_says_so(short_state):
    sock = _listen(daemon_channel.socket_path(SID))
    config = {f"key{i:04d}": "x" * 100 for i in range(200)}
    try:
        assert daemon_channel.run_started({"id": "run-2", "config": config}) is True
        msg = _recv(sock)
    finally:
        sock.close()
    assert msg["config_truncated"] is True
    assert 0 < len(msg["config"]) < len(config)
    compact = json.dumps(msg["config"], separators=(",", ":"))
    assert len(compact.encode()) <= daemon_channel.MAX_CONFIG_BYTES


def test_a_message_the_os_refuses_as_too_big_is_resent_smaller(short_state, monkeypatch):
    """macOS caps a UNIX datagram at a few KB. EMSGSIZE drops the bulky fields
    and tries again; the run id and session always get through."""
    import errno

    sent: list[bytes] = []

    class Picky:
        def __init__(self, *_a):
            pass

        def setsockopt(self, *_a):
            pass

        def settimeout(self, _t):
            pass

        def sendto(self, data, _path):
            if len(data) > 200:
                raise OSError(errno.EMSGSIZE, "Message too long")
            sent.append(data)

        def close(self):
            pass

    path = daemon_channel.socket_path(SID)
    real = _listen(path)  # a real socket file so the S_ISSOCK check passes
    try:
        monkeypatch.setattr(daemon_channel.socket, "socket", Picky)
        assert daemon_channel.run_started(
            {"id": "run-3", "description": "d" * 500, "config": {"a": 1}, "tags": ["t"]}
        ) is True
    finally:
        real.close()
    msg = json.loads(sent[0])
    assert msg["run_id"] == "run-3" and msg["session_id"] == SID
    assert "description" not in msg and "config" not in msg


# -- the SDK's run lifecycle announces --------------------------------------------------


def test_client_run_announces_the_open_and_finish_announces_the_end(short_state, app, tmp_path):
    from tests.conftest import make_client

    sock = _listen(daemon_channel.socket_path(SID))
    try:
        client = make_client(app, tmp_spool=tmp_path / "spool")
        run = client.run(description="floating", tags=["a"], config={"lr": 1}, intent="see it")
        started = _recv(sock)
        run.finish("completed")
        ended = _recv(sock)
    finally:
        sock.close()
    assert started["event"] == "run started"
    assert started["run_id"] == run.id
    assert started["intent"] == "see it"
    assert started["config"] == {"lr": 1}
    assert ended == {"event": "run ended", "session_id": SID, "run_id": run.id, "status": "completed"}


def test_a_run_opens_normally_with_no_daemon_listening(short_state, app, tmp_path):
    from tests.conftest import make_client

    client = make_client(app, tmp_spool=tmp_path / "spool")
    started = time.monotonic()
    run = client.run(description="nobody home")
    run.finish("completed")
    assert time.monotonic() - started < 5
    assert app.runs[run.id]["status"] == "completed"


# -- E2: the session travels to remote jobs --------------------------------------------


def test_forwarding_env_names_the_session_a_remote_job_should_carry(monkeypatch):
    for key, value in ENV.items():
        monkeypatch.setenv(key, value)
    assert agent_session.forwarding_env() == {"PROBE_AGENT_SESSION": f"claude_code:{SID}"}


def test_a_job_with_only_the_forwarded_session_sends_the_session_headers():
    env = {"PROBE_AGENT_SESSION": f"claude_code:{SID}"}
    assert agent_session.resolve_agent_session(env) == ("claude_code", SID)
    assert agent_session.agent_session_headers(env) == {
        agent_session.AGENT_HEADER: "claude_code",
        agent_session.AGENT_SESSION_HEADER: SID,
    }


@pytest.mark.parametrize(
    "raw",
    ["", "claude_code", "cursor:" + SID, "nobody:" + SID, "claude_code:bad id", "claude_code:x"],
)
def test_a_malformed_or_uncaptured_forwarded_session_is_ignored(raw):
    assert agent_session.resolve_agent_session({"PROBE_AGENT_SESSION": raw}) is None


def test_a_local_agent_always_wins_over_a_forwarded_session():
    env = {**ENV, "PROBE_AGENT_SESSION": "pi:99999999-9999-4999-8999-999999999999"}
    assert agent_session.resolve_agent_session(env) == ("claude_code", SID)


def test_execute_hands_the_child_the_session_with_the_run_id(app, tmp_path, monkeypatch):
    from tests.conftest import make_client

    for key, value in ENV.items():
        monkeypatch.setenv(key, value)
    out = tmp_path / "seen.txt"
    client = make_client(app, tmp_spool=tmp_path / "spool")
    run = client.run(description="wrapped")
    run.execute(
        [
            sys.executable,
            "-c",
            f"import os,pathlib;pathlib.Path({str(out)!r}).write_text("
            "os.environ['PROBE_RUN_ID']+' '+os.environ['PROBE_AGENT_SESSION'])",
        ]
    )
    run_id, session = out.read_text().split()
    assert run_id == run.id
    assert session == f"claude_code:{SID}"


def test_the_hand_off_notice_lists_the_session_to_forward(app, tmp_path, monkeypatch, capsys):
    from probe import cli

    from tests.conftest import make_client

    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    for key, value in ENV.items():
        monkeypatch.setenv(key, value)
    rc = cli.main(["exec", "--detached-launcher", "--", sys.executable, "-c", "pass"])
    assert rc == 0
    err = capsys.readouterr().err
    assert f"PROBE_AGENT_SESSION=claude_code:{SID}" in err
    assert "PROBE_RUN_ID=" in err
