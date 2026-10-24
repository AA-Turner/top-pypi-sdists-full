"""The Probe service on Windows (plan R3, D17): a named pipe only this user
opens, Windows process identity, file locks, the service's folder under
%LOCALAPPDATA%, and the service recording sessions there.

Runs on Windows only (the `service-windows` CI job); every other system has
its own suites. A throwaway LOCALAPPDATA and USERPROFILE: nothing here reaches
the runner's real profile.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(os.name != "nt", reason="Windows only (plan R3)")


def _wait(predicate, timeout: float):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        value = predicate()
        if value:
            return value
        time.sleep(0.05)
    return predicate()


@pytest.fixture
def win_home(tmp_path, monkeypatch):
    from probe.service import client, paths

    local = tmp_path / "Local"
    profile = tmp_path / "profile"
    local.mkdir()
    profile.mkdir()
    monkeypatch.setenv("LOCALAPPDATA", str(local))
    monkeypatch.setenv("USERPROFILE", str(profile))
    monkeypatch.setenv("HOME", str(profile))
    monkeypatch.setenv("PROBE_SERVICE_DISCOVERY_S", "0")
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "30")
    monkeypatch.setenv("PROBE_SERVICE_KEEPER", "0")
    # Its own LOCALAPPDATA, so its own service folder, and so its own pipe.
    paths.private_dir(paths.service_dir())
    client.write_runtime(sys.executable, "test")
    started = []

    class Home:
        def start(self):
            client.ensure()
            answer = _wait(lambda: self.status(), 20)
            assert answer, self.log()
            started.append(answer["pid"])
            return answer

        def status(self):
            try:
                return client.call("service.status", {}, client="cli", client_version="test")
            except OSError:
                return None

        def log(self):
            try:
                return paths.log_path().read_text(encoding="utf-8")
            except OSError:
                return "(no log)"

    yield Home()
    for pid in started:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True, check=False)


def test_the_service_folder_and_pipe_are_this_users():
    from probe.service import paths, winpipe

    assert paths.WINDOWS
    assert str(paths.root_dir()).startswith(os.environ["LOCALAPPDATA"]) or "AppData" in str(paths.root_dir())
    sid = winpipe.user_sid()
    assert sid.startswith("S-1-")
    assert paths.pipe_name().startswith(r"\\.\pipe\probe-service-")
    assert paths._windows_guid(), "MachineGuid read from the registry"


def test_process_identity_is_the_creation_time_and_never_kills():
    from probe.service import procid

    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        start = _wait(lambda: procid.start_time(child.pid), 5)
        assert start and start.isdigit()
        assert procid.alive(child.pid, start) is True
        assert procid.exists(child.pid) is True
        assert procid.proc(child.pid).ppid == os.getpid()
        assert child.poll() is None, "asking about it never terminated it"
    finally:
        child.kill()
        child.wait()
    assert procid.alive(child.pid, start) is False
    assert procid.exists(child.pid) is False


def test_a_lock_is_per_open_handle(tmp_path):
    from probe.service import paths

    path = tmp_path / "x.lock"
    first = os.open(path, os.O_RDWR | os.O_CREAT)
    second = os.open(path, os.O_RDWR | os.O_CREAT)
    try:
        assert paths.try_lock(first) is True
        assert paths.try_lock(second) is False
        paths.unlock(first)
        assert paths.try_lock(second) is True
    finally:
        os.close(first)
        os.close(second)


def test_the_service_serves_its_pipe_and_registers_a_session(win_home):
    from probe.service import client

    status = win_home.start()
    assert status["state"] in ("running", "discovering", "grace")  # grace: nothing holds it yet
    agent = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    try:
        owner = _wait(lambda: client.owner_of(agent.pid), 5)
        assert owner
        answer = client.register("s-win", "claude_code", "inline", owner, 1)
        assert answer is not None
        listing = client.call("session.list", {}, client="cli", client_version="test")
        assert [s["sid"] for s in listing["sessions"]] == ["s-win"]
        agent.kill()
        agent.wait()
        assert _wait(lambda: client.call("session.list", {}, client="cli", client_version="test")["sessions"] == [],
                     10), "the owner's exit ends the session (the poll watcher)"
    finally:
        if agent.poll() is None:
            agent.kill()


def test_the_service_records_a_session_itself(win_home, tmp_path):
    """Plan A2 on Windows: no `tap watch`, no Git Bash wrapper."""
    from probe.service import client
    from tests.test_service_recorders import _params, _tap

    win_home.start()
    agent = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    try:
        owner = _wait(lambda: client.owner_of(agent.pid), 5)
        root = _tap(tmp_path / "tap", "0.10.0")
        params = _params("s-rec", owner, root, "0.10.0", tmp_path)
        params["env"]["HOME"] = os.environ["USERPROFILE"]
        answer = client.call("session.record", params, client="tap", client_version="0.10.0")
        assert answer["recording"] is True, answer
        events = Path(os.environ["USERPROFILE"]) / "recorded.jsonl"
        assert _wait(lambda: events.exists() and "started" in events.read_text(), 10), win_home.log()
        assert client.call("session.finish", {"sid": "s-rec", "wait": 5}, client="tap",
                           client_version="0.10.0") == {"recording": True, "finished": True}
        lines = [json.loads(line)["event"] for line in events.read_text().splitlines()]
        assert lines == ["started", "ended"]
    finally:
        agent.kill()


def test_another_users_pipe_is_never_trusted(monkeypatch):
    """The client checks the serving process's user (a pipe made first by
    someone else under the name)."""
    from probe.service import winpipe

    monkeypatch.setattr(winpipe, "process_sid", lambda pid: "S-1-5-21-0-0-0-500")
    name = rf"\\.\pipe\probe-service-test-{os.getpid()}"
    handle = winpipe.create_pipe(name, True)
    try:
        with pytest.raises(PermissionError):
            winpipe.connect(name, 2.0)
    finally:
        import _winapi

        _winapi.CloseHandle(handle)


def test_the_keeper_is_never_installed_under_another_profile():
    from probe.service import keeper

    os.environ[keeper.ENV] = "1"
    try:
        assert keeper.wanted() is False, "USERPROFILE is the test's"
    finally:
        os.environ[keeper.ENV] = "0"


def test_a_cli_update_stops_the_service_and_starts_it_again(win_home, monkeypatch):
    """Windows cannot replace a file the service holds open: the CLI's own
    updater stops it for the upgrade and starts it again after (R3)."""
    from probe.cli import upgrading, updater
    from probe.service import client

    first = win_home.start()
    seen = []

    def upgrade(install, current, target):
        seen.append(win_home.status())
        return updater.CliResult(True, True, False, current, current, "fake")

    monkeypatch.setattr(updater, "upgrade_cli", upgrade)
    with upgrading._service_stopped_on_windows(updater.Install(updater.Method.UV_TOOL)) as stopped:
        assert stopped is True
        upgrade(None, "1", "1")
        # A hook, a tap or the keeper asking meanwhile starts none.
        assert client.ensure() != client.Ensured.SPAWNED
        assert win_home.status() is None
    assert seen == [None], "nothing answered during the upgrade"
    again = _wait(lambda: win_home.status(), 20)
    assert again and again["pid"] != first["pid"]


def test_a_session_link_waits_on_the_pipe_and_registers_once(win_home, monkeypatch):
    """`select` takes sockets only on Windows: a link that used it on the pipe
    reconnected and registered again on every pass (thousands a second)."""
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap"))
    from tap import service_link
    from tap.service import client as tap_client

    win_home.start()
    calls = []
    real = tap_client.Connection.call

    def counting(self, method, params=None):
        calls.append(method)
        return real(self, method, params)

    monkeypatch.setattr(tap_client.Connection, "call", counting)
    agent = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    try:
        owner = _wait(lambda: tap_client.owner_of(agent.pid), 5)
        link = service_link.ServiceLink("s-link", harness="claude_code", mode_fn=lambda sid: "inline",
                                        owner_fn=lambda: owner, heartbeat_s=20).start()
        assert _wait(lambda: "session.register" in calls, 10), win_home.log()
        time.sleep(3)
        link.stop(5)
    finally:
        agent.kill()
    assert calls.count("session.register") == 1, calls[:20]


def test_the_keeper_task_runs_on_battery_too(tmp_path, monkeypatch):
    """Created from XML: `schtasks /SC MINUTE` takes the AC-only defaults."""
    from probe.service import keeper

    name = f"Probe keeper test {os.getpid()}"
    monkeypatch.setattr(keeper, "_task_name", lambda: name)
    monkeypatch.setattr(keeper, "_task_marker", lambda: tmp_path / "marker.txt")
    monkeypatch.setattr(keeper.paths, "root_dir", lambda: tmp_path)
    try:
        assert keeper._install_schtasks(sys.executable) == "installed"
        assert keeper._install_schtasks(sys.executable) == "current"
        shown = subprocess.run(["schtasks", "/Query", "/TN", name, "/XML"], capture_output=True, text=True,
                               check=False)
        assert shown.returncode == 0, shown.stderr
        assert "<DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>" in shown.stdout
        assert "<StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>" in shown.stdout
        assert "PT1M" in shown.stdout and "probe.service.keeper" in shown.stdout
    finally:
        keeper._remove_schtasks()
    gone = subprocess.run(["schtasks", "/Query", "/TN", name], capture_output=True, text=True, check=False)
    assert gone.returncode != 0


def test_an_action_child_runs_with_the_services_own_path():
    """No login shell on Windows: the child keeps the service's PATH as it is."""
    import asyncio

    from probe.service import loginenv

    env = asyncio.run(loginenv.child_env(vars=True))
    assert env == {"PATH": os.environ.get("PATH", "")}


