"""The warm hook host (`hooks/zygote.py`) and the dispatcher's way to it (plan A0, D20, D28, D34, D36).

What these hold:
  * an event handed to the host runs exactly as it would have here: the
    route's output, its veto, its stderr, the session's environment and folder,
    the payload; and the route that walks up to its agent learns the harness's
    pid (PROBE_HOOK_PARENT_PID);
  * EXACTLY ONCE: a host that is not ready within the client's wait never runs
    the event, which runs here instead; one told to go is the only one that runs it;
  * a host lost after `G` reads as exit 0, never a veto, never a hang past the budget;
  * a route that overruns its deadline is killed with what it started;
  * the host exits when its service is gone or its dispatcher changes;
  * the service starts a host only for a Probe plugin folder (`hooks.host`).
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

AGENT = Path(__file__).resolve().parents[1]
HOOKS = AGENT / "plugins" / "probe-research" / "hooks"

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the hooks are POSIX shell")

_WHO = """import json, os, sys
print(json.dumps({"payload": sys.stdin.read(), "parent": os.environ.get("PROBE_HOOK_PARENT_PID"),
                  "hosted": os.environ.get("PROBE_HOOK_HOSTED"), "cwd": os.getcwd(), "x": os.environ.get("X_TEST")}))
"""


def _route(script: str) -> dict:
    return {"type": "command", "command": f"/bin/bash -c 'ROOT=\"${{PLUGIN_ROOT:-${{CLAUDE_PLUGIN_ROOT:-}}}}\"; exec python3 \"$ROOT/hooks/{script}\"'"}


def _plugin(tmp_path: Path, routes: dict, scripts: dict | None = None) -> Path:
    root = tmp_path / "plugin"
    hooks = root / "hooks"
    hooks.mkdir(parents=True)
    for name in ("dispatch.py", "dispatch.sh", "zygote.py", "_service_paths.py"):
        shutil.copy2(HOOKS / name, hooks / name)
    (hooks / "routes.json").write_text(json.dumps(routes))
    for name, body in (scripts or {}).items():
        (hooks / name).write_text(body)
    return root


def _socket(root: Path) -> str:
    sys.path.insert(0, str(HOOKS))
    try:
        import dispatch

        return dispatch.host_socket(str(root))
    finally:
        sys.path.pop(0)


@pytest.fixture
def host(tmp_path):
    """Start the host for a plugin folder; stop it at the end."""
    started = []

    def start(root: Path, service_pid: int | None = None) -> subprocess.Popen:
        path = _socket(root)
        proc = subprocess.Popen(
            [sys.executable, "-S", str(root / "hooks" / "zygote.py"), path, str(service_pid or os.getpid())],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        started.append((proc, path))
        deadline = time.monotonic() + 10
        while not os.path.exists(path):
            assert time.monotonic() < deadline, "the host never listened"
            assert proc.poll() is None, proc.stdout.read()
            time.sleep(0.02)
        return proc

    yield start
    for proc, path in started:
        proc.kill()
        proc.wait()
        if os.path.exists(path):
            os.unlink(path)


def _env(root: Path, **extra) -> dict:
    return {"PATH": os.environ["PATH"], "HOME": str(root.parent / "home"), "CLAUDE_PLUGIN_ROOT": str(root), **extra}


def _dispatch(root: Path, lane: str, payload: str, env: dict, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["/bin/bash", str(root / "hooks" / "dispatch.sh"), lane], input=payload,
                          capture_output=True, text=True, env=env, cwd=str(cwd or root.parent), timeout=30)


ROUTES = {"hooks": {
    "UserPromptSubmit": [{"lane": "prompt", "hooks": [_route("who.py")]}],
    "PreToolUse": [{"lane": "pre-tool", "matcher": "^Bash$",
                    "hooks": [{"type": "command", "command": "/bin/bash -c 'cat >/dev/null; echo blocked >&2; exit 2'"}]}],
}}


def test_a_hosted_event_runs_as_it_would_here(tmp_path, host):
    root = _plugin(tmp_path, ROUTES, {"who.py": _WHO})
    work = tmp_path / "work"
    work.mkdir()
    payload = '{"session_id": "s", "prompt": "hi"}\n'
    local = _dispatch(root, "prompt", payload, _env(root, X_TEST="1", PROBE_HOOK_HOST="off"), cwd=work)
    host(root)
    hosted = _dispatch(root, "prompt", payload, _env(root, X_TEST="1"), cwd=work)
    assert local.returncode == hosted.returncode == 0, (local.stderr, hosted.stderr)
    here, there = json.loads(local.stdout), json.loads(hosted.stdout)
    assert there["hosted"] == "1" and here["hosted"] is None
    assert there["parent"] and int(there["parent"]) > 1  # the harness's pid, for the agent lookup
    for key in ("payload", "cwd", "x"):
        assert here[key] == there[key], key


def test_a_hosted_veto_is_a_veto_and_its_stderr_reaches_the_harness(tmp_path, host):
    root = _plugin(tmp_path, ROUTES, {"who.py": _WHO})
    host(root)
    vetoed = _dispatch(root, "pre-tool", '{"tool_name": "Bash"}', _env(root))
    assert (vetoed.returncode, vetoed.stderr.strip()) == (2, "blocked")


def test_a_tool_no_route_matches_never_reaches_the_host(tmp_path, host):
    root = _plugin(tmp_path, ROUTES, {"who.py": _WHO})
    proc = host(root)
    started = time.monotonic()
    result = _dispatch(root, "pre-tool", '{"tool_name": "Read"}', _env(root))
    assert result.returncode == 0 and result.stdout == ""
    assert time.monotonic() - started < 2
    assert proc.poll() is None


def _silent_host(path: str, *, answer: bytes | None, accepted: list) -> threading.Thread:
    """A stand-in host: accepts, reads, then answers `answer` (None: nothing) and
    records whether it was told to go."""
    os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
    if os.path.exists(path):
        os.unlink(path)
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(path)
    server.listen(4)

    def serve():
        conn, _ = server.accept()
        conn.settimeout(5)
        try:
            data, fds, _, _ = socket.recv_fds(conn, 1 << 20, 4)
            for fd in fds:
                os.close(fd)
            if answer is not None:
                time.sleep(0.05)
                conn.sendall(answer)
                accepted.append(conn.recv(1))
            else:
                time.sleep(1.0)  # past the client's wait
                try:
                    accepted.append(conn.recv(1))
                except OSError:
                    accepted.append(b"")
        finally:
            conn.close()
            server.close()
            os.unlink(path)

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    return thread


def test_a_host_not_ready_in_time_never_runs_the_event_which_runs_here(tmp_path):
    root = _plugin(tmp_path, ROUTES, {"who.py": _WHO})
    told = []
    thread = _silent_host(_socket(root), answer=None, accepted=told)
    started = time.monotonic()
    result = _dispatch(root, "prompt", '{"session_id": "s"}', _env(root, X_TEST="here"))
    elapsed = time.monotonic() - started
    thread.join(5)
    assert result.returncode == 0 and json.loads(result.stdout)["x"] == "here"  # ran here, once
    assert json.loads(result.stdout)["hosted"] is None
    assert told == [b""], "the host was never told to go"
    assert elapsed < 0.3 + 0.9  # the 300 ms wait, plus a python start or two


def test_a_host_lost_after_go_reads_as_success_never_a_veto(tmp_path):
    root = _plugin(tmp_path, ROUTES, {"who.py": _WHO})
    told = []
    thread = _silent_host(_socket(root), answer=b"R", accepted=told)
    result = _dispatch(root, "pre-tool", '{"tool_name": "Bash"}', _env(root))
    thread.join(5)
    assert told == [b"G"]
    assert result.returncode == 0 and result.stdout == ""  # the host owned it, and is gone: fail open


def test_a_route_past_its_deadline_is_killed_with_what_it_started(tmp_path, host):
    slow = {"hooks": {"UserPromptSubmit": [{"lane": "prompt", "hooks": [
        {"type": "command", "command": "/bin/bash -c 'cat >/dev/null; sleep 30; echo late'", "timeout": 1}]}]}}
    root = _plugin(tmp_path, slow)
    host(root)
    started = time.monotonic()
    result = _dispatch(root, "prompt", '{"session_id": "s"}', _env(root))
    assert time.monotonic() - started < 9 and "late" not in result.stdout
    assert result.returncode == 0


def test_the_host_leaves_when_its_service_is_gone_or_its_dispatcher_changes(tmp_path, host):
    root = _plugin(tmp_path, ROUTES, {"who.py": _WHO})
    gone = subprocess.Popen(["sleep", "30"])
    proc = host(root, service_pid=gone.pid)
    gone.kill()
    gone.wait()
    assert proc.wait(timeout=10) == 0
    proc = host(root)
    os.utime(root / "hooks" / "dispatch.py", (time.time() + 5, time.time() + 5))
    assert proc.wait(timeout=10) == 0


def test_the_service_hosts_only_a_probe_plugin_folder(tmp_path, monkeypatch):
    from probe.service import hookhosts

    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    hosts = hookhosts.HookHosts(lambda message: None)
    root = _plugin(tmp_path, ROUTES, {"who.py": _WHO})
    assert "refused" in hosts.host({"root": str(root)})  # no plugin manifest
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": "probe-research"}))
    assert "refused" in hosts.host({"root": "relative"})
    try:
        answer = hosts.host({"root": str(root)})
        assert answer == {"running": True, "started": True}, answer
        assert hosts.host({"root": str(root)}) == {"running": True, "started": False}
        path = hookhosts.host_socket(str(root))
        assert str(path) == _socket(root)
        deadline = time.monotonic() + 10
        while not path.exists():
            assert time.monotonic() < deadline
            time.sleep(0.02)
    finally:
        hosts.close()


# -- review fixes (R2: Claude critic, Codex) ------------------------------------------


def test_a_route_that_does_not_read_its_stdin_costs_the_hosted_event_nothing(tmp_path, host):
    """A fresh python3 ignores SIGPIPE; the host's child must too, or the
    dispatcher feeding a route that already exited is killed, and the event's
    context and veto are lost (critic P0: 37 of 40 real prompt events)."""
    lane = {"hooks": {"UserPromptSubmit": [{"lane": "prompt", "hooks": [
        {"type": "command", "command": "/bin/bash -c 'exit 0'"},
        {"type": "command", "command": "/bin/bash -c 'cat >/dev/null; echo \"{\\\"hookSpecificOutput\\\": {\\\"hookEventName\\\": \\\"UserPromptSubmit\\\", \\\"additionalContext\\\": \\\"ctx\\\"}}\"'"},
        {"type": "command", "command": "/bin/bash -c 'cat >/dev/null; echo no >&2; exit 2'"},
    ]}]}}
    root = _plugin(tmp_path, lane)
    payload = json.dumps({"session_id": "s", "prompt": "x" * 200_000})  # past any pipe buffer
    local = [_dispatch(root, "prompt", payload, _env(root, PROBE_HOOK_HOST="off")) for _ in range(3)]
    host(root)
    hosted = [_dispatch(root, "prompt", payload, _env(root)) for _ in range(6)]
    want = {(r.returncode, "ctx" in r.stdout) for r in local}
    assert want == {(2, True)} or want == {(2, False)}, [(r.returncode, r.stdout, r.stderr) for r in local]
    assert {(r.returncode, "ctx" in r.stdout) for r in hosted} == want


def test_an_event_the_host_will_not_start_runs_here(tmp_path, host):
    """Stopping between `R` and the fork: the host says `N`, never closes the
    event unread (lost)."""
    root = _plugin(tmp_path, ROUTES, {"who.py": _WHO})
    proc = host(root)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect(_socket(root))
    body = b"{}"
    header = {"v": 1, "argv": ["prompt"], "cwd": str(tmp_path), "env": _env(root), "parent": os.getpid(),
              "deadline": time.time() + 30, "payload": len(body)}
    socket.send_fds(sock, [json.dumps(header).encode() + b"\n" + body], [1, 2])
    assert sock.recv(1) == b"R"
    proc.send_signal(15)
    time.sleep(0.8)  # the host left its loop
    try:
        sock.sendall(b"G")
    except OSError:
        pass
    assert sock.recv(1) == b"N"
    sock.close()
    assert proc.wait(10) == 0


def test_a_caller_in_a_sandbox_is_never_hosted(tmp_path, host):
    """An agent's sandboxed tool command could hand the host an environment
    and PATH of its choosing, and run outside its sandbox: the host closes the
    connection at once, and the event runs where it is."""
    if not sys.platform.startswith("linux"):
        pytest.skip("no-new-privs is Linux's")
    root = _plugin(tmp_path, ROUTES, {"who.py": _WHO})
    host(root)
    script = (
        "import ctypes, socket, sys\n"
        "assert ctypes.CDLL(None, use_errno=True).prctl(38, 1, 0, 0, 0) == 0\n"  # PR_SET_NO_NEW_PRIVS
        "s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); s.settimeout(5); s.connect(sys.argv[1])\n"
        "try:\n"
        "    s.sendall(b'{\"v\": 1, \"payload\": 0}\\n'); got = s.recv(1)\n"
        "except (ConnectionResetError, BrokenPipeError):\n"  # refused before the write landed
        "    got = b''\n"
        "print(repr(got))\n"
    )
    confined = subprocess.run([sys.executable, "-c", script, _socket(root)], capture_output=True, text=True, timeout=20)
    assert confined.stdout.strip() == "b''", confined.stderr
    # And the dispatcher in that sandbox runs its event here, as before.
    result = _dispatch(root, "prompt", '{"session_id": "s"}', _env(root, X_TEST="free"))
    assert json.loads(result.stdout)["hosted"] == "1", "an unconfined caller is still hosted"


def test_another_events_pipes_are_not_held_open_by_a_slow_one(tmp_path, host):
    """Each child closes the stdout/stderr other events handed the host: a fast
    event's pipe ends when it does, not when a slow sibling exits."""
    lanes = {"hooks": {
        "UserPromptSubmit": [{"lane": "prompt", "hooks": [
            {"type": "command", "command": "/bin/bash -c 'cat >/dev/null; sleep 4'", "timeout": 10}]}],
        "PreToolUse": [{"lane": "pre-tool", "matcher": "^Bash$", "hooks": [
            {"type": "command", "command": "/bin/bash -c 'cat >/dev/null; echo quick'"}]}],
    }}
    root = _plugin(tmp_path, lanes)
    host(root)
    slow = subprocess.Popen(["/bin/bash", str(root / "hooks" / "dispatch.sh"), "prompt"], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=_env(root), cwd=str(tmp_path))
    slow.stdin.write(b'{"session_id": "s"}')
    slow.stdin.close()
    time.sleep(0.5)  # the slow one is running in the host
    started = time.monotonic()
    quick = _dispatch(root, "pre-tool", '{"tool_name": "Bash"}', _env(root))
    assert "quick" in quick.stdout
    assert time.monotonic() - started < 2.5, "the quick event's pipe stayed open behind the slow one"
    slow.wait(15)


