# src/canonmap/connectors/mysql_connector/db_client.py

from typing import Any, List, Optional

from canonmap.connectors.mysql_connector.models import DMLResult, CreateHelperFieldsPayload
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
        if_exists: str = "append",
    ) -> int:
        """Import a CSV/XLSX/TSV file into MySQL.

        - Infers accurate MySQL types with robust coercion rules
        - Creates the table if missing (or replaces if requested)
        - Appends by default when table exists
        Returns number of rows written.
        """
        return _import_table_from_file(
            self._connector, file_path, table_name, if_exists=if_exists
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
        if_exists: str = "error",
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
            if_exists=if_exists,
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


