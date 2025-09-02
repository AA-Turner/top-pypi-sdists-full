import inspect
from typing import override

import fastmcp
import pandas as pd
import sqlalchemy as sa

from bir_mcp.config import SqlContext
from bir_mcp.core import BaseMcp, build_readonly_tools
from bir_mcp.utils import filter_dict_by_keys, split_schema_table


class SQL(BaseMcp):
    def __init__(
        self,
        sql_context: SqlContext,
        sample_rows_in_table_info: int = 5,
        timezone: str = "UTC",
    ):
        super().__init__(timezone=timezone)
        self.sql_context = sql_context
        self.engine = self.sql_context.connection.get_engine()
        self.inspector = sa.inspect(self.engine)
        self.sample_rows_in_table_info = sample_rows_in_table_info

    @override
    def get_tag(self):
        name = self.sql_context.name or self.sql_context.connection_name
        return f"sql_{name}"

    @override
    def get_mcp_server_without_components(self):
        server = fastmcp.FastMCP(
            name="MCP server with SQL tools",
            instructions=inspect.cleandoc("""
                Contains tools to work with SQL databases.
            """),
        )
        return server

    @override
    def get_mcp_tools(self, max_output_length: int | None = None, tags: set[str] | None = None):
        read_tools = [
            self.get_database_info,
            self.get_available_table_names,
            self.get_table_info,
            self.execute_query,
        ]
        tools = build_readonly_tools(read_tools, max_output_length=max_output_length, tags=tags)
        return tools

    def read_sql_to_dict(self, sql) -> dict:
        df = pd.read_sql(sql, self.engine)
        df_dict = df.to_dict(orient="split", index=False)
        # The CSV option if more reliable in terms of being able to serialize to string.
        # df = pd.read_sql(sql, self.engine)
        # buffer = io.StringIO()
        # df.to_csv(buffer, index=False)
        # csv_table = buffer.getvalue()
        return df_dict

    def get_database_info(self) -> dict:
        """
        Get info about the database, such as its dialect and version,
        as well as the connection name for reference in other tools.
        """
        dialect = self.inspector.dialect
        info = {
            "dialect": dialect.name,
            "connection_name": self.sql_context.connection_name,
        }
        if dialect.server_version_info:
            info["server_version"] = ".".join(map(str, dialect.server_version_info))

        return info

    def get_available_table_names(self) -> dict:
        """Get available schema-qualified table names."""
        # The available tables are those that are explicitly specified in the config.
        # It is done this way for predictability and efficiency to avoid fetching all
        # table names from the database, which can be slow for large databases.
        # It is not guaranteed that SQL connection user has permissions to select the
        # returned tables, but to check it, either a fragile probe SQL is needed or
        # a table reflection has to be performed, which can add up to the latency.
        schema_tables = []
        for schema_table in self.sql_context.schema_tables:
            schema, table = split_schema_table(schema_table)
            if self.inspector.has_table(schema=schema, table_name=table):
                schema_tables.append(schema_table)

        tables = {"schema_tables": sorted(schema_tables)}
        return tables

    def get_table_info(self, schema_table: str, include_sample_rows: bool = False) -> dict:
        """
        Get SQL table info, such as the create table SQL statement, column comments,
        primary and foreign keys, indexes, and sample rows.
        """
        schema_tables = self.get_available_table_names()["schema_tables"]
        if schema_table not in schema_tables:
            raise ValueError(f"Table {schema_table} is not available.")

        schema, table = split_schema_table(schema_table)

        sa_table = sa.Table(table, sa.MetaData(), schema=schema, autoload_with=self.engine)
        create_table = sa.schema.CreateTable(sa_table).compile(self.engine)
        create_table = "\n".join(line.strip() for line in str(create_table).strip().splitlines())

        column_comments = {c.name: c.comment for c in sa_table.columns if c.comment}

        primary_key = self.inspector.get_pk_constraint(table, schema)
        primary_key_columns = primary_key.get("constrained_columns")

        foreign_keys = self.inspector.get_foreign_keys(table, schema)
        foreign_keys = [
            filter_dict_by_keys(
                fk, ["constrained_columns", "referred_schema", "referred_table", "referred_columns"]
            )
            for fk in foreign_keys
        ]

        indexes = self.inspector.get_indexes(table, schema)
        index_columns = [i.get("column_names") for i in indexes]

        table_info = {
            "create_table_statement": create_table,
            "column_comments": column_comments,
            "primary_key_columns": primary_key_columns,
            "foreign_keys": foreign_keys,
            "index_columns": index_columns,
        }
        if include_sample_rows:
            query = sa.select(sa_table).limit(self.sample_rows_in_table_info)
            sample_rows = self.read_sql_to_dict(query)
            table_info["sample_rows"] = sample_rows

        return table_info

    def execute_query(self, query: str) -> dict:
        """
        Execute an SQL query and return the result. Whenever possible, follow the following optimization principles:
        - Select only the columns that are needed.
        - Use aggregations to reduce the amount of data returned.
        - When joining, filtering and sorting, prefer indexed columns.
        - Avoid applying functions to indexed columns in the filtering clauses.
        """
        table = self.read_sql_to_dict(query)
        return table
