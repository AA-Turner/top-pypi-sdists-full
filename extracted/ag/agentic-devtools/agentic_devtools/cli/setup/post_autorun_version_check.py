"""Post-autorun installed-version re-read helper.

After ``_autorun_setup_dev_tools`` executes the generated setup script, the
installed version of ``agentic-devtools`` may have changed (e.g. the script
ran ``pip install``).  This module provides two helpers:

* ``capture_startup_version()`` — snapshot ``agentic_devtools.__version__``
  at process start (pure in-process read, cannot fail).
* ``check_post_autorun_version()`` — re-read the *installed* version via a
  subprocess call to ``importlib.metadata.version``.  Returns ``None`` on
  any failure (non-fatal, warning only).
"""

from __future__ import annotations

import subprocess
import sys

import agentic_devtools

from ..subprocess_utils import run_safe

_VERSION_READ_TIMEOUT_SECONDS: int = 10


def capture_startup_version() -> str:
    """Return the in-process ``agentic_devtools.__version__`` string.

    This is a pure in-process read with no subprocess or I/O.
    """
    return agentic_devtools.__version__


def check_post_autorun_version(startup_version: str) -> str | None:
    """Re-read the installed package version via a subprocess.

    Spawns a fresh Python interpreter to query ``importlib.metadata`` so that
    any ``pip install`` performed by the autorun phase is reflected.

    Args:
        startup_version: The version captured at process start (used only for
            context in this function's contract — the caller performs the
            comparison).

    Returns:
        The stripped installed version string, or ``None`` when the read fails
        for any reason (non-zero exit, empty output, timeout, OS error).
        Failures emit a warning to stderr but are never fatal.
    """
    try:
        result = run_safe(
            [
                sys.executable,
                "-c",
                "from importlib.metadata import version; print(version('agentic-devtools'))",
            ],
            capture_output=True,
            text=True,
            timeout=_VERSION_READ_TIMEOUT_SECONDS,
            shell=False,
        )
    except FileNotFoundError:
        print(
            "  ⚠ Post-autorun version check: Python interpreter not found",
            file=sys.stderr,
        )
        return None
    except subprocess.TimeoutExpired:
        print(
            "  ⚠ Post-autorun version check: subprocess timed out",
            file=sys.stderr,
        )
        return None
    except OSError as exc:
        print(
            f"  ⚠ Post-autorun version check: OS error — {exc}",
            file=sys.stderr,
        )
        return None

    if result.returncode != 0:
        _stderr_raw = " ".join((result.stderr or "").strip().splitlines())
        _stderr_snippet = (_stderr_raw[:120] + "…") if len(_stderr_raw) > 120 else _stderr_raw
        _stderr_suffix = f"; stderr: {_stderr_snippet}" if _stderr_snippet else ""
        print(
            f"  ⚠ Post-autorun version check: subprocess exited with code {result.returncode}{_stderr_suffix}",
            file=sys.stderr,
        )
        return None

    # Normalize to the first non-empty line to guard against sitecustomize/
    # user startup-hook noise that may write extra lines to stdout.
    version_str = next(
        (line.strip() for line in result.stdout.splitlines() if line.strip()),
        None,
    )
    if not version_str:
        print(
            "  ⚠ Post-autorun version check: subprocess returned empty output",
            file=sys.stderr,
        )
        return None

    return version_str