def test_an_action_childs_events_are_read_on_windows(win_home, monkeypatch):
    """The proactor cannot read an ordinary pipe: a thread reads the child's
    events and hands them to the loop."""
    import asyncio

    from probe.service import children

    script = ("import json, sys; request = json.loads(sys.stdin.read());"
              "print(json.dumps({'event': 'progress', 'echo': request['n']}), flush=True);"
              "print('not json', flush=True);"
              "print(json.dumps({'event': 'done'}), flush=True); sys.exit(3)")
    monkeypatch.setattr(children, "core_argv", lambda action: [sys.executable, "-c", script])
    seen = []
    code = asyncio.run(children.run_events("test", {"n": 7}, on_event=seen.append))
    assert code == 3
    assert seen == [{"event": "progress", "echo": 7}, {"event": "done"}]


def test_a_hook_route_runs_under_git_bash(tmp_path, monkeypatch):
    """A lane with more than one route starts each through bash: `/bin/bash`
    is no file a native Python can start on Windows, and every such route
    failed there without a word."""
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "plugins" / "probe-research" / "hooks"))
    import dispatch

    bash = dispatch._bash()
    assert Path(bash).is_file() and "system32" not in bash.lower(), bash
    out = tmp_path / "ran.txt"
    command = ("/bin/bash -c 'printf \"%s %s\\n\" \"$(date +%s)\" \"${CLAUDE_PLUGIN_ROOT:-none}\" >> \"$OUT\"'")
    done = subprocess.run([bash, "-c", command], env={**os.environ, "OUT": str(out), "CLAUDE_PLUGIN_ROOT": "C:/x"},
                          capture_output=True, text=True, timeout=30, check=False)
    assert done.returncode == 0, done.stderr
    assert out.read_text().split()[1] == "C:/x"


