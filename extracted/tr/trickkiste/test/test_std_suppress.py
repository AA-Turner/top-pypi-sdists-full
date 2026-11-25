"""Unit tests for trickkiste.std_suppress (runs `sh` as the child)"""

import subprocess
import sys

import pytest

pytestmark = pytest.mark.unit


def suppress(timeout: float, script: str) -> subprocess.CompletedProcess[str]:
    """`suppress` run on `sh -c @script` in a separate interpreter"""
    return subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-m",
            "trickkiste.std_suppress",
            str(timeout),
            "sh",
            "-c",
            script,
        ],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )


def test_quick_success_is_silent() -> None:
    result = suppress(5, "echo out; echo err >&2")
    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")


def test_quick_failure_prints_everything() -> None:
    result = suppress(5, "echo out; echo err >&2; exit 3")
    assert (result.returncode, result.stdout, result.stderr) == (
        3,
        "out\n",
        "err\n",
    )


def test_slow_run_prints_everything() -> None:
    result = suppress(0.1, "echo out; sleep 0.5; echo err >&2")
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        "out\n",
        "err\n",
    )


def test_output_after_first_stream_closed_is_kept() -> None:
    result = suppress(0.1, "echo out; exec 1>&-; sleep 0.5; echo err >&2")
    assert (result.stdout, result.stderr) == ("out\n", "err\n")