# -- SessionEnd is never hosted (#3300 review) --------------------------------------


SESSION_END = {"hooks": {"SessionEnd": [{"lane": "session-end", "hooks": [_route("who.py")]}]}}


def test_session_end_runs_here_even_with_a_warm_host(tmp_path, host):
    """A host holds the harness's output pipes, so a stalled one kept Claude
    Code's 1.5 s SessionEnd phase open past the cutoff: SessionEnd runs here."""
    root = _plugin(tmp_path, SESSION_END, {"who.py": _WHO})
    host(root)
    result = _dispatch(root, "session-end", '{"session_id": "s", "reason": "exit"}', _env(root, X_TEST="end"))
    assert result.returncode == 0, result.stderr
    there = json.loads(result.stdout)
    assert there["hosted"] != "1" and there["x"] == "end"


@pytest.mark.parametrize(("codex", "bound"), [(False, 1.5), (True, 3.0)], ids=["claude-code", "codex"])
def test_a_stalled_host_is_never_asked_for_session_end(tmp_path, codex, bound):
    root = _plugin(tmp_path, SESSION_END, {"who.py": _WHO})
    told: list = []
    _silent_host(_socket(root), answer=None, accepted=told)
    env = _env(root)
    if codex:
        env = {**{k: v for k, v in env.items() if k != "CLAUDE_PLUGIN_ROOT"}, "PLUGIN_ROOT": str(root)}
    started = time.monotonic()
    result = _dispatch(root, "session-end", '{"session_id": "s"}', env)
    elapsed = time.monotonic() - started
    assert result.returncode == 0 and json.loads(result.stdout)["hosted"] != "1"
    assert told == [], "the host was asked"
    assert elapsed < bound, elapsed
