# canonmap/services/artifact_generator/schema/db_types/mariadb/generate_mariadb_loader_script.py
# Module for generating MariaDB table creation scripts from schemas

import logging
from pathlib import Path
from typing import Optional, Dict, List, Union
from canonmap.utils.logger import setup_logger

logger = setup_logger(__name__)


def generate_mariadb_loader_script(
    schema: Union[Dict, Dict[str, Dict]],
    table_name: Union[str, List[str]],
    output_file_path: Optional[str] = "create_mariadb_table.py",
    table_relationships: Optional[Dict[str, List[str]]] = None,
    is_combined: bool = False
) -> str:
    """
    Return a Python script that safely creates MariaDB table(s) based on schema. Optionally writes to file.
    
    Args:
        schema: Schema dictionary for a single table or multiple tables
        table_name: Name of the table or list of table names
        output_file_path: Optional path to write the script to
        table_relationships: Optional dict mapping table names to their related tables
        is_combined: Whether this is a combined script for multiple tables
    """

    def _generate_create_table_sql(table_schema: Dict, table: str) -> str:
        """Generate CREATE TABLE SQL for a single table."""
        column_defs = []
        for col, props in table_schema.items():
            col_def = f"`{col}` {props['data_type']}"
            column_defs.append(col_def)
        
        # Add foreign key constraints if relationships exist
        if table_relationships and table in table_relationships:
            for related_table in table_relationships[table]:
                # Look for potential foreign key columns
                for col in table_schema:
                    if col.endswith('_id') or col.endswith('_ref'):
                        ref_table = col[:-3]  # Remove _id or _ref
                        if ref_table == related_table:
                            column_defs.append(f"FOREIGN KEY (`{col}`) REFERENCES `{related_table}`(`id`)")
        
        return f"CREATE TABLE `{table}` (\n    " + ",\n    ".join(column_defs) + "\n);"

    if is_combined:
        # Multi-table mode: generate for all tables
        create_sqls = []
        for table in table_name:
            table_schema = schema[table]
            create_sqls.append(_generate_create_table_sql(table_schema, table))
        create_sql = "\n\n".join(create_sqls)
        script_code = f'''\
import mariadb

# --- User Configuration ---
DB_CONFIG = {{
    "host": "localhost",
    "port": 3306,
    "user": "your_username",
    "password": "your_password",
    "database": "your_database"
}}

# --- SQL ---
create_sqls = {repr(create_sqls)}
table_names = {repr(table_name)}

# --- Connect and Create Tables if Not Exist ---
conn = mariadb.connect(**DB_CONFIG)
cursor = conn.cursor()

for table, create_sql in zip(table_names, create_sqls):
    cursor.execute("SHOW TABLES LIKE %s", (table,))
    if cursor.fetchone():
        print(f"⚠️ Table '{{table}}' already exists. Skipping.")
    else:
        cursor.execute(create_sql)
        conn.commit()
        print(f"✅ Table '{{table}}' created successfully.")

cursor.close()
conn.close()
'''
    else:
        # Single-table mode: only generate for one table, use string literal
        create_sql = _generate_create_table_sql(schema, table_name)
        script_code = f'''\
import mariadb

# --- User Configuration ---
DB_CONFIG = {{
    "host": "localhost",
    "port": 3306,
    "user": "your_username",
    "password": "your_password",
    "database": "your_database"
}}

# --- SQL ---
create_sql = """{create_sql}"""

# --- Connect and Create Table if Not Exists ---
conn = mariadb.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute("SHOW TABLES LIKE %s", ("{table_name}",))
if cursor.fetchone():
    print(f"⚠️ Table '{table_name}' already exists. No action taken.")
else:
    cursor.execute(create_sql)
    conn.commit()
    print(f"✅ Table '{table_name}' created successfully.")

cursor.close()
conn.close()
'''

    # Optionally write to file
    if output_file_path:
        Path(output_file_path).write_text(script_code)
        logger.info(f"Data loader script written to: {output_file_path}")

    return script_code