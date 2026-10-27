"""The OS keeper starts the Probe service again after a crash (plan D35).

The system's own scheduler (a systemd user timer, a launchd agent, a Task
Scheduler task on Windows) runs `python -m probe.service.keeper` every minute;
it starts a service only when a session the service recorded still has its
agent running and none answers. The units are written in a throwaway home with
`systemctl`/`launchctl`/`schtasks` stood in by recording fakes: no test touches
this account's real user manager or Task Scheduler (`test_service_windows.py`
makes one real task, and deletes it).
"""

from __future__ import annotations

import contextlib
import json
import os
import plistlib
import subprocess
import sys
from pathlib import Path

import pytest

from probe.service import keeper, lifeboat, paths, recorders
from tests.service_harness import kill_agent, service_home, spawn_agent, wait_for  # noqa: F401

WINDOWS = os.name == "nt"
#: Linux's and macOS's keepers, written through `systemctl`/`launchctl` stood
#: in by shell scripts on PATH: Windows starts no `#!` script (and has its own
#: keeper, a Task Scheduler task: the `schtasks` tests below).
POSIX_UNITS = pytest.mark.skipif(WINDOWS, reason="the systemctl/launchctl fakes are shell scripts on PATH, which "
                                 "Windows cannot start; its keeper is a scheduled task (the schtasks tests)")


@pytest.fixture
def fake_tools(tmp_path, monkeypatch):
    """`systemctl` and `launchctl` that answer yes and record their calls;
    on Windows `schtasks`, through `keeper._run` (no real task is made)."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "calls.jsonl"
    if WINDOWS:
        def run(argv):
            with open(calls, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(argv) + "\n")
            return subprocess.CompletedProcess(argv, 0, "", "")

        monkeypatch.setattr(keeper, "_run", run)
    for name in ("systemctl", "launchctl"):
        script = bin_dir / name
        script.write_text(
            "#!/bin/sh\n"
            f"printf '%s\\n' \"$(python3 -c 'import json,sys; print(json.dumps(sys.argv[1:]))' {name} \"$@\")\" >> {calls}\n"
            'case "$*" in *is-active*) echo active ;; esac\n'
            "exit 0\n"
        )
        script.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "home" / ".config"))
    monkeypatch.setenv(keeper.ENV, "1")
    monkeypatch.setattr(keeper, "_own_home", lambda: True)
    monkeypatch.setattr(keeper, "_python", lambda: "/opt/probe/bin/python")

    def boat(login=None) -> str:
        """The lifeboat's install, its wrapper only (`test_lifeboat.py` covers the rest)."""
        lifeboat.wrapper_path().parent.mkdir(parents=True, exist_ok=True)
        lifeboat.wrapper_path().write_text("#!/bin/sh\nexit 0\n")
        return "current"

    monkeypatch.setattr(lifeboat, "install", boat)

    def read():
        try:
            return [json.loads(line) for line in calls.read_text().splitlines()]
        except OSError:
            return []

    return read


@POSIX_UNITS
def test_linux_gets_a_user_timer_written_once(fake_tools, monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "platform", "linux")
    assert keeper.install() == "installed"
    unit = (tmp_path / "home" / ".config" / "systemd" / "user" / "probe-service-keeper.service").read_text()
    timer = (tmp_path / "home" / ".config" / "systemd" / "user" / "probe-service-keeper.timer").read_text()
    wrapper = tmp_path / "home" / ".local" / "state" / "probe" / "lifeboat" / "lifeboat.sh"
    assert f'ExecStart=/bin/sh "{wrapper}" keeper' in unit, "the lifeboat's wrapper, by its fixed path (B2)"
    assert "python" not in unit, "no release's interpreter is named: the wrapper finds it"
    assert "KillMode=process" in unit, "the service it starts outlives the oneshot"
    assert f"TimeoutStartSec={keeper.START_TIMEOUT_S}" in unit, "a stuck run never holds the timer off for good"
    assert "OnUnitActiveSec=60s" in timer and "WantedBy=timers.target" in timer
    assert ["systemctl", "--user", "enable", "--now", "probe-service-keeper.timer"] in fake_tools()
    before = len(fake_tools())
    assert keeper.install() == "current"
    assert ["systemctl", "--user", "enable", "--now", "probe-service-keeper.timer"] not in fake_tools()[before:]
    keeper.remove()
    assert not (tmp_path / "home" / ".config" / "systemd" / "user" / "probe-service-keeper.timer").exists()
    assert ["systemctl", "--user", "disable", "--now", "probe-service-keeper.timer"] in fake_tools()


