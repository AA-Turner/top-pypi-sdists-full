"""The OS keeper starts the Probe service again after a crash (plan D35).

The system's own scheduler (a systemd user timer, a launchd agent) runs
`python -m probe.service.keeper` every minute; it starts a service only when
a session the service recorded still has its agent running and none answers.
The units are written in a throwaway home with `systemctl`/`launchctl`
stood in by recording fakes: no test touches this account's real user manager.
"""

from __future__ import annotations

import json
import os
import plistlib
import sys
from pathlib import Path

import pytest

from probe.service import keeper, paths, recorders
from tests.service_harness import kill_agent, service_home, spawn_agent, wait_for  # noqa: F401

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the keeper is for macOS and Linux (Windows: R3)")


@pytest.fixture
def fake_tools(tmp_path, monkeypatch):
    """`systemctl` and `launchctl` that answer yes and record their calls."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "calls.jsonl"
    for name in ("systemctl", "launchctl"):
        script = bin_dir / name
        script.write_text(
            "#!/bin/sh\n"
            f"printf '%s\\n' \"$(python3 -c 'import json,sys; print(json.dumps(sys.argv[1:]))' {name} \"$@\")\" >> {calls}\n"
            'case "$*" in *is-active*) echo active ;; esac\n'
            "exit 0\n"
        )
        script.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{os.environ['PATH']}")
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "home" / ".config"))
    monkeypatch.setenv(keeper.ENV, "1")
    monkeypatch.setattr(keeper, "_own_home", lambda: True)
    monkeypatch.setattr(keeper, "_python", lambda: "/opt/probe/bin/python")

    def read():
        try:
            return [json.loads(line) for line in calls.read_text().splitlines()]
        except OSError:
            return []

    return read


def test_linux_gets_a_user_timer_written_once(fake_tools, monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "platform", "linux")
    assert keeper.install() == "installed"
    unit = (tmp_path / "home" / ".config" / "systemd" / "user" / "probe-service-keeper.service").read_text()
    timer = (tmp_path / "home" / ".config" / "systemd" / "user" / "probe-service-keeper.timer").read_text()
    assert 'ExecStart="/opt/probe/bin/python" -I -m probe.service.keeper' in unit
    assert "KillMode=process" in unit, "the service it starts outlives the oneshot"
    assert "OnUnitActiveSec=60s" in timer and "WantedBy=timers.target" in timer
    assert ["systemctl", "--user", "enable", "--now", "probe-service-keeper.timer"] in fake_tools()
    before = len(fake_tools())
    assert keeper.install() == "current"
    assert ["systemctl", "--user", "enable", "--now", "probe-service-keeper.timer"] not in fake_tools()[before:]
    keeper.remove()
    assert not (tmp_path / "home" / ".config" / "systemd" / "user" / "probe-service-keeper.timer").exists()
    assert ["systemctl", "--user", "disable", "--now", "probe-service-keeper.timer"] in fake_tools()


def test_macos_gets_a_launch_agent(fake_tools, monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "platform", "darwin")
    assert keeper.install() == "installed"
    plist = plistlib.loads((tmp_path / "home" / "Library" / "LaunchAgents" / f"{keeper.LABEL}.plist").read_bytes())
    assert plist["ProgramArguments"] == ["/opt/probe/bin/python", "-I", "-m", "probe.service.keeper"]
    assert plist["StartInterval"] == 60 and plist["RunAtLoad"] is False
    assert plist["AbandonProcessGroup"] is True
    assert any(c[:2] == ["launchctl", "bootstrap"] for c in fake_tools())


def test_never_for_a_home_that_is_not_the_accounts_own(monkeypatch, tmp_path):
    """A test's (or a sandbox's) HOME: this account's real user manager is never touched."""
    monkeypatch.setenv("HOME", str(tmp_path))
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
    once removed it stays removed until Probe is set up again (Codex R2)."""
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(paths, "home", lambda: tmp_path / "home")
    assert keeper.install() == "installed"
    keeper.remove()
    assert keeper.install() == "not wanted (uninstalled)"
    keeper.allow()
    assert keeper.install() == "installed"


def test_removal_never_touches_another_accounts_manager(fake_tools, monkeypatch):
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(keeper, "_own_home", lambda: False)
    keeper.remove()
    assert fake_tools() == [], "a test's (or a sandbox's) HOME never reaches the real user manager"


def test_systemctl_finds_the_user_manager_from_the_services_clean_environment(monkeypatch, tmp_path):
    """The service's environment has no XDG_RUNTIME_DIR or session bus (Codex R2)."""
    if not hasattr(os, "getuid"):
        pytest.skip("POSIX")
    runtime = tmp_path / "run"
    runtime.mkdir()
    (runtime / "bus").write_text("")
    monkeypatch.delenv("DBUS_SESSION_BUS_ADDRESS", raising=False)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(runtime))
    env = keeper._manager_env()
    assert env["XDG_RUNTIME_DIR"] == str(runtime)
    assert env["DBUS_SESSION_BUS_ADDRESS"] == f"unix:path={runtime / 'bus'}"
