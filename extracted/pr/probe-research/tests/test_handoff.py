"""The frozen hand-off (`probe._shared.handoff`): stage 1 and the lifeboat (plan A1, B1).

Nothing here installs anything for real or touches this machine's Probe:
`uv` is a fake on PATH that builds a fake environment (an executable
`bin/python` shell script that records the argv, the environment, its pid
and whether the install lock's fd reached it), the release manifest and
PyPI are a local `http.server`, and HOME, XDG_*, CLAUDE_CONFIG_DIR,
CODEX_HOME and PI_CODING_AGENT_DIR are tmp dirs. A stage 1 that would exec
runs either in a subprocess (`handoff.py --stage1`, the real exec) or with
`_exec` replaced (in-process, to read what it would have run).
"""

from __future__ import annotations

import fcntl
import json
import os
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from probe._shared import handoff

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="POSIX flock, exec and shebangs")

HANDOFF = Path(handoff.__file__)

_FAKE_PYTHON = """#!/bin/sh
if [ "$1" = "-I" ] && [ "$2" = "-c" ]; then
  # The hand-off's import check (`handoff.starts`), never recorded.
  [ -n "$FAKE_PY_IMPORT_FAIL" ] && { echo "ModuleNotFoundError: No module named 'probe.core.adopt'" >&2; exit 1; }
  [ -n "$FAKE_PY_IMPORT_SLEEP" ] && exec sleep "$FAKE_PY_IMPORT_SLEEP"
  [ -n "$FAKE_PY_IMPORT_KILLED" ] && kill -9 $$
  exit 0
fi
out="${FAKE_PY_OUT:-/dev/null}"
{
  echo "pid=$$"
  echo "argv=$*"
  echo "adopt=$PROBE_UPDATE_ADOPT"
  echo "fd=$PROBE_INSTALL_LOCK_FD"
  if [ -n "$PROBE_INSTALL_LOCK_FD" ] && [ -e "/proc/$$/fd/$PROBE_INSTALL_LOCK_FD" ]; then echo "fd_open=yes"; else echo "fd_open=no"; fi
  echo "trigger=$PROBE_HANDOFF_TRIGGER"
  echo "from=$PROBE_HANDOFF_FROM"
  echo "dropped=$PROBE_HANDOFF_DROPPED_WITH"
} > "$out.tmp" && mv "$out.tmp" "$out"
[ -n "$FAKE_PY_SLEEP" ] && sleep "$FAKE_PY_SLEEP"
exit 0
"""

_FAKE_UV = """#!{python}
import json, os, sys
from pathlib import Path

args = sys.argv[1:]
log = os.environ.get("FAKE_UV_LOG")
if log:
    with open(log, "a") as handle:
        handle.write(json.dumps({{"argv": args, "tool_dir": os.environ.get("UV_TOOL_DIR"),
                                  "bin_dir": os.environ.get("UV_TOOL_BIN_DIR")}}) + "\\n")
if args[:2] == ["tool", "dir"]:
    print(os.environ.get("FAKE_UV_TOOL_DIR", ""))
    sys.exit(0)
if args[:2] != ["tool", "install"]:
    sys.exit(2)
if os.environ.get("FAKE_UV_FAIL"):
    print("error: no solution", file=sys.stderr)
    sys.exit(1)
if os.environ.get("FAKE_UV_SLEEP"):
    import time
    time.sleep(float(os.environ["FAKE_UV_SLEEP"]))
if os.environ.get("FAKE_UV_FAIL_PYTHON") and "--python" in args:
    print("error: the requested interpreter is gone", file=sys.stderr)
    sys.exit(1)
if os.environ.get("FAKE_UV_FAIL_WITH") and "--with" in args:
    print("  x No solution found when resolving tool dependencies:", file=sys.stderr)
    print("  `-> wandb conflicts with probe-research", file=sys.stderr)
    sys.exit(1)
if os.environ.get("FAKE_UV_WITH_SAYS") and "--with" in args:
    print(os.environ["FAKE_UV_WITH_SAYS"], file=sys.stderr)
    sys.exit(2)
if os.environ.get("FAKE_UV_FAIL_IF") and any(os.environ["FAKE_UV_FAIL_IF"] in a for a in args):
    print("error: Distribution not found at: file:///gone/" + os.environ["FAKE_UV_FAIL_IF"], file=sys.stderr)
    sys.exit(2)
spec = next(a for a in args if a.startswith("probe-research["))
version = spec.split("==", 1)[1]
env = Path(os.environ["UV_TOOL_DIR"]) / "probe-research"
site = env / "lib" / "python3.12" / "site-packages"
(site / f"probe_research-{{version}}.dist-info").mkdir(parents=True, exist_ok=True)
(site / "probe" / "_shared").mkdir(parents=True, exist_ok=True)
(site / "probe" / "_shared" / "handoff.py").write_text("")
(env / "bin").mkdir(parents=True, exist_ok=True)
python = env / "bin" / "python"
python.write_text(Path(os.environ["FAKE_PYTHON_SRC"]).read_text())
python.chmod(0o755)
if os.environ.get("FAKE_UV_NO_RECEIPT"):
    sys.exit(0)
(env / "uv-receipt.toml").write_text("[tool]\\n")
sys.exit(int(os.environ.get("FAKE_UV_EXIT", "0")))
"""


def fake_env(env: Path, version: str, *, adopt_capable: bool = True, receipt: bool = True) -> Path:
    """A version env as uv leaves it: `bin/python` (the recording shell
    script), its dist-info, its receipt (uv writes it last) and (an
    adopt-capable release) this file."""
    env.mkdir(parents=True, exist_ok=True)
    if receipt:
        (env / "uv-receipt.toml").write_text("[tool]\n")
    site = env / "lib" / "python3.12" / "site-packages"
    (site / f"probe_research-{version}.dist-info").mkdir(parents=True, exist_ok=True)
    if adopt_capable:
        (site / "probe" / "_shared").mkdir(parents=True, exist_ok=True)
        (site / "probe" / "_shared" / "handoff.py").write_text("")
    (env / "bin").mkdir(parents=True, exist_ok=True)
    python = env / "bin" / "python"
    python.write_text(_FAKE_PYTHON)
    python.chmod(0o755)
    return env