@POSIX_UNITS
def test_macos_gets_a_launch_agent(fake_tools, monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "platform", "darwin")
    assert keeper.install() == "installed"
    plist = plistlib.loads((tmp_path / "home" / "Library" / "LaunchAgents" / f"{keeper.LABEL}.plist").read_bytes())
    wrapper = tmp_path / "home" / ".local" / "state" / "probe" / "lifeboat" / "lifeboat.sh"
    assert plist["ProgramArguments"] == ["/bin/sh", str(wrapper), "keeper"]
    assert plist["StartInterval"] == 60 and plist["RunAtLoad"] is False
    assert plist["AbandonProcessGroup"] is True
    assert any(c[:2] == ["launchctl", "bootstrap"] for c in fake_tools())


@POSIX_UNITS
def test_no_unit_names_a_wrapper_that_is_not_there(fake_tools, monkeypatch, tmp_path):
    """A lifeboat that could not be installed leaves the units as they were
    (an older release's keep working): a unit never names a missing file."""
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(lifeboat, "install", lambda login=None: "failed: OSError('disk full')")
    assert keeper.install() == "no lifeboat (lifeboat: failed: OSError('disk full'))"
    assert not (tmp_path / "home" / ".config" / "systemd" / "user" / "probe-service-keeper.service").exists()
    assert fake_tools() == []


@POSIX_UNITS
def test_an_uninstall_removes_the_lifeboat_too(fake_tools, monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "platform", "linux")
    assert keeper.install() == "installed"
    (lifeboat.root() / "current").mkdir()
    (lifeboat.root() / "current" / "handoff.py").write_text("HANDOFF_VERSION = 1\n")
    keeper.remove()
    assert not lifeboat.root().exists(), "no session start runs a lifeboat Probe was uninstalled from"


@pytest.mark.skipif(WINDOWS, reason="passwd entries are POSIX's")
def test_a_uid_with_no_passwd_entry_takes_an_owned_home_outside_every_temp_folder(monkeypatch, tmp_path):
    """A pod's uid is often the runtime's, with no passwd entry: `_own_home`
    used to say no, and no lifeboat was ever installed there. $HOME counts
    when it is an existing folder the uid owns, never under a temp folder (a
    test's or a sandbox's HOME, which this suite's is)."""
    import pwd

    def no_entry(uid):
        raise KeyError(f"getpwuid(): uid not found: {uid}")

    monkeypatch.setattr(pwd, "getpwuid", no_entry)
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    assert keeper._own_home() is False, "under the temp folder: a test's HOME"
    monkeypatch.setattr(keeper, "_temp_roots", lambda: ["/nonexistent-temp-root"])
    assert keeper._own_home() is True
    for bad in (str(tmp_path / "missing"), "relative/home", "/"):
        monkeypatch.setenv("HOME", bad)
        assert keeper._own_home() is False, bad
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setattr(keeper.os, "getuid", lambda: os.stat(home).st_uid + 1)
    assert keeper._own_home() is False, "a folder another uid owns"


