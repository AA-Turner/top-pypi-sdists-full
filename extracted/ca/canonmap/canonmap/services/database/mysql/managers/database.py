# canonmap/services/database/mysql/managers/database.py
import logging
logger = logging.getLogger(__name__)

import pickle
import os
import json
import re
from typing import List, Optional, Dict, Any
from collections import defaultdict

import mysql.connector

from canonmap.services.database.mysql.config import MySQLConfig
from canonmap.services.database.mysql.cursor import get_cursor
from canonmap.services.database.mysql.schemas import TableField, Database
from canonmap.services.database.mysql.utils.datetime_formats import DATETIME_TYPES, infer_date_format

class DatabaseManager:
    def __init__(
        self, 
        connection_manager: MySQLConfig,
    ):
        self.connection_manager = connection_manager
        self.autocommit = connection_manager.autocommit

    def create_database(
        self, 
        database: Database,
    ) -> None:
        conn = self.connection_manager.connect()
        
        with get_cursor(conn) as cursor:
            cursor.execute(
                "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
                "WHERE SCHEMA_NAME = %s",
                (database.database_name,)
            )
            already_exists = cursor.fetchone() is not None
            
            if already_exists:
                logger.info(f"Database '{database.database_name}' already exists")
            else:
                logger.info(f"Database '{database.database_name}' does not exist, creating it...")
                cursor.execute(f"CREATE DATABASE `{database.database_name}`")
                if self.autocommit:
                    conn.commit()
                logger.info(f"Database '{database.database_name}' created successfully")
        
        self.connection_manager.database = database.database_name
        self.connection_manager.close()
        self.connection_manager.connect()

    def drop_database(
        self, 
        database_name: Database, 
        autocommit: bool = None,
    ) -> None:
        clean_name = database_name.database_name.strip()
        
        # Use method parameter if provided, otherwise use instance default
        should_autoconfirm = autocommit if autocommit is not None else self.autocommit
        
        if not should_autoconfirm:
            resp1 = input(
                f"Are you sure you want to delete database '{clean_name}'? "
                "This will remove the entire database and all its tables. [y/N]: "
            )
            if resp1.strip().lower() not in ('y', 'yes'):
                logger.info(
                    f"Deletion of database '{clean_name}' cancelled at first prompt."
                )
                return
            resp2 = input(
                f"Type 'DELETE' to permanently delete database '{clean_name}': "
            )
            if resp2.strip() != 'DELETE':
                logger.info(
                    f"Deletion of database '{clean_name}' cancelled at second prompt."
                )
                return

        conn = self.connection_manager.connect()
        with get_cursor(conn) as cursor:
            cursor.execute(
                "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
                "WHERE SCHEMA_NAME = %s",
                (clean_name,)
            )
            if not cursor.fetchone():
                logger.warning(f"Database '{clean_name}' does not exist; nothing to delete.")
                return

        with get_cursor(conn) as cursor:
            cursor.execute(f"DROP DATABASE `{clean_name}`;")
        if self.autocommit:
            conn.commit()
        logger.info(f"Database '{clean_name}' deleted successfully.")

        if self.connection_manager.database == clean_name:
            self.connection_manager.database = None

    def generate_schema(
        self,
        schema_name: str,
        fields_to_include: Optional[List[TableField]] = None,
        fields_to_exclude: Optional[List[TableField]] = None,
        tables_to_include: Optional[List[str]] = None,
        num_examples: int = 10,
        include_helper_fields: bool = False,
        save_dir: str = ".",
        save_json_version: Optional[str] = None,
    ) -> str:
        conn = self.connection_manager.connect()
        schema = defaultdict(dict)

        # fetch table/column/type info
        with get_cursor(conn) as cursor:
            if tables_to_include:
                placeholders = ', '.join(['%s'] * len(tables_to_include))
                cursor.execute(
                    f"SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE "
                    f"FROM INFORMATION_SCHEMA.COLUMNS "
                    f"WHERE TABLE_SCHEMA=%s AND TABLE_NAME IN ({placeholders})",
                    (self.connection_manager.database,) + tuple(tables_to_include)
                )
            else:
                cursor.execute(
                    "SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE "
                    "FROM INFORMATION_SCHEMA.COLUMNS "
                    "WHERE TABLE_SCHEMA=%s",
                    (self.connection_manager.database,)
                )
            columns = cursor.fetchall()

        # filter include/exclude sets
        include_set = set((f.table_name.table_name if hasattr(f.table_name, 'table_name') else f.table_name, f.field_name) for f in fields_to_include or [])
        exclude_set = set((f.table_name.table_name if hasattr(f.table_name, 'table_name') else f.table_name, f.field_name) for f in fields_to_exclude or [])

        filtered_columns = []
        for table, col, typ in columns:
            if not include_helper_fields and col.startswith("__") and col.endswith("__"):
                continue

            if fields_to_include:
                if (table, col) not in include_set:
                    continue
            elif fields_to_exclude:
                if (table, col) in exclude_set:
                    continue

            filtered_columns.append((table, col, typ))

        # sample data for each field
        with get_cursor(conn) as cursor:
            for table, col, typ in filtered_columns:
                samples: List[Any] = []

                # stratified PK-range sampling: 3/4/3 from three equal buckets
                try:
                    cursor.execute(
                        "SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                        "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_KEY='PRI'",
                        (self.connection_manager.database, table)
                    )
                    pk_info = cursor.fetchone()
                    if not pk_info or pk_info[1].upper() not in ("INT","BIGINT","SMALLINT","MEDIUMINT","TINYINT"):
                        raise ValueError("No suitable integer PK")

                    pk_col = pk_info[0]
                    cursor.execute(f"SELECT MIN(`{pk_col}`), MAX(`{pk_col}`) FROM `{table}`")
                    min_id, max_id = cursor.fetchone()
                    import random

                    total = max_id - min_id + 1
                    size = total // 3
                    buckets = [
                        (min_id,           min_id + size - 1, 3),
                        (min_id + size,    min_id + 2*size - 1, 4),
                        (min_id + 2*size,  max_id,             3),
                    ]

                    for start, end, want in buckets:
                        got = []
                        trials = 0
                        while len(got) < want and trials < want * 10:
                            trials += 1
                            rand_id = random.randint(start, end)
                            cursor.execute(
                                f"SELECT `{col}` FROM `{table}` "
                                f"WHERE `{pk_col}` >= %s AND `{col}` IS NOT NULL LIMIT 1",
                                (rand_id,)
                            )
                            row = cursor.fetchone()
                            if row and row[0] not in got:
                                got.append(row[0])
                        samples.extend(got)
                        logger.debug(
                            f"Bucket {start}–{end}: wanted {want}, got {len(got)} after {trials} trials"
                        )
                except Exception:
                    # fallback reservoir sampling on first 10000 distinct values
                    cursor.execute(
                        f"SELECT DISTINCT `{col}` FROM `{table}` "
                        "WHERE `{col}` IS NOT NULL LIMIT 10000"
                    )
                    import random
                    reservoir: List[Any] = []
                    for idx, row in enumerate(cursor):
                        val = row[0]
                        if idx < num_examples:
                            reservoir.append(val)
                        else:
                            j = random.randint(0, idx)
                            if j < num_examples:
                                reservoir[j] = val
                    samples = reservoir
                    logger.debug(
                        f"Used fallback reservoir sampling for {table}.{col} ({len(samples)} samples)"
                    )

                # assemble field info
                field_info: Dict[str, Any] = {
                    "data_type": typ,
                    "data": samples
                }
                if typ.lower() in DATETIME_TYPES:
                    field_info["datetime_format"] = infer_date_format(samples)

                schema[table][col] = field_info

        # persist schema
        os.makedirs(save_dir, exist_ok=True)
        out_path = os.path.join(save_dir, f"{schema_name}.pkl")
        with open(out_path, "wb") as f:
            pickle.dump(dict(schema), f)
        logger.info(f"Schema pickle written to {out_path}")

        if save_json_version:
            json_dir = os.path.dirname(save_json_version)
            if json_dir:
                os.makedirs(json_dir, exist_ok=True)
            schema_dict = json.loads(json.dumps(dict(schema), default=str))
            with open(save_json_version, "w", encoding="utf-8") as jf:
                json.dump(schema_dict, jf, indent=2)
            logger.info(f"Schema JSON written to {save_json_version}")

        return out_path

    def list_databases(
        self,
        show_fields: bool = False,
        show_system_data: bool = False
    ) -> dict:
        conn = self.connection_manager.connect()
        schema: Dict[str, Any] = {}

        with get_cursor(conn) as cursor:
            cursor.execute("SHOW DATABASES")
            dbs = [row[0] for row in cursor.fetchall()]

            if not show_system_data:
                system_dbs = {"information_schema", "mysql", "performance_schema", "sys"}
                dbs = [db for db in dbs if db not in system_dbs]

            for db in dbs:
                cursor.execute(f"SHOW TABLES FROM `{db}`")
                tables = [row[0] for row in cursor.fetchall()]

                if show_fields:
                    table_info: Dict[str, List[str]] = {}
                    for tbl in tables:
                        cursor.execute(f"SHOW COLUMNS FROM `{db}`.`{tbl}`")
                        cols = [col[0] for col in cursor.fetchall()]
                        table_info[tbl] = cols
                    schema[db] = table_info
                else:
                    schema[db] = tables

        logger.info(
            f"Retrieved schema for {len(schema)} databases "
            f"(show_fields={show_fields}, show_system_data={show_system_data})"
        )
        return schema

    def execute_query(
        self, 
        sql_query: str, 
        limit: Optional[int] = 100
    ) -> Dict[str, Any]:
        """
        Executes a given SQL query and returns the result.
        If a limit is provided, it will be applied intelligently. If the original query
        has a stricter (smaller) limit, it will be respected.
        
        Args:
            sql_query: The SQL query to execute
            limit: Optional limit to apply to the query
            
        Returns:
            Dictionary containing the result data, error (if any), and final SQL
        """
        conn = self.connection_manager.connect()
        params: List[Any] = []

        if limit is not None:
            limit_pattern = re.compile(r'LIMIT\s+(\d+)\s*;?\s*$', re.IGNORECASE)
            match = limit_pattern.search(sql_query)

            if match:
                existing_limit = int(match.group(1))
                if limit < existing_limit:
                    sql_query = limit_pattern.sub('LIMIT %s', sql_query)
                    params.append(limit)
                    logger.info(
                        f"Replacing existing LIMIT {existing_limit} with new, stricter LIMIT {limit}"
                    )
                else:
                    logger.info(
                        f"Respecting existing LIMIT {existing_limit} as it is stricter than requested LIMIT {limit}"
                    )
            else:
                sql_query = sql_query.rstrip().rstrip(";") + " LIMIT %s"
                params.append(limit)
                logger.info(f"Appending new LIMIT {limit} to query")

        try:
            with get_cursor(conn, dictionary=True) as cursor:
                cursor.execute(sql_query, tuple(params))
                result = cursor.fetchall()

            # Build a display version of the SQL
            final_sql = sql_query
            if params:
                temp_sql = sql_query
                for param in params:
                    temp_sql = temp_sql.replace('%s', str(param), 1)
                final_sql = temp_sql

            return {"data": result, "error": None, "final_sql": final_sql}
        except mysql.connector.Error as e:
            logger.error(f"Error executing query: {e}")
            return {"data": None, "error": str(e), "final_sql": sql_query}

