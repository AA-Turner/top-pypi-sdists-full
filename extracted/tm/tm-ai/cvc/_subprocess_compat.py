"""Windows console-flash suppression for ``subprocess`` calls.

Every time CVC shells out to ``git``, ``launchctl``, ``netstat``, ``lsof``,
``taskkill``, etc. on Windows, the OS briefly opens a console window for the
child process unless we pass ``CREATE_NO_WINDOW`` *and* a ``STARTUPINFO`` with
``SW_HIDE``. The flash is invisible on macOS and Linux (different process
model), so the bug is Windows-only.

The dashboard fires ~6-8 git subprocess calls on every refresh (status, log,
branch, ahead/behind, etc.) — that's the "terminal flashes 7-8 times when I
click anything" report.

Use:

.. code-block:: python

    from cvc._subprocess_compat import HIDDEN_KW
    subprocess.run([...], capture_output=True, **HIDDEN_KW)

All values are no-ops on non-Windows by design — calling ``**HIDDEN_KW`` on
POSIX inserts nothing.
"""

from __future__ import annotations

import subprocess
import sys
from typing import Any

__all__ = ["HIDDEN_KW", "hidden_subprocess_kwargs"]

_IS_WINDOWS = sys.platform == "win32"

# 0x08000000 — CREATE_NO_WINDOW. Defined locally because the constant isn't
# guaranteed to exist on non-Windows subprocess modules.
_CREATE_NO_WINDOW = 0x08000000


def _build_hidden_kwargs() -> dict[str, Any]:
    if not _IS_WINDOWS:
        return {}
    kwargs: dict[str, Any] = {"creationflags": _CREATE_NO_WINDOW}
    # STARTUPINFO with SW_HIDE — belt-and-braces. CREATE_NO_WINDOW alone is
    # sufficient for true console children, but some shims (npm.cmd via
    # cmd.exe) honor STARTUPINFO instead. Setting both costs nothing.
    try:
        si = subprocess.STARTUPINFO()  # type: ignore[attr-defined]
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # type: ignore[attr-defined]
        si.wShowWindow = subprocess.SW_HIDE  # type: ignore[attr-defined]
        kwargs["startupinfo"] = si
    except AttributeError:
        # Non-Windows Python builds don't have STARTUPINFO. Shouldn't happen
        # given the platform guard above, but keep the fallback safe.
        pass
    return kwargs


# Frozen at import time. Each subprocess call gets a *fresh shallow copy*
# whenever the dict is spread with ``**`` — STARTUPINFO objects are
# thread-safe to share read-only.
HIDDEN_KW: dict[str, Any] = _build_hidden_kwargs()


def hidden_subprocess_kwargs() -> dict[str, Any]:
    """Function form for callers that prefer not to import a module-level
    constant. Returns a fresh dict (safe to mutate).
    """
    return dict(HIDDEN_KW)
