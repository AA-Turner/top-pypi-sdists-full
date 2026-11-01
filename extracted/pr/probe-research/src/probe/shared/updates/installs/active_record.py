"""the active.json record: active/previous version, rejected versions, dropped --with extras."""

from __future__ import annotations

import contextlib
import json
import os
import time
from pathlib import Path

from .. import handoff
ACTIVE_NAME = "active.json"


# -- the record ------------------------------------------------------------------


def _record_path(tools: Path | None = None) -> Path:
    return versions_root(tools) / ACTIVE_NAME


def record(tools: Path | None = None) -> dict:
    try:
        data = json.loads(_record_path(tools).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _write_record(data: dict, tools: Path | None = None) -> None:
    target = _record_path(tools)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(f"{target.name}.{os.getpid()}.tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(data, handle)
        os.replace(tmp, target)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


def active(tools: Path | None = None) -> Path | None:
    """The version env the tool path names now, resolved; None when it is a
    plain folder (no switch yet) or missing."""
    env = tool_env(tools)
    if not is_link(env):
        return None
    try:
        return env.resolve(strict=True)
    except OSError:
        return None


#: A rejected version is skipped this long, then tried again (plan I1, A5).
REJECT_TTL_S = handoff.REJECT_TTL_S


def _mark(value: object) -> dict | None:
    """One `rejected` entry as `{"at", "reason"}`: today's shape, or an older
    bare timestamp. None for anything else."""
    if isinstance(value, dict):
        at = value.get("at")
        reason = value.get("reason")
    else:
        at, reason = value, ""
    if isinstance(at, bool) or not isinstance(at, (int, float)):
        return None
    return {"at": float(at), "reason": reason if isinstance(reason, str) else ""}


def rejected(tools: Path | None = None, *, now: float | None = None) -> dict:
    """`{version: {"at", "reason"}}`: versions switched back from on this
    machine (D5) less than REJECT_TTL_S ago. Skipped while they are; a newer
    release than a rejected one is never held off by it (only the newest
    release is ever the target)."""
    value = record(tools).get("rejected")
    if not isinstance(value, dict):
        return {}
    now = time.time() if now is None else now
    out = {}
    for version, raw in value.items():
        mark = _mark(raw)
        if mark is not None and now - mark["at"] < REJECT_TTL_S:
            out[version] = mark
    return out


def reject(version: str, reason: str, tools: Path | None = None) -> None:
    """Mark `version` rejected now; the entries past REJECT_TTL_S go."""
    data = record(tools)
    marks = rejected(tools)
    marks[version] = {"at": time.time(), "reason": reason[:500]}
    data["rejected"] = marks
    _write_record(data, tools)


def set_fields(tools: Path | None = None, **fields: object) -> None:
    """Set fields of the record (`active.json`); None takes one out."""
    data = record(tools)
    for name, value in fields.items():
        if value is None:
            data.pop(name, None)
        else:
            data[name] = value
    _write_record(data, tools)


def record_dropped_with(packages: list, tools: Path | None = None, *, python: str | None = None) -> None:
    """What the active env lacks of the install before it: the `--with`
    packages that would not install beside it (`dropped_with`) and the exact
    Python it ran on (`dropped_python`), for `probe doctor`'s re-add line and
    for the next install to try again first. Empty clears each."""
    set_fields(tools, dropped_with=[str(p) for p in packages][:20] or None, dropped_python=python or None)


def dropped_with(tools: Path | None = None) -> list[str]:
    value = record(tools).get("dropped_with")
    return [str(p) for p in value] if isinstance(value, list) else []


def dropped_python(tools: Path | None = None) -> str | None:
    value = record(tools).get("dropped_python")
    return value if isinstance(value, str) and value else None


def clear_rejected(version: str, tools: Path | None = None) -> bool:
    """A person asked for `version` itself (an install, `probe repair`):
    its rejection on this machine goes (R-T2). True when there was one."""
    data = record(tools)
    marks = data.get("rejected")
    if not isinstance(marks, dict) or version not in marks:
        return False
    marks.pop(version, None)
    data["rejected"] = marks
    _write_record(data, tools)
    return True
from probe.shared.updates.installs.layout import tool_env, versions_root  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.link import is_link  # noqa: E402 -- pieces need each other; the front door loads this one first