def test_a_plain_python_route_starts_its_python_at_once(monkeypatch):
    """No bash in between for a plain python route on Windows: each bash start
    costs a few hundred milliseconds there, on every event."""
    hooks = Path(__file__).resolve().parents[1] / "plugins" / "probe-research" / "hooks"
    monkeypatch.syspath_prepend(str(hooks))
    import dispatch

    routes = json.loads((hooks / "routes.json").read_text(encoding="utf-8"))
    plain = [h for groups in routes["hooks"].values() for g in groups for h in g["hooks"]
             if dispatch.plain_route(h["command"])]
    assert plain
    argv, env = dispatch._route_argv(plain[0])
    assert argv[0] == sys.executable and Path(argv[1]).is_file() and env is not None


def test_session_end_signals_the_recorder_where_it_looks(tmp_path):
    """SessionEnd under Git Bash touches the end sentinel the service's
    recorder watches (`tap.config.shutdown_sentinel`): its name and folder."""
    import tempfile

    hooks = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap" / "hooks"
    monkey_dispatch = Path(__file__).resolve().parents[1] / "plugins" / "probe-research" / "hooks"
    sys.path.insert(0, str(monkey_dispatch))
    try:
        import dispatch

        bash = dispatch._bash()
    finally:
        sys.path.remove(str(monkey_dispatch))
    sid = f"s-end-{os.getpid()}"
    folder = Path(tempfile.gettempdir())
    for suffix in ("shutdown", "hosted"):
        (folder / f"probe-research-tap-watcher-{sid}.{suffix}").unlink(missing_ok=True)
    payload = json.dumps({"session_id": sid, "reason": "other", "hook_event_name": "SessionEnd"})
    done = subprocess.run([bash, str(hooks / "session-end.sh")], input=payload, capture_output=True, text=True,
                          timeout=60, check=False, env={**os.environ, "HOME": str(tmp_path)})
    assert done.returncode == 0, done.stderr
    names = sorted(p.name for p in folder.glob(f"probe-research-tap-watcher-{sid}*"))
    assert names == [f"probe-research-tap-watcher-{sid}.shutdown"], (names, done.stderr[-500:])


