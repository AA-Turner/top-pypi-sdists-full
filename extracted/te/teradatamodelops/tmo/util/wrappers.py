import logging
import os
from typing import Optional

from sqlalchemy import Engine
from teradataml import DataFrame, get_context
from teradataml import copy_to_sql as _teradataml_copy_to_sql

logger = logging.getLogger(__name__)

__all__ = ["copy_to_sql", "to_sql", "execute_sql_in_context", "execute_sql"]


# ---------------------------------------------------------------------------
# teradataml bug workaround: _get_database_names called with schema_name=None
#
# When copy_to_sql is called with temporary=True, teradataml internally sets
# schema_name=None (volatile tables always live in the user's session database
# and do not accept a schema_name). However, _DataTransferUtils._validate()
# then calls DataFrameUtils._get_database_names(connection, None) BEFORE
# checking "if self.schema_name is not None", executing:
#
#   SELECT ... FROM dbc.databasesV WHERE databasename = ? [parameters: (None,)]
#
# Teradata rejects NULL as a parameter in this context, raising an error.
# We patch _get_database_names to return [] immediately when schema_name is
# None — which is semantically correct (nothing to validate) and matches what
# the caller does with the result when schema_name is None anyway.
# ---------------------------------------------------------------------------

# Populated at import time if the patch is successfully applied.
_original_get_database_names = None
_patched_get_database_names = None

try:
    from teradataml.dataframe.dataframe_utils import DataFrameUtils as _DataFrameUtils

    _original_get_database_names = _DataFrameUtils._get_database_names

    def _patched_get_database_names(connection, schema_name):
        """Null-safe wrapper for DataFrameUtils._get_database_names.

        Returns an empty list immediately when schema_name is None instead of
        executing a SQL query with a NULL parameter (which Teradata rejects).
        """
        if schema_name is None:
            return []
        return _original_get_database_names(connection, schema_name)

    _DataFrameUtils._get_database_names = staticmethod(_patched_get_database_names)
    logger.debug(
        "Applied teradataml bug workaround: DataFrameUtils._get_database_names "
        "now guards against schema_name=None (temporary=True path)."
    )
except Exception as _patch_err:
    logger.warning(
        f"Could not apply _get_database_names patch: {_patch_err}. "
        "Calls with temporary=True may fail if schema_name resolves to None."
    )


def copy_to_sql(
    df: DataFrame, table_name: str, schema_name: Optional[str] = None, **kwargs
) -> None:
    """
    Wrapper around teradataml.copy_to_sql that automatically uses the database/schema
    configured via tmo_create_context if schema_name is not explicitly provided.

    Takes the same parameters as teradataml.copy_to_sql. If schema_name is not
    specified, it is resolved from the VMO_CONN_DATABASE environment variable
    (set by tmo_create_context) or from the active teradataml configure settings.

    Args:
        df: pandas DataFrame to copy to Teradata.
        table_name (str): Name of the target Teradata table.
        schema_name (str, optional): Database/schema name. If not provided, uses
            the database configured via tmo_create_context (VMO_CONN_DATABASE).
        **kwargs: Additional keyword arguments forwarded to teradataml.copy_to_sql
            (e.g. if_exists, types, primary_index, temporary, etc.).

    Example:
        >>> from tmo import copy_to_sql
        >>> copy_to_sql(df=my_df, table_name="my_table", if_exists="replace")
        # schema_name resolved automatically from VMO_CONN_DATABASE
    """
    if schema_name is None:
        schema_name = _get_context_schema()
        if schema_name:
            logger.debug(
                f"copy_to_sql: schema_name not provided, using '{schema_name}' "
                "from tmo_create_context"
            )

    # Only pass schema_name when it is set — teradataml queries dbc.databasesV
    # to validate the value and raises an error when None is passed explicitly.
    if schema_name is not None:
        _teradataml_copy_to_sql(
            df, table_name=table_name, schema_name=schema_name, **kwargs
        )
    else:
        _teradataml_copy_to_sql(df, table_name=table_name, **kwargs)


# ---------------------------------------------------------------------------
# DataFrame.to_sql — schema-aware wrapper + monkey-patch
# ---------------------------------------------------------------------------

# Capture the original teradataml implementation before we replace it so both
# the standalone helper and the monkey-patch can delegate to it without risk
# of infinite recursion.
_original_DataFrame_to_sql = DataFrame.to_sql


def _resolve_schema_and_call_to_sql(
    df_instance: DataFrame,
    table_name: str,
    schema_name: Optional[str] = None,
    **kwargs,
) -> None:
    """Shared implementation used by both ``to_sql`` and the DataFrame patch.

    Resolves schema_name from tmo_create_context when not provided, then
    delegates to the original teradataml ``DataFrame.to_sql``.
    """
    if schema_name is None:
        schema_name = _get_context_schema()
        if schema_name:
            logger.debug(
                f"to_sql: schema_name not provided, using '{schema_name}' "
                "from tmo_create_context"
            )
    # Only pass schema_name when it is set — teradataml queries dbc.databasesV
    # to validate the value and raises an error when None is passed explicitly.
    if schema_name is not None:
        _original_DataFrame_to_sql(
            df_instance, table_name, schema_name=schema_name, **kwargs
        )
    else:
        _original_DataFrame_to_sql(df_instance, table_name, **kwargs)


