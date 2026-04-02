import io

import pandas as pd
from sqlalchemy import func, inspect, text
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.engine import Engine

from seshat.source.exceptions import PostgresConstraintError

COPY_QUERY = (
    "COPY {table_name} FROM STDIN WITH (FORMAT csv, HEADER TRUE,  DELIMITER '\t');"
)


class PostgresUtils:
    @staticmethod
    def parse_table_name(table_name: str) -> tuple[str, str]:
        """
        Parse a table name that might include a schema prefix.
        Returns (schema_name, table_name)
        """
        if "." in table_name:
            parts = table_name.split(".", 1)
            # Remove quotes if present
            schema = parts[0].strip('"')
            table = parts[1].strip('"')
            return schema, table
        return None, table_name.strip('"')

    @staticmethod
    def copy(engine: Engine, table_name: str, df: pd.DataFrame):
        """
        Copy data to a PostgreSQL table.
        table_name can be schema-qualified (e.g., "schema.table" or '"schema"."table"')
        """
        # If table_name is already properly formatted with quotes, use it as-is
        # Otherwise, parse and format it
        if '"."' in table_name:
            # Already properly formatted like '"schema"."table"'
            formatted_table = table_name
        else:
            schema_name, actual_table = PostgresUtils.parse_table_name(table_name)
            if schema_name:
                formatted_table = f'"{schema_name}"."{actual_table}"'
            else:
                formatted_table = f'"{actual_table}"'

        csv_content = io.StringIO()
        df.to_csv(csv_content, sep="\t", header=True, index=False)
        csv_content.seek(0)
        conn = engine.raw_connection()
        cur = conn.cursor()
        cur.copy_expert(COPY_QUERY.format(table_name=formatted_table), csv_content)
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_constraint_name(table_name, id_columns):
        """
        Generate a unique constraint name based on table and id columns.
        Uses only the actual table name (without schema) for naming.
        """
        # Remove schema prefix if present
        _, actual_table = PostgresUtils.parse_table_name(table_name)
        cols_part = "_".join(sorted(id_columns))
        return f"uq_{actual_table}_{cols_part}"

    @staticmethod
    def constraint_exists(engine, table, constraint_name):
        """
        Check if a unique constraint exists on a table.
        Properly handles schema-qualified tables.
        """
        insp = inspect(engine)
        # Get schema from table object if it has one
        schema = getattr(table, "schema", None)

        # Get unique constraints for the table in the specific schema
        for cons in insp.get_unique_constraints(table.name, schema=schema):
            if cons["name"] == constraint_name:
                return True
        return False

    @staticmethod
    def ensure_unique_constraint(engine, table, schema):
        """
        Ensure a unique constraint exists for the given table and schema.
        Properly handles schema-qualified tables.
        """
        id_cols = [col.to for col in schema.get_id(return_first=False)]
        constraint_name = PostgresUtils.get_constraint_name(table.name, id_cols)

        if PostgresUtils.constraint_exists(engine, table, constraint_name):
            return True

        try:
            # Build fully qualified table name if schema is present
            if hasattr(table, "schema") and table.schema:
                qualified_table_name = f'"{table.schema}"."{table.name}"'
            else:
                qualified_table_name = f'"{table.name}"'

            sql = 'ALTER TABLE {table_name} ADD CONSTRAINT "{constraint_name}" UNIQUE ({cols});'.format(
                table_name=qualified_table_name,
                constraint_name=constraint_name,
                cols=", ".join(['"{}"'.format(col) for col in id_cols]),
            )
            with engine.connect() as conn:
                trans = conn.begin()
                conn.execute(text(sql))
                trans.commit()
            return True
        except Exception as e:
            error_msg = str(e).lower()
            if "duplicate" in error_msg or "unique" in error_msg:
                raise PostgresConstraintError(
                    f"Cannot create unique constraint '{constraint_name}' on table '{table.name}': "
                    f"duplicate data exists for columns {id_cols}."
                )
            elif "permission" in error_msg or "not allowed" in error_msg:
                raise PostgresConstraintError(
                    f"Insufficient privileges to create unique constraint '{constraint_name}' on table '{table.name}'."
                )
            else:
                raise

    @staticmethod
    def generate_upsert_stmt(table, values, config):
        """
        Perform an upsert (insert or update) on a Postgres table with custom update functions.
        The table object already contains schema information if applicable.
        """
        id_cols = config.schema.get_id(return_first=False)
        update_cols = [col for col in config.schema.cols if not col.is_id]
        col_to_func_map = {
            col.original: col.update_func or "replace"
            for col in config.schema.cols
            if not col.is_id
        }

        upsert_rows = []
        for row in values:
            upsert_row = {col.to: row[col.original] for col in config.schema.cols}
            upsert_rows.append(upsert_row)

        insert_stmt = pg.insert(table)
        update_dict = {}

        for col in update_cols:
            func_name = col_to_func_map.get(col.original)
            if func_name == "sum":
                update_dict[col.to] = func.coalesce(table.c[col.to], 0) + func.coalesce(
                    insert_stmt.excluded[col.to], 0
                )
            elif func_name == "mean":
                update_dict[col.to] = (
                    func.coalesce(table.c[col.to], 0)
                    + func.coalesce(insert_stmt.excluded[col.to], 0)
                ) / 2
            else:
                update_dict[col.to] = insert_stmt.excluded[col.to]

        conflict_cols = [col.to for col in id_cols]
        stmt = insert_stmt.values(upsert_rows)
        return stmt.on_conflict_do_update(
            index_elements=conflict_cols, set_=update_dict
        )
