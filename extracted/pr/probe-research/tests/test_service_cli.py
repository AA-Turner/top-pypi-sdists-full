"""`probe service status|start|stop`, and the CLI's runtime.json record (plan T3, X2)."""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

from probe.service import paths
from tests.service_harness import service_home, wait_for  # noqa: F401 -- a fixture

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")


def _probe(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "probe.cli", "service", *args], capture_output=True, text=True, timeout=60
    )


def test_status_start_stop(service_home):
    down = _probe("status", "--json")
    assert down.returncode == 1 and json.loads(down.stdout) == {"running": False}
    started = _probe("start")
    assert started.returncode == 0, started.stderr
    status = _probe("status", "--json")
    assert status.returncode == 0
    body = json.loads(status.stdout)
    assert body["state"] in ("discovering", "running", "grace") and isinstance(body["pid"], int)
    stopped = _probe("stop")
    assert stopped.returncode == 0 and "stopped" in stopped.stdout
    assert service_home.wait_exit(body["pid"], 3.0)
    assert _probe("stop").stdout.strip() == "probe service: not running"


def test_start_records_this_interpreter_when_none_is(service_home):
    paths.runtime_path().unlink()
    started = _probe("start")
    assert started.returncode == 0, started.stderr
    assert json.loads(paths.runtime_path().read_text())["python"] == os.path.abspath(sys.executable)


def test_runtime_is_recorded_only_from_the_uv_tool_env(service_home, monkeypatch):
    from probe.cli import service_cli

    paths.runtime_path().unlink()
    monkeypatch.setattr(sys, "prefix", "/home/x/.venv")
    service_cli.record_runtime()
    assert not paths.runtime_path().exists()
    monkeypatch.setattr(sys, "prefix", "/home/x/.local/share/uv/tools/probe-research")
    service_cli.record_runtime()
    recorded = json.loads(paths.runtime_path().read_text())
    assert recorded["python"] == os.path.abspath(sys.executable) and recorded["cli_version"]
    stamp = paths.runtime_path().stat().st_mtime_ns
    service_cli.record_runtime()  # unchanged: not rewritten
    assert paths.runtime_path().stat().st_mtime_ns == stamp
    assert paths.runtime_path().stat().st_mode & 0o777 == 0o600


def test_status_says_what_the_updater_did(service_home):
    from probe.cli import service_cli

    _probe("start")
    shown = _probe("status")
    assert shown.returncode == 0, shown.stderr
    assert "  updates: automatic updates off, last check never" in shown.stdout
    line = service_cli.update_line(
        {"enabled": True, "in_progress": False, "last_check": 0, "last_result": {"ok": False},
         "next_check": 3600, "deferred": {"at": 0, "reason": "daemon_recording"}}
    )
    assert "(failed)" in line and "deferred" in line and "daemon_recording" in line and "next " in line
    assert service_cli.update_line({"in_progress": True, "step": "app"}) == "updating now (app)"
    _probe("stop")


def test_an_update_that_did_not_complete_reads_as_failed():
    """A record an older service wrote: the cycle `ok`, its CLI-and-plugins
    step done, but the update child said `complete: false` (live test C). Every
    surface reads it as failed: `probe service status`, `probe doctor`'s row,
    `probe status --json`'s `last_ok`."""
    from probe.cli import service_calls, service_cli

    last = {"ok": True, "steps": {"cli_and_plugins": {"state": "done", "exit_code": 0, "ok": True,
                                                       "complete": False}}}
    update = {"enabled": True, "in_progress": False, "last_check": 0, "last_result": last, "next_check": 3600}
    assert "(failed)" in service_cli.update_line(update)
    assert service_calls.cycle_ok(last) is False
    assert service_calls.cycle_ok({"ok": True, "steps": {"cli_and_plugins": {"state": "done", "complete": True}}})
    assert service_calls.cycle_ok({"ok": False}) is False and service_calls.cycle_ok(None) is None
    assert "(failed)" in service_calls.update_text({"enabled": True, "last_check": 0,
                                                   "last_ok": service_calls.cycle_ok(last)})


def test_start_refuses_while_an_uninstall_stopped_halfway_and_never_finishes_it(monkeypatch):
    """`probe service start` is no installer: an uninstall that stopped halfway
    is NOT finished from here (that would leave the CLI env this runs from on
    disk, tracked by nothing). It says `probe uninstall` finishes it, starts
    nothing, and exits 2; it names the finisher copy only once it exists."""
    from typer.testing import CliRunner

    from probe.cli import service_cli, uninstall
    from probe.service import client

    paths.private_dir(paths.uninstall_dir())
    paths.uninstall_barrier_path().write_text(json.dumps(
        {"v": 1, "pid": 999999999, "start": "1", "at": 0, "phase": "integrations", "plan": ""}))
    monkeypatch.setattr(uninstall, "finish_interrupted", lambda: pytest.fail("only an installer finishes it"))
    started = []
    monkeypatch.setattr(client, "ensure", lambda **kw: started.append(kw) or client.Ensured.SPAWNED)
    monkeypatch.setattr(service_cli, "record_runtime", lambda **kw: started.append("runtime"))
    result = CliRunner().invoke(service_cli.service_app, ["start"])
    assert result.exit_code == 2, result.output
    assert ("an uninstall of Probe stopped at its 'integrations' step and must be finished first: "
            "run `probe uninstall`" in result.output)
    assert "finisher.py" not in result.output
    assert not started and paths.uninstall_barrier_path().exists()
    (paths.uninstall_dir() / uninstall.FINISHER_NAME).write_text("")  # from "finishing" on, it may be named
    assert "finisher.py" in CliRunner().invoke(service_cli.service_app, ["start"]).output
    assert not started
