"""Scrub this machine's own identity and every credential out of diagnostic text.

One implementation for everything Probe sends ITS OWN TEAM about a machine:
the update reports (`probe.cli.update_report`) and the diagnostic reports
(`probe.core.report`). The server scrubs again; it does not trust this.

Order matters: this machine's home folder and login name go FIRST, then every
home-shaped path and credential (`probe.sdk.redaction.scrub_text`, plus the
Windows spellings it misses). A pattern only knows the usual places
(`/home/x`, `/Users/x`); a home at `/fsx/dave` or `/data/users/carol` is caught
only by knowing it.

Imports nothing from `probe.cli` (the `_shared` rule); the SDK's scrubber is
imported when a text is scrubbed, never at import.
"""

from __future__ import annotations

import getpass
import re
from pathlib import Path

#: Windows home folders in every spelling a child's output carries them: plain,
#: as Python's escaped repr (`'C:\\Users\\alice'` in an OSError), with forward
#: slashes, in any letter case. `scrub_text` knows only the plain one.
WINDOWS_HOME = re.compile(
    r"[A-Za-z]:(?:\\{1,2}|/)(?:users|documents and settings)(?:\\{1,2}|/)[^\\/\s'\"]+",
    re.IGNORECASE,
)


def home_and_user() -> tuple[str, str]:
    """This machine's home folder and login name ("" when unreadable)."""
    try:
        home = str(Path.home())
    except Exception:  # noqa: BLE001 - no HOME: nothing to remove
        home = ""
    try:
        user = getpass.getuser()
    except Exception:  # noqa: BLE001
        user = ""
    return home, user


def strip_own_identity(text: str) -> str:
    """This machine's home folder -> `~` and login name -> `<user>`, BEFORE any
    pattern runs. The home is matched plain, with doubled backslashes (Python's
    repr of a Windows path) and with forward slashes, in any letter case."""
    home, user = home_and_user()
    if len(home) > 1:
        spellings = {home, home.replace("\\", "\\\\"), home.replace("\\", "/")}
        for spelling in sorted(spellings, key=len, reverse=True):
            text = re.sub(re.escape(spelling), "~", text, flags=re.IGNORECASE)
    # Whole words only and 3+ characters: a two-letter login would otherwise
    # eat every `uv` in the text.
    if len(user) >= 3:
        text = re.sub(
            rf"(?<![A-Za-z0-9_.-]){re.escape(user)}(?![A-Za-z0-9_])", "<user>", text,
            flags=re.IGNORECASE,
        )
    return text


def scrub(text: str) -> str:
    """`text` without this machine's home and login, other home folders, or any
    credential. Raises when the scrubber does: a caller withholds the text then,
    never sends it raw."""
    from probe.sdk.redaction import scrub_text

    return scrub_text(WINDOWS_HOME.sub("~", strip_own_identity(text)))
