from __future__ import annotations

import re
from abc import ABC
from typing import Any, List, Optional, Protocol, Tuple

from loguru import logger

from gable.openapi import SourceType


class DbapiReader(ABC):
    """
    Reads the information schema from a database using the DBAPI.

    This class is based on the Recap DBAPIReader, which can be found at:
    https://github.com/recap-build/recap/blob/main/recap/readers/dbapi.py

    The purpose of this class is to provide a simplified version of the Recap
    DBAPIReader, removing the dependency on the Recap library. It allows for reading
    the information schema from a database using any DBAPI-compliant driver.

    Based on discussions in Recap, I chose to forgo the use of sqlalchemy, as it is a
    large dependency that is not necessary for the purpose of this library. Instead, we
    can use the DBAPI directly.

    Usage:
    Call the `get_information_schema` method to retrieve the information schema of the
    database.

    Example:
    ```python
    reader = DbapiReader(connection=database_connection_object)
    column_info = reader.get_information_schema(schema="public")
    ```

    Note: This class requires a DBAPI-compliant driver to be installed and imported
    separately.

    Attributes:
        connection (DBAPIConnection): The DBAPI connection object used to interact with
            the database.

    Methods:
        get_information_schema(): Retrieves the information schema of the connected
            database.

    """

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def _fetch_information_schema_postgres(
        self, cursor: Cursor, schema: str, tables: Optional[list[str]] = None
    ) -> None:
        if tables:
            logger.trace(
                re.sub(
                    r"\s+",
                    " ",
                    f"""Querying information schema:
                        SELECT
                            information_schema.columns.*,
                            pg_attribute.attndims,
                            enums.enum_values
                        FROM information_schema.columns
                        JOIN pg_catalog.pg_namespace
                            ON pg_catalog.pg_namespace.nspname = information_schema.columns.table_schema
                        JOIN pg_catalog.pg_class
                            ON pg_catalog.pg_class.relname = information_schema.columns.table_name AND pg_catalog.pg_class.relnamespace = pg_catalog.pg_namespace.oid
                        JOIN pg_catalog.pg_attribute
                            ON pg_catalog.pg_attribute.attrelid = pg_catalog.pg_class.oid AND pg_catalog.pg_attribute.attname = information_schema.columns.column_name
                        -- Join to get the enum values
                        LEFT JOIN pg_catalog.pg_type
                            ON pg_catalog.pg_type.oid = pg_catalog.pg_attribute.atttypid
                            AND pg_catalog.pg_type.typtype = 'e' -- Ensuring it's an enum type
                        LEFT JOIN (
                            SELECT
                                enumtypid,
                                array_agg(enumlabel) AS enum_values
                            FROM pg_catalog.pg_enum
                            GROUP BY enumtypid
                        ) enums ON enums.enumtypid = pg_catalog.pg_type.oid
                        WHERE table_schema = '{schema}'
                            AND table_name IN ('{','.join(tables)}')
                            ORDER BY ordinal_position ASC""",
                )
            )
            cursor.execute(
                f"""
                    SELECT
                        information_schema.columns.*,
                        pg_attribute.attndims,
                        enums.enum_values
                    FROM information_schema.columns
                    JOIN pg_catalog.pg_namespace
                        ON pg_catalog.pg_namespace.nspname = information_schema.columns.table_schema
                    JOIN pg_catalog.pg_class
                        ON pg_catalog.pg_class.relname = information_schema.columns.table_name AND pg_catalog.pg_class.relnamespace = pg_catalog.pg_namespace.oid
                    JOIN pg_catalog.pg_attribute
                        ON pg_catalog.pg_attribute.attrelid = pg_catalog.pg_class.oid AND pg_catalog.pg_attribute.attname = information_schema.columns.column_name
                    -- Join to get the enum values
                    LEFT JOIN pg_catalog.pg_type
                        ON pg_catalog.pg_type.oid = pg_catalog.pg_attribute.atttypid
                        AND pg_catalog.pg_type.typtype = 'e' -- Ensuring it's an enum type
                    LEFT JOIN (
                        SELECT
                            enumtypid,
                            array_agg(enumlabel) AS enum_values
                        FROM pg_catalog.pg_enum
                        GROUP BY enumtypid
                    ) enums ON enums.enumtypid = pg_catalog.pg_type.oid
                    WHERE table_schema = {self.param_style}
                        AND table_name IN {self.param_style}
                    ORDER BY ordinal_position ASC
                """,
                [schema, tuple(tables)],  # type: ignore
            )
        else:
            logger.trace(
                re.sub(
                    r"\s+",
                    " ",
                    f"""Querying information schema:
                    SELECT
                        information_schema.columns.*,
                        pg_attribute.attndims,
                        enums.enum_values
                    FROM information_schema.columns
                    JOIN pg_catalog.pg_namespace
                        ON pg_catalog.pg_namespace.nspname = information_schema.columns.table_schema
                    JOIN pg_catalog.pg_class
                        ON pg_catalog.pg_class.relname = information_schema.columns.table_name AND pg_catalog.pg_class.relnamespace = pg_catalog.pg_namespace.oid
                    JOIN pg_catalog.pg_attribute
                        ON pg_catalog.pg_attribute.attrelid = pg_catalog.pg_class.oid AND pg_catalog.pg_attribute.attname = information_schema.columns.column_name
                    -- Join to get the enum values
                    LEFT JOIN pg_catalog.pg_type
                        ON pg_catalog.pg_type.oid = pg_catalog.pg_attribute.atttypid
                        AND pg_catalog.pg_type.typtype = 'e' -- Ensuring it's an enum type
                    LEFT JOIN (
                        SELECT
                            enumtypid,
                            array_agg(enumlabel) AS enum_values
                        FROM pg_catalog.pg_enum
                        GROUP BY enumtypid
                    ) enums ON enums.enumtypid = pg_catalog.pg_type.oid
                    WHERE table_schema = '{schema}'
                        ORDER BY ordinal_position ASC""",
                )
            )
            cursor.execute(
                f"""
                    SELECT
                        information_schema.columns.*,
                        pg_attribute.attndims,
                        enums.enum_values
                    FROM information_schema.columns
                    JOIN pg_catalog.pg_namespace
                        ON pg_catalog.pg_namespace.nspname = information_schema.columns.table_schema
                    JOIN pg_catalog.pg_class
                        ON pg_catalog.pg_class.relname = information_schema.columns.table_name AND pg_catalog.pg_class.relnamespace = pg_catalog.pg_namespace.oid
                    JOIN pg_catalog.pg_attribute
                        ON pg_catalog.pg_attribute.attrelid = pg_catalog.pg_class.oid AND pg_catalog.pg_attribute.attname = information_schema.columns.column_name
                    -- Join to get the enum values
                    LEFT JOIN pg_catalog.pg_type
                        ON pg_catalog.pg_type.oid = pg_catalog.pg_attribute.atttypid
                        AND pg_catalog.pg_type.typtype = 'e' -- Ensuring it's an enum type
                    LEFT JOIN (
                        SELECT
                            enumtypid,
                            array_agg(enumlabel) AS enum_values
                        FROM pg_catalog.pg_enum
                        GROUP BY enumtypid
                    ) enums ON enums.enumtypid = pg_catalog.pg_type.oid
                    WHERE table_schema = {self.param_style}
                    ORDER BY ordinal_position ASC
                """,
                [schema],  # type: ignore
            )

    def _fetch_information_schema_mysql(
        self, cursor: Cursor, schema: str, tables: Optional[list[str]] = None
    ) -> None:
        if tables:
            logger.trace(
                re.sub(
                    r"\s+",
                    " ",
                    f"Querying information schema: \
                    SELECT * FROM information_schema.columns WHERE table_schema = '{schema}' \
                        AND table_name IN ('{','.join(tables)}') \
                        ORDER BY ordinal_position ASC",
                )
            )
            cursor.execute(
                f"""
                    SELECT
                        *
                    FROM information_schema.columns
                    WHERE table_schema = {self.param_style}
                        AND table_name IN {self.param_style}
                    ORDER BY ordinal_position ASC
                """,
                [schema, tuple(tables)],  # type: ignore
            )
        else:
            logger.trace(
                re.sub(
                    r"\s+",
                    " ",
                    f"Querying information schema: \
                    SELECT * FROM information_schema.columns WHERE table_schema = '{schema}' \
                        ORDER BY ordinal_position ASC",
                )
            )
            cursor.execute(
                f"""
                    SELECT
                        *
                    FROM information_schema.columns
                    WHERE table_schema = {self.param_style}
                    ORDER BY ordinal_position ASC
                """,
                [schema],  # type: ignore
            )

    def _fetch_information_schema_mssql(
        self, cursor: Cursor, schema: str, tables: Optional[list[str]] = None
    ) -> None:
        if tables:
            logger.trace(
                re.sub(
                    r"\s+",
                    " ",
                    f"Querying information schema: \
                        SELECT \
                            isc.* \
                        FROM information_schema.columns AS isc \
                        JOIN (select name from sysobjects where OBJECTPROPERTY(id,N'IsTable')=1 and OBJECTPROPERTY(id,N'IsMSShipped')=0) as user_tables \
                        ON isc.table_name = user_tables.name \
                        WHERE table_schema = '{schema}' \
                            AND table_name IN ('{','.join(tables)}') \
                        ORDER BY ordinal_position ASC",
                )
            )
            cursor.execute(
                f"""
                    SELECT
                        isc.*
                    FROM information_schema.columns AS isc
                    JOIN (select name from sysobjects where OBJECTPROPERTY(id,N'IsTable')=1 and OBJECTPROPERTY(id,N'IsMSShipped')=0) as user_tables
                    ON isc.table_name = user_tables.name
                    WHERE isc.table_schema = {self.param_style}
                        AND isc.table_name IN {self.param_style}
                    ORDER BY ordinal_position ASC
                """,
                [schema, tuple(tables)],  # type: ignore
            )
        else:
            logger.trace(
                re.sub(
                    r"\s+",
                    " ",
                    f"Querying information schema: \
                        SELECT \
                            isc.* \
                        FROM information_schema.columns AS isc \
                        JOIN (select name from sysobjects where OBJECTPROPERTY(id,N'IsTable')=1 and OBJECTPROPERTY(id,N'IsMSShipped')=0) as user_tables \
                        ON isc.table_name = user_tables.name \
                        WHERE isc.table_schema = '{schema}' \
                        ORDER BY ordinal_position ASC",
                )
            )
            cursor.execute(
                f"""
                    SELECT
                        isc.*
                    FROM information_schema.columns AS isc
                    JOIN (select name from sysobjects where OBJECTPROPERTY(id,N'IsTable')=1 and OBJECTPROPERTY(id,N'IsMSShipped')=0) as user_tables
                    ON isc.table_name = user_tables.name
                    WHERE isc.table_schema = {self.param_style}
                    ORDER BY ordinal_position ASC
                """,
                [schema],  # type: ignore
            )

    def get_information_schema(
        self, source_type: SourceType, schema: str, tables: Optional[list[str]] = None
    ) -> list[dict[str, Any]]:
        if tables:
            logger.debug(
                f"Getting information schema for tables in schema {schema}: {','.join(tables)}"
            )
        else:
            logger.debug(
                f"Getting information schema for all tables in schema {schema}"
            )
        # Query the information schema to get the current database, schema, and catalog
        cursor = self.connection.cursor()

        if source_type == SourceType.postgres:
            self._fetch_information_schema_postgres(cursor, schema, tables)
        elif source_type == SourceType.mysql:
            self._fetch_information_schema_mysql(cursor, schema, tables)
        elif source_type == SourceType.mssql:
            self._fetch_information_schema_mssql(cursor, schema, tables)
        else:
            raise TypeError(f"Unsupported source_type: {source_type}")

        # Create a dictionary for each row of the information schema
        names = [
            name[0].decode().upper() if isinstance(name[0], bytes) else name[0].upper()
            for name in cursor.description
        ]
        table_name_index = names.index("TABLE_NAME")
        fields = []
        rows = cursor.fetchall()
        logger.trace(f"Found {len(rows)} rows in information schema")
        distinct_tables = set()
        for row in rows:
            distinct_tables.add(row[table_name_index])
            column_props = dict(
                zip(
                    names,
                    tuple(
                        # MySQL returns everything as byte arrays, so we need to decode
                        bs.decode("utf-8") if isinstance(bs, bytes) else bs
                        for bs in row
                    ),
                )
            )
            fields.append(column_props)
        # Return the results
        logger.debug(
            f"{len(distinct_tables)} tables found: {','.join(list(distinct_tables))}"
        )
        return fields

    @property
    def param_style(self) -> str:
        return "%s"


class Connection(Protocol):
    def close(self) -> None: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...

    def cursor(self) -> Cursor: ...


class Cursor(Protocol):
    def execute(self, query: str, parameters: Tuple = ()) -> None: ...

    def executemany(self, query: str, parameter_list: List[Tuple]) -> None: ...

    def fetchone(self) -> Tuple: ...

    def fetchall(self) -> List[Tuple]: ...

    def fetchmany(self, size: int) -> List[Tuple]: ...

    @property
    def description(self) -> List[Tuple]: ...