def test_never_for_a_home_that_is_not_the_accounts_own(monkeypatch, tmp_path):
    """A test's (or a sandbox's) HOME: this account's real user manager is never touched."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))  # the home on Windows
    monkeypatch.setenv(keeper.ENV, "1")
    assert keeper.wanted() is False
    assert keeper.install() == "not wanted"


def test_it_starts_the_service_only_for_a_live_recorded_session(service_home, tmp_path):
    agent, owner = spawn_agent()
    try:
        assert keeper.main() == 0
        assert service_home.status() is None, "nothing recorded: nothing to start"
        paths.private_dir(paths.service_dir())
        (paths.service_dir() / recorders.RECORDERS_NAME).write_text(json.dumps(
            {"v": recorders.RECORDERS_VERSION, "sessions": [{"sid": "s1", "owner": owner}]}))
        assert keeper.needed() is True
        assert keeper.main() == 0
        assert wait_for(service_home.status, 10.0), "a recorded session's service is started again"
        kill_agent(agent)
        assert wait_for(lambda: keeper.needed() is False, 5.0)
    finally:
        kill_agent(agent)


def test_an_uninstall_keeps_the_keeper_off_until_a_setup(fake_tools, monkeypatch, tmp_path):
    """Uninstall races the service's own start, which installs the keeper:
    once removed it stays removed until Probe is set up again (Codex R2).
    POSIX through the Linux timer; Windows through its scheduled task."""
    if not WINDOWS:
        monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(paths, "home", lambda: tmp_path / "home")
    assert keeper.install() == "installed"
    keeper.remove()
    assert keeper.install() == "not wanted (uninstalled)"
    keeper.allow()
    assert keeper.install() == "installed"


def test_removal_never_touches_another_accounts_manager(fake_tools, monkeypatch):
    if not WINDOWS:
        monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(keeper, "_own_home", lambda: False)
    keeper.remove()
    assert fake_tools() == [], "a test's (or a sandbox's) HOME never reaches the real user manager"


@pytest.mark.skipif(not hasattr(os, "getuid"), reason="systemd's per-user runtime folder (/run/user/<uid>): Linux")
def test_systemctl_finds_the_user_manager_from_the_services_clean_environment(monkeypatch, tmp_path):
    """The service's environment has no XDG_RUNTIME_DIR or session bus (Codex R2)."""
    runtime = tmp_path / "run"
    runtime.mkdir()
    (runtime / "bus").write_text("")
    monkeypatch.delenv("DBUS_SESSION_BUS_ADDRESS", raising=False)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(runtime))
    env = keeper._manager_env()
    assert env["XDG_RUNTIME_DIR"] == str(runtime)
    assert env["DBUS_SESSION_BUS_ADDRESS"] == f"unix:path={runtime / 'bus'}"


def test_windows_gets_one_scheduled_task_written_from_its_xml(monkeypatch, tmp_path):
    """The Windows keeper (R3): `schtasks /Create /XML` (on battery too), not
    again while it is current, `/Delete` on removal. `schtasks` is stood in
    (`keeper._run`), so no real task is made on any system."""
    calls, xml = [], []

    def run(argv):
        calls.append(argv)
        if argv[:2] == ["schtasks", "/Create"]:
            xml.append(Path(argv[argv.index("/XML") + 1]).read_text(encoding="utf-16"))
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setattr(keeper, "_run", run)
    monkeypatch.setattr(paths, "root_dir", lambda: tmp_path)
    python = tmp_path / "env" / "python.exe"
    python.parent.mkdir()
    python.touch()
    python.with_name("pythonw.exe").touch()
    name = keeper._task_name()
    assert keeper._install_schtasks(str(python)) == "installed"
    assert calls[0][:5] == ["schtasks", "/Create", "/F", "/TN", name]
    (task,) = xml
    assert f"<Command>{python.with_name('pythonw.exe')}</Command>" in task, "pythonw: no console window"
    assert "<Arguments>-I -m probe.service.keeper</Arguments>" in task and "<Interval>PT1M</Interval>" in task
    assert "<DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>" in task
    assert not list(tmp_path.glob(".keeper-task.*.xml")), "the definition file goes"
    assert keeper._install_schtasks(str(python)) == "current"
    assert calls[-1] == ["schtasks", "/Query", "/TN", name] and len(xml) == 1
    keeper._remove_schtasks()
    assert calls[-1] == ["schtasks", "/Delete", "/F", "/TN", name]
    assert not (tmp_path / "keeper-task.txt").exists()


# -- `service_down` (crash-report plan B3) --------------------------------------------


