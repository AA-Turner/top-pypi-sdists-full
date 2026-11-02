"""Run actionlint on changed workflow files."""

from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path

from agentic_devtools.cli.checks.check_result import _CheckResult
from agentic_devtools.cli.checks.workflow_paths import select_changed_workflow_files


def check_workflow_files(cwd: Path) -> _CheckResult:
    """Lint the changed workflow files selected for this repository."""
    started = time.monotonic()
    files = select_changed_workflow_files(cwd)
    label = "Lint changed workflows"
    if not files:
        return _CheckResult(label, True, "OK - no changed workflow files.", time.monotonic() - started)

    actionlint = shutil.which("actionlint")
    if actionlint is None:
        return _CheckResult(
            label,
            False,
            "ERROR: 'actionlint' was not found on PATH. Install it with "
            "bash scripts/install-actionlint.sh; the pinned version is in scripts/actionlint-version.txt.",
            time.monotonic() - started,
        )

    try:
        result = subprocess.run(
            [actionlint, *files],
            cwd=cwd,
            capture_output=True,
            text=True,
            shell=False,
        )
    except OSError as exc:
        return _CheckResult(
            label,
            False,
            f"ERROR: could not run actionlint ({exc}). Verify the installation with "
            "bash scripts/install-actionlint.sh; the pinned version is in scripts/actionlint-version.txt.",
            time.monotonic() - started,
        )

    return _CheckResult(
        label,
        result.returncode == 0,
        (result.stdout + result.stderr).rstrip(),
        time.monotonic() - started,
    )
