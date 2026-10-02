"""Ctrl-C during a script's auto-close at exit must still exit by SIGINT.

Regression for the #2056 (0.193.0) follow-up: a script that calls
``probe.init(...)`` and then dies from an uncaught ``KeyboardInterrupt`` used
to exit with code 1 instead of being re-killed by SIGINT (returncode -2, 130
in a shell), even though the run's status was correctly recorded as
``canceled``.

Cause: at interpreter exit, ``fluent._finish_at_exit`` calls ``run.finish()``,
which (via ``Client._report_delivery(final=True)``) used to do a LAZY
``from probe._shared import telemetry`` inside its inner ``send()``. Importing
a module for the first time during interpreter finalization clears CPython
3.12's "unhandled KeyboardInterrupt" flag, so Python exits 1 instead of
re-raising SIGINT. The fix hoists that import to module load time in
client.py, well before any close can run.

This must run in a REAL child process: every in-process test in this suite
already imports ``probe._shared.telemetry`` itself (directly or via a
fixture), which would hide the bug. The child below imports nothing but
``probe`` and must not go through any test helper that pre-imports telemetry.
"""

from __future__ import annotations

import signal
import subprocess
import sys

from tests.served_fake_app import child_env, serve

#: How a process that dies of an uncaught KeyboardInterrupt exits: re-killed by
#: SIGINT on POSIX, STATUS_CONTROL_C_EXIT on Windows (CPython 3.8+).
_EXITED_BY_CTRL_C = 0xC000013A if sys.platform == "win32" else -signal.SIGINT

_CHILD_SOURCE = """
import sys
assert "probe._shared.telemetry" not in sys.modules
import probe
run = probe.init(experiment="e1", name="r1")
run.log({"loss": 1.0}, step=0)
raise KeyboardInterrupt
"""


def test_ctrl_c_after_probe_init_exits_by_sigint_not_one(app, tmp_path):
    app.seed_experiment("e1")
    with serve(app) as url:
        env = child_env(url)
        proc = subprocess.run(
            [sys.executable, "-c", _CHILD_SOURCE],
            env=env,
            cwd=tmp_path,
            capture_output=True,
            text=True,
            timeout=120,
        )
    assert proc.returncode == _EXITED_BY_CTRL_C, (
        f"returncode={proc.returncode}, stderr tail:\n{proc.stderr[-3000:]}"
    )
    (run_id,) = app.runs
    assert app.runs[run_id]["status"] == "canceled"