class _Server:
    """The release manifest (`/v1/client-version`) and PyPI's JSON, each one
    an answer the test sets (a status and a body), counted."""

    def __init__(self) -> None:
        self.answers = {"/v1/client-version": (200, {"cli": {"latest": "0.2.0"}}),
                        "/pypi/probe-research/json": (200, {"info": {"version": "0.2.0"}})}
        self.hits: dict[str, int] = {}
        server = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):  # noqa: N802 - http.server's name
                server.hits[self.path] = server.hits.get(self.path, 0) + 1
                status, body = server.answers.get(self.path, (404, {}))
                data = json.dumps(body).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def log_message(self, *_args):
                pass

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def manifest(self, latest: str | None, status: int = 200) -> None:
        self.answers["/v1/client-version"] = (status, {"cli": {"latest": latest}} if latest else {})

    def pypi(self, version: str | None, status: int = 200) -> None:
        self.answers["/pypi/probe-research/json"] = (status, {"info": {"version": version}} if version else {})

    def close(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()


@pytest.fixture
def server():
    found = _Server()
    yield found
    found.close()


@pytest.fixture
def machine(tmp_path, monkeypatch, server):
    """A machine with today's CLI (0.1.0) as uv made it: the tool folder, the
    fake uv on PATH, env.json naming them, the fake manifest. Every home the
    code could reach is a tmp dir."""
    home = tmp_path / "home"
    home.mkdir()
    for name, value in {
        "HOME": home, "XDG_STATE_HOME": tmp_path / "xdg-state", "XDG_CONFIG_HOME": tmp_path / "xdg-config",
        "XDG_DATA_HOME": tmp_path / "xdg-data", "CLAUDE_CONFIG_DIR": tmp_path / "claude",
        "CODEX_HOME": tmp_path / "codex", "PI_CODING_AGENT_DIR": tmp_path / "pi",
    }.items():
        monkeypatch.setenv(name, str(value))
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy",
                 "UV_TOOL_DIR", "PROBE_UPDATE_ADOPT", "PROBE_INSTALL_LOCK_FD", "PROBE_HANDOFF_NOW",
                 "PROBE_HANDOFF_DROPPED_WITH", "FAKE_UV_FAIL", "FAKE_UV_FAIL_PYTHON", "FAKE_UV_FAIL_WITH",
                 "FAKE_UV_WITH_SAYS", "FAKE_UV_FAIL_IF", "FAKE_UV_NO_RECEIPT", "FAKE_UV_EXIT",
                 "FAKE_UV_SLEEP", "FAKE_PY_IMPORT_FAIL", "FAKE_PY_IMPORT_SLEEP", "FAKE_PY_IMPORT_KILLED"):
        monkeypatch.delenv(name, raising=False)
    tools = tmp_path / "share" / "uv" / "tools"
    fake_env(tools / handoff.DIST, "0.1.0")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_python = tmp_path / "fake-python.sh"
    fake_python.write_text(_FAKE_PYTHON)
    uv = bin_dir / "uv"
    uv.write_text(_FAKE_UV.format(python=sys.executable))
    uv.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    monkeypatch.setenv("FAKE_UV_LOG", str(tmp_path / "uv.log"))
    monkeypatch.setenv("FAKE_PYTHON_SRC", str(fake_python))
    monkeypatch.setenv("FAKE_PY_OUT", str(tmp_path / "exec.out"))
    monkeypatch.setenv(handoff.PYPI_URL_ENV, server.url + "/pypi/probe-research/json")

    class Machine:
        pass

    m = Machine()
    m.tmp, m.home, m.tools, m.uv, m.server = tmp_path, home, tools, uv, server
    m.root = tools.parent / handoff.VERSIONS_DIRNAME
    m.out = tmp_path / "exec.out"
    m.write_env = lambda **over: _write_env(m, **over)
    m.uv_calls = lambda: [json.loads(line) for line in (tmp_path / "uv.log").read_text().splitlines()] \
        if (tmp_path / "uv.log").exists() else []
    m.write_env()
    return m


def _write_env(m, **over) -> None:
    data = {
        "v": 1, "tools": str(m.tools), "versions_root": str(m.root), "uv": str(m.uv), "base_python": None,
        "active_python": str(m.tools / handoff.DIST / "bin" / "python"), "extras": ["all", "daemon"],
        "with": [], "python_request": None, "index_env": {}, "base_url": m.server.url,
        "auto_update": True, "managed": True, "socket": str(m.tmp / "no-service.sock"),
    }
    data.update(over)
    path = handoff.env_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


class Execd(Exception):
    def __init__(self, python, argv, env, fd):
        super().__init__("exec")
        self.python, self.argv, self.env, self.fd = Path(python), argv, env, fd


@pytest.fixture
def no_exec(monkeypatch):
    """In-process stage 1: what it would exec, raised instead (`Execd`)."""

    def fake(python, argv, env, fd, before_exec):
        if before_exec is not None:
            before_exec()
        raise Execd(python, argv, env, fd)

    monkeypatch.setattr(handoff, "_exec", fake)


def _parse(out: Path) -> dict:
    return dict(line.split("=", 1) for line in out.read_text().splitlines() if "=" in line)


def _wait_for(path: Path, timeout: float = 15.0) -> None:
    deadline = time.monotonic() + timeout
    while not path.exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    assert path.exists(), f"{path} never appeared"


# -- versions ------------------------------------------------------------------------


def test_only_plain_releases_compare():
    assert handoff.newer("0.10.0", "0.9.9") and handoff.newer("1.2.3.1", "1.2.3")
    assert not handoff.newer("1.2.3", "1.2.3.0")
    for odd in ("1.0.0rc1", "1.0", "v1.0.0", "1.0.0+local", "", None, "1.0.0.dev1"):
        assert not handoff.newer(odd, "0.0.1") and not handoff.newer("9.9.9", odd)


def test_the_selftest_needs_nothing_but_the_standard_library():
    done = subprocess.run([sys.executable, "-I", "-S", str(HANDOFF), "--selftest"], capture_output=True, text=True)
    assert done.returncode == 0, done.stderr


# -- the install lock ------------------------------------------------------------------


#: Argv tails that make a holder one of our updates (`handoff.holder_kind`), or not.
UPDATE_CHILD_ARGV = ["-m", "probe.core.run", "update"]
CLI_UPDATE_ARGV = ["/home/u/.local/bin/probe", "--base-url", "https://x.example", "wizard", "--action", "update"]
STRANGER_ARGV = ["notes-about-probe.core.run update"]


