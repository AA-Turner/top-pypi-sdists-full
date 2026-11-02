"""pin pi's installed package in a detached child at session start."""

from __future__ import annotations
import subprocess
import sys


def _ensure_pi_pin() -> None:
    """pi's session start, with no pin of the installed package yet (an install
    or `pi update` by hand, or a package before the shim's first update): pin it
    in a detached child, so this session's shim can switch to it at a later turn
    and the next session starts on it (kimi/pi update parity P1). Never fails."""
    try:
        from . import pins as pi_pins

        if not pi_pins.pin_due():
            return
        import subprocess

        from probe._shared import oscompat

        subprocess.Popen(  # noqa: S603 -- this interpreter, our own module
            [sys.executable, "-m", "probe.cli.pi_pins"],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            close_fds=True, **oscompat.DETACHED,  # off pi's console: no shared Ctrl-C on Windows
        )
    except Exception:  # noqa: BLE001 -- a pin is never worth a failed session start
        return
