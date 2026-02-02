from __future__ import annotations

from typing import Any

from nsj_rest_lib2.compiler.migration_compiler_util import MigrationCompilerUtil


class MigrationCompilerAlterTable:
    def compile(
        self,
        table_name: str,
        column_specs: list[dict[str, Any]],
        pk_columns: list[str],
        rename_operations: list[tuple[str, str]] | None = None,
        fk_specs: list[dict[str, str]] | None = None,
    ) -> list[str]:
        lines: list[str] = []
        rename_operations = rename_operations or []
        fk_specs = fk_specs or []

        for old_col, new_col in rename_operations:
            lines.append(
                f"        IF exists_column('{table_name}', '{old_col}') AND NOT exists_column('{table_name}', '{new_col}') THEN"
            )
            lines.append(
                f"            ALTER TABLE {table_name} RENAME COLUMN {old_col} TO {new_col};"
            )
            lines.append("        END IF;")

        for spec in column_specs:
            column_name = spec["column_name"]
            default_literal = (
                MigrationCompilerUtil.quote_literal(spec["default"])
                if spec["default"] is not None
                else None
            )
            default_literal_text = (
                f"{default_literal}::text" if default_literal is not None else None
            )
            not_null_literal = "TRUE" if spec["not_null"] else "FALSE"

            lines.append(f"        -- coluna {column_name}")
            lines.append(
                f"        IF NOT exists_column('{table_name}', '{column_name}') THEN"
            )
            lines.append(
                MigrationCompilerUtil.indent_sql(
                    self._build_add_column_sql(table_name, spec), 12
                )[0]
            )

            self._append_enum_and_max_checks(lines, table_name, column_name, spec, 12)

            if spec["description"]:
                lines.append(
                    "            "
                    + MigrationCompilerUtil.comment_on_column(
                        table_name, column_name, spec["description"]
                    )
                    + ";"
                )

            lines.append("        ELSE")

            # Alteração de tipo
            lines.append(
                f"            IF NOT validate_column_properties('{table_name}', '{column_name}', '{spec['sql_type']}') THEN"
            )
            lines.append(
                f"                ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE {spec['sql_type']};"
            )
            lines.append("            END IF;")

            # Alteração de nulidade
            lines.append(f"            IF {not_null_literal} THEN")
            lines.append(
                f"                IF NOT column_is_not_null('{table_name}', '{column_name}') THEN"
            )
            lines.append(
                f"                    ALTER TABLE {table_name} ALTER COLUMN {column_name} SET NOT NULL;"
            )
            lines.append("                END IF;")
            lines.append("            ELSE")
            lines.append(
                f"                IF column_is_not_null('{table_name}', '{column_name}') THEN"
            )
            lines.append(
                f"                    ALTER TABLE {table_name} ALTER COLUMN {column_name} DROP NOT NULL;"
            )
            lines.append("                END IF;")
            lines.append("            END IF;")

            # Alteração de default
            if default_literal is None:
                lines.append(
                    f"            IF column_default_expr('{table_name}', '{column_name}') IS NOT NULL THEN"
                )
                lines.append(
                    f"                ALTER TABLE {table_name} ALTER COLUMN {column_name} DROP DEFAULT;"
                )
                lines.append("            END IF;")
            else:
                lines.append(
                    f"            IF NOT column_default_equals('{table_name}', '{column_name}', {default_literal_text}) THEN"
                )
                lines.append(
                    f"                ALTER TABLE {table_name} ALTER COLUMN {column_name} SET DEFAULT {default_literal};"
                )
                lines.append("            END IF;")

            # Checks e comentários
            self._append_enum_and_max_checks(lines, table_name, column_name, spec, 12)

            if spec["description"]:
                lines.append(
                    "            "
                    + MigrationCompilerUtil.comment_on_column(
                        table_name, column_name, spec["description"]
                    )
                    + ";"
                )

            lines.append("        END IF;")

        if pk_columns:
            lines.append(f"        IF NOT table_has_primary_key('{table_name}') THEN")
            lines.append(
                f"            {MigrationCompilerUtil.add_primary_key(table_name, pk_columns)};"
            )
            lines.append("        END IF;")

        for fk in fk_specs:
            lines.append(
                f"        IF NOT fk_constraint_matches('{table_name}', '{fk['column_name']}', '{fk['ref_table']}', '{fk['ref_column']}') THEN"
            )
            fk_constraint_name = MigrationCompilerUtil.check_constraint_name(
                table_name, fk["column_name"], "fk"
            )
            lines.append(
                f"            {MigrationCompilerUtil.drop_constraint_if_exists(table_name, fk_constraint_name)};"
            )
            lines.append(
                f"            ALTER TABLE {table_name} ADD CONSTRAINT {fk_constraint_name} FOREIGN KEY ({fk['column_name']}) REFERENCES {fk['ref_table']}({fk['ref_column']});"
            )
            lines.append("        END IF;")

        return lines

    def _append_enum_and_max_checks(
        self,
        lines: list[str],
        table_name: str,
        column_name: str,
        spec: dict[str, Any],
        indent: int,
    ) -> None:
        if spec["enum_values"]:
            formatted_values = ", ".join(
                MigrationCompilerUtil.quote_literal(v) for v in spec["enum_values"]
            )
            lines.append(
                f"{' ' * indent}IF NOT enum_constraint_matches('{table_name}', '{column_name}', ARRAY[{formatted_values}]) THEN"
            )
            lines.extend(
                MigrationCompilerUtil.indent_sql(
                    ";\n".join(
                        MigrationCompilerUtil.add_enum_check_constraint(
                            table_name, column_name, spec["enum_values"]
                        )
                    )
                    + ";",
                    indent + 4,
                )
            )
            lines.append(f"{' ' * indent}END IF;")

        if spec["maximum"] is not None and spec["is_numeric"]:
            lines.append(
                f"{' ' * indent}IF NOT max_constraint_matches('{table_name}', '{column_name}', {spec['maximum']}) THEN"
            )
            lines.extend(
                MigrationCompilerUtil.indent_sql(
                    ";\n".join(
                        MigrationCompilerUtil.add_max_check_constraint(
                            table_name, column_name, spec["maximum"]
                        )
                    )
                    + ";",
                    indent + 4,
                )
            )
            lines.append(f"{' ' * indent}END IF;")

    def _build_add_column_sql(self, table_name: str, spec: dict[str, Any]) -> str:
        clause = f"ALTER TABLE {table_name} ADD COLUMN {spec['column_name']} {spec['sql_type']}"
        if spec["not_null"]:
            clause += " NOT NULL"
        if spec["default"] is not None:
            clause += f" DEFAULT {MigrationCompilerUtil.quote_literal(spec['default'])}"
        clause += ";"
        return clause
