# src/canonmap/connectors/mysql_connector/db_client.py

from typing import Any, List, Optional
import json
import os
from decimal import Decimal
from datetime import date, datetime, time

from canonmap.connectors.mysql_connector.models import (
    DMLResult,
    CreateHelperFieldsPayload,
    TableField,
    TableFieldDict,
    TableFieldInput,
)
from canonmap.connectors.mysql_connector.connector import MySQLConnector
from canonmap.connectors.mysql_connector.services.helper_fields_service import (
    create_helper_fields as _create_helper_fields,
)
from canonmap.connectors.mysql_connector.services.import_table_service import (
    import_table_from_file as _import_table_from_file,
)
from canonmap.connectors.mysql_connector.services import constraint_service as constraints
from canonmap.connectors.mysql_connector.services import field_service as fields
from canonmap.connectors.mysql_connector.services import schema_service as schema
from canonmap.connectors.mysql_connector.utils.sql_identifiers import (
    quote_identifier as _q,
)


class DBClient:
    """High-level DB client using MySQLConnector."""

    def __init__(self, connector: MySQLConnector):
        self._connector = connector

    def create_helper_fields(
        self,
        payload: "dict | CreateHelperFieldsPayload",
    ) -> None:
        """Facade method; delegates to the standalone helper implementation.

        Preferred input is a plain dict or CreateHelperFieldsPayload.
        """
        _create_helper_fields(self._connector, payload)

    def import_table_from_file(
        self,
        file_path: str,
        table_name: Optional[str] = None,
        *,
        if_table_exists: str = "append",
    ) -> int:
        """Import a CSV/XLSX/TSV file into MySQL.

        - Infers accurate MySQL types with robust coercion rules
        - Creates the table if missing (or replaces if requested)
        - Appends by default when table exists
        Returns number of rows written.
        """
        return _import_table_from_file(
            self._connector, file_path, table_name, if_table_exists=if_table_exists
        )

    def create_table(
        self,
        table_name: str,
        fields_ddl: str,
        *,
        if_not_exists: bool = True,
        temporary: bool = False,
        table_options: Optional[str] = None,
    ) -> DMLResult:
        """Create a table with the provided DDL.

        - table_name: unqualified table name; will be quoted with backticks
        - fields_ddl: raw field definitions, e.g. "id BIGINT PRIMARY KEY, name VARCHAR(255) NOT NULL"
        - if_not_exists: include IF NOT EXISTS guard
        - temporary: create a TEMPORARY table
        - table_options: optional suffix (e.g. "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")
        """

        prefix = "CREATE " + ("TEMPORARY " if temporary else "") + "TABLE "
        if_clause = "IF NOT EXISTS " if if_not_exists else ""
        name_sql = _q(table_name)
        options_sql = f" {table_options.strip()}" if table_options and table_options.strip() else ""
        sql = f"{prefix}{if_clause}{name_sql} ({fields_ddl}){options_sql}"

        # Execute as a write. MySQL returns rowcount=0 for DDL, we surface that in the DMLResult shape.
        result = self._connector.execute_query(sql, params=None, allow_writes=True)  # type: ignore
        return result  # type: ignore[return-value]

    def create_field(
        self,
        table_name: str,
        field_name: str,
        field_ddl: Optional[str] = None,
        *,
        if_field_exists: str = "error",
        first: bool = False,
        after: Optional[str] = None,
        sample_values: Optional[List[Any]] = None,
    ) -> DMLResult:
        """Create a field (column) on an existing table, delegating to the field util.

        See util for inference details.
        """
        return fields.create_field(
            self._connector,
            table_name,
            field_name,
            field_ddl,
            if_field_exists=if_field_exists,
            first=first,
            after=after,
            sample_values=sample_values,
        )  # type: ignore

    def create_auto_increment_pk(
        self,
        table_name: str,
        field_name: str = "id",
        *,
        replace: bool = False,
        unsigned: bool = True,
        start_with: Optional[int] = None,
    ) -> DMLResult:
        """Create an AUTO_INCREMENT primary key column on a table (or replace existing PK)."""
        return schema.create_auto_increment_pk(
            self._connector,
            table_name,
            field_name,
            replace=replace,
            unsigned=unsigned,
            start_with=start_with,
        )  # type: ignore

    def add_primary_key(self, table_name: str, columns: List[str], *, replace: bool = False) -> DMLResult:
        """Add a PRIMARY KEY on one or more columns. Set replace=True to drop existing PK first."""
        return constraints.add_primary_key(
            self._connector, table_name, columns, replace=replace
        )  # type: ignore

    def drop_primary_key(self, table_name: str) -> DMLResult:
        """Drop the PRIMARY KEY from a table."""
        return constraints.drop_primary_key(self._connector, table_name)  # type: ignore

    def add_foreign_key(
        self,
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
        """Add a FOREIGN KEY constraint. If constraint_name is provided and replace=True, drop it first.

        on_delete/on_update accepted values (case-insensitive): CASCADE, SET NULL, RESTRICT, NO ACTION
        """
        return constraints.add_foreign_key(
            self._connector,
            table_name,
            columns,
            ref_table,
            ref_columns,
            constraint_name=constraint_name,
            on_delete=on_delete,
            on_update=on_update,
            replace=replace,
        )  # type: ignore

    def drop_foreign_key(self, table_name: str, constraint_name: str) -> DMLResult:
        """Drop a FOREIGN KEY by name."""
        return constraints.drop_foreign_key(
            self._connector, table_name, constraint_name
        )  # type: ignore

    def create_database(
        self,
        database_name: str,
        *,
        if_not_exists: bool = True,
        charset: Optional[str] = None,
        collate: Optional[str] = None,
    ) -> DMLResult:
        """Create a database/schema.

        - if_not_exists: include IF NOT EXISTS guard
        - charset: optional DEFAULT CHARACTER SET (e.g., "utf8mb4")
        - collate: optional COLLATE (e.g., "utf8mb4_0900_ai_ci")
        """

        if_clause = "IF NOT EXISTS " if if_not_exists else ""
        name_sql = _q(database_name)
        charset_sql = f" DEFAULT CHARACTER SET {charset.strip()}" if charset and charset.strip() else ""
        collate_sql = f" COLLATE {collate.strip()}" if collate and collate.strip() else ""
        sql = f"CREATE DATABASE {if_clause}{name_sql}{charset_sql}{collate_sql}"

        result = self._connector.execute_query(sql, params=None, allow_writes=True)  # type: ignore
        return result  # type: ignore[return-value]

    def generate_schema(
        self,
        table_fields: Optional[List[TableFieldInput]] = None,
        num_examples: int = 10,
        *,
        save_location: Optional[str] = None,
        schema_name: str,
        if_schema_exists: str = "replace",
    ) -> dict:
        """Generate schema metadata for the current database.

        - When table_fields is provided, restrict output to those table/field pairs
          (table_fields can be a list of TableField, dicts with keys {table_name, field_name}, or
          strings like "table.field" as per TableFieldInput contract).
        - When table_fields is None or empty, include all user tables in the current database.
        - For each field include:
            - name
            - data_type (information_schema.COLUMNS.DATA_TYPE)
            - column_type (full MySQL type)
            - is_nullable (bool)
            - default
            - field_example_data: up to num_examples random distinct non-null values
            - datetime_format: for DATE/DATETIME/TIMESTAMP/TIME/YEAR types, the expected format string
        - Excludes helper/dunder columns (e.g., __<field>_<transform>__ and __cm_tmp_pk__).
        - If save_location is provided, schema will be written to that directory using schema_name.
          schema_name may or may not include a .json extension; it will be enforced.
        - if_schema_exists: "skip" to not overwrite existing file; "replace" to overwrite.
        """

        def _normalize_table_fields(raw: Optional[List[TableFieldInput]]) -> dict[str, set[str]]:
            mapping: dict[str, set[str]] = {}
            if not raw:
                return mapping
            for item in raw:
                if isinstance(item, TableField):
                    t, f = item.table_name, item.field_name
                elif isinstance(item, dict):  # TableFieldDict
                    t = str(item.get("table_name", "")).strip()
                    f = str(item.get("field_name", "")).strip()
                elif isinstance(item, str):
                    if "." in item:
                        t, f = item.split(".", 1)
                    elif ":" in item:
                        t, f = item.split(":", 1)
                    else:
                        # If malformed, skip silently; upstream validation is expected
                        continue
                    t, f = t.strip(), f.strip()
                else:
                    continue
                if not t or not f:
                    continue
                # Exclude dunder/helper columns
                if f.startswith("__") and f.endswith("__"):
                    continue
                mapping.setdefault(t, set()).add(f)
            return mapping

        def _infer_datetime_format(data_type: str, column_type: str) -> Optional[str]:
            dt = (data_type or "").lower()
            has_fractional = "(" in column_type and ")" in column_type and column_type.lower().rstrip().endswith(")") and any(ch.isdigit() for ch in column_type)
            if dt == "date":
                return "%Y-%m-%d"
            if dt in ("datetime", "timestamp"):
                return "%Y-%m-%d %H:%M:%S.%f" if has_fractional else "%Y-%m-%d %H:%M:%S"
            if dt == "time":
                return "%H:%M:%S.%f" if has_fractional else "%H:%M:%S"
            if dt == "year":
                return "%Y"
            return None

        # Build the table -> fields mapping if provided
        requested: dict[str, set[str]] = _normalize_table_fields(table_fields)

        def _to_json_safe(value: Any) -> Any:
            if value is None:
                return None
            if isinstance(value, Decimal):
                # Preserve exact representation
                return str(value)
            if isinstance(value, (datetime, date, time)):
                # ISO format for temporal values
                return value.isoformat()
            if isinstance(value, (bytes, bytearray)):
                # Best-effort UTF-8 decode
                try:
                    return value.decode("utf-8")  # type: ignore[arg-type]
                except Exception:
                    return str(value)
            return value

        # Fetch candidate tables
        tables: List[str] = []
        if requested:
            tables = [t for t in requested.keys() if t and not t.startswith("__")]
        else:
            rows_resp = self._connector.execute_query(
                """
                SELECT TABLE_NAME
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
                """
            )
            rows = rows_resp.get("data") or []
            tables = [r["TABLE_NAME"] for r in rows if r["TABLE_NAME"] and not str(r["TABLE_NAME"]).startswith("__")]

        result: dict[str, dict] = {"tables": {}}

        # Normalize num_examples
        try:
            k = int(num_examples)
            num = k if k > 0 else 10
        except Exception:
            num = 10

        for table_name in tables:
            t_q = _q(table_name)
            # Fetch columns metadata
            cols_resp = self._connector.execute_query(
                """
                SELECT COLUMN_NAME, DATA_TYPE, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION
                """,
                [table_name],
            )
            cols = cols_resp.get("data") or []

            # Filter columns: exclude dunder/helper
            def _is_helper_column(name: str) -> bool:
                if not name:
                    return True
                n = name.strip()
                return (n.startswith("__") and n.endswith("__")) or n == "__cm_tmp_pk__"

            allowed_fields: set[str] | None = requested.get(table_name) if requested else None

            fields_list: List[dict] = []
            for c in cols:
                col_name = c["COLUMN_NAME"]
                if _is_helper_column(col_name):
                    continue
                if allowed_fields is not None and col_name not in allowed_fields:
                    continue

                data_type = c["DATA_TYPE"]
                column_type = c["COLUMN_TYPE"]
                is_nullable = str(c["IS_NULLABLE"]).upper() == "YES"
                default_val = c["COLUMN_DEFAULT"]

                # Fetch random distinct non-null examples
                examples_sql = f"SELECT DISTINCT { _q(col_name) } AS val FROM { t_q } WHERE { _q(col_name) } IS NOT NULL ORDER BY RAND() LIMIT {int(num)}"
                example_rows_resp = self._connector.execute_query(examples_sql)
                example_rows = example_rows_resp.get("data") or []
                example_values = [_to_json_safe(r.get("val")) for r in example_rows]

                field_info: dict[str, Any] = {
                    "name": col_name,
                    "data_type": data_type,
                    "column_type": column_type,
                    "is_nullable": is_nullable,
                    "default": _to_json_safe(default_val),
                    "field_example_data": example_values,
                }

                dt_fmt = _infer_datetime_format(data_type, column_type)
                if dt_fmt:
                    field_info["datetime_format"] = dt_fmt

                fields_list.append(field_info)

            result["tables"][table_name] = {"fields": fields_list}

        # Persist to disk when requested
        if save_location:
            mode = (if_schema_exists or "replace").strip().lower()
            if mode not in ("skip", "replace"):
                raise ValueError("if_schema_exists must be one of: 'skip', 'replace'")
            # Enforce filename ends with .json, sanitize to basename
            raw_name = (schema_name or "").strip()
            if not raw_name:
                raise ValueError("schema_name must be a non-empty string when save_location is provided")
            base = os.path.basename(raw_name)
            if not base.lower().endswith(".json"):
                base = f"{base}.json"

            dir_path = os.path.abspath(os.path.expanduser(save_location))
            os.makedirs(dir_path, exist_ok=True)

            save_path = os.path.join(dir_path, base)
            if os.path.exists(save_path) and mode == "skip":
                pass
            else:
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

        return result