def _holder_script(root: Path, hold_s: float) -> str:
    return (
        "import fcntl, os, sys, time\n"
        f"fd = os.open({str(handoff.lock_path(root))!r}, os.O_RDWR | os.O_CREAT)\n"
        "fcntl.flock(fd, fcntl.LOCK_EX)\n"
        "print('held', flush=True)\n"
        f"time.sleep({hold_s})\n"
    )


def _holder(tmp_path: Path, root: Path, *, ours: bool = True, tail: list | None = None, hold_s: float = 60.0,
            new_group: bool = True) -> subprocess.Popen:
    """A process holding the install lock, its argv ending in `tail` (our
    update child's, or a stranger's). Ready once it prints."""
    root.mkdir(parents=True, exist_ok=True)
    tail = tail if tail is not None else (UPDATE_CHILD_ARGV if ours else STRANGER_ARGV)
    child = subprocess.Popen([sys.executable, "-c", _holder_script(root, hold_s), *tail], stdout=subprocess.PIPE,
                             text=True, start_new_session=new_group)
    assert child.stdout.readline().strip() == "held"
    return child


def _record(root: Path, pid: int, *, minutes_ago: float, awake_minutes: float | None = None) -> None:
    """The holder record, `minutes_ago` by the wall clock and `awake_minutes`
    (default the same) by the awake clock."""
    awake = minutes_ago if awake_minutes is None else awake_minutes
    (root / handoff.LOCK_RECORD_NAME).write_text(json.dumps({
        "pid": pid, "start": handoff.proc_start(pid), "cmd": " ".join(handoff.proc_argv(pid) or []),
        "at": time.time() - minutes_ago * 60, "mono": time.monotonic() - awake * 60}))


def _alive(pid: int) -> bool:
    return handoff.proc_start(pid) is not None


@pytest.mark.parametrize("argv, kind", [
    (["/usr/bin/python3", "-I", "-m", "probe.core.run", "update"], handoff.UPDATE_CHILD),
    (["python3", "-I", "/home/u/.local/state/probe/lifeboat/current/handoff.py", "--lifeboat"], handoff.HANDOFF_RUN),
    (["/home/u/.local/bin/probe", "update", "--yes"], handoff.CLI_UPDATE),
    (["python3", "/home/u/.local/bin/probe", "--base-url", "https://x", "wizard", "--yes", "--action", "update"],
     handoff.CLI_UPDATE),
    (["python3", "-I", "-m", "probe.cli", "wizard", "--action=update"], handoff.CLI_UPDATE),
    (["python3", "-m", "probe.cli.version_refresh", "--apply", "--no-daemon"], handoff.CLI_UPDATE),
    (["python3", "-m", "probe.cli.version_refresh", "--apply-if-newer"], handoff.CLI_UPDATE),
    (["python3", "-m", "probe.cli.version_refresh"], None),
    (["vim", "notes-about-probe.core.run update"], None),
    (["/home/u/.local/bin/probe", "wizard"], None),
    (["/home/u/.local/bin/probe", "log", "update"], None),
    (["python3", "-m", "probe.core.run", "status"], None),
    (["less", "handoff.py.orig"], None),
    ([], None),
])
def test_only_our_updates_are_recognized_token_by_token(argv, kind):
    assert handoff.holder_kind(argv) == kind


def test_a_free_lock_is_taken_and_names_its_holder(machine):
    fd = handoff.take_lock(machine.root, wait_s=0)
    try:
        assert fd is not None and handoff.holds(machine.root)
        record = json.loads((machine.root / handoff.LOCK_RECORD_NAME).read_text())
        assert record["pid"] == os.getpid() and record["start"] == handoff.proc_start(os.getpid())
        with handoff.install_lock(machine.root, wait_s=0):  # re-entrant in the holder
            pass
    finally:
        handoff.release_lock(fd)
    assert not handoff.holds(machine.root)


def test_a_live_holder_is_waited_for(machine):
    child = _holder(machine.tmp, machine.root, ours=False, hold_s=1.5)
    started = time.monotonic()
    fd = handoff.take_lock(machine.root, wait_s=30)
    try:
        assert fd is not None and time.monotonic() - started >= 1.0
    finally:
        handoff.release_lock(fd)
        child.wait(5)


def test_a_holder_that_is_not_our_update_is_never_stopped(machine):
    child = _holder(machine.tmp, machine.root, ours=False)
    try:
        _record(machine.root, child.pid, minutes_ago=90)
        assert handoff.take_lock(machine.root, wait_s=1.0) is None
        with pytest.raises(handoff.LockBusy):
            with handoff.install_lock(machine.root, wait_s=0.2):
                pass
        assert child.poll() is None
    finally:
        child.kill()
        child.wait(5)


def test_our_update_past_45_minutes_is_stopped_and_the_lock_taken(machine):
    child = _holder(machine.tmp, machine.root, ours=True)
    try:
        _record(machine.root, child.pid, minutes_ago=44)
        assert handoff.take_lock(machine.root, wait_s=1.0) is None  # not yet past it
        assert child.poll() is None
        _record(machine.root, child.pid, minutes_ago=46)
        fd = handoff.take_lock(machine.root, wait_s=20)
        assert fd is not None
        handoff.release_lock(fd)
        assert child.wait(5) == -15  # SIGTERM to the group it leads
    finally:
        if child.poll() is None:
            child.kill()


def test_a_holder_asleep_with_its_laptop_is_not_stale(machine):
    """45 min by the wall clock, 1 min awake: the machine slept over a running
    update, which has not run long at all."""
    child = _holder(machine.tmp, machine.root, ours=True)
    try:
        _record(machine.root, child.pid, minutes_ago=50, awake_minutes=1)
        assert handoff.take_lock(machine.root, wait_s=1.0) is None
        assert child.poll() is None
    finally:
        child.kill()
        child.wait(5)


def _group(tmp_path: Path, root: Path, tail: list) -> tuple[subprocess.Popen, int, int]:
    """A group leader (the service, say) with two children in ITS group: the
    lock holder (argv ending in `tail`) and a bystander. `(leader, holder pid,
    bystander pid)`."""
    root.mkdir(parents=True, exist_ok=True)
    script = (
        "import subprocess, sys, time\n"
        f"holder = subprocess.Popen([sys.executable, '-c', {_holder_script(root, 60)!r}, *{tail!r}],"
        " stdout=subprocess.PIPE, text=True)\n"
        "assert holder.stdout.readline().strip() == 'held'\n"
        "bystander = subprocess.Popen(['sleep', '60'])\n"
        "print(holder.pid, bystander.pid, flush=True)\n"
        "time.sleep(60)\n"
    )
    leader = subprocess.Popen([sys.executable, "-c", script], stdout=subprocess.PIPE, text=True, start_new_session=True)
    holder_pid, bystander_pid = (int(word) for word in leader.stdout.readline().split())
    return leader, holder_pid, bystander_pid


