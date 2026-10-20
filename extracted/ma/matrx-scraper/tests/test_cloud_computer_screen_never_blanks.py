"""The screen never blanks while a person watches (live walk, 2026-10-17).

Xvfb's default screen saver blanks after 600 s without X input. An agent drives
Chrome through CDP, which is no X input, so a person watching an agent work saw
a black screen after ten minutes (``xset q`` on the machine: ``timeout: 600``,
``prefer blanking: yes``). The X server starts with blanking and DPMS off, and
the Cloud Computer desktop turns it off again and logs the result.
"""

from __future__ import annotations

import re
import shlex
from pathlib import Path

DOCKER = Path(__file__).resolve().parents[1] / "docker"


def _xvfb_args() -> list[str]:
    script = (DOCKER / "browser-worker-entrypoint.sh").read_text()
    lines = [line for line in script.splitlines() if re.match(r"\s*Xvfb\s", line)]
    assert len(lines) == 1, lines
    return shlex.split(lines[0].rstrip("& "))


def test_xvfb_starts_with_blanking_off_and_no_unknown_options() -> None:
    args = _xvfb_args()
    # Xvfb has no DPMS: "-nodpms" made it exit at once and machines booted only by
    # luck (2026-10-18, image ddd709c947). The desktop turns DPMS off with xset.
    assert "-nodpms" not in args
    assert "-s" in args and args[args.index("-s") + 1] == "0"


def test_desktop_turns_blanking_off_and_logs_it() -> None:
    script = (DOCKER / "cloud-computer" / "cloud-computer-desktop.sh").read_text()
    assert "xset s off s noblank -dpms" in script
    assert "blanking=${blank_state}" in script
