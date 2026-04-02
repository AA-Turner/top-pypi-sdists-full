from typing import Callable, Optional

import sqlalchemy as db
from sqlalchemy import (
    Column,
    Engine,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    create_engine,
    inspect,
)

from seshat.transformer.schema import Schema


class SQLMixin:
    filters: Optional[dict]
    table_name: str
    query: Optional[str]
    query_fn: Optional[Callable]
    schema: Schema
    url: str
    limit: Optional[int] = None
    _engine: Optional[Engine] = None

    def get_query(self, filters=None, *args, **kwargs):
        query = f"SELECT {self._get_query_columns()} FROM {self.table_name}"
        if getattr(self, "query", None):
            query = self.query
        if getattr(self, "query_fn", None):
            query = self.query_fn(*args, **kwargs)
        return query + self.generate_sql_from_filter(
            {**self.filters, **(filters or {})}
        )

    def _get_query_columns(self):
        columns = "*"
        if self.schema and self.schema.exclusive:
            columns = self.schema.selected_cols_str
        return columns

    @classmethod
    def generate_sql_from_filter(cls, filters):
        sql = ""
        for key, value in filters.items():
            prefix = "AND"
            if not sql:
                prefix = "WHERE"
            if isinstance(value, dict):
                val = value["val"]
                if "type" in value:
                    val = cls.get_converted_value(value["val"], value["type"])
                sql += f" {prefix} {key} {value['op']} {val}"
            else:
                sql += f" {prefix} {key}={value}"
        return sql

    @staticmethod
    def get_converted_value(value, type_):
        if type_ == "str":
            return f"'{value}'"
        return value

    def get_engine(self) -> Engine:
        """
        Get or create a cached SQLAlchemy engine.

        The engine is cached to avoid creating multiple connection pools,
        which can lead to connection exhaustion under concurrent load.

        Uses pool_pre_ping=True to automatically handle stale/broken connections
        by testing them before use and reconnecting if needed.
        """
        if self._engine is None:
            self._engine = create_engine(self.url, pool_pre_ping=True)
        return self._engine

    def dispose_engine(self):
        """
        Dispose the cached engine and its connection pool.

        Call this method when you're done using the database connection
        to properly release all resources.
        """
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None

    def get_from_db(self, query):
        with self.get_engine().connect() as conn:
            result = conn.execute(query)
            result = result.fetchmany(self.limit) if self.limit else result.fetchall()
            conn.close()
            return result

    def write_on_db(self, *args, **kwargs):
        with self.get_engine().connect() as conn:
            trans = conn.begin()
            conn.execute(*args, **kwargs)
            trans.commit()
            conn.close()

    def _parse_table_name(self, table_name: str) -> tuple[Optional[str], str]:
        """
        Parse a table name that might include a schema prefix.
        Returns (schema_name, table_name)
        """
        if "." in table_name:
            parts = table_name.split(".", 1)
            return parts[0], parts[1]
        return None, table_name

    def ensure_table_exists(self, table: str, schema: Schema):
        engine = self.get_engine()
        db_schema, table_name = self._parse_table_name(table)

        # Check if table exists in the specific schema
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names(schema=db_schema)

        if table_name in existing_tables:
            return
        self.create_table(schema, table)

    def create_table(self, schema: Schema, table: str):
        db_schema, table_name = self._parse_table_name(table)

        table_columns = []
        pk_cols = []
        for col in schema.cols:
            col_name = col.to or col.original
            col_type = getattr(db, col.dtype or "String")
            table_columns.append(Column(col_name, col_type, primary_key=col.is_id))
            if col.is_id:
                pk_cols.append(col_name)
        constraints = []
        if pk_cols:
            constraints.append(
                PrimaryKeyConstraint(
                    *pk_cols, name=f"{table_name}_pk_{'_'.join(pk_cols)}"
                )
            )
        _, metadata = self.get_table(
            table, False, *table_columns, *constraints, extend_existing=True
        )
        metadata.create_all(self.get_engine())

    def get_table(self, table_name, autoload, *args, **kwargs):
        db_schema, actual_table_name = self._parse_table_name(table_name)

        metadata = MetaData()
        if autoload:
            kwargs.setdefault("autoload_with", self.get_engine())

        if db_schema:
            kwargs["schema"] = db_schema

        return Table(actual_table_name, metadata, *args, **kwargs), metadata