@pytest.mark.parametrize("tail", [UPDATE_CHILD_ARGV, CLI_UPDATE_ARGV])
def test_a_stale_holder_in_another_process_group_is_stopped_alone(machine, tail):
    """The service runs its update child in ITS process group: stopping the
    child must never take the service (or anything else in it) along."""
    leader, holder, bystander = _group(machine.tmp, machine.root, tail)
    try:
        assert os.getpgid(holder) == leader.pid != holder
        _record(machine.root, holder, minutes_ago=46)
        fd = handoff.take_lock(machine.root, wait_s=20)
        assert fd is not None
        handoff.release_lock(fd)
        assert not _alive(holder)
        assert _alive(bystander) and leader.poll() is None
    finally:
        os.killpg(leader.pid, 9)
        leader.wait(5)


def test_a_stale_cli_update_that_leads_its_group_is_stopped_by_pid(machine):
    """A person's `probe update` in a terminal leads its job's group: it alone
    is stopped (what it started is left to finish or fail on its own)."""
    child = _holder(machine.tmp, machine.root, tail=CLI_UPDATE_ARGV)
    try:
        assert os.getpgid(child.pid) == child.pid
        _record(machine.root, child.pid, minutes_ago=46)
        fd = handoff.take_lock(machine.root, wait_s=20)
        assert fd is not None
        handoff.release_lock(fd)
        assert child.wait(5) == -15
    finally:
        if child.poll() is None:
            child.kill()


# -- stage 1 ---------------------------------------------------------------------------


def test_nothing_newer_returns_to_the_caller(machine, no_exec):
    machine.server.manifest("0.1.0")
    answer = handoff.stage1("cli")
    assert answer["result"] == handoff.Result.CURRENT and answer["active"] == "0.1.0"
    assert machine.uv_calls() == [] and not handoff.holds(machine.root)


def test_a_newer_release_is_installed_beside_and_handed_the_update(machine, no_exec):
    with pytest.raises(Execd) as caught:
        handoff.stage1("session_start")
    run = caught.value
    target = machine.root / "0.2.0" / handoff.DIST
    assert run.python == target / "bin" / "python"
    assert run.argv == ["-m", "probe.core.run", "update"]
    assert run.env[handoff.ADOPT_ENV] == str(target)
    assert run.env[handoff.TRIGGER_ENV] == "session_start" and run.env[handoff.FROM_ENV] == "0.1.0"
    assert run.env[handoff.LOCK_FD_ENV] == str(run.fd) and handoff.DROPPED_WITH_ENV not in run.env
    (call,) = machine.uv_calls()
    assert call["argv"][:4] == ["tool", "install", "--refresh-package", "probe-research"]
    assert "probe-research[all,daemon]==0.2.0" in call["argv"]
    assert call["tool_dir"] == str(machine.root / "0.2.0") and call["bin_dir"] == str(machine.root / "0.2.0" / ".bin")
    # The running install is untouched: release code switches, never this.
    assert not (machine.tools / handoff.DIST).is_symlink()
    assert not handoff.holds(machine.root)  # an exec that did not happen gave it back


def test_a_complete_env_is_not_installed_again(machine, no_exec):
    fake_env(machine.root / "0.2.0" / handoff.DIST, "0.2.0")
    with pytest.raises(Execd):
        handoff.stage1("cli")
    assert machine.uv_calls() == []


def test_the_manifest_down_reads_pypi(machine, no_exec):
    machine.server.manifest(None, status=500)
    machine.server.pypi("0.3.0")
    with pytest.raises(Execd) as caught:
        handoff.stage1("cli")
    assert caught.value.env[handoff.ADOPT_ENV] == str(machine.root / "0.3.0" / handoff.DIST)


def test_neither_answering_changes_nothing(machine, no_exec):
    machine.server.manifest(None, status=503)
    machine.server.pypi(None, status=503)
    answer = handoff.stage1("cli")
    assert answer["result"] == handoff.Result.NO_TARGET
    assert machine.uv_calls() == [] and not (machine.root / "0.2.0").exists()


def test_the_active_version_is_what_the_tool_path_runs_not_its_folders_name(machine, no_exec):
    """A person ran `uv tool upgrade` through the link: the env in folder
    0.1.0 is 0.2.0 now. A manifest still at 0.2.0 is not newer (and one
    lagging behind never reads as a reason to install an older release)."""
    import shutil

    shutil.rmtree(machine.tools / handoff.DIST)
    upgraded = fake_env(machine.root / "0.1.0" / handoff.DIST, "0.2.0")
    (machine.tools / handoff.DIST).symlink_to(upgraded, target_is_directory=True)
    shutil.rmtree(upgraded / "lib/python3.12/site-packages/probe_research-0.1.0.dist-info", ignore_errors=True)
    assert handoff.Layout(machine.tools).active_version() == "0.2.0"
    assert handoff.stage1("cli")["result"] == handoff.Result.CURRENT
    assert machine.uv_calls() == []


def test_an_answer_that_is_not_http_is_no_answer(machine):
    """A proxy or a captive portal speaking garbage: http.client raises its
    own errors (not OSError), and the read is simply unanswered."""
    import socket

    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)

    def serve():
        conn, _ = listener.accept()
        conn.recv(4096)
        conn.sendall(b"garbage that is not a status line\r\n\r\n")
        conn.close()

    threading.Thread(target=serve, daemon=True).start()
    try:
        assert handoff.fetch_json(f"http://127.0.0.1:{listener.getsockname()[1]}/x", dict(os.environ)) is None
    finally:
        listener.close()


def test_a_manifest_naming_no_plain_release_is_not_newer(machine, no_exec):
    machine.server.manifest("0.2.0rc1")
    machine.server.pypi("0.1.0")
    assert handoff.stage1("cli")["result"] == handoff.Result.CURRENT


