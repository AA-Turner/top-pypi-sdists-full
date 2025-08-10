# src/canonmap/connectors/mysql_connector/services/import_table_service.py

from __future__ import annotations

import os
import re
from typing import Any, Optional, Tuple

import pandas as pd
from sqlalchemy import create_engine, types
from sqlalchemy.engine import URL
from canonmap.connectors.mysql_connector.utils.sql_identifiers import quote_identifier as _q
from canonmap.connectors.mysql_connector.utils.db_metadata import table_exists as _table_exists
from canonmap.connectors.mysql_connector.utils.type_inference import (
    coerce_boolean_series as _coerce_boolean_series,
    coerce_datetime_series as _coerce_datetime_series,
    coerce_numeric_series as _coerce_numeric_series,
)


def _read_file(file_path: str) -> pd.DataFrame:
    ext = os.path.splitext(file_path)[1].lower()
    if ext in {".csv", ".tsv"}:
        sep = "\t" if ext == ".tsv" else ","
        return pd.read_csv(file_path, dtype=str, sep=sep)
    if ext in {".xlsx", ".xls"}:
        return pd.read_excel(file_path, dtype=str)
    raise ValueError(f"Unsupported file extension for import: {ext}")


def _infer_schema_and_coerce(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict, str]:
    sql_types: dict[str, Any] = {}
    column_ddls: list[str] = []
    coerced = pd.DataFrame(index=df.index)

    for col in df.columns:
        series = df[col]

        # Try datetime
        dt_series, ok_dt = _coerce_datetime_series(series)
        if ok_dt:
            sql_types[col] = types.DateTime()
            coerced[col] = dt_series
            column_ddls.append(f"{_q(col)} DATETIME")
            continue

        # Try numeric
        num_series, dec_meta, is_int, ok_num = _coerce_numeric_series(series)
        if ok_num:
            coerced[col] = num_series
            if is_int:
                sql_types[col] = types.BigInteger()
                column_ddls.append(f"{_q(col)} BIGINT")
            else:
                precision, scale = dec_meta if dec_meta else (38, 9)
                sql_types[col] = types.Numeric(precision=precision, scale=scale)
                column_ddls.append(f"{_q(col)} DECIMAL({precision},{scale})")
            continue

        # Try boolean
        bool_series, ok_bool = _coerce_boolean_series(series)
        if ok_bool:
            sql_types[col] = types.Boolean()
            coerced[col] = bool_series
            column_ddls.append(f"{_q(col)} BOOLEAN")
            continue

        # Fallback to VARCHAR/TEXT
        s = series.astype("string").str.strip()
        max_len = int(s.map(lambda x: len(x) if x is not None and x is not pd.NA else 0).max())
        coerced[col] = s.where(s.ne(""), None)
        if max_len <= 0:
            max_len = 255
        if max_len > 1024:
            sql_types[col] = types.Text()
            column_ddls.append(f"{_q(col)} TEXT")
        else:
            sql_types[col] = types.String(length=max(32, max_len))
            column_ddls.append(f"{_q(col)} VARCHAR({max(32, max_len)})")

    fields_ddl = ", ".join(column_ddls)
    return coerced, sql_types, fields_ddl


def _import_table_from_file(
    connector: Any,
    file_path: str,
    table_name: Optional[str] = None,
    *,
    if_exists: str = "append",
) -> int:
    """Import CSV/XLSX file into MySQL with type inference and coercion.

    - Reads the file with dtype=str, infers robust types, coerces invalid values to NULL
    - Creates the table with accurate MySQL types
    - Loads the data in batches
    Returns number of rows written.
    """
    df_raw = _read_file(file_path)

    if table_name is None:
        base = os.path.basename(file_path)
        stem = os.path.splitext(base)[0]
        table_name = re.sub(r"[^A-Za-z0-9_]+", "_", stem).lower().strip("_") or "imported_table"

    # Infer schema and coerce values
    df, sql_types, fields_ddl = _infer_schema_and_coerce(df_raw)

    # Build SQLAlchemy engine from connector config
    cfg = connector.config
    url = URL.create(
        "mysql+mysqlconnector",
        username=cfg.user,
        password=cfg.password,
        host=cfg.host,
        database=cfg.database,
    )
    engine = create_engine(url, pool_pre_ping=True)

    # Handle table existence policy
    exists = _table_exists(connector, table_name)
    if if_exists not in {"append", "replace", "fail"}:
        raise ValueError("if_exists must be one of 'append' | 'replace' | 'fail'")
    if exists:
        if if_exists == "fail":
            raise RuntimeError(f"Table '{table_name}' already exists")
        if if_exists == "replace":
            connector.execute_query(
                f"DROP TABLE IF EXISTS {_q(table_name)}",
                allow_writes=True,
            )
            exists = False

    # Create table if needed with precise DDL
    if not exists:
        connector.execute_query(
            f"CREATE TABLE {_q(table_name)} ({fields_ddl})",
            allow_writes=True,
        )

    # Load data using pandas
    try:
        df.to_sql(
            table_name,
            con=engine,
            if_exists="append",
            index=False,
            dtype=sql_types,
            method="multi",
            chunksize=1000,
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        # Fallback: if appending into an existing table fails due to range/type issues,
        # try widening the offending numeric column and retry once.
        if "Out of range value for column" in msg:
            # Extract column name between quotes
            import re as _re
            m = _re.search(r"for column '([^']+)'", msg)
            if m:
                offending = m.group(1)
                try:
                    connector.execute_query(
                        f"ALTER TABLE {_q(table_name)} MODIFY COLUMN {_q(offending)} DECIMAL(38,9) NULL",
                        allow_writes=True,
                    )
                    # Retry once
                    df.to_sql(
                        table_name,
                        con=engine,
                        if_exists="append",
                        index=False,
                        dtype=sql_types,
                        method="multi",
                        chunksize=1000,
                    )
                except Exception:
                    raise
                else:
                    return int(len(df))
        raise

    return int(len(df))


def import_table_from_file(
    connector: Any,
    file_path: str,
    table_name: Optional[str] = None,
    *,
    if_exists: str = "append",
) -> int:
    """Public wrapper for importing a table from file (non-underscored API)."""
    return _import_table_from_file(connector, file_path, table_name, if_exists=if_exists)

