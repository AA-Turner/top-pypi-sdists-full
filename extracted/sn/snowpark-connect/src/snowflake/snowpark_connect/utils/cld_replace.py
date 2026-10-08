#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Run a CLD Iceberg replace's source query before the published table is dropped.

Glue catalog-linked databases reject ``CREATE OR REPLACE ... AS SELECT``
(093664), ``SWAP WITH`` (093059), and ``RENAME`` (004535), so a replace has
to ``DROP`` the target and ``CREATE`` it again. Running the source query
first surfaces row-level errors (bad casts, ``raise_error``) while the
published table still exists. The rows stay in Snowflake's persisted query
result; the load after the ``DROP`` reads them with ``RESULT_SCAN`` instead
of re-running the query or staging them in a table that external engines
could see.
"""

import uuid

from snowflake.snowpark import DataFrame, Session
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code


def _run_cld_replace_source_query(
    df: DataFrame,
    statement_params: dict[str, str] | None,
) -> str:
    """Execute ``df`` and return the query id of its result.

    ``DataFrame._execute_and_get_query_id`` runs the plan without fetching
    rows to the client and returns the id of the final statement, which is
    what ``RESULT_SCAN`` must read. Its docstring says stored procedures;
    the same call works for a client session, and the id it returns is the
    last query of the plan rather than an anonymous-block wrapper.
    """
    query_id = df._execute_and_get_query_id(statement_params=statement_params)
    try:
        uuid.UUID(query_id)
    except (TypeError, ValueError, AttributeError):
        exception = RuntimeError(
            f"Could not get a query id for the CLD replace source query: {query_id!r}"
        )
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception
    return query_id


def _attach_cld_replace_recovery(exc: BaseException, query_id: str) -> None:
    """Record how to load ``query_id`` on an exception the client will see.

    A failure of the ``CREATE`` or ``INSERT`` runs after the published table
    has been dropped. The source rows are still in Snowflake's result cache.
    ``str(exc)`` is the client message. Snowpark copies ``message`` into
    ``_pretty_msg`` when the exception is built, and later rewrites read
    ``message``, so the note has to be on both.
    """
    note = (
        "The published table was dropped before this statement failed. "
        "The source rows can still be loaded with "
        f"SELECT * FROM TABLE(RESULT_SCAN('{query_id}'))."
    )
    message = getattr(exc, "message", None)
    if isinstance(message, str):
        if note not in message:
            exc.message = f"{message} {note}"
        pretty = getattr(exc, "_pretty_msg", None)
        if isinstance(pretty, str) and note not in pretty:
            exc._pretty_msg = f"{pretty} {note}"
        return
    text = exc.args[0] if exc.args and isinstance(exc.args[0], str) else str(exc)
    if note not in text:
        tail = exc.args[1:] if exc.args else ()
        exc.args = (f"{text} {note}", *tail)


def _insert_cld_table_from_result_scan(
    session: Session,
    table_name: str,
    columns_sql: str,
    query_id: str,
    statement_params: dict[str, str] | None = None,
) -> None:
    """Load ``query_id`` into an already-created CLD Iceberg table.

    ``columns_sql`` is the target column list in the same order as the
    source query's output. ``INSERT`` assigns by position, so that list,
    ``SELECT *``, and the preceding ``CREATE`` must all come from the same
    fields in the same order.
    """
    session.sql(
        f"INSERT INTO {table_name} ({columns_sql}) "
        f"SELECT * FROM TABLE(RESULT_SCAN('{query_id}'))"
    ).collect(statement_params=statement_params)
