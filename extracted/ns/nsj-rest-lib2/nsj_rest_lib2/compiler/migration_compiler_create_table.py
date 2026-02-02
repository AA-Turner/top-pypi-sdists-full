from __future__ import annotations

from typing import Any

from nsj_rest_lib2.compiler.migration_compiler_util import MigrationCompilerUtil


class MigrationCompilerCreateTable:
    def compile(
        self,
        table_name: str,
        column_specs: list[dict[str, Any]],
        pk_columns: list[str],
        fk_specs: list[dict[str, str]],
    ) -> str:
        column_definitions: list[str] = []
        for spec in column_specs:
            col_def = f"{spec['column_name']} {spec['sql_type']}"
            if spec["not_null"]:
                col_def += " NOT NULL"
            if spec["default"] is not None:
                col_def += f" DEFAULT {MigrationCompilerUtil.quote_literal(spec['default'])}"
            column_definitions.append(col_def)

        if pk_columns:
            pk_constraint = (
                f"CONSTRAINT {table_name}_pkey PRIMARY KEY ({', '.join(pk_columns)})"
            )
            column_definitions.append(pk_constraint)

        for fk in fk_specs:
            fk_name = MigrationCompilerUtil.check_constraint_name(
                table_name, fk["column_name"], "fk"
            )
            column_definitions.append(
                f"CONSTRAINT {fk_name} FOREIGN KEY ({fk['column_name']}) REFERENCES {fk['ref_table']}({fk['ref_column']})"
            )

        columns_block = ",\n    ".join(column_definitions)
        create_lines = [
            f"CREATE TABLE {table_name} (",
            f"    {columns_block}",
            ");",
        ]

        for spec in column_specs:
            if spec["description"]:
                create_lines.append(
                    MigrationCompilerUtil.comment_on_column(
                        table_name, spec["column_name"], spec["description"]
                    )
                    + ";"
                )

            if spec["enum_values"]:
                create_lines.extend(
                    [
                        stmt + ";"
                        for stmt in MigrationCompilerUtil.add_enum_check_constraint(
                            table_name, spec["column_name"], spec["enum_values"]
                        )
                    ]
                )

            if spec["maximum"] is not None and spec["is_numeric"]:
                create_lines.extend(
                    [
                        stmt + ";"
                        for stmt in MigrationCompilerUtil.add_max_check_constraint(
                            table_name, spec["column_name"], spec["maximum"]
                        )
                    ]
                )

        return "\n".join(create_lines)
