"""execute_kane_cli — the run-time walk of a branch nobody recorded.

kane-cli joins THIS Appium session (server URL + session id) and the agent
walks the objective; the driver is the same before and after. The verb raises
when it cannot hand off (smart off, no kane-cli, no session) and when kane-cli
ran and failed — an unrecorded branch that does not run is a test failure.
"""
import subprocess

import pytest

import testmu_appium
from testmu_appium import _config
from testmu_appium._errors import TestmuConfigError
from testmu_appium._helpers import kane_cli


class _Executor:
    _url = "https://mobile-hub.lambdatest.com/wd/hub"


class _Driver:
    command_executor = _Executor()
    session_id = "sess-123"


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    monkeypatch.setattr(_config, "smart_enabled", lambda: True)
    monkeypatch.setenv("LT_USERNAME", "u")
    monkeypatch.setenv("LT_ACCESS_KEY", "k")
    monkeypatch.setenv("TESTMUAI_ENV", "stage")
    monkeypatch.setattr(kane_cli.shutil, "which", lambda name: "/usr/local/bin/kane-cli")


def _spawn(monkeypatch, returncode=0, stderr=""):
    calls = []

    def run(cmd, **kw):
        calls.append((cmd, kw))
        return subprocess.CompletedProcess(cmd, returncode, stdout="ok", stderr=stderr)

    monkeypatch.setattr(kane_cli.subprocess, "run", run)
    return calls


def test_the_handoff_names_this_session_and_its_dialect(monkeypatch):
    calls = _spawn(monkeypatch)

    assert testmu_appium.execute_kane_cli(_Driver(), objective='@v16:"click on Sign In"') is True

    (cmd, kw), = calls
    assert cmd[:3] == ["/usr/local/bin/kane-cli", "run", '@v16:"click on Sign In"']
    assert cmd[3:9] == [
        "--appium-url", "https://mobile-hub.lambdatest.com/wd/hub",
        "--appium-session-id", "sess-123",
        "--target", "android",
    ]
    assert "--local" in cmd and "--agent" in cmd
    assert cmd[cmd.index("--env") + 1] == "stage"
    assert kw["timeout"] == kane_cli._TIMEOUT_S


def test_smart_off_is_refused_without_spawning(monkeypatch):
    monkeypatch.setattr(_config, "smart_enabled", lambda: False)
    calls = _spawn(monkeypatch)

    with pytest.raises(TestmuConfigError, match="smart mode is not enabled"):
        testmu_appium.execute_kane_cli(_Driver(), objective="x")
    assert calls == []


def test_no_kane_cli_on_path_is_refused_without_spawning(monkeypatch):
    monkeypatch.setattr(kane_cli.shutil, "which", lambda name: None)
    calls = _spawn(monkeypatch)

    with pytest.raises(TestmuConfigError, match="not on PATH"):
        testmu_appium.execute_kane_cli(_Driver(), objective="x")
    assert calls == []


def test_variable_references_in_the_objective_are_resolved(monkeypatch):
    calls = _spawn(monkeypatch)
    testmu_appium.set_var("username", "ada")

    testmu_appium.execute_kane_cli(_Driver(), objective="type {{username}} in the field")

    (cmd, _), = calls
    assert cmd[2] == "type ada in the field"


def test_the_binding_settings_are_reapplied_after_the_handoff(monkeypatch):
    _spawn(monkeypatch)
    applied = []
    from testmu_appium import _session
    monkeypatch.setattr(_session, "_apply_driver_settings", lambda driver: applied.append(driver))

    driver = _Driver()
    testmu_appium.execute_kane_cli(driver, objective="x")

    assert applied == [driver]


def test_settings_are_reapplied_even_when_the_branch_fails(monkeypatch):
    _spawn(monkeypatch, returncode=1, stderr="boom")
    applied = []
    from testmu_appium import _session
    monkeypatch.setattr(_session, "_apply_driver_settings", lambda driver: applied.append(driver))

    with pytest.raises(RuntimeError):
        testmu_appium.execute_kane_cli(_Driver(), objective="x")
    assert len(applied) == 1


def test_a_failed_branch_walk_raises(monkeypatch):
    _spawn(monkeypatch, returncode=2, stderr="objective not met")

    with pytest.raises(RuntimeError, match="exit 2.*objective not met"):
        testmu_appium.execute_kane_cli(_Driver(), objective="x")


def test_a_driver_without_a_session_is_refused(monkeypatch):
    _spawn(monkeypatch)

    class _NoSession(_Driver):
        session_id = None

    with pytest.raises(TestmuConfigError):
        testmu_appium.execute_kane_cli(_NoSession(), objective="x")


def test_the_url_falls_back_to_the_configured_endpoint(monkeypatch):
    calls = _spawn(monkeypatch)
    monkeypatch.setattr(_config, "run_target", "local", raising=False)
    monkeypatch.setitem(_config._config, "appium_url", "http://127.0.0.1:4723")

    class _Bare:
        command_executor = object()
        session_id = "s1"

    testmu_appium.execute_kane_cli(_Bare(), objective="x")
    (cmd, _), = calls
    assert cmd[cmd.index("--appium-url") + 1] == "http://127.0.0.1:4723"
