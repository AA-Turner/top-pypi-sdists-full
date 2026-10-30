"""DuckDB as a SQL engine: what ``sqlutils`` runs a statement on when it names no connection (a
statement with a connection runs on the connection's own engine).

- :mod:`.engine` -- the kernel's DuckDB: set up once (:func:`.engine._ensure_duckdb`), then one
  statement at a time (:func:`.engine._run_local_duckdb`).
- :mod:`.extensions` -- the managed extension baseline applied at setup.
- :mod:`.catalogs` -- the project's data catalogs kept attached between statements: every
  ``LAKEHOUSE`` connection's Glue catalogs and every ``ATHENA`` connection's workgroup, signing
  with ``credential_chain`` secrets, attached afresh by ``sqlutils.attach_local_catalogs()`` at
  kernel start and on every change the frontend reports.

Rows are read one way, :func:`_one_row`: DuckDB 2.0 has no ``fetchone()`` on a relation.
"""

from typing import Optional


def _one_row(duck, statement: str) -> Optional[tuple]:
    """The first row ``statement`` answers on ``duck``, ``None`` when none: ``sql(...).fetchall()``,
    which DuckDB 1.x and 2.0 both have, where ``execute(...)`` would leave the rest of the result on
    the connection, in the way of the next statement."""
    rows = duck.sql(statement).fetchall()
    return rows[0] if rows else None