def test_cancel_reaches_a_child_in_its_own_group_and_nothing_else(tmp_path):
    """`action.cancel` on Windows: CTRL_BREAK to the action child's process
    group, which it gets as SIGBREAK (never TerminateProcess, which would cut
    a credentials write short). As in production: the sender is a process
    started with CREATE_NO_WINDOW (the service: a console of its own, hidden),
    the child in its own process group in that console."""
    seen, result = tmp_path / "break.txt", tmp_path / "result.txt"
    child = ("import signal, sys, time, pathlib\n"
             "def on(n, f):\n"
             f"    pathlib.Path(r'{seen}').write_text('break'); sys.exit(130)\n"
             "signal.signal(signal.SIGBREAK, on)\n"
             f"pathlib.Path(r'{seen}.ready').write_text('ready')\n"
             # Short sleeps, as the approval poll waits: a Windows sleep wakes
             # for Ctrl+C only, so the handler runs at the next wake.
             "for _ in range(300):\n"
             "    time.sleep(0.1)\n")
    sender = ("import signal, subprocess, sys, time, pathlib\n"
              f"child = subprocess.Popen([sys.executable, '-c', {child!r}], creationflags=0x00000200)\n"
              "deadline = time.monotonic() + 20\n"
              f"while not pathlib.Path(r'{seen}.ready').exists() and time.monotonic() < deadline:\n"
              "    time.sleep(0.05)\n"
              "child.send_signal(signal.CTRL_BREAK_EVENT)\n"
              "try:\n"
              "    code = child.wait(20)\n"
              "except subprocess.TimeoutExpired:\n"
              "    child.kill(); code = 'timeout'\n"
              f"pathlib.Path(r'{result}').write_text(str(code))\n")
    done = subprocess.run([sys.executable, "-c", sender], creationflags=0x08000000, timeout=60,  # CREATE_NO_WINDOW
                          capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stderr
    assert result.read_text() == "130", (result.read_text(), done.stderr)
    assert seen.read_text() == "break"


def test_a_json_run_ignores_ctrl_break_outside_its_approval_wait():
    import signal

    from probe.core import events

    with events.session(True):
        assert signal.getsignal(signal.SIGBREAK) == signal.SIG_IGN
        with events.interruptible():
            assert signal.getsignal(signal.SIGBREAK) is events._interrupt
        assert signal.getsignal(signal.SIGBREAK) == signal.SIG_IGN


def test_a_spawned_update_sees_its_parent_exit():
    # `os.kill(pid, 0)` answers nothing on Windows (a dead pid included), so the
    # update child spawned by a command waited its whole 30 min for it.
    from probe._shared import autoupdate

    gone = subprocess.Popen([sys.executable, "-c", "pass"])
    gone.wait(timeout=30)
    assert autoupdate.pid_is_alive(os.getpid())
    assert not autoupdate.pid_is_alive(gone.pid)
    started = time.monotonic()
    assert autoupdate.wait_for_pid_exit(gone.pid, timeout=10)
    assert time.monotonic() - started < 2


def test_a_detached_update_child_never_holds_its_command(tmp_path):
    import importlib

    cli_main = importlib.import_module("probe.cli.main")  # `probe.cli.main` the function shadows it
    pid_file = tmp_path / "child.pid"
    child = (f"import os, pathlib, time\npathlib.Path(r'{pid_file}').write_text(str(os.getpid()))\n"
             "time.sleep(30)\n")
    started = time.monotonic()
    cli_main._spawn_detached([sys.executable, "-c", child], dict(os.environ))
    assert time.monotonic() - started < 2, "the command waited on its update child"
    deadline = time.monotonic() + 20
    while not pid_file.exists() and time.monotonic() < deadline:
        time.sleep(0.1)
    pid = int(pid_file.read_text())
    try:
        from probe._shared import autoupdate

        assert autoupdate.pid_is_alive(pid), "the child runs on after its command returned"
    finally:
        import signal

        os.kill(pid, signal.SIGTERM)  # TerminateProcess


def test_the_service_starts_on_the_base_interpreter_never_a_venv_launcher(tmp_path):
    # The venv launcher runs its child in a KILL_ON_JOB_CLOSE job: the service
    # died, silently, with whatever ended its launcher (Windows live run).
    from probe.service import client

    venv = tmp_path / "v"
    subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(venv)], check=True, timeout=120)
    launcher = venv / "Scripts" / "python.exe"
    argv, env = client._without_venv_launcher([str(launcher), "-I", "-m", "probe.service"], {"HOME": "x"})
    assert os.path.normcase(argv[0]) != os.path.normcase(str(launcher))
    assert os.path.basename(argv[0]).lower() == "python.exe" and os.path.isfile(argv[0])
    assert argv[1:] == ["-I", "-m", "probe.service"]
    assert env == {"HOME": "x", "__PYVENV_LAUNCHER__": str(launcher)}
    done = subprocess.run([*argv[:2], "-c", "import sys; print(sys.prefix)"], env={**os.environ, **env},
                          capture_output=True, text=True, timeout=60)
    assert os.path.normcase(done.stdout.strip()) == os.path.normcase(str(venv)), done.stderr
    # Not a venv (no pyvenv.cfg beside it): unchanged.
    plain = str(tmp_path / "plain" / "Scripts" / "python.exe")
    assert client._without_venv_launcher([plain, "-I"], {}) == ([plain, "-I"], {})


