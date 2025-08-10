# src/canonmap/connectors/mysql_connector/utils/dml.py

"""Data Manipulation Language (DML) helpers.

This module contains utilities for performing efficient data-changing
operations (INSERT/UPDATE/DELETE). The helpers here favor bulk-oriented SQL
to minimize round-trips and row-by-row updates.

Exposed helpers
---------------
- bulk_case_update_by_pk: Execute a single CASE-based UPDATE keyed by a list of
  primary-key values to set a target column per-row in one statement.

Design notes
------------
- All SQL identifiers are safely quoted using backticks.
- Values are parameterized; only the optional where_suffix is appended raw and
  is expected to be produced by trusted code (e.g., " AND (`col` IS NULL)").
- Each call runs inside a transaction via the provided connector.
"""

from __future__ import annotations

from typing import Any, Iterable

from canonmap.connectors.mysql_connector.utils.sql_identifiers import quote_identifier as _q


def bulk_case_update_by_pk(
    connector: Any,
    table_name: str,
    pk_col: str,
    target_col: str,
    updates: Iterable[tuple[Any, Any]],  # (new_value, pk)
    *,
    where_suffix: str = "",
) -> None:
    """Perform a batched UPDATE using a CASE expression keyed by primary key.

    This constructs and executes SQL of the form:

        UPDATE `table`
        SET `target` = CASE `pk`
            WHEN %s THEN %s
            WHEN %s THEN %s
            ...
        END
        WHERE `pk` IN (%s, %s, ...)[<where_suffix>]

    Parameters
    - connector: Object exposing transaction() and DB-API cursor to execute SQL
    - table_name: Name of the table to update
    - pk_col: Primary-key column name used to match rows
    - target_col: Column to set with per-row values
    - updates: Iterable of (new_value, pk_value) pairs
    - where_suffix: Optional raw SQL string appended to the WHERE clause for
      additional filtering (e.g., " AND (`target` IS NULL)"). Must be trusted.

    Notes
    - Identifiers are quoted with backticks; values are passed as parameters.
    - Executes inside a transaction; caller gets atomicity at statement scope.
    - Intended for medium-sized batches (e.g., a few thousand rows) as used by
      the helper-field population pipeline.
    """
    table = _q(table_name)
    pk = _q(pk_col)
    tgt = _q(target_col)

    pks = [pk for _, pk in updates]
    case_parts = []
    case_params: list[Any] = []
    for val, pkv in updates:
        case_parts.append("WHEN %s THEN %s")
        case_params.extend([pkv, val])

    in_params = pks
    sql = (
        f"UPDATE {table} "
        f"SET {tgt} = CASE {pk} " + " ".join(case_parts) + " END "
        f"WHERE {pk} IN (" + ",".join(["%s"] * len(in_params)) + ")" + where_suffix
    )
    params = tuple(case_params + in_params)

    with connector.transaction() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        cursor.close()