def _reject(machine, version: str, hours_ago: float, *, old_format: bool = False) -> None:
    at = time.time() - hours_ago * 3600
    machine.root.mkdir(parents=True, exist_ok=True)
    mark = at if old_format else {"at": at, "reason": "the new service did not answer"}
    (machine.root / handoff.ACTIVE_NAME).write_text(json.dumps({"rejected": {version: mark}}))


@pytest.mark.parametrize("old_format", [False, True])
def test_a_version_rejected_today_is_skipped(machine, no_exec, old_format):
    _reject(machine, "0.2.0", hours_ago=3, old_format=old_format)
    assert handoff.stage1("cli")["result"] == handoff.Result.REJECTED
    assert machine.uv_calls() == []


def test_a_rejection_expires_after_24_hours(machine, no_exec):
    _reject(machine, "0.2.0", hours_ago=25)
    with pytest.raises(Execd):
        handoff.stage1("cli")


def test_a_rejected_version_never_holds_off_a_newer_one(machine, no_exec):
    _reject(machine, "0.2.0", hours_ago=1)
    machine.server.manifest("0.3.0")
    with pytest.raises(Execd) as caught:
        handoff.stage1("cli")
    assert caught.value.env[handoff.ADOPT_ENV].endswith("/0.3.0/probe-research")


def test_a_python_pin_uv_cannot_use_is_retried_with_uvs_own(machine, no_exec, monkeypatch):
    machine.write_env(python_request="/gone/bin/python3.12", **{"with": ["wandb>=0.17"]})
    monkeypatch.setenv("FAKE_UV_FAIL_PYTHON", "1")
    with pytest.raises(Execd) as caught:
        handoff.stage1("cli")
    first, second = machine.uv_calls()
    assert "--python" in first["argv"] and "--python" not in second["argv"]
    assert second["argv"][-2:] == ["--with", "wandb>=0.17"]  # kept
    assert handoff.DROPPED_WITH_ENV not in caught.value.env


def test_with_packages_that_will_not_resolve_are_left_out_and_named(machine, no_exec, monkeypatch):
    machine.write_env(**{"with": ["wandb>=0.17", "torch"]})
    monkeypatch.setenv("FAKE_UV_FAIL_WITH", "1")
    with pytest.raises(Execd) as caught:
        handoff.stage1("cli")
    first, second = machine.uv_calls()
    assert "--with" in first["argv"] and "--with" not in second["argv"]
    assert json.loads(caught.value.env[handoff.DROPPED_WITH_ENV]) == ["wandb>=0.17", "torch"]


@pytest.mark.parametrize("said", [
    "error: Distribution not found at: file:///home/u/src/mine",
    "error: Git operation failed: Repository not found",
    "error: Failed to build `mine @ file:///home/u/src/mine`",
    "error: Failed to fetch: network unreachable",
])
def test_with_packages_are_left_out_last_whatever_failed(machine, no_exec, monkeypatch, said):
    """A deleted local path, a repository gone, a build that fails: any
    failure with the `--with` packages leaves them out as the LAST try, and
    names them -- the CLI never stays behind for a package of the person's
    (the next install tries them again first)."""
    machine.write_env(**{"with": ["mine @ file:///home/u/src/mine"]})
    monkeypatch.setenv("FAKE_UV_WITH_SAYS", said)
    with pytest.raises(Execd) as caught:
        handoff.stage1("cli")
    first, last = machine.uv_calls()
    assert "--with" in first["argv"] and "--with" not in last["argv"]
    assert json.loads(caught.value.env[handoff.DROPPED_WITH_ENV]) == ["mine @ file:///home/u/src/mine"]


def test_a_package_an_earlier_install_left_out_that_still_fails_is_left_out_again(machine, no_exec, monkeypatch):
    """Tried again first; failing, the same install goes on without it (and
    keeps the person's other `--with` packages)."""
    machine.root.mkdir(parents=True, exist_ok=True)
    (machine.root / handoff.ACTIVE_NAME).write_text(json.dumps({"dropped_with": ["gone-pkg"]}))
    machine.write_env(**{"with": ["wandb>=0.17"]})
    monkeypatch.setenv("FAKE_UV_FAIL_IF", "gone-pkg")
    with pytest.raises(Execd) as caught:
        handoff.stage1("cli")
    first, second = machine.uv_calls()
    assert first["argv"][-4:] == ["--with", "wandb>=0.17", "--with", "gone-pkg"]
    assert second["argv"][-2:] == ["--with", "wandb>=0.17"]
    assert json.loads(caught.value.env[handoff.DROPPED_WITH_ENV]) == ["gone-pkg"]


def test_the_attempts_go_from_as_recorded_to_no_with_at_all():
    assert handoff.attempts(["a"], ["b"], "/py") == [(["a", "b"], "/py"), (["a", "b"], None), (["a"], None),
                                                      ([], None)]
    assert handoff.attempts([], [], None) == [([], None)]
    assert handoff.attempts(["A_b>=1"], ["a-b"], None) == [(["A_b>=1"], None), ([], None)]


def test_with_packages_an_earlier_install_left_out_are_tried_first(machine, no_exec):
    machine.root.mkdir(parents=True, exist_ok=True)
    (machine.root / handoff.ACTIVE_NAME).write_text(json.dumps({"dropped_with": ["torch==2.4", "wandb"]}))
    machine.write_env(**{"with": ["wandb>=0.17"]})
    with pytest.raises(Execd) as caught:
        handoff.stage1("cli")
    (call,) = machine.uv_calls()
    assert call["argv"][-4:] == ["--with", "wandb>=0.17", "--with", "torch==2.4"]  # wandb once
    assert handoff.DROPPED_WITH_ENV not in caught.value.env


def test_an_install_uv_says_failed_is_not_used(machine, no_exec, monkeypatch):
    """uv exited non-zero though the files are there: not an install."""
    monkeypatch.setenv("FAKE_UV_EXIT", "1")
    answer = handoff.stage1("cli")
    assert answer["result"] == handoff.Result.INSTALL_FAILED
    assert not (machine.root / "0.2.0").exists()


def test_a_half_finished_env_is_installed_again(machine, no_exec):
    """No receipt (uv writes it last): an install cut short, never exec'd as it is."""
    fake_env(machine.root / "0.2.0" / handoff.DIST, "0.2.0", receipt=False)
    with pytest.raises(Execd):
        handoff.stage1("cli")
    assert len(machine.uv_calls()) == 1
    assert (machine.root / "0.2.0" / handoff.DIST / "uv-receipt.toml").exists()