def test_a_route_past_its_own_timeout_ends_with_what_it_started(tmp_path, monkeypatch):
    """A route over its timeout ends with its bash and the python that bash
    started (no process groups here: its tree, by pid), and run_all returns
    near the deadline rather than when the route would have finished."""
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "plugins" / "probe-research" / "hooks"))
    import dispatch
    from probe._shared import oscompat

    pidfile = tmp_path / "child.pid"
    script = tmp_path / "sleeper.py"
    script.write_text(f"import os, time\nopen(r'{pidfile}', 'w').write(str(os.getpid()))\ntime.sleep(60)\n")
    python = Path(sys.executable).as_posix()
    hook = {"command": f"'{python}' '{script.as_posix()}'", "timeout": 3}
    started = time.monotonic()
    results = dispatch.run_all([hook], b"{}", time.monotonic() + 20)
    took = time.monotonic() - started
    assert results[0][1] is None and took < 15, (results, took)
    pid = int(pidfile.read_text())

    def alive() -> bool:
        try:
            oscompat.probe_pid(pid)
        except ProcessLookupError:
            return False
        return True

    deadline = time.monotonic() + 10
    while alive() and time.monotonic() < deadline:
        time.sleep(0.2)
    assert not alive(), f"the route's python {pid} outlived its deadline"