@pytest.fixture
def down(service_home, monkeypatch):
    """A recorded session whose agent runs (the keeper is needed), reports on,
    and the report child stood in: what it would have been asked."""
    from probe.service import watch

    monkeypatch.setenv(watch.REPORTS_ENV, "1")
    agent, owner = spawn_agent()
    sent: list = []
    monkeypatch.setattr(watch, "report_blocking", lambda params: sent.append(params) or (0, {"sent": True, "id": "r-9"}))

    class Down:
        def record(self, **env):
            paths.private_dir(paths.service_dir())
            (paths.service_dir() / recorders.RECORDERS_NAME).write_text(json.dumps({
                "v": recorders.RECORDERS_VERSION,
                "sessions": [{"sid": "s1", "owner": owner, "env": {"HOME": str(service_home.home), **env}}],
            }))

        def log(self) -> list:
            return [line for line in service_home.log().splitlines() if "probe-service-keeper[" in line]

    d = Down()
    d.sent, d.owner = sent, owner
    d.record()
    try:
        yield d
    finally:
        kill_agent(agent)


@contextlib.contextmanager
def _wedged():
    """What a wedged service leaves: its address takes a connection and never
    answers. A UNIX socket's backlog; on Windows a pipe instance of the
    service's name that nobody reads (`winpipe`)."""
    if WINDOWS:
        import _winapi

        from probe.service import winpipe

        handle = winpipe.create_pipe(paths.pipe_name(), True)
        try:
            yield
        finally:
            _winapi.CloseHandle(handle)
        return
    import socket as socket_mod

    wedged = socket_mod.socket(socket_mod.AF_UNIX, socket_mod.SOCK_STREAM)
    wedged.bind(str(paths.socket_path()))
    wedged.listen(8)  # it takes connections into its backlog and never answers
    try:
        yield
    finally:
        wedged.close()
        paths.socket_path().unlink()


def test_a_hello_reply_is_an_answer_and_a_connect_alone_is_not(service_home):
    import time

    assert keeper._answers() == keeper.Down.NO_SERVICE
    paths.ensure_dirs()
    with _wedged():
        began = time.monotonic()
        assert keeper._answers() == keeper.Down.WEDGED
        assert time.monotonic() - began < keeper.HELLO_TIMEOUT_S + 2
    service_home.start()
    assert keeper._answers() is None


class Ticks:
    """The keeper's minutes: wall and monotonic time (`keeper._monotonic`) as the scheduler runs it."""

    def __init__(self, monkeypatch) -> None:
        self.wall, self.mono = 1_000_000.0, 500.0
        monkeypatch.setattr(keeper, "_monotonic", lambda: self.mono, raising=False)

    def settle(self, down, started=None, *, after: float = 60.0, asleep: float = 0.0) -> None:
        self.wall += after + asleep
        self.mono += after
        keeper._settle(down, started, now=self.wall)


def test_five_minutes_needed_and_unanswered_are_one_service_down_report_every_6_hours(down, monkeypatch):
    t = Ticks(monkeypatch)
    t.settle(keeper.Down.NO_SERVICE, "spawned", after=0)
    for _ in range(4):
        t.settle(keeper.Down.NO_SERVICE, "spawned")
    assert down.sent == [], "4 minutes are not 5"
    t.settle(keeper.Down.BACKOFF, "backoff")
    (params,) = down.sent
    assert params["auto"] is True and params["family"] == "service_down" and params["reason"] == "backoff"
    assert params["sid"] is None and params["env"] == {} and params["facts"]["down_s"] == 300
    t.settle(keeper.Down.BACKOFF, "backoff")
    t.settle(None)  # it answers again
    for _ in range(10):
        t.settle(keeper.Down.WEDGED, "running")
    assert len(down.sent) == 1, "one in the report's 6 h, down again or not"
    t.settle(keeper.Down.WEDGED, "running", after=keeper.REPORT_EVERY_S)  # a gap of 6 h: counted again from here
    for _ in range(5):
        t.settle(keeper.Down.WEDGED, "running")
    assert [p["reason"] for p in down.sent] == ["backoff", "wedged"]
    lines = down.log()
    assert any("none answers (no_service)" in line for line in lines)
    assert any("none answers (backoff)" in line for line in lines), "a new reason is a new line"
    assert any("answers again" in line for line in lines)
    assert sum("report service_down (backoff): sent r-9" in line for line in lines) == 1
    assert len([line for line in lines if "and none answers (wedged)" in line]) == 1, "one line per change"
    assert any("none answers (wedged) after a gap" in line for line in lines), "the 6 h gap restarted the count"


