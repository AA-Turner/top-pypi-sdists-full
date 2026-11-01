"""the device error log and crash line `probe doctor` shows (and analytics.track for daemon errors)."""

from __future__ import annotations
import os
import time


#: `daemon-errors.log` moves to `daemon-errors.log.1` past this (plan B7): one
#: older generation is kept, so the log never grows without bound.
DEVICE_ERRORS_MAX_BYTES = 1024 * 1024


def _device_error(text: str) -> None:
    """The shared device-level error log `probe doctor` and the status line show.

    Every line goes through the shared scrubber first (`probe._shared.scrub`:
    credentials, this machine's home and login): it carries exception text, and
    diagnostic reports carry its tail. Past `DEVICE_ERRORS_MAX_BYTES` it moves
    to `.1`; two workers rotating at once can lose that older generation, never
    a new line."""
    path = _state_base() / "daemon-errors.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from probe._shared import scrub

        text = " ".join(scrub.scrub(text).splitlines())
    except Exception:  # noqa: BLE001 -- withheld rather than written raw
        text = "(an error line was withheld: it could not be scrubbed)"
    try:
        if path.stat().st_size > DEVICE_ERRORS_MAX_BYTES:
            os.replace(path, path.with_name(path.name + ".1"))
    except OSError:
        pass  # not there yet, or another worker rotated it first
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {text}\n")


def _crash_detail(exc: BaseException) -> str:
    """`Type: message` for the crash line, scrubbed WHOLE and then clipped: a
    credential cut in half by the clip could slip past the scanner."""
    try:
        from probe._shared import scrub

        message = scrub.scrub(str(exc))
    except Exception:  # noqa: BLE001 -- withheld rather than written raw
        message = "(message withheld: it could not be scrubbed)"
    return f"{type(exc).__name__}: {message[:300]}"
from probe.daemon.worker.files import _state_base  # noqa: E402 -- pieces need each other; the front door loads this one first
