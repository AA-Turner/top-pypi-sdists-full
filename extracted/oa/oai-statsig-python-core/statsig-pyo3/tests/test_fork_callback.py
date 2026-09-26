import os
import subprocess
import sys


def test_fork_after_shutdown_does_not_deadlock_on_python_callback() -> None:
    proc = subprocess.run(
        [sys.executable, "tests/fork_callback_runner.py"],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
        env={**os.environ, "RUST_BACKTRACE": "full"},
    )

    assert proc.returncode == 0, f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
