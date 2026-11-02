"""Core creates its own tables: the migrations in schema/sql/, applied at start.

Each file runs once per SCHEMA, in name order, recorded in ``core_migrations``
(name, applied_at). Files headed ``-- DB: inference_engine`` belong to the wrapper's
database, not core's, and are skipped here. An advisory lock keeps two core
processes from applying the same file at once. The files are idempotent anyway
(CREATE ... IF NOT EXISTS), so a database made before this ledger existed takes
them again without harm.

TWO DATABASE LAYOUTS (install/installer.py):
  * own-cluster (default) / --create-db: a database of core's own, public schema —
    HUGPY_CORE_SCHEMA is unset, the migrations' unqualified names land in public.
  * existing-DSN (--db-dsn): an orbit SCHEMA inside a shared, account-owned database.
    The core DSN carries ``options=-c search_path=<schema>,public`` so this connects
    straight into the schema; ensure() also CREATEs it (idempotent) and pins the
    session, so every unqualified CREATE below — and core_migrations itself — lands
    in the orbit's schema, never public. The migration SQL carries NO hardcoded
    ``public.`` (021 was a pg_dump; stripped) for exactly this reason. The advisory
    lock key folds the schema in, so two orbits in one database never serialise or
    cross; NOTIFY channels are schema-suffixed the same way (functions.notify_channel).
"""
from __future__ import annotations

import hashlib
import logging
import os
from typing import List, Optional

from hugpy_core.imports.constants import ENV_CORE_SCHEMA
from hugpy_core.imports.functions import core_dsn

logger = logging.getLogger("hugpy_core")

SQL_DIR = os.path.join(os.path.dirname(__file__), "sql")
LOCK_KEY = 0x6875_6770_7963   # "hugpyc"
OTHER_DB = "-- DB: inference_engine"


def _schema_salt(schema: str) -> int:
    """A stable 31-bit salt from a schema name, folded into the advisory-lock key
    so each orbit schema locks on its own key (the lock is per-database)."""
    return int.from_bytes(hashlib.sha1(schema.encode("utf-8")).digest()[:4], "big") & 0x7FFF_FFFF


def files() -> List[str]:
    """Core's migrations, in order (the wrapper-DB ones left out)."""
    out = []
    for name in sorted(os.listdir(SQL_DIR)):
        if not name.endswith(".sql"):
            continue
        with open(os.path.join(SQL_DIR, name), encoding="utf-8") as f:
            if f.readline().startswith(OTHER_DB):
                continue
        out.append(name)
    return out


def ensure(dsn: Optional[str] = None, schema: Optional[str] = None) -> List[str]:
    """Apply every migration this schema has not had yet; returns their names.

    ``schema`` None = the HUGPY_CORE_SCHEMA env (the installer sets it only in the
    existing-DSN layout); 'public'/unset = core's own database, no schema step."""
    import psycopg
    from psycopg import sql
    schema = (schema if schema is not None else os.environ.get(ENV_CORE_SCHEMA, "")).strip() or None
    applied: List[str] = []
    with psycopg.connect(dsn or core_dsn(), autocommit=True, connect_timeout=5) as c:
        if schema and schema != "public":
            # create the orbit schema if absent and pin the session to it, so the
            # unqualified CREATEs below (and core_migrations) land there, not public.
            c.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema)))
            c.execute(sql.SQL("SET search_path TO {}, public").format(sql.Identifier(schema)))
        lock_key = LOCK_KEY ^ (_schema_salt(schema) if schema and schema != "public" else 0)
        c.execute("SELECT pg_advisory_lock(%s)", (lock_key,))
        try:
            c.execute("CREATE TABLE IF NOT EXISTS core_migrations ("
                      " name text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now())")
            done = {r[0] for r in c.execute("SELECT name FROM core_migrations").fetchall()}
            for name in files():
                if name in done:
                    continue
                with open(os.path.join(SQL_DIR, name), encoding="utf-8") as f:
                    c.execute(f.read())
                c.execute("INSERT INTO core_migrations (name) VALUES (%s)", (name,))
                applied.append(name)
        finally:
            c.execute("SELECT pg_advisory_unlock(%s)", (lock_key,))
    if applied:
        logger.info("schema: applied %s%s", ", ".join(applied),
                    f" in schema {schema}" if schema and schema != "public" else "")
    return applied


__all__ = ["ensure", "files", "SQL_DIR"]
