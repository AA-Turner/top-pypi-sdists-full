# src/canonmap/connectors/mysql_connector/services/field_service.py

from __future__ import annotations

from typing import Any, List, Optional

from canonmap.connectors.mysql_connector.models import DMLResult
from canonmap.connectors.mysql_connector.utils.sql_identifiers import quote_identifier as _q


def _clean_numeric_string(value: Any) -> Optional[str]:
    try:
        import pandas as pd
    except Exception:  # pragma: no cover
        pd = None  # type: ignore
    if pd is not None and (value is None or (isinstance(value, float) and pd.isna(value))):
        return None
    s = str(value).strip()
    if s == "":
        return None
    import re as _re
    s = _re.sub(r"[\s,$]", "", s)
    if s.count(",") == 1 and s.count(".") == 0:
        s = s.replace(",", ".")
    return s


def _infer_mysql_type(samples: List[Any]) -> str:
    # Try datetime
    try:
        import pandas as pd
        dt = pd.to_datetime(pd.Series(samples, dtype="string"), errors="coerce", utc=False)
        if float(dt.notna().mean()) >= 0.9:
            return "DATETIME NULL"
    except Exception:
        pass

    # Try numeric
    from decimal import Decimal, InvalidOperation
    cleaned = [_clean_numeric_string(v) for v in samples]

    def to_decimal(x: Optional[str]) -> Optional[Decimal]:
        if x in (None, ""):
            return None
        try:
            return Decimal(x)
        except (InvalidOperation, ValueError):
            return None

    decimals = [to_decimal(x) for x in cleaned]
    non_null = [d for d in decimals if d is not None]
    non_null_ratio = (len(non_null) / max(1, len([v for v in samples if v is not None])))
    if len(non_null) >= 1 and non_null_ratio >= 0.9:
        int_like = all(d == d.to_integral_value() for d in non_null)
        if int_like:
            return "BIGINT NULL"
        # Estimate precision/scale
        max_digits = 1
        max_scale = 0
        for d in non_null:
            sign, digits, exp = d.as_tuple()
            digits_count = len(digits)
            scale = -exp if exp < 0 else 0
            integer_digits = digits_count - scale
            max_digits = max(max_digits, integer_digits + scale)
            max_scale = max(max_scale, scale)
        precision = min(max(1, max_digits), 38)
        scale = min(max(0, max_scale), 18)
        return f"DECIMAL({precision},{scale}) NULL"

    # Try boolean
    truthy = {"1", "true", "t", "yes", "y"}
    falsy = {"0", "false", "f", "no", "n"}

    def to_bool(x: Any) -> Optional[bool]:
        if x is None:
            return None
        s = str(x).strip().lower()
        if s in truthy:
            return True
        if s in falsy:
            return False
        return None

    bools = [to_bool(v) for v in samples]
    non_na_bools = [b for b in bools if b is not None]
    if len(non_na_bools) >= 1 and (len(non_na_bools) / max(1, len([v for v in samples if v is not None])) >= 0.9):
        return "BOOLEAN NULL"

    # Fallback VARCHAR sized to sample lengths
    try:
        lens = [len(str(v)) for v in samples if v is not None]
        max_len = max(lens) if lens else 255
    except Exception:
        max_len = 255
    if max_len > 1024:
        return "TEXT NULL"
    return f"VARCHAR({max(32, max_len)}) NULL"


def create_field(
    connector: Any,
    table_name: str,
    field_name: str,
    field_ddl: Optional[str] = None,
    *,
    if_exists: str = "error",
    first: bool = False,
    after: Optional[str] = None,
    sample_values: Optional[List[Any]] = None,
) -> DMLResult:
    if if_exists not in {"error", "skip", "replace"}:
        raise ValueError("if_exists must be one of 'error' | 'skip' | 'replace'")
    if first and after:
        raise ValueError("Specify either first=True or after=..., not both")

    # Check existence via information_schema
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
            (table_name, field_name),
        )
        exists = cur.fetchone() is not None
        cur.close()

    table = _q(table_name)
    col = _q(field_name)
    pos_clause = " FIRST" if first else (f" AFTER {_q(after)}" if after else "")

    ddl = field_ddl.strip() if field_ddl else None
    if not ddl:
        if sample_values and len(sample_values) > 0:
            ddl = _infer_mysql_type(sample_values)
        else:
            ddl = "VARCHAR(255) NULL"

    if exists:
        if if_exists == "skip":
            return {"affected_rows": 0}
        if if_exists == "error":
            raise RuntimeError(f"Column {field_name!r} already exists in table {table_name!r}")
        if if_exists == "replace":
            connector.execute_query(
                f"ALTER TABLE {table} DROP COLUMN {col}", allow_writes=True
            )
            return connector.execute_query(
                f"ALTER TABLE {table} ADD COLUMN {col} {ddl}{pos_clause}", allow_writes=True
            )

    # Add new column
    return connector.execute_query(
        f"ALTER TABLE {table} ADD COLUMN {col} {ddl}{pos_clause}", allow_writes=True
    )


