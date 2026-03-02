"""SQL compatibility layer — SQLite ↔ PostgreSQL."""
from __future__ import annotations

import re
from typing import Any

from salmalm.db.connection import _USE_PG

_OR_IGNORE_RE = re.compile(r"INSERT\s+OR\s+IGNORE\s+INTO", re.IGNORECASE)
_OR_REPLACE_RE = re.compile(
    r"INSERT\s+OR\s+REPLACE\s+INTO\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\)",
    re.IGNORECASE | re.DOTALL,
)


def _rewrite_insert_or_replace(sql: str) -> str:
    def _replace(match: re.Match[str]) -> str:
        table = match.group(1).strip()
        cols = [c.strip() for c in match.group(2).split(",")]
        vals = match.group(3).strip()
        conflict_col = cols[0]
        updates = ", ".join(f"{c}=EXCLUDED.{c}" for c in cols[1:])
        if not updates:
            return f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({vals}) ON CONFLICT ({conflict_col}) DO NOTHING"
        return (
            f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({vals}) "
            f"ON CONFLICT ({conflict_col}) DO UPDATE SET {updates}"
        )

    return _OR_REPLACE_RE.sub(_replace, sql)


def adapt_sql(sql: str) -> str:
    """Convert SQLite SQL to PostgreSQL-compatible SQL when needed."""
    if not _USE_PG:
        return sql

    out = sql.replace("?", "%s")
    out = _OR_IGNORE_RE.sub("INSERT INTO", out)
    if "INSERT OR REPLACE" in out.upper():
        out = _rewrite_insert_or_replace(out)
    return out


def q(sql: str, params: Any = None) -> tuple[str, Any]:
    """Return (adapted_sql, params) ready for conn.execute()."""
    return adapt_sql(sql), params
