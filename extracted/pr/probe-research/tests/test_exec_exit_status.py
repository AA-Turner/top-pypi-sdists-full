"""How a wrapped child's exit becomes the run's status.

`probe exec` is the zero-instrumentation path: wrap a command, get crash alerts
without touching the script. That makes its exit mapping the only thing
standing between a researcher's own Ctrl-C and a crash email about it.
"""

from __future__ import annotations

import json
import signal
import subprocess
import sys
import time

import pytest

from probe.sdk.run import _status_for_exit
from tests.conftest import make_client, open_run
from tests.served_fake_app import child_env, serve

#: SIGKILL's number where the platform has none (Windows): the mapping under
#: test is arithmetic on exit codes, not a signal delivery.
_SIGKILL = int(getattr(signal, "SIGKILL", 9))

#: A child killed BY a signal, as a POSIX shell and `subprocess` report it.
#: Windows has no such death -- a "signal" there is TerminateProcess with an
#: exit code -- so the end-to-end signal tests are POSIX-only.
_posix_signals = pytest.mark.skipif(sys.platform == "win32", reason="POSIX signal deaths; Windows has none")


def test_a_clean_exit_completes() -> None:
    assert _status_for_exit(0) == "completed"


@pytest.mark.parametrize("code", [-signal.SIGINT, 128 + int(signal.SIGINT)])
def test_ctrl_c_is_canceled_not_failed(code: int) -> None:
    """SIGINT is a decision, not a defect -- the call `fluent.py` already makes
    for the in-process path when it maps KeyboardInterrupt.

    Both spellings: `subprocess.run` reports a signalled child as -N, and a
    shell in between reports 128+N.
    """
    assert _status_for_exit(code) == "canceled"


@pytest.mark.parametrize(
    "code",
    [1, 2, -_SIGKILL, 128 + _SIGKILL, -signal.SIGTERM, 128 + int(signal.SIGTERM)],
)
def test_everything_else_still_fails(code: int) -> None:
    """SIGTERM and SIGKILL stay failures on purpose. A scheduler preempting a
    job, an eviction, a kill from another session -- those are the deaths a
    researcher does NOT already know about, and they are what the crash email
    exists for. Only the interrupt the person typed is a decision.
    """
    assert _status_for_exit(code) == "failed"


def test_a_plain_exit_code_two_is_not_mistaken_for_sigint() -> None:
    """128+SIGINT is 130; a bare 2 is an ordinary non-zero exit and argparse's
    favourite. Conflating them would silence real failures."""
    assert _status_for_exit(2) == "failed"


# -- through `probe exec`, with real processes (plan 2.1) ----------------------
_TERMINAL = {"completed", "failed", "canceled", "crashed"}


def _terminal_patches(app, run_id) -> list[str]:
    statuses = []
    for request in app.requests:
        if request.method == "PATCH" and request.url.path == f"/v1/runs/{run_id}":
            status = json.loads(request.content or b"{}").get("status")
            if status in _TERMINAL:
                statuses.append(status)
    return statuses


def _probe_exec(*command: str) -> list[str]:
    return [sys.executable, "-m", "probe.cli", "exec", "--experiment", "e1", "--", *command]


def test_a_job_that_exits_2_under_probe_exec_closes_failed(app, tmp_path):
    """The child joins the launcher's run and closes it first; the launcher's
    `only_if_running` then defers to it. Its `sys.exit(2)` used to reach atexit
    as `completed` -- so the one verdict that counted was the wrong one."""
    app.seed_experiment("e1")
    child = tmp_path / "train.py"
    child.write_text("import sys, probe\nprobe.init()\nsys.exit(2)\n")
    with serve(app) as url:
        proc = subprocess.run(
            _probe_exec(sys.executable, str(child)),
            env=child_env(url),
            cwd=tmp_path,
            capture_output=True,
            text=True,
            timeout=120,
        )
    assert proc.returncode == 2, proc.stderr[-2000:]
    (run_id,) = app.runs
    assert app.runs[run_id]["status"] == "failed"
    assert _terminal_patches(app, run_id) == ["failed"], "the child's verdict, written once"


