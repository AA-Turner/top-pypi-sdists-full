from __future__ import annotations

from typing import Any

from nsj_rest_lib2.compiler.edl_model.primitives import PrimitiveTypes, PropertyType


class MigrationCompilerUtil:
    """
    Funções utilitárias para montagem de trechos SQL usados nas migrações.
    """

    SQL_TYPE_MAP = {
        PrimitiveTypes.STRING: "varchar(250)",
        PrimitiveTypes.TEXT: "varchar",
        PrimitiveTypes.NUMBER: "numeric(20,8)",
        PrimitiveTypes.INTEGER: "integer",
        PrimitiveTypes.BOOLEAN: "boolean",
        PrimitiveTypes.UUID: "uuid",
        PrimitiveTypes.CURRENCY: "numeric(20,4)",
        PrimitiveTypes.QUANTITY: "numeric(20,4)",
        PrimitiveTypes.CPF: "varchar(20)",
        PrimitiveTypes.CNPJ: "varchar(20)",
        PrimitiveTypes.CPF_CNPJ: "varchar(20)",
        PrimitiveTypes.EMAIL: "varchar(100)",
        PrimitiveTypes.DATE: "date",
        PrimitiveTypes.DATETIME: "timestamp with time zone",
        PrimitiveTypes.DURATION: "interval",
    }

    @staticmethod
    def resolve_sql_type(datatype: PropertyType, max_length: int | None) -> str:
        if not isinstance(datatype, PrimitiveTypes):
            raise ValueError(f"Tipo de propriedade não suportado para SQL: {datatype}")

        base_type = MigrationCompilerUtil.SQL_TYPE_MAP.get(datatype)
        if not base_type:
            raise ValueError(f"Tipo de propriedade não mapeado para SQL: {datatype}")

        if datatype in (PrimitiveTypes.STRING, PrimitiveTypes.TEXT) and max_length:
            return f"varchar({max_length})"

        return base_type

    @staticmethod
    def is_numeric(datatype: PropertyType) -> bool:
        if not isinstance(datatype, PrimitiveTypes):
            return False
        return datatype in (
            PrimitiveTypes.NUMBER,
            PrimitiveTypes.INTEGER,
            PrimitiveTypes.CURRENCY,
            PrimitiveTypes.QUANTITY,
        )

    @staticmethod
    def quote_literal(value: Any) -> str:
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return str(value)
        escaped = str(value).replace("'", "''")
        return f"'{escaped}'"

    @staticmethod
    def comment_on_column(table_name: str, column_name: str, description: str) -> str:
        escaped = description.replace("'", "''")
        return (
            f"COMMENT ON COLUMN {table_name}.{column_name} IS '{escaped}'"
        )

    @staticmethod
    def drop_constraint_if_exists(table_name: str, constraint_name: str) -> str:
        return f"ALTER TABLE {table_name} DROP CONSTRAINT IF EXISTS {constraint_name}"

    @staticmethod
    def check_constraint_name(table_name: str, column_name: str, suffix: str) -> str:
        safe_table = table_name.replace(".", "_")
        return f"{safe_table}_{column_name}_{suffix}"

    @staticmethod
    def add_enum_check_constraint(
        table_name: str, column_name: str, values: list[Any]
    ) -> list[str]:
        statements: list[str] = []
        constraint_name = MigrationCompilerUtil.check_constraint_name(
            table_name, column_name, "enum_chk"
        )
        statements.append(
            MigrationCompilerUtil.drop_constraint_if_exists(
                table_name, constraint_name
            )
        )
        if values:
            formatted_values = ", ".join(
                MigrationCompilerUtil.quote_literal(v) for v in values
            )
            statements.append(
                f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} "
                f"CHECK ({column_name} IN ({formatted_values}))"
            )
        return statements

    @staticmethod
    def add_max_check_constraint(
        table_name: str, column_name: str, maximum: int | float
    ) -> list[str]:
        statements: list[str] = []
        constraint_name = MigrationCompilerUtil.check_constraint_name(
            table_name, column_name, "max_chk"
        )
        statements.append(
            MigrationCompilerUtil.drop_constraint_if_exists(
                table_name, constraint_name
            )
        )
        statements.append(
            f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} "
            f"CHECK ({column_name} <= {maximum})"
        )
        return statements

    @staticmethod
    def add_primary_key(
        table_name: str, column_names: list[str], constraint_name: str | None = None
    ) -> str:
        constraint = constraint_name or f"{table_name}_pkey"
        columns = ", ".join(column_names)
        return (
            f"ALTER TABLE {table_name} "
            f"ADD CONSTRAINT {constraint} PRIMARY KEY ({columns})"
        )

    @staticmethod
    def drop_primary_key(table_name: str, constraint_name: str | None = None) -> str:
        constraint = constraint_name or f"{table_name}_pkey"
        return f"ALTER TABLE {table_name} DROP CONSTRAINT IF EXISTS {constraint}"

    @staticmethod
    def indent_sql(sql: str, spaces: int) -> list[str]:
        prefix = " " * spaces
        return [prefix + line if line else prefix for line in sql.split("\n")]
