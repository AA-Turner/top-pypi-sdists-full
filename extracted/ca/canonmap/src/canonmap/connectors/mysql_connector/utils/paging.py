# src/canonmap/connectors/mysql_connector/utils/paging.py

from __future__ import annotations

from typing import Any, Optional

from canonmap.connectors.mysql_connector.utils.sql_identifiers import quote_identifier as _q


def fetch_chunk(
    connector: Any,
    table_name: str,
    pk_col: str,
    source_col: str,
    last_pk: Optional[Any],
    limit: int,
) -> list[dict]:
    table = _q(table_name)
    pk = _q(pk_col)
    src = _q(source_col)

    with connector.get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        if last_pk is None:
            sql = f"SELECT {pk} AS pk, {src} AS src FROM {table} ORDER BY {pk} ASC LIMIT %s"
            cursor.execute(sql, (limit,))
        else:
            sql = f"SELECT {pk} AS pk, {src} AS src FROM {table} WHERE {pk} > %s ORDER BY {pk} ASC LIMIT %s"
            cursor.execute(sql, (last_pk, limit))
        fetched = cursor.fetchall()
        cursor.close()

    rows: list[dict] = []
    for r in fetched:
        rows.append({pk_col: r["pk"], source_col: r["src"]})
    return rows