def to_sql(
    df: DataFrame, table_name: str, schema_name: Optional[str] = None, **kwargs
) -> None:
    """
    Wrapper around teradataml.DataFrame.to_sql that automatically uses the
    database/schema configured via tmo_create_context if schema_name is not
    explicitly provided.

    Takes the same parameters as teradataml.DataFrame.to_sql. If schema_name is
    not specified, it is resolved from the VMO_CONN_DATABASE environment variable
    (set by tmo_create_context) or from the active teradataml configure settings.

    Args:
        df: teradataml DataFrame to write to Teradata.
        table_name (str): Name of the target Teradata table.
        schema_name (str, optional): Database/schema name. If not provided, uses
            the database configured via tmo_create_context (VMO_CONN_DATABASE).
        **kwargs: Additional keyword arguments forwarded to
            teradataml.DataFrame.to_sql (e.g. if_exists, primary_index,
            temporary, types, etc.).

    Example:
        >>> from tmo import to_sql
        >>> to_sql(df=my_tdf, table_name="my_table", if_exists="replace")
        # schema_name resolved automatically from VMO_CONN_DATABASE
    """
    _resolve_schema_and_call_to_sql(df, table_name, schema_name=schema_name, **kwargs)


def _tmo_patched_DataFrame_to_sql(
    self: DataFrame, table_name: str, schema_name: Optional[str] = None, **kwargs
) -> None:
    """Schema-aware replacement for teradataml.DataFrame.to_sql.

    Installed on ``teradataml.DataFrame`` at import time so users can call
    ``df.to_sql(table_name)`` directly — schema_name is resolved automatically
    from tmo_create_context, exactly like the standalone ``to_sql`` helper.

    All original parameters (if_exists, primary_index, temporary, types, …)
    are forwarded unchanged.
    """
    _resolve_schema_and_call_to_sql(self, table_name, schema_name=schema_name, **kwargs)


# Apply the patch so ``df.to_sql(...)`` benefits from automatic schema resolution.
DataFrame.to_sql = _tmo_patched_DataFrame_to_sql


def execute_sql_in_context(context: Engine, statement: str, parameters=None):
    from teradataml.common.exceptions import TeradataMlException
    from teradataml.common.messages import Messages
    from teradataml.common.messagecodes import MessageCodes

    if context is None:
        raise TeradataMlException(
            Messages.get_message(MessageCodes.INVALID_CONTEXT_CONNECTION),
            MessageCodes.INVALID_CONTEXT_CONNECTION,
        )

    # NOTE: the cursor and the pooled connection MUST be released before this
    # function returns. The previous implementation left the teradatasql cursor
    # open and never returned the connection to the pool, which kept an active
    # request on the session. The next statement issued on that same session
    # then failed with:
    #   [Error 3105] [SQLState HY000] Dispatcher internal error:
    #   Please do not re-submit request.
    # This was especially visible with JWT sessions during `evaluate`, where
    # record_evaluation_stats issues several statements back to back.
    #
    # We materialise the result here so callers keep the familiar cursor-like
    # API (fetchall/fetchone/iteration/rowcount/description) while the
    # underlying resources are freed immediately. The connection is returned to
    # the pool WITHOUT physically disconnecting, so session-scoped objects such
    # as VOLATILE tables created by a previous statement remain visible to
    # subsequent statements that reuse the same session.
    raw_conn = context.raw_connection()
    try:
        cursor = raw_conn.driver_connection.cursor()
        try:
            cursor.execute(statement, parameters)
            # `description` is None for statements that do not produce a result
            # set (DDL/DML such as CREATE/INSERT/DELETE/SET QUERY_BAND).
            rows = cursor.fetchall() if cursor.description is not None else None
            rowcount = cursor.rowcount
            description = cursor.description
        finally:
            cursor.close()
    finally:
        raw_conn.close()

    if (rowcount is None or rowcount < 0) and rows is not None:
        rowcount = len(rows)

    return _MaterializedResult(rows, rowcount, description)


class _MaterializedResult:
    """Eagerly-fetched, cursor-like result.

    Holds the rows already read from the cursor so the underlying pooled
    connection and cursor can be released immediately (preventing the leaked
    active-request that caused Teradata error 3105). Exposes the subset of the
    DBAPI cursor API used across the SDK: ``fetchall``, ``fetchone``,
    ``fetchmany``, iteration, ``rowcount`` and ``description``.
    """

    def __init__(self, rows, rowcount, description):
        self._rows = list(rows) if rows is not None else []
        self.rowcount = rowcount if rowcount is not None else -1
        self.description = description

    def fetchall(self):
        rows, self._rows = self._rows, []
        return rows

    def fetchone(self):
        return self._rows.pop(0) if self._rows else None

    def fetchmany(self, size=1):
        chunk = self._rows[:size]
        del self._rows[:size]
        return chunk

    def __iter__(self):
        rows, self._rows = self._rows, []
        return iter(rows)

    def __len__(self):
        return len(self._rows)


def execute_sql(statement: str, parameters=None):
    return execute_sql_in_context(get_context(), statement, parameters)


def _get_context_schema() -> Optional[str]:
    """
    Resolves the default schema/database from the tmo_create_context configuration.

    Resolution order:
    1. VMO_CONN_DATABASE environment variable (primary source, same as tmo_create_context).
    2. teradataml configure.temp_table_database (set by tmo_create_context).
    3. teradataml configure._current_database_name (active connection database).

    Returns:
        str | None: The resolved schema/database name, or None if not configured.
    """
    # 1. Primary: VMO_CONN_DATABASE env var (same source as tmo_create_context)
    database = os.getenv("VMO_CONN_DATABASE")
    if database:
        return database

    # 2. Fallback: teradataml configure settings populated by tmo_create_context
    try:
        from teradataml import configure

        if getattr(configure, "temp_table_database", None):
            return configure.temp_table_database

        if getattr(configure, "_current_database_name", None):
            return configure._current_database_name
    except Exception as e:
        logger.debug(f"Could not resolve schema from teradataml configure: {e}")

    return None
