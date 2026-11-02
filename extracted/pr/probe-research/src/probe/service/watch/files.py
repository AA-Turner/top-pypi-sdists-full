"""read and write the watch's small JSON files (0600, whole or not at all), through foundation/durable's Store."""

from __future__ import annotations
import contextlib
import json
import os
import threading
from pathlib import Path
#: The watch's own record: the incidents reported once ever (a rejected
#: version, a tap that would not load, an update cycle's streak, a session's
#: lost recorder per registration), the oldest dropped past MAX_ONCE.
STATE_NAME = "watch.json"


# -- small files --------------------------------------------------------------


def read_json(path: Path, limit: int = 1024 * 1024) -> object:
    """A small JSON file's value, or None (missing, too big, unreadable)."""
    try:
        with open(path, "rb") as handle:
            raw = handle.read(limit + 1)
    except OSError:
        return None
    if len(raw) > limit:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None


def write_json(path: Path, value: object) -> bool:
    """0600, whole or not at all. False when it could not be written (a full
    disk, a read-only folder). Never raises."""
    tmp = path.with_name(f"{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    try:
        with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as handle:
            json.dump(value, handle)
        os.replace(tmp, path)
        return True
    except OSError:
        return False
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)