def test_an_env_whose_update_does_not_import_is_deleted_never_execd(machine, no_exec, monkeypatch):
    """It would die before it could reject itself, and every later update
    would exec it again: deleted, so the next update installs it afresh."""
    monkeypatch.setenv("FAKE_PY_IMPORT_FAIL", "1")
    answer = handoff.stage1("cli")
    assert answer["result"] == handoff.Result.INSTALL_FAILED and "does not start" in answer["detail"]
    assert "probe.core.adopt" in answer["detail"]
    assert not (machine.root / "0.2.0").exists()
    assert (machine.tools / handoff.DIST).is_dir()  # the active one untouched


def test_an_import_check_that_cannot_run_keeps_the_env_for_the_next_try(machine, no_exec, monkeypatch):
    """A timeout on a loaded machine is the machine's, not the release's: the
    env is not exec'd now, and not deleted either."""
    monkeypatch.setattr(handoff, "IMPORT_TIMEOUT_S", 0.5)
    monkeypatch.setenv("FAKE_PY_IMPORT_SLEEP", "5")
    answer = handoff.stage1("cli")
    assert answer["result"] == handoff.Result.UNCHECKED and "timed out" in answer["detail"]
    assert handoff.complete(machine.root / "0.2.0" / handoff.DIST, "0.2.0")
    monkeypatch.delenv("FAKE_PY_IMPORT_SLEEP")
    with pytest.raises(Execd):
        handoff.stage1("cli")
    assert len(machine.uv_calls()) == 1  # not installed again


def test_an_import_check_killed_by_a_signal_keeps_the_env(machine, no_exec, monkeypatch):
    """The OOM killer is the machine's, not proof of a broken release."""
    monkeypatch.setenv("FAKE_PY_IMPORT_KILLED", "1")
    answer = handoff.stage1("cli")
    assert answer["result"] == handoff.Result.UNCHECKED and "killed by signal 9" in answer["detail"]
    assert handoff.complete(machine.root / "0.2.0" / handoff.DIST, "0.2.0")


def test_a_uv_that_times_out_ends_the_install(machine, no_exec, monkeypatch):
    """A hung uv is the machine or the network: the other tries would hang the
    same way, and four of them would outlast the service's 30 min."""
    monkeypatch.setattr(handoff, "UV_TIMEOUT_S", 0.5)
    monkeypatch.setenv("FAKE_UV_SLEEP", "5")
    machine.write_env(python_request="/gone/bin/python3.12", **{"with": ["wandb"]})
    answer = handoff.stage1("cli")
    assert answer["result"] == handoff.Result.INSTALL_FAILED and "timed out" in answer["detail"]
    assert len(machine.uv_calls()) == 1 and not (machine.root / "0.2.0").exists()


def test_the_tries_together_stay_within_the_budget(machine, no_exec, monkeypatch):
    monkeypatch.setattr(handoff, "INSTALL_BUDGET_S", 0)
    answer = handoff.stage1("cli")
    assert answer["result"] == handoff.Result.INSTALL_FAILED and "ran out" in answer["detail"]
    assert machine.uv_calls() == []


def test_an_install_that_fails_every_way_leaves_nothing(machine, no_exec, monkeypatch):
    monkeypatch.setenv("FAKE_UV_FAIL", "1")
    answer = handoff.stage1("cli")
    assert answer["result"] == handoff.Result.INSTALL_FAILED and "no solution" in answer["detail"]
    assert not (machine.root / "0.2.0").exists()


def test_the_caller_overrides_what_env_json_says(machine, no_exec, tmp_path):
    handoff.env_path().unlink()  # a release's first update: no env.json yet
    with pytest.raises(Execd):
        handoff.stage1("cli", tools=str(machine.tools), base_url=machine.server.url,
                       install_inputs={"extras": ["daemon"], "with": ["x==1"], "python_request": None,
                                       "uv": str(machine.uv)})
    (call,) = machine.uv_calls()
    assert "probe-research[all,daemon]==0.2.0" in call["argv"] and call["argv"][-2:] == ["--with", "x==1"]


def test_a_lock_another_live_update_holds_answers_busy(machine, no_exec):
    child = _holder(machine.tmp, machine.root, ours=False)
    try:
        assert handoff.stage1("cli", wait_s=0.5)["result"] == handoff.Result.BUSY
    finally:
        child.kill()
        child.wait(5)


def test_an_adopting_process_never_installs(machine, no_exec, monkeypatch):
    monkeypatch.setenv(handoff.ADOPT_ENV, str(machine.root / "0.2.0" / handoff.DIST))
    assert handoff.stage1("cli")["result"] == handoff.Result.ADOPT
    assert machine.uv_calls() == []


def test_no_uv_tool_install_is_not_ours_to_update(machine, no_exec):
    """A pip, pipx or project install has no uv tool env: nothing is asked,
    locked or written (plan D4: a researcher's own environment is never touched)."""
    import shutil

    shutil.rmtree(machine.tools / handoff.DIST)
    assert handoff.stage1("cli")["result"] == handoff.Result.NOT_MANAGED
    assert not machine.root.exists() and machine.server.hits == {} and machine.uv_calls() == []


def test_the_exec_keeps_the_pid_and_hands_over_the_lock(machine):
    """The real exec: `handoff.py --stage1` becomes the new env's
    `python -I -m probe.core.run update` in the same process (the service's
    barrier and its over-run killer name that pid), the lock fd open in it."""
    child = subprocess.Popen([sys.executable, "-I", str(HANDOFF), "--stage1", "--trigger", "cli"],
                             env={**os.environ, "FAKE_PY_SLEEP": "3"}, stdin=subprocess.DEVNULL,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        _wait_for(machine.out)
        seen = _parse(machine.out)
        assert seen["pid"] == str(child.pid)
        assert seen["argv"] == "-I -m probe.core.run update"
        assert seen["adopt"] == str(machine.root / "0.2.0" / handoff.DIST)
        assert seen["fd_open"] == "yes" and seen["from"] == "0.1.0" and seen["trigger"] == "cli"
        probe = os.open(handoff.lock_path(machine.root), os.O_RDWR)
        try:
            with pytest.raises(BlockingIOError):  # still held: by the exec'd process
                fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
        finally:
            os.close(probe)
    finally:
        out, err = child.communicate(timeout=20)
    assert child.returncode == 0, err
    fd = handoff.take_lock(machine.root, wait_s=0)  # free once it exited
    assert fd is not None
    handoff.release_lock(fd)


# -- the lifeboat ----------------------------------------------------------------------


T0 = 1_800_000_000.0


def _lifeboat(trigger: str, at: float, **env) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-I", str(HANDOFF), "--lifeboat", "--trigger", trigger],
        env={**os.environ, handoff.NOW_ENV: str(at), **env}, capture_output=True, text=True, timeout=60,
    )


