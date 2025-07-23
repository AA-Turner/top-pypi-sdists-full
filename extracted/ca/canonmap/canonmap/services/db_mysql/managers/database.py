# canonmap/services/db_mysql/managers/database.py

import logging
import pickle
import os
import json
from typing import List, Optional
from collections import defaultdict

import mysql.connector

from canonmap.services.db_mysql.adapters.connection import ConnectionManager
from canonmap.services.db_mysql.adapters.cursor import get_cursor
from canonmap.services.db_mysql.schemas import TableField
from canonmap.services.db_mysql.helpers.datetime_formats import DATETIME_TYPES, infer_date_format

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(
        self, 
        connection_manager: ConnectionManager,
    ):
        self.connection_manager = connection_manager

    def connect_to_database(
        self, 
        db_name: str, 
        create_if_not_exists: bool = True,
    ) -> None:
        conn = self.connection_manager.connect()
        
        with get_cursor(conn) as cursor:
            cursor.execute(
                "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
                "WHERE SCHEMA_NAME = %s",
                (db_name,)
            )
            already_exists = cursor.fetchone() is not None
            
            if already_exists:
                logger.info(f"Database '{db_name}' already exists")
            elif create_if_not_exists:
                logger.info(f"Database '{db_name}' does not exist, creating it...")
                cursor.execute(f"CREATE DATABASE `{db_name}`")
                conn.commit()
                logger.info(f"Database '{db_name}' created successfully")
            else:
                raise RuntimeError(f"Database '{db_name}' does not exist and create_if_not_exists=False")
        
        self.connection_manager.close()
        self.connection_manager.config.database = db_name
        
        config = {
            "host": self.connection_manager.config.host,
            "user": self.connection_manager.config.user,
            "password": self.connection_manager.config.password,
            "port": self.connection_manager.config.port,
            "database": db_name,
        }
        
        try:
            self.connection_manager.conn = mysql.connector.connect(**config)
            logger.info(f"Connected to database '{db_name}'")
        except mysql.connector.Error as e:
            logger.error(f"Could not connect to database '{db_name}': {e}")
            raise RuntimeError(f"Could not connect to database '{db_name}': {e}") from e

    def create_database(
        self, 
        db_name: str,
    ) -> None:
        conn = self.connection_manager.connect()
        
        with get_cursor(conn) as cursor:
            cursor.execute(
                "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
                "WHERE SCHEMA_NAME = %s",
                (db_name,)
            )
            already_exists = cursor.fetchone() is not None
            
            if already_exists:
                logger.info(f"Database '{db_name}' already exists")
            else:
                logger.info(f"Database '{db_name}' does not exist, creating it...")
                cursor.execute(f"CREATE DATABASE `{db_name}`")
                conn.commit()
                logger.info(f"Database '{db_name}' created successfully")
        
        self.connection_manager.config.database = db_name
        self.connection_manager.close()
        self.connection_manager.connect()

    def delete_database(
        self, 
        database_name: str, 
        skip_confirm: bool = False,
    ) -> None:
        clean_name = database_name.strip()
        if not skip_confirm:
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

        conn = self.connection_manager.connect(create_database=False)
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
        conn.commit()
        logger.info(f"Database '{clean_name}' deleted successfully.")

        if self.connection_manager.config.database == clean_name:
            self.connection_manager.config.database = None

    def generate_schema(
        self,
        schema_name: str,
        fields_to_include: Optional[List[TableField]] = None,
        fields_to_exclude: Optional[List[TableField]] = None,
        num_examples: int = 10,
        include_helper_fields: bool = False,
        save_dir: str = ".",
        save_json_version: Optional[str] = None,
    ) -> str:
        conn = self.connection_manager.connect()
        schema = defaultdict(dict)

        with get_cursor(conn) as cursor:
            cursor.execute(
                "SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=%s",
                (self.connection_manager.config.database,)
            )
            columns = cursor.fetchall()

        include_set = set((f.table_name, f.field_name) for f in fields_to_include or [])
        exclude_set = set((f.table_name, f.field_name) for f in fields_to_exclude or [])

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

        if not fields_to_include and not fields_to_exclude:
            filtered_columns = columns

        with get_cursor(conn) as cursor:
            for table, col, typ in filtered_columns:
                cursor.execute(
                    f"SELECT `{col}` FROM `{table}` WHERE `{col}` IS NOT NULL ORDER BY RAND() LIMIT %s",
                    (num_examples,)
                )
                samples = [row[0] for row in cursor.fetchall()]
                field_info = {
                    "data_type": typ,
                    "data": samples
                }
                if typ.lower() in DATETIME_TYPES:
                    field_info["datetime_format"] = infer_date_format(samples)
                schema[table][col] = field_info

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
        schema: dict = {}

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
                    table_info: dict = {}
                    for table in tables:
                        cursor.execute(f"SHOW COLUMNS FROM `{db}`.`{table}`")
                        cols = [col[0] for col in cursor.fetchall()]
                        table_info[table] = cols
                    schema[db] = table_info
                else:
                    schema[db] = tables

        logger.info(
            f"Retrieved schema for {len(schema)} databases "
            f"(show_fields={show_fields}, show_system_data={show_system_data})"
        )
        return schema
    