def test_sys_exit_of_main_under_probe_exec_closes_with_the_real_code(app, tmp_path):
    """`sys.exit(main())` looks sys.exit up BEFORE main() calls probe.init(), so
    no wrapper sees the exit. The child used to close `completed` on a guess
    and the launcher, holding the real code, deferred to it. Now the child
    leaves the close to the launcher when nothing told it how it ended."""
    app.seed_experiment("e1")
    child = tmp_path / "train.py"
    child.write_text(
        "import sys, probe\n"
        "def main():\n"
        "    probe.init()\n"
        "    probe.log({'loss': 0.5}, step=1)\n"
        "    return 2\n"
        "if __name__ == '__main__':\n"
        "    sys.exit(main())\n"
    )
    with serve(app) as url:
        proc = subprocess.run(
            _probe_exec(sys.executable, str(child)),
            env=child_env(url),
            cwd=tmp_path,
            capture_output=True,
            text=True,
            timeout=120,
        )
    assert proc.returncode == 2, proc.stderr[-2000:]
    (run_id,) = app.runs
    assert _terminal_patches(app, run_id) == ["failed"], "one close, the launcher's"
    codes = [
        s["attributes"].get("exit_code") for s in app.spans.get(run_id, []) if s["span_type"] == "process"
    ]
    assert 2 in codes
    assert app.metric_points_posted[run_id], "the child's data still arrives"


@pytest.mark.parametrize("finalize", [True, False])
def test_the_child_is_told_which_run_its_launcher_finalizes(
    app, launcher_run, monkeypatch, finalize
):
    """The run's id, and explicit both ways: a submitted job must not inherit
    an outer `probe exec`'s value."""
    monkeypatch.setenv("PROBE_EXEC_FINALIZES", "an-outer-run")
    seen = {}

    def launch(argv, *, env, **_kw):
        seen.update(env)
        return subprocess.CompletedProcess(argv, 0)

    monkeypatch.setattr(subprocess, "run", launch)
    launcher_run.execute(["python", "train.py"], finalize=finalize, capture_outputs=False)
    assert seen["PROBE_EXEC_FINALIZES"] == (launcher_run.id if finalize else "")


def test_a_run_a_sweep_driver_opens_under_probe_exec_is_closed_by_its_job(app, tmp_path):
    """The driver opens run B and starts a job with PROBE_RUN_ID=B -- the job
    inherits the driver's launcher flag, but that flag names the DRIVER's run.
    B's job must close B itself, or B is reaped `crashed` and mails an alarm."""
    app.seed_experiment("e1")
    (tmp_path / "job.py").write_text("import probe\nprobe.init()\nprobe.log({'acc': 0.9}, step=1)\n")
    driver = tmp_path / "driver.py"
    driver.write_text(
        "import os, subprocess, sys\n"
        "from probe.sdk.client import Client\n"
        "c = Client()\n"
        "b = c.run(experiment='e1', name='swept', heartbeat=False, capture_outputs=False)\n"
        "env = {**os.environ, 'PROBE_RUN_ID': b.id, 'PROBE_RUN_EPOCH': str(b.write_epoch)}\n"
        "job = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'job.py')\n"
        "rc = subprocess.run([sys.executable, job], env=env).returncode\n"
        "print('SWEPT', b.id, flush=True)\n"
        "c.close()\n"
        "sys.exit(rc)\n"
    )
    with serve(app) as url:
        proc = subprocess.run(
            _probe_exec(sys.executable, str(driver)),
            env=child_env(url),
            cwd=tmp_path,
            capture_output=True,
            text=True,
            timeout=120,
        )
    assert proc.returncode == 0, proc.stderr[-2000:]
    (swept,) = [line.split()[1] for line in proc.stdout.splitlines() if line.startswith("SWEPT")]
    assert _terminal_patches(app, swept) == ["completed"], "the job closed its own run"
    (driver_run,) = [rid for rid in app.runs if rid != swept]
    assert _terminal_patches(app, driver_run) == ["completed"], "the launcher closed the driver's"


