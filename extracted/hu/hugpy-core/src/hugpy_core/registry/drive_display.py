"""Core central-drive settings and capacity display helpers."""
from __future__ import annotations

import os
import shutil

GIB = 1024 ** 3
ENV_DRIVES = "HUGPY_CENTRAL_DRIVES"


def parse_drives(spec: str | None) -> list[dict]:
    """Parse comma-separated ``path[:max_gib]`` central-drive declarations."""
    out = []
    for item in (spec or "").split(","):
        item = item.strip()
        if not item:
            continue
        path, _, cap = item.partition(":")
        try:
            max_bytes = int(float(cap) * GIB) if cap.strip() else None
        except ValueError:
            max_bytes = None
        out.append({"path": os.path.abspath(os.path.expanduser(path.strip())),
                    "max_bytes": max_bytes})
    return out


def drives_from_env(environ=None) -> list[dict]:
    return parse_drives((environ if environ is not None else os.environ).get(ENV_DRIVES))


# Central's drives are a SETTING like any worker's (operator 2026-10-23: "central
# should be no different than any other"): the stored list wins; the env
# designation is only its starting value. settings_policies key 'central_drives'.
POLICY_KEY = "central_drives"


def _policy_conn():
    import psycopg
    from psycopg.rows import dict_row
    from hugpy_core.imports.functions import core_dsn
    return psycopg.connect(core_dsn(), row_factory=dict_row, connect_timeout=5)


def saved_drives():
    """The stored central drive list, or None when never set."""
    try:
        with _policy_conn() as conn:
            row = conn.execute("SELECT value FROM settings_policies WHERE key=%s", (POLICY_KEY,)).fetchone()
    except Exception:  # noqa: BLE001 — no store: the env designation stands
        return None
    if not row or not isinstance(row["value"], list):
        return None
    return [{"path": d["path"], "max_bytes": d.get("max_bytes")} for d in row["value"]
            if isinstance(d, dict) and d.get("path")]


def declared_drives() -> list[dict]:
    """Central's drives: the stored setting, else the env designation."""
    saved = saved_drives()
    return saved if saved is not None else drives_from_env()


def save_drives(items, updated_by="console") -> list[dict]:
    """Validate and store central's drive list [{path, max_gib|None}]."""
    from psycopg.types.json import Jsonb
    if not isinstance(items, list):
        raise ValueError("drives must be a list")
    out, seen = [], set()
    for it in items:
        path = str((it or {}).get("path") or "").strip()
        if not path:
            continue
        if not os.path.isabs(path):
            raise ValueError(f"{path!r} is not an absolute path")
        if not os.path.isdir(path):
            raise ValueError(f"{path!r} is not a folder on this machine")
        path = os.path.normpath(path)
        if path in seen:
            continue
        seen.add(path)
        gib = (it or {}).get("max_gib")
        if gib in ("", None):
            max_bytes = None
        else:
            try:
                max_bytes = int(float(gib) * GIB)
            except (TypeError, ValueError):
                raise ValueError(f"budget for {path!r} must be a number of GiB") from None
            if max_bytes < 0:
                raise ValueError(f"budget for {path!r} cannot be negative")
        out.append({"path": path, "max_bytes": max_bytes})
    with _policy_conn() as conn:
        conn.execute("INSERT INTO settings_policies (key, value, updated_by) VALUES (%s,%s,%s) "
                     "ON CONFLICT (key) DO UPDATE SET value=EXCLUDED.value, updated_by=EXCLUDED.updated_by, "
                     "updated_at=now()", (POLICY_KEY, Jsonb(out), updated_by))
    return out


def drive_usage(drive: dict, held_bytes: int) -> dict:
    """Report a declared drive's filesystem room and configured cap."""
    try:
        usage = shutil.disk_usage(drive["path"])
        total, free = int(usage.total), int(usage.free)
    except OSError:
        total = free = None
    cap = drive.get("max_bytes")
    room = free
    if cap is not None:
        room = min(free if free is not None else cap, max(0, cap - held_bytes))
    return {"path": drive["path"], "max_bytes": cap, "fs_total": total,
            "fs_free": free, "held_bytes": held_bytes, "room": room}
