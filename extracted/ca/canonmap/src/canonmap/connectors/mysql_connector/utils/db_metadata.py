# src/canonmap/connectors/mysql_connector/utils/db_metadata.py

from __future__ import annotations

from typing import Any, Optional


def table_exists(connector: Any, table_name: str) -> bool:
    with connector.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 1
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = %s
            LIMIT 1
            """,
            (table_name,),
        )
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists


def column_exists(connector: Any, table_name: str, column_name: str) -> bool:
    with connector.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
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
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists


def get_primary_key_columns(connector: Any, table_name: str) -> list[str]:
    with connector.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
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
        rows = cursor.fetchall()
        cursor.close()
        return [r[0] for r in rows]


def get_existing_auto_increment_column(connector: Any, table_name: str) -> Optional[str]:
    with connector.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
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
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else None


