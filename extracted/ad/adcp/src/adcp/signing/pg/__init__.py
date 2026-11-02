"""PostgreSQL-backed implementations for the signing module.

This sub-package ships backends that require PostgreSQL via psycopg3.
They live here (and behind the ``[pg]`` optional extra) so the base
``adcp.signing`` import path stays free of SQL dependencies for users
who only need the pure-Python primitives.

Available when ``adcp[pg]`` is installed:

* :class:`PgReplayStore` — multi-instance-safe replay store for the
  RFC 9421 verifier pipeline.

The schema DDL ships alongside the Python code at
``adcp/signing/pg/replay_store.sql`` so integrators can run it through
whatever migration tool they use (Alembic, Flyway, psql, ...).
"""

from __future__ import annotations

from adcp.signing.pg.replay_store import PgReplayStore

__all__ = ["PgReplayStore"]
