"""The 5 h live-run harness (`tests/live/`, `.github/workflows/live-run.yml`):
dispatched by hand only, and its Windows parts never run here.

The run itself lasts hours on three runners (release plan section 10, D24-D27,
D46), so nothing routine may start it: the workflow has `workflow_dispatch`
and nothing else, and no test lane collects its files (none is a `test_*.py`).
What this checks on every Linux run instead: the harness still loads and
answers `--help` on this Python, the workflow's defaults are the release run's
(300 min, all three systems, release r3), and the probe shim's Windows branch
(wait for `probe daemon worker`, never `os.execv`, which there exits at once
and made the tap's supervisor respawn ~100 workers) stays the Windows branch.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import types
from pathlib import Path

import pytest
import yaml

AGENT = Path(__file__).resolve().parents[1]
LIVE = AGENT / "tests" / "live"
WORKFLOW = AGENT.parent / ".github" / "workflows" / "live-run.yml"
HARNESS = ("live_run.py", "probe_shim.py", "session_agent.py", "standin_claude.py")


def _workflow() -> dict:
    # BaseLoader: PyYAML's default reads the `on:` key as True.
    return yaml.load(WORKFLOW.read_text(), Loader=yaml.BaseLoader)


def test_the_live_run_is_dispatched_by_hand_only():
    spec = _workflow()
    assert set(spec["on"]) == {"workflow_dispatch"}, "never on push, pull_request or a schedule"
    assert "TEMPORARY" not in WORKFLOW.read_text(), "a branch's temporary trigger or step came along"


def test_its_defaults_are_the_release_run():
    inputs = _workflow()["on"]["workflow_dispatch"]["inputs"]
    assert inputs["duration_minutes"]["default"] == "300"
    assert inputs["systems"]["default"] == "macos-latest,ubuntu-latest,windows-latest"
    assert inputs["release"]["default"] == "r3"


def test_no_test_lane_collects_the_harness():
    assert sorted(p.name for p in LIVE.glob("*.py")) == sorted(HARNESS)
    others = [p.name for p in WORKFLOW.parent.glob("*.y*ml") if p != WORKFLOW and "tests/live" in p.read_text()]
    assert others == [], "only live-run.yml runs the harness"


@pytest.mark.parametrize("name", HARNESS)
def test_the_harness_compiles_here(name):
    compile((LIVE / name).read_text(encoding="utf-8"), name, "exec")


def test_the_driver_loads_and_answers_help_without_windows():
    done = subprocess.run([sys.executable, str(LIVE / "live_run.py"), "--help"], capture_output=True, text=True,
                          timeout=60, check=False)
    assert done.returncode == 0, done.stderr
    assert "--smoke" in done.stdout and "--expect-hosted" in done.stdout


def _live_run():
    name = "_live_run_driver"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, LIVE / "live_run.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module  # before exec: its dataclasses look themselves up there
        spec.loader.exec_module(module)
    return sys.modules[name]


@pytest.fixture
def run(tmp_path):
    live_run = _live_run()
    return live_run.Run(live_run.parse_args(["--root", str(tmp_path / "root"), "--out", str(tmp_path / "out")]))


#: A command that leaves a grandchild holding its stdout and stderr, as `probe
#: service stop` (or a daemon worker) does, and prints that grandchild's pid.
_LEAVES_A_GRANDCHILD = (
    "import subprocess, sys; "
    "g = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)']); "
    "print(g.pid, flush=True)"
)


def _kill(pid_text: str) -> None:
    import contextlib
    import os
    import signal

    with contextlib.suppress(ValueError, OSError):
        os.kill(int(pid_text.split()[0]), signal.SIGKILL)


def test_a_command_whose_grandchild_keeps_its_output_does_not_hang_the_driver(run):
    """A pipe ends only when its last writer closes it: with pipes, the driver
    waited for the grandchild (POSIX: the whole timeout; Windows: forever)."""
    import os
    import time

    started = time.monotonic()
    done = run.run_cmd([sys.executable, "-c", _LEAVES_A_GRANDCHILD], env=dict(os.environ), timeout=30)
    try:
        assert time.monotonic() - started < 10, "the driver waited for the grandchild"
        assert done.returncode == 0 and done.stdout.split()[0].isdigit(), done
    finally:
        _kill(done.stdout)


def test_a_command_past_its_timeout_is_killed_and_reads_as_124(run):
    import os
    import time

    code = _LEAVES_A_GRANDCHILD.replace('print(g.pid, flush=True)', 'print(g.pid, flush=True); time.sleep(60)')
    code = code.replace("import subprocess, sys", "import subprocess, sys, time")
    started = time.monotonic()
    done = run.run_cmd([sys.executable, "-c", code], env=dict(os.environ), timeout=2)
    try:
        assert time.monotonic() - started < 15
        assert done.returncode == 124 and "timed out after 2s" in done.stderr
        assert done.stdout.split()[0].isdigit(), "what it printed before is kept"
    finally:
        _kill(done.stdout)


def test_a_hung_end_phase_still_writes_its_report_and_exits(run, monkeypatch, tmp_path):
    """Past `--end-budget-min` the watchdog names the step, writes the report from
    what the run has (marked partial) and exits 2: a Windows run sat 20+ min after
    its last upload and the job died with no report."""
    import json

    live_run = _live_run()
    exits = []
    monkeypatch.setattr(live_run.os, "_exit", exits.append)
    run.results = [{"id": "recording.complete", "status": "pass", "detail": "all there"}]
    run.step("cleanup")
    run.end_watchdog(0.0, 0.01)
    assert exits == [2]
    report = json.loads((tmp_path / "out" / "report.json").read_text())
    assert report["meta"]["result"] == "fail" and "`cleanup`" in report["meta"]["partial"]
    assert [c["id"] for c in report["checks"]] == ["recording.complete"], "what the run had is kept"
    assert any("cleanup" in e for e in report["harness_errors"])
    assert "PARTIAL: the end phase hung in cleanup" in (tmp_path / "out" / "summary.txt").read_text()


def test_an_end_phase_that_finishes_leaves_the_watchdog_quiet(run, monkeypatch):
    live_run = _live_run()
    monkeypatch.setattr(live_run.os, "_exit", lambda code: pytest.fail("the watchdog fired"))
    run.end_done.set()
    run.end_watchdog(0.0, 0.01)
    assert run.harness_errors == []


def test_a_report_that_is_only_slow_is_left_to_finish(run, monkeypatch):
    """Past the budget with the main thread inside its report (holding the lock):
    the watchdog waits for it, and a report that lands is the run's report."""
    import threading
    import time

    live_run = _live_run()
    exits = []
    monkeypatch.setattr(live_run.os, "_exit", exits.append)
    run._report_lock.acquire()
    watchdog = threading.Thread(target=run.end_watchdog, args=(0.0, 0.01))
    watchdog.start()
    time.sleep(0.3)  # past the budget, waiting for the lock
    run.end_done.set()
    run._report_lock.release()
    watchdog.join(10)
    assert not watchdog.is_alive() and exits == [] and run.harness_errors == []


