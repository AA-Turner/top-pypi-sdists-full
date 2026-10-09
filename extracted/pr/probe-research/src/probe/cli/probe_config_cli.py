"""`probe doctor`'s check for retired folder defaults, and `--fix`.

Folder defaults (`<folder>/.probe/config.json`, #1252) set where a session
STARTED; `.probe.config` replaced them with a list of paths Probe never records.
An old one set to `off` or `read` still counts as `*` (`probe_config`), so
nothing starts recording when the feature retires; this finds them and, with
`--fix`, writes the `.probe.config` that says the same and deletes the old file.

The files live wherever a researcher once ran `probe session default --folder`,
so the search is bounded: the working directory's ancestors, then a walk below
the working directory and below home, a few levels deep, for a few seconds.
"""

from __future__ import annotations

import os
import time

from ..sdk import probe_config as pc

_MAX_DEPTH = 4
_BUDGET_S = 3.0


def _legacy_path(folder: str) -> str:
    return os.path.join(folder, pc.LEGACY_DIRNAME, pc.LEGACY_FILENAME)


def find(start: str | None = None, *, budget_s: float = _BUDGET_S, home: str | None = None) -> list[str]:
    """Folders holding a retired folder default, sorted. Never raises."""
    found: set[str] = set()
    try:
        here = os.path.abspath(start or os.getcwd())
    except OSError:
        here = os.path.expanduser("~")
    current = here
    while True:
        if os.path.isfile(_legacy_path(current)):
            found.add(current)
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    deadline = time.monotonic() + budget_s
    home_dir = home if home is not None else os.path.expanduser("~")
    for root in dict.fromkeys([here, home_dir]):
        stack = [(root, 0)]
        while stack and time.monotonic() < deadline:
            folder, depth = stack.pop()
            if os.path.isfile(_legacy_path(folder)):
                found.add(folder)
            if depth >= _MAX_DEPTH:
                continue
            try:
                with os.scandir(folder) as it:
                    for entry in it:
                        if entry.name in pc.SCAN_SKIP_DIRS or entry.name == pc.LEGACY_DIRNAME:
                            continue
                        try:
                            if entry.is_dir(follow_symlinks=False):
                                stack.append((entry.path, depth + 1))
                        except OSError:
                            continue
            except OSError:
                continue
    return sorted(found)


def convert(folder: str) -> str:
    """Turn one retired folder default into what it means now. The new file is
    written BEFORE the old one goes, so no moment exists where neither applies."""
    legacy = _legacy_path(folder)
    state = pc.legacy_default(folder)
    target = os.path.join(folder, pc.CONFIG_NAME)
    if state in ("off", "read-only"):
        existing = ""
        if os.path.isfile(target):
            with open(target, encoding="utf-8") as handle:
                existing = handle.read()
        if not existing.splitlines()[:1] == ["*"]:
            tmp = f"{target}.{os.getpid()}.tmp"
            with open(tmp, "w", encoding="utf-8") as handle:
                handle.write("*\n" + existing)
            os.replace(tmp, target)
        message = f"Turned `{pc.shown(legacy)}` into `{pc.shown(target)}` (`*`)."
    else:
        message = f"Deleted `{pc.shown(legacy)}` (it did nothing)."
    os.remove(legacy)
    try:
        os.rmdir(os.path.dirname(legacy))
    except OSError:
        pass  # the folder holds something else: left alone
    return message


def doctor_rows(*, fix: bool = False, start: str | None = None) -> list[str]:
    """`probe doctor`'s lines for retired folder defaults (none when there are none)."""
    rows: list[str] = []
    for folder in find(start):
        state = pc.legacy_default(folder)
        legacy = pc.shown(_legacy_path(folder))
        if fix:
            try:
                rows.append("  " + convert(folder))
            except OSError as exc:
                rows.append(f"  Could not convert `{legacy}`: {exc}")
            continue
        if state in ("off", "read-only"):
            word = "off" if state == "off" else "read"
            rows.append("  " + pc.DOCTOR_OLD_DEFAULT.format(path=legacy, state=word, dir=pc.shown(folder)))
        else:
            rows.append("  " + pc.DOCTOR_OLD_DEFAULT_ON.format(path=legacy))
    return rows
