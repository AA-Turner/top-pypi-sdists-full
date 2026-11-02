"""Shared pure helpers — the environment reads that were duplicated across
modules, resolved once here.

Stdlib-only at import time; no heavy dependency is pulled in by importing this.
"""
from __future__ import annotations

import os
from typing import Optional

from hugpy_core.imports import constants as C


def core_dsn() -> str:
    """hugpy central's own DB DSN (env ``HUGPY_CORE_DB``, default
    ``dbname=hugpy_core``). Was inlined in 6 modules as DB / CORE_DSN /
    PRESENCE_DSN."""
    return os.environ.get(C.ENV_CORE_DB, C.DEFAULT_CORE_DSN)


def self_base() -> str:
    """This box's own front-door base URL, using the configured Core listener."""
    explicit = os.environ.get(C.ENV_SELF_BASE)
    if explicit:
        return explicit.rstrip("/")
    host = (os.environ.get("HUGPY_CORE_HOST") or "").split(",", 1)[0].strip()
    if host and host not in ("0.0.0.0", "::"):
        return f"http://{host}:{os.environ.get('HUGPY_CORE_PORT') or '7002'}"
    return C.DEFAULT_SELF_BASE.rstrip("/")


def env_str(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.environ.get(name, default)
    if v is None:
        return None
    v = v.strip()
    return v or default


def env_float(name: str, default: Optional[float] = None) -> Optional[float]:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw)
    except ValueError:
        return default


# ── pair knobs (model_workers.user_settings): one validator + one effective view ──
def validate_pair_knobs(sets: dict) -> dict:
    from hugpy_settings.settings_validation import validate_pair_knobs as validate
    return validate(sets)


def effective_pair_settings(user_settings: Optional[dict]) -> dict:
    """The effective value of every pair knob the console shows: the stored value
    when present, else the Auto default (``PAIR_SETTING_DEFAULTS``), else ``None``
    (= Auto, no fixed default). ONE server-side source so the console never has to
    know the defaults. Accepts the legacy ``ctx_range`` as ``ctx_range_enabled``."""
    us = dict(user_settings or {})
    if us.get("auto_goal") == "resident":
        us["auto_goal"] = "quality"
    if "ctx_range" in us and "ctx_range_enabled" not in us:
        us["ctx_range_enabled"] = us.pop("ctx_range")
    return {k: us.get(k, C.PAIR_SETTING_DEFAULTS.get(k)) for k in C.PAIR_KNOB_KEYS}


def notify_channel(base: str, schema: Optional[str] = None) -> str:
    """The orbit-scoped LISTEN/NOTIFY channel name for ``base``.

    Postgres NOTIFY channels are per-DATABASE, not per-schema; the no-privilege
    install puts one orbit per schema inside a shared database (install/), so two
    orbits would otherwise cross on the same channel. The channel is suffixed with
    the orbit's schema unless that is the default ``public`` (kept bare for the
    legacy / --create-db layout, and matching the SQL triggers' own
    ``current_schema()`` suffixing). ``schema`` None = read it from the env the
    installer writes (``HUGPY_CORE_SCHEMA``); the Python listeners instead pass
    the schema their own connection reports (``SELECT current_schema()``) so the
    name always agrees with the trigger that fired it."""
    sch = (schema if schema is not None else os.environ.get(C.ENV_CORE_SCHEMA, "")).strip()
    return base if (not sch or sch == "public") else f"{base}__{sch}"


def listen_channel(conn, base: str) -> str:
    """LISTEN on ``base`` scoped to this CONNECTION's own schema, matching the SQL
    triggers' ``current_schema()`` suffix, and return the channel listened on. ONE
    place so every core listener and every trigger agree: in the default ``public``
    schema the channel is bare (legacy / own-cluster install); under an orbit schema
    (existing-DSN install) it is ``base__<schema>`` so two orbits in one database do
    not cross. The schema is read from the connection (not the env) so it is exactly
    what the firing trigger saw."""
    from psycopg import sql
    try:
        schema = conn.execute("SELECT current_schema()").fetchone()[0]
    except Exception:  # noqa: BLE001 — a search_path we cannot read: the bare channel
        schema = None
    chan = notify_channel(base, schema)
    conn.execute(sql.SQL("LISTEN {}").format(sql.Identifier(chan)))
    return chan