def test_the_end_budget_covers_a_longer_final_wait(tmp_path):
    live_run = _live_run()
    default = live_run.Run(live_run.parse_args(["--root", str(tmp_path / "a")]))
    longer = live_run.Run(live_run.parse_args(["--root", str(tmp_path / "b"), "--final-wait-s", "600"]))
    assert default.end_budget_s() == 15 * 60
    assert longer.end_budget_s() > 600 + 240 + 90, "a healthy longer wait is not a hang"


def test_the_stand_in_worker_is_refused_on_windows(monkeypatch):
    """It holds its lock with fcntl (probe_shim.py), which Windows has not."""
    live_run = _live_run()
    monkeypatch.setattr(live_run, "WINDOWS", True)
    with pytest.raises(SystemExit):
        live_run.parse_args(["--daemon-session", "standin"])
    monkeypatch.setattr(live_run, "WINDOWS", False)
    assert live_run.parse_args(["--daemon-session", "standin"]).daemon_session == "standin"


def _shim():
    spec = importlib.util.spec_from_file_location("_live_probe_shim", LIVE / "probe_shim.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class _Exec(Exception):
    pass


@pytest.mark.parametrize("system", ["nt", "posix"])
def test_the_shim_waits_for_the_daemon_worker_on_windows_and_execs_it_elsewhere(system, tmp_path, monkeypatch):
    shim = _shim()
    calls = []

    def execv(path, argv):
        calls.append(("execv", argv))
        raise _Exec

    fake_os = types.ModuleType("os")
    fake_os.__dict__.update(vars(shim.os))
    fake_os.name, fake_os.execv = system, execv
    monkeypatch.setattr(shim, "os", fake_os)
    monkeypatch.setattr(shim.subprocess, "call", lambda argv: calls.append(("call", argv)) or 0)
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["probe", "daemon", "worker", "--session-id", "s1"])
    if system == "nt":
        assert shim.main() == 0
        assert [kind for kind, _ in calls] == ["call"], "Windows: a child the shim waits for"
    else:
        with pytest.raises(_Exec):
            shim.main()
        assert [kind for kind, _ in calls] == ["execv"], "elsewhere: exec'd in place"
    assert calls[0][1][1:] == ["daemon", "worker", "--session-id", "s1"]
