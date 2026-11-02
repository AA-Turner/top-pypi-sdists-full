"""Durable wrapper endpoints and credentials in Flask Core's database.

This is the independent intake service's source of registrations. Its contents
are private: callers must not publish the ``key`` field to presence or UI APIs.
"""
from __future__ import annotations

from typing import Any

from psycopg.types.json import Jsonb

from hugpy_core.imports.functions import core_dsn


def _connect():
    import psycopg
    from psycopg.rows import dict_row
    return psycopg.connect(core_dsn(), row_factory=dict_row, connect_timeout=5)


def all() -> list[dict[str, Any]]:
    with _connect() as conn:
        return [row["config"] for row in conn.execute(
            "SELECT config FROM core_worker_registrations ORDER BY name")]


def get(name: str) -> dict[str, Any] | None:
    with _connect() as conn:
        row = conn.execute("SELECT config FROM core_worker_registrations WHERE name=%s", (name,)).fetchone()
    return row["config"] if row else None


def upsert(config: dict[str, Any]) -> dict[str, Any]:
    name = str(config.get("name") or "").strip()
    url = str(config.get("url") or "").strip().rstrip("/")
    if not name or not url.startswith(("http://", "https://")):
        raise ValueError("worker name and HTTP(S) URL are required")
    incoming = {key: value for key, value in config.items() if key != "key" or value}
    with _connect() as conn:
        previous = conn.execute(
            "SELECT config FROM core_worker_registrations WHERE name=%s FOR UPDATE", (name,)).fetchone()
        saved = {**(previous["config"] if previous else {}), **incoming, "name": name, "url": url}
        conn.execute("INSERT INTO core_worker_registrations(name,config) VALUES (%s,%s) "
                     "ON CONFLICT(name) DO UPDATE SET config=EXCLUDED.config,updated_at=now()",
                     (name, Jsonb(saved)))
    return saved


def is_connected(config: dict | None) -> bool:
    """A saved connection is live unless the operator disconnected it."""
    return bool(config) and config.get("connected", True) is not False


def set_connected(name: str, connected: bool) -> dict[str, Any] | None:
    """Disconnect or reconnect a saved Wrapper connection. The endpoint and key stay
    saved either way, so reconnecting is one switch, never a new enrollment."""
    import time as _time
    with _connect() as conn:
        row = conn.execute("SELECT config FROM core_worker_registrations WHERE name=%s FOR UPDATE",
                           (name,)).fetchone()
        if not row:
            return None
        saved = {**row["config"], "connected": bool(connected), "connected_changed_at": _time.time()}
        conn.execute("UPDATE core_worker_registrations SET config=%s, updated_at=now() WHERE name=%s",
                     (Jsonb(saved), name))
        if not connected:
            # presence keeps the worker listed (and saved) but reports it disconnected,
            # so routing treats it as offline and the console offers Reconnect
            conn.execute("UPDATE worker_presence SET payload = payload || %s WHERE worker=%s",
                         (Jsonb({"connected": False, "status": "disconnected"}), name))
    return saved