@_posix_signals
def test_probe_exec_reports_a_signal_death_the_way_a_shell_does(app, tmp_path):
    """A child killed by SIGTERM exits -15; handed to exit() raw that is 241.
    A shell, and whatever reads the code next, expects 143."""
    app.seed_experiment("e1")
    child = tmp_path / "killed.py"
    child.write_text("import os, signal, time\nos.kill(os.getpid(), signal.SIGTERM)\ntime.sleep(30)\n")
    with serve(app) as url:
        proc = subprocess.run(
            _probe_exec(sys.executable, str(child)),
            env=child_env(url),
            cwd=tmp_path,
            capture_output=True,
            text=True,
            timeout=120,
        )
    assert proc.returncode == 128 + int(signal.SIGTERM), proc.stderr[-2000:]
    (run_id,) = app.runs
    assert _terminal_patches(app, run_id) == ["failed"], "SIGTERM stays a failure (#1843)"


@_posix_signals
def test_ctrl_c_reaching_the_launcher_closes_the_run_canceled(app, tmp_path):
    """Ctrl-C reaches the whole foreground process group, so the launcher takes
    it too. It closed the process span and re-raised, and the run sat `running`
    until the reaper called it `crashed` and mailed the person who pressed it."""
    app.seed_experiment("e1")
    started = tmp_path / "started"
    child = tmp_path / "sleep.py"
    child.write_text(
        "import pathlib, sys, time\npathlib.Path(sys.argv[1]).write_text('up')\ntime.sleep(120)\n"
    )
    with serve(app) as url:
        launcher = subprocess.Popen(
            _probe_exec(sys.executable, str(child), str(started)),
            env=child_env(url),
            cwd=tmp_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            deadline = time.monotonic() + 60
            while not started.exists() and time.monotonic() < deadline:
                time.sleep(0.05)
            assert started.exists(), "the child never started"
            launcher.send_signal(signal.SIGINT)
            _, err = launcher.communicate(timeout=60)
        finally:
            if launcher.poll() is None:
                launcher.kill()
                launcher.wait()
    assert launcher.returncode != 0, err[-2000:]
    (run_id,) = app.runs
    assert app.runs[run_id]["status"] == "canceled", err[-2000:]
    assert _terminal_patches(app, run_id) == ["canceled"]


@pytest.fixture
def launcher_run(app, monkeypatch):
    """A real Run on the fake backend, for the launcher's own failure modes."""
    monkeypatch.setenv("PROBE_AUTO_SNAPSHOT", "0")
    client = make_client(app)
    run = open_run(client, experiment="e1", name="wrapped", heartbeat=False)
    yield run
    client.close()


def _raise(exc: BaseException):
    def launch(*_a, **_kw):
        raise exc

    return launch


def test_a_launcher_that_broke_for_its_own_reasons_leaves_the_verdict(app, launcher_run, monkeypatch):
    """A fork failure or a bad argv is not the run being stopped on purpose;
    the reaper's verdict is the honest one there."""
    monkeypatch.setattr(subprocess, "run", _raise(OSError("fork failed")))
    with pytest.raises(OSError, match="fork failed"):
        launcher_run.execute(["python", "train.py"], capture_outputs=False)

    assert _terminal_patches(app, launcher_run.id) == []


def test_a_hand_off_writes_no_status_on_ctrl_c(app, launcher_run, monkeypatch):
    """`finalize=False`: this process SUBMITTED the job, so its interrupt says
    nothing about how the job ends."""
    monkeypatch.setattr(subprocess, "run", _raise(KeyboardInterrupt()))
    with pytest.raises(KeyboardInterrupt):
        launcher_run.execute(["python", "train.py"], finalize=False, capture_outputs=False)

    assert _terminal_patches(app, launcher_run.id) == []


def test_ctrl_c_does_not_overwrite_a_verdict_the_job_already_wrote(app, launcher_run, monkeypatch):
    """`only_if_running`: a job that closed itself from inside owns the verdict."""

    def job_closes_itself_then_interrupt(*_a, **_kw):
        app.runs[launcher_run.id]["status"] = "failed"
        raise KeyboardInterrupt

    monkeypatch.setattr(subprocess, "run", job_closes_itself_then_interrupt)
    with pytest.raises(KeyboardInterrupt):
        launcher_run.execute(["python", "train.py"], capture_outputs=False)

    assert app.runs[launcher_run.id]["status"] == "failed"
    assert _terminal_patches(app, launcher_run.id) == []