def test_the_lifeboat_acts_after_12_hours_behind_by_its_own_clock(machine):
    done = _lifeboat("session", T0)
    assert done.returncode == 0, done.stderr
    state = handoff.read_state()
    assert state["first_seen_behind"] == T0 and state["behind_version"] == "0.2.0"
    assert state["last_manifest"] == {"latest": "0.2.0", "at": T0}
    hits = machine.server.hits.get("/v1/client-version", 0)
    assert _lifeboat("session", T0 + 600).returncode == 0
    assert machine.server.hits.get("/v1/client-version", 0) == hits  # at most hourly
    assert _lifeboat("session", T0 + 11 * 3600).returncode == 0
    assert machine.uv_calls() == [] and not handoff.acted_path().exists()
    assert handoff.read_state()["first_seen_behind"] == T0  # continuously behind

    assert _lifeboat("session", T0 + 12 * 3600 + 1).returncode == 0
    _wait_for(machine.out)  # the detached stage 1 installed 0.2.0 and handed it the update
    seen = _parse(machine.out)
    assert seen["trigger"] == handoff.Trigger.LIFEBOAT and seen["argv"] == "-I -m probe.core.run update"
    acted = json.loads(handoff.acted_path().read_text())
    assert acted["reason"] == "behind" and acted["from"] == "0.1.0" and acted["to"] == "0.2.0"
    assert acted["trigger"] == handoff.Trigger.LIFEBOAT
    assert handoff.read_state()["last_act"]["reason"] == "behind"


def test_the_lifeboat_clock_restarts_once_the_machine_is_current(machine):
    assert _lifeboat("session", T0).returncode == 0
    machine.server.manifest("0.1.0")
    assert _lifeboat("session", T0 + 2 * 3600).returncode == 0
    assert handoff.read_state()["first_seen_behind"] is None
    machine.server.manifest("0.2.0")
    assert _lifeboat("session", T0 + 4 * 3600).returncode == 0
    assert _lifeboat("session", T0 + 13 * 3600).returncode == 0
    assert handoff.read_state()["first_seen_behind"] == T0 + 4 * 3600
    assert machine.uv_calls() == []


@pytest.mark.parametrize("setting", [{"auto_update": False}, {"managed": False}])
def test_the_lifeboat_never_acts_with_updates_off_or_on_a_cli_it_does_not_manage(machine, setting):
    machine.write_env(**setting)
    (handoff.state_path()).write_text(json.dumps({"v": 1, "first_seen_behind": T0 - 24 * 3600}))
    for trigger in ("session", "keeper"):
        assert _lifeboat(trigger, T0).returncode == 0
    assert machine.server.hits == {} and machine.uv_calls() == [] and not handoff.acted_path().exists()
    assert json.loads(handoff.state_path().read_text())["first_seen_behind"] == T0 - 24 * 3600


def _refusing_socket(machine) -> str:
    """A service socket nothing listens on (the service exits when no session
    needs it): connecting is refused."""
    import socket

    path = machine.tmp / "service.sock"
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(str(path))
    sock.close()
    return str(path)


def test_a_silent_service_on_a_current_machine_changes_nothing(machine):
    """An idle machine's service has exited: 10 minutes of keeper runs with
    its socket refusing, nothing newer out, a previous version to go back to
    -- and the lifeboat neither switches, rejects nor installs anything. It
    asks the service for a check once (it has none of its own yet)."""
    import shutil

    machine.server.manifest("0.1.0")
    active = fake_env(machine.root / "0.1.0" / handoff.DIST, "0.1.0")
    previous = fake_env(machine.root / "0.0.9" / handoff.DIST, "0.0.9")
    shutil.rmtree(machine.tools / handoff.DIST)
    (machine.tools / handoff.DIST).symlink_to(active, target_is_directory=True)
    record = {"active": str(active), "previous": str(previous)}
    (machine.root / handoff.ACTIVE_NAME).write_text(json.dumps(record))
    check_out = machine.tmp / "check.out"
    machine.write_env(active_python=str(active / "bin" / "python"), socket=_refusing_socket(machine))

    assert _lifeboat("keeper", T0, FAKE_PY_OUT=str(check_out)).returncode == 0
    _wait_for(check_out)  # (c): `check-now --trigger keeper`, the service's own check
    assert _parse(check_out)["argv"] == "-I -m probe.service.client check-now --trigger keeper"
    check_out.unlink()
    for minute in range(1, 11):
        assert _lifeboat("keeper", T0 + 60 * minute, FAKE_PY_OUT=str(check_out)).returncode == 0
    time.sleep(1.0)
    state = handoff.read_state()
    assert state["service_down_since"] == T0 and state["last_act"] is None
    assert not check_out.exists()  # once per 6 h, not every minute
    assert json.loads((machine.root / handoff.ACTIVE_NAME).read_text()) == record  # nothing rejected
    assert not handoff.acted_path().exists() and machine.uv_calls() == []
    assert (machine.tools / handoff.DIST).resolve() == active.resolve()


def _answering_socket(machine) -> str:
    """A service socket that answers `service.hello`, as a live service does."""
    import socket

    path = machine.tmp / "live.sock"
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    listener.bind(str(path))
    listener.listen(4)

    def serve() -> None:
        while True:
            try:
                conn, _ = listener.accept()
            except OSError:
                return
            with conn:
                conn.recv(65536)
                conn.sendall(b'{"jsonrpc": "2.0", "id": 1, "result": {"service_version": "0.1.0"}}\n')

    threading.Thread(target=serve, daemon=True).start()
    return str(path)


def _check_asked(check_out: Path) -> bool:
    """Did a lifeboat run ask the service for a check (`check-now --trigger keeper`)?"""
    deadline = time.monotonic() + 10
    while not check_out.exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    return check_out.exists() and _parse(check_out)["argv"] == "-I -m probe.service.client check-now --trigger keeper"


