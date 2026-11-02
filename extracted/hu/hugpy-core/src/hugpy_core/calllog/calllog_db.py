"""Core reads its own mirrored call log through its single database connection."""
from __future__ import annotations

def dsn() -> str:
    from hugpy_core.imports.functions import core_dsn
    return core_dsn()


def store():
    """The one abstract_database handle on the wrapper DB (hugpy_wrapper): a
    bootstrap-free ``PgStateStore`` (it never runs schema or mirror cleanup, so
    this reader never mutates the wrapper's database). Every core read/write of
    the call log goes through its ``.sql`` — verbatim psycopg ``%s``, tuples."""
    from abstract_database import PgStateStore
    return PgStateStore(dsn(), bootstrap=False, connect_timeout=5)
