# src/canonmap/connectors/mysql_connector/services/schema_service.py

from __future__ import annotations

from typing import Any, Optional

from canonmap.connectors.mysql_connector.models import DMLResult
from canonmap.connectors.mysql_connector.utils.sql_identifiers import quote_identifier as _q


def _primary_key_columns(connector: Any, table_name: str) -> list[str]:
    with connector.get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT k.COLUMN_NAME
            FROM information_schema.TABLE_CONSTRAINTS t
            JOIN information_schema.KEY_COLUMN_USAGE k
              ON k.CONSTRAINT_NAME = t.CONSTRAINT_NAME
             AND k.TABLE_SCHEMA = t.TABLE_SCHEMA
             AND k.TABLE_NAME = t.TABLE_NAME
            WHERE t.CONSTRAINT_TYPE = 'PRIMARY KEY'
              AND t.TABLE_SCHEMA = DATABASE()
              AND t.TABLE_NAME = %s
            ORDER BY k.ORDINAL_POSITION
            """,
            (table_name,),
        )
        cols = [r[0] for r in cur.fetchall()]
        cur.close()
        return cols


def _column_exists(connector: Any, table_name: str, column_name: str) -> bool:
    with connector.get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT 1
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = %s
              AND COLUMN_NAME = %s
            LIMIT 1
            """,
            (table_name, column_name),
        )
        exists = cur.fetchone() is not None
        cur.close()
        return exists


def _existing_auto_increment_column(connector: Any, table_name: str) -> Optional[str]:
    with connector.get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT COLUMN_NAME
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = %s
              AND EXTRA LIKE '%auto_increment%'
            LIMIT 1
            """,
            (table_name,),
        )
        row = cur.fetchone()
        cur.close()
        return row[0] if row else None


def create_auto_increment_pk(
    connector: Any,
    table_name: str,
    field_name: str = "id",
    *,
    replace: bool = False,
    unsigned: bool = True,
    start_with: Optional[int] = None,
) -> DMLResult:
    """Create an AUTO_INCREMENT primary key column.

    - Drops existing PK if replace=True (but will not automatically remove AUTO_INCREMENT from other columns)
    - Adds the column if missing and sets it as PRIMARY KEY with AUTO_INCREMENT
    - If start_with is provided (> 0), sets table AUTO_INCREMENT to that value
    """

    existing_ai = _existing_auto_increment_column(connector, table_name)
    if existing_ai and existing_ai != field_name:
        raise RuntimeError(
            f"Table '{table_name}' already has AUTO_INCREMENT on column '{existing_ai}'. "
            "Please remove it before creating a new AUTO_INCREMENT primary key."
        )

    pk_cols = _primary_key_columns(connector, table_name)
    if pk_cols:
        if not replace:
            raise RuntimeError(
                f"Table '{table_name}' already has a PRIMARY KEY on ({', '.join(pk_cols)}). "
                "Pass replace=True to drop and recreate."
            )
        connector.execute_query(f"ALTER TABLE {_q(table_name)} DROP PRIMARY KEY", allow_writes=True)

    col_exists = _column_exists(connector, table_name, field_name)
    t = _q(table_name)
    c = _q(field_name)
    unsigned_sql = " UNSIGNED" if unsigned else ""

    if not col_exists:
        sql = (
            f"ALTER TABLE {t} "
            f"ADD COLUMN {c} BIGINT{unsigned_sql} NOT NULL AUTO_INCREMENT, "
            f"ADD PRIMARY KEY ({c})"
        )
        connector.execute_query(sql, allow_writes=True)
    else:
        connector.execute_query(f"ALTER TABLE {t} ADD PRIMARY KEY ({c})", allow_writes=True)
        connector.execute_query(
            f"ALTER TABLE {t} MODIFY COLUMN {c} BIGINT{unsigned_sql} NOT NULL AUTO_INCREMENT",
            allow_writes=True,
        )

    if start_with is not None and start_with > 0:
        connector.execute_query(
            f"ALTER TABLE {t} AUTO_INCREMENT = {int(start_with)}",
            allow_writes=True,
        )

    return {"affected_rows": 0}