def test_an_idle_service_asked_for_a_check_answers_and_nothing_is_rescued(machine):
    """Behind, the service silent: it is most often an idle machine (the
    service exits when no session needs it). The lifeboat ASKS, which starts
    the service; the service answers by the next run and updates the machine
    the usual way. No rescue, so no "rescued" alert for a routine update."""
    check_out = machine.tmp / "check.out"
    machine.write_env(socket=_refusing_socket(machine))
    assert _lifeboat("keeper", T0, FAKE_PY_OUT=str(check_out)).returncode == 0
    assert _check_asked(check_out) and handoff.read_state()["asked_at"] == T0
    machine.write_env(socket=_answering_socket(machine))  # the ask woke it
    for minute in (1, 6, 10):
        assert _lifeboat("keeper", T0 + 60 * minute).returncode == 0
    time.sleep(0.5)
    assert not handoff.acted_path().exists() and machine.uv_calls() == [] and not machine.out.exists()
    assert handoff.read_state()["last_act"] is None and handoff.read_state()["service_down_since"] is None


def test_a_service_long_silent_but_never_asked_is_asked_not_rescued(machine):
    """THE bug of HANDOFF_VERSION 1: an idle machine's service has been
    silent for hours (it exits when no session needs it) and a release comes
    out. v1 rescued it at once -- a routine update through the lifeboat, and
    a "rescued" alert per idle machine. v2 asks first."""
    check_out = machine.tmp / "check.out"
    machine.write_env(socket=_refusing_socket(machine))
    handoff.write_state({"v": 1, "first_seen_behind": T0 - 3600, "behind_version": "0.2.0",
                         "service_down_since": T0 - 6 * 3600, "last_keeper_check": T0 - 60})
    assert _lifeboat("keeper", T0, FAKE_PY_OUT=str(check_out)).returncode == 0
    assert _check_asked(check_out) and handoff.read_state()["asked_at"] == T0
    time.sleep(0.5)
    assert not handoff.acted_path().exists() and machine.uv_calls() == [] and not machine.out.exists()


def test_a_service_that_never_answers_the_ask_is_rescued_after_five_minutes(machine):
    """A service that crashes at start never answers the ask: 5 minutes on,
    with the machine still behind, the lifeboat installs the newest release
    (stage 1), not 12 h later."""
    check_out = machine.tmp / "check.out"
    machine.write_env(socket=_refusing_socket(machine))
    assert _lifeboat("keeper", T0, FAKE_PY_OUT=str(check_out)).returncode == 0
    assert _check_asked(check_out) and handoff.read_state()["asked_at"] == T0
    check_out.unlink()
    assert _lifeboat("keeper", T0 + 180, FAKE_PY_OUT=str(check_out)).returncode == 0  # asked 3 min ago: waits
    time.sleep(0.5)
    assert machine.uv_calls() == [] and not handoff.acted_path().exists() and not check_out.exists()

    assert _lifeboat("keeper", T0 + 360).returncode == 0
    _wait_for(machine.out)
    seen = _parse(machine.out)
    assert seen["adopt"] == str(machine.root / "0.2.0" / handoff.DIST) and seen["trigger"] == handoff.Trigger.LIFEBOAT
    acted = json.loads(handoff.acted_path().read_text())
    assert acted["reason"] == "service_down" and acted["from"] == "0.1.0" and acted["to"] == "0.2.0"
    assert "rejected" not in handoff.Layout(machine.tools).record()


def test_an_ask_older_than_half_an_hour_is_asked_again_not_acted_on(machine):
    """A silence half an hour after an ask says nothing about the service
    now (it answered, did its update, and went idle again): ask afresh."""
    check_out = machine.tmp / "check.out"
    machine.write_env(socket=_refusing_socket(machine))
    handoff.write_state({"v": 1, "first_seen_behind": T0 - 3600, "behind_version": "0.2.0",
                         "asked_at": T0 - 31 * 60, "last_keeper_check": T0 - 60})
    assert _lifeboat("keeper", T0, FAKE_PY_OUT=str(check_out)).returncode == 0
    assert _check_asked(check_out) and handoff.read_state()["asked_at"] == T0
    time.sleep(0.5)
    assert not handoff.acted_path().exists() and machine.uv_calls() == [] and not machine.out.exists()


def test_a_current_machine_with_a_silent_service_is_not_asked(machine):
    """Not behind: nothing to bring forward, so no ask (and, its own check
    recent, no check either), whatever the socket says."""
    check_out = machine.tmp / "check.out"
    machine.server.manifest("0.1.0")
    machine.write_env(socket=_refusing_socket(machine))
    handoff.write_state({"v": 1, "last_keeper_check": T0 - 60})
    for minute in (0, 6, 40):
        assert _lifeboat("keeper", T0 + 60 * minute, FAKE_PY_OUT=str(check_out)).returncode == 0
    time.sleep(0.5)
    assert handoff.read_state()["asked_at"] is None and not check_out.exists()
    assert not handoff.acted_path().exists() and machine.uv_calls() == []


def test_a_rescue_waits_an_hour_only_to_retry_the_same_release(machine):
    """A rescue of 0.2.0 failed (an uninstallable wheel) a minute ago: 0.2.0
    is not tried again within the hour, but 0.3.0, out since, is tried at once."""
    handoff.write_state({"v": 1, "first_seen_behind": T0 - 13 * 3600, "behind_version": "0.2.0",
                         "last_act": {"at": T0 - 60, "reason": "behind", "from": "0.1.0", "to": "0.2.0"}})
    assert _lifeboat("session", T0).returncode == 0
    time.sleep(0.5)
    assert not machine.out.exists() and machine.uv_calls() == []
    assert handoff.read_state()["last_act"]["at"] == T0 - 60

    machine.server.manifest("0.3.0")
    state = handoff.read_state()
    state["last_manifest"] = None  # read it again now
    handoff.write_state(state)
    assert _lifeboat("session", T0 + 60).returncode == 0
    _wait_for(machine.out)
    assert _parse(machine.out)["adopt"] == str(machine.root / "0.3.0" / handoff.DIST)
    assert handoff.read_state()["last_act"]["to"] == "0.3.0"


def test_an_offline_lifeboat_reads_the_manifest_at_most_hourly(machine):
    machine.server.manifest(None, status=503)
    machine.server.pypi(None, status=503)
    for minute in range(3):
        assert _lifeboat("session", T0 + 60 * minute).returncode == 0
    assert machine.server.hits == {"/v1/client-version": 1, "/pypi/probe-research/json": 1}
    assert handoff.read_state()["first_seen_behind"] is None
