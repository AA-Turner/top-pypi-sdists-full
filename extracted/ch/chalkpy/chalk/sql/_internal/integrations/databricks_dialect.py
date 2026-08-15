from __future__ import annotations

from typing import Any

from databricks.sql import exc as dbsql_exc

try:
    # databricks-sql-connector 2.x bundles the SQLAlchemy 1.4-compatible dialect here.
    from databricks.sqlalchemy.dialect import DatabricksDialect
except ImportError:
    try:
        # databricks-sql-connector 3.x layout; its dialect requires sqlalchemy>=2 and
        # raises AttributeError (not ImportError) under sqlalchemy 1.4, so catch broadly
        # and rewrap either failure into one actionable error.
        from databricks.sqlalchemy import DatabricksDialect
    except Exception as e:
        raise ImportError(
            "Could not import the Databricks SQLAlchemy dialect. The installed "
            + "databricks-sql-connector/sqlalchemy pairing does not provide one "
            + "(databricks-sql-connector 2.x works with sqlalchemy 1.4; the 3.x dialect "
            + "requires sqlalchemy>=2)."
        ) from e


class ChalkDatabricksDialect(DatabricksDialect):
    """DatabricksDialect with working stale-connection detection.

    Databricks SQL sessions are closed server-side (idle timeout, warehouse restart)
    while the client-side ``Connection.open`` flag stays True, so a pooled connection
    can go stale without the client noticing. The upstream dialect inherits
    SQLAlchemy's default ``is_disconnect``, which always returns False — with it,
    SQLAlchemy neither invalidates the dead session after it errors nor recycles it
    under ``pool_pre_ping``, and the pool serves the dead session forever.

    Registered under ``databricks+chalk://`` by ``DatabricksSourceImpl``.
    """

    supports_statement_cache = True

    def is_disconnect(self, e: Exception, connection: Any, cursor: Any) -> bool:
        # RequestError is databricks-sql-connector's transport-level failure (the
        # request never completed usefully). Treating every one as a disconnect is
        # deliberately eager: a false positive only costs a reconnect, while a false
        # negative poisons the pool.
        if isinstance(e, dbsql_exc.RequestError):
            return True
        # Statement-level errors against a dead session name the handle explicitly,
        # e.g. "INVALID_STATE: Invalid SessionHandle: SessionHandle [...]".
        return "Invalid SessionHandle" in str(e)
