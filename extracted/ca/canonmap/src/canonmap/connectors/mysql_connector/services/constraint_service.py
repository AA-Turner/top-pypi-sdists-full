# src/canonmap/connectors/mysql_connector/services/constraint_service.py

from __future__ import annotations

from typing import Any, List, Optional

from canonmap.connectors.mysql_connector.models import DMLResult
from canonmap.connectors.mysql_connector.utils.sql_identifiers import quote_identifier as _q


def add_primary_key(connector: Any, table_name: str, columns: List[str], *, replace: bool = False) -> DMLResult:
    table = _q(table_name)
    cols = ", ".join(_q(c) for c in columns)
    if replace:
        connector.execute_query(f"ALTER TABLE {table} DROP PRIMARY KEY", allow_writes=True)
    return connector.execute_query(
        f"ALTER TABLE {table} ADD PRIMARY KEY ({cols})",
        allow_writes=True,
    )


def drop_primary_key(connector: Any, table_name: str) -> DMLResult:
    table = _q(table_name)
    return connector.execute_query(f"ALTER TABLE {table} DROP PRIMARY KEY", allow_writes=True)


def add_foreign_key(
    connector: Any,
    table_name: str,
    columns: List[str],
    ref_table: str,
    ref_columns: List[str],
    *,
    constraint_name: Optional[str] = None,
    on_delete: Optional[str] = None,
    on_update: Optional[str] = None,
    replace: bool = False,
) -> DMLResult:
    valid_actions = {"CASCADE", "SET NULL", "RESTRICT", "NO ACTION"}

    def _action_sql(keyword: str, value: Optional[str]) -> str:
        if not value:
            return ""
        v = value.strip().upper()
        if v not in valid_actions:
            raise ValueError(f"Invalid {keyword} action: {value!r}")
        return f" {keyword} {v}"

    table = _q(table_name)
    ref_t = _q(ref_table)
    cols = ", ".join(_q(c) for c in columns)
    ref_cols = ", ".join(_q(c) for c in ref_columns)

    constraint_sql = f"CONSTRAINT {_q(constraint_name)} " if constraint_name else ""

    if replace and constraint_name:
        try:
            connector.execute_query(
                f"ALTER TABLE {table} DROP FOREIGN KEY {_q(constraint_name)}",
                allow_writes=True,
            )
        except Exception:
            # Ignore if it didn't exist
            pass

    sql = (
        f"ALTER TABLE {table} ADD {constraint_sql}FOREIGN KEY ({cols}) REFERENCES {ref_t} ({ref_cols})"
        f"{_action_sql('ON DELETE', on_delete)}{_action_sql('ON UPDATE', on_update)}"
    )
    return connector.execute_query(sql, allow_writes=True)


def drop_foreign_key(connector: Any, table_name: str, constraint_name: str) -> DMLResult:
    table = _q(table_name)
    fk = _q(constraint_name)
    return connector.execute_query(f"ALTER TABLE {table} DROP FOREIGN KEY {fk}", allow_writes=True)