def _six_minutes_down(t: Ticks) -> None:
    t.settle(keeper.Down.NO_SERVICE, "spawned", after=0)
    for _ in range(6):
        t.settle(keeper.Down.NO_SERVICE, "spawned")


def test_a_live_session_that_turns_reports_off_stops_service_down(down, monkeypatch):
    down.record(PROBE_DIAGNOSTICS="off")
    _six_minutes_down(Ticks(monkeypatch))
    assert down.sent == []
    assert any("service_down (no_service) not reported: session s1 does not allow reports" in line
               for line in down.log())


def test_a_registered_session_that_said_nothing_stops_service_down(down, monkeypatch):
    """Every live session must say yes (R3-D7): an older tap's registration says nothing."""
    import time

    paths.registry_path().write_text(json.dumps({"v": 1, "saved_at": time.time(), "sessions": [{
        "sid": "old-tap", "harness": "claude_code", "mode": "inline", "owner": down.owner, "generation": 1,
        "registered_at": time.time(), "heartbeat_at": time.time(), "state_dir": None,
    }]}))
    _six_minutes_down(Ticks(monkeypatch))
    assert down.sent == []
    assert any("not reported: session old-tap does not allow reports" in line for line in down.log())


def test_main_counts_a_back_off_and_an_answer_clears_it(down, monkeypatch):
    from probe.service import client

    monkeypatch.setattr(keeper, "_answers", lambda: keeper.Down.NO_SERVICE)
    monkeypatch.setattr(client, "ensure", lambda **kw: client.Ensured.BACKOFF)
    assert keeper.main() == 0
    state = json.loads((paths.service_dir() / keeper.STATE_NAME).read_text())
    assert state["reason"] == keeper.Down.BACKOFF and state["ensure"] == "backoff"
    monkeypatch.setattr(keeper, "_answers", lambda: None)
    assert keeper.main() == 0
    assert "down_since" not in json.loads((paths.service_dir() / keeper.STATE_NAME).read_text())


def test_a_machine_that_slept_counts_only_the_minutes_it_was_awake_and_down(down, monkeypatch):
    """Review #2: down at the lid's close and down at its opening, an hour
    apart, are not an hour down: the count starts again after a gap."""
    t = Ticks(monkeypatch)
    t.settle(keeper.Down.NO_SERVICE, "spawned", after=0)
    t.settle(keeper.Down.NO_SERVICE, "spawned")
    t.settle(keeper.Down.NO_SERVICE, "spawned", asleep=3600)
    t.settle(keeper.Down.NO_SERVICE, "spawned")
    assert down.sent == []
    for _ in range(4):
        t.settle(keeper.Down.NO_SERVICE, "spawned")
    assert [p["facts"]["down_s"] for p in down.sent] == [300]


@pytest.mark.skipif(hasattr(os, "geteuid") and os.geteuid() == 0, reason="root writes a read-only folder")
def test_a_state_the_keeper_cannot_save_sends_no_report(down, monkeypatch):
    """Review #7: on a full disk the record of the last report is lost, and
    every minute would report again."""
    monkeypatch.setattr(keeper, "_monotonic", lambda: 5_000.0, raising=False)
    now = 1_000_000.0
    (paths.service_dir() / keeper.STATE_NAME).write_text(json.dumps({
        "down_since": now - 600, "reason": "no_service", "checked_at": now - 60, "checked_mono": 5_000.0 - 60,
        "down_for": 540,
    }))
    paths.log_path().touch()
    folder = paths.service_dir()
    with contextlib.ExitStack() as unsaved:
        if WINDOWS:
            # A folder's read-only flag stops nothing there; a reader holding
            # the record open (no FILE_SHARE_DELETE, as Python opens files)
            # fails the replace onto it.
            unsaved.enter_context(open(folder / keeper.STATE_NAME, "rb"))  # noqa: SIM115
        else:
            folder.chmod(0o500)  # nothing new can be written there
            unsaved.callback(folder.chmod, 0o700)
        for n in range(3):
            keeper._settle(keeper.Down.NO_SERVICE, "spawned", now=now + 30 * n)
    assert down.sent == []
    assert any("not reported: the keeper's state could not be saved" in line for line in down.log())
