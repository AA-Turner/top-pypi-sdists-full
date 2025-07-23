# canonmap/services/db_mysql/managers/table.py

import logging
import re
from pathlib import Path
from typing import Union, Optional, List, Dict, Any

from canonmap.services.db_mysql.adapters.connection import ConnectionManager
from canonmap.services.db_mysql.schemas import TableField, FieldTransform
from canonmap.services.db_mysql.adapters.cursor import get_cursor

from canonmap.services.db_mysql.schemas import CreateDDLResponse # type: ignore

logger = logging.getLogger(__name__)

class TableManager:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    #########################################################
    # Table Creation
    #########################################################
    def create_table_from_ddl(
        self,
        ddl: Union[str, Path, CreateDDLResponse],
        if_exists: str = 'skip',
    ) -> None:
        ddl_sql = ddl
        try:
            path = Path(ddl)
            if path.exists():
                if path.suffix.lower() != '.sql':
                    raise ValueError(
                        f"Invalid file extension for DDL file: {ddl!r}. Must end with '.sql'."
                    )
                ddl_sql = path.read_text()
        except (OSError, TypeError):
            # Check if it's a CreateDDLResponse object
            if hasattr(ddl, 'ddl'):
                ddl_sql = ddl.ddl
            else:
                ddl_sql = ddl  # keep original if not a file

        conn = self.connection_manager.connect()
        statements = [stmt.strip() for stmt in ddl_sql.split(';') if stmt.strip()]
        
        tables_created = []
        tables_skipped = []
        
        with get_cursor(conn) as cursor:
            for stmt in statements:
                # Check if this is a CREATE TABLE statement
                if stmt.strip().upper().startswith('CREATE TABLE'):
                    # Extract table name from CREATE TABLE statement
                    # table_name = self._extract_table_name(stmt)
                    match = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"]?(\w+)[`"]?\s*\(', stmt, re.IGNORECASE)
                    table_name = match.group(1) if match else None
                    if table_name:
                        # Check if table exists
                        cursor.execute(
                            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
                            "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s",
                            (self.connection_manager.config.database, table_name)
                        )
                        table_exists = cursor.fetchone() is not None
                        
                        if table_exists:
                            if if_exists == 'skip':
                                logger.info(f"Table '{table_name}' already exists, skipping creation.")
                                tables_skipped.append(table_name)
                                continue
                            elif if_exists == 'replace':
                                logger.info(f"Table '{table_name}' already exists, dropping and recreating.")
                                cursor.execute(f"DROP TABLE `{table_name}`")
                                tables_created.append(table_name)
                            elif if_exists == 'error':
                                raise ValueError(f"Table '{table_name}' already exists. Use if_exists='skip' or 'replace' to handle this.")
                        else:
                            tables_created.append(table_name)
                
                # Execute the statement
                cursor.execute(stmt)
        
        conn.commit()
        
        # Log clear summary of what happened
        if tables_created:
            logger.info(f"Successfully created tables: {', '.join(tables_created)}")
        if tables_skipped:
            logger.info(f"Skipped existing tables: {', '.join(tables_skipped)}")
        if not tables_created and not tables_skipped:
            logger.info("No table creation statements found in DDL.")
    
    def create_table_from_data(
        self,
        data: List[Dict[str, Any]],
        table_name: str,
        if_exists: str = "append",
        chunk_size: int = 1000,
        ddl_statement: Optional[str] = None
    ):
        if not data:
            logger.warning(f"No data provided to load into table '{table_name}'. Nothing to load.")
            return

        conn = self.connection_manager.connect()
        with get_cursor(conn) as cursor:
            # Check if table exists
            cursor.execute(
                "SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
                (self.connection_manager.config.database, table_name),
            )
            table_exists = cursor.fetchone() is not None

            # Handle if_exists logic
            if table_exists:
                if if_exists == "replace":
                    logger.info(f"Table '{table_name}' exists and if_exists is 'replace'. Dropping and recreating table.")
                    cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
                    conn.commit()
                    if ddl_statement:
                        self.create_table_from_ddl(ddl_statement)
                        logger.info(f"Table '{table_name}' recreated.")
                    else:
                        raise ValueError(f"DDL statement required when if_exists='replace' and table doesn't exist.")
                elif if_exists == "fail":
                    raise ValueError(f"Table '{table_name}' already exists. Set if_exists to 'append' or 'replace'.")
                # if 'append', do nothing to the table structure
            
            elif not table_exists:
                if if_exists in ["append", "fail"]:
                    logger.info(f"Table '{table_name}' does not exist. Creating it now.")
                    if ddl_statement:
                        self.create_table_from_ddl(ddl_statement)
                        logger.info(f"Table '{table_name}' created.")
                    else:
                        raise ValueError(f"DDL statement required when table doesn't exist.")

            # Get column names from first row
            columns = list(data[0].keys())
            placeholders = ", ".join(["%s"] * len(columns))
            columns_sql = ", ".join([f"`{col}`" for col in columns])

            # Insert data in chunks
            total_inserted = 0
            for start in range(0, len(data), chunk_size):
                chunk = data[start : start + chunk_size]
                # Convert each row to tuple in the same order as columns
                chunk_data = [tuple(row[col] for col in columns) for row in chunk]
                sql = f"INSERT INTO `{table_name}` ({columns_sql}) VALUES ({placeholders})"
                cursor.executemany(sql, chunk_data)
                total_inserted += len(chunk_data)
            
            conn.commit()
            logger.info(f"Inserted {total_inserted} rows into '{table_name}'.")


    #########################################################
    # Table TableField Management
    #########################################################
    def create_table_fields(
        self,
        fields: list["TableField"],
        pk_field: str | None = None,
        batch_size: int = 10_000,
    ) -> dict[str, list[str]]:
        """
        For each TableField(table_name, field_name, field_transform) create a derived column:
        initialism  -> FIRST LETTERS ONLY (ABC)
        phonetic    -> Double Metaphone primary code
        soundex     -> MySQL SOUNDEX()

        Returns: {table_name: [new_field_names]}
        """
        # Group/validate
        by_table: dict[str, list[TableField]] = {}
        for f in fields:
            kind = (f.field_transform or "").lower()
            if kind not in {"initialism", "phonetic", "soundex"}:
                raise ValueError(f"Invalid transform '{f.field_transform}' for {f.table_name}.{f.field_name}")
            by_table.setdefault(f.table_name, []).append(f)

        conn = self.connection_manager.connect()

        import math, re
        try:
            from metaphone import doublemetaphone
        except ImportError:
            doublemetaphone = None

        def to_initialism(text: str | None) -> str | None:
            if not text:
                return None
            parts = re.findall(r"[A-Za-z]+", text)
            return "".join(p[0].upper() for p in parts) if parts else None

        def to_phonetic(text: str | None) -> str | None:
            if not text:
                return None
            if doublemetaphone is None:
                raise RuntimeError("metaphone package not installed")
            p, s = doublemetaphone(text)
            return p or s or None

        created: dict[str, list[str]] = {}

        for table_name, flist in by_table.items():
            # Decide PK (use provided or auto)
            effective_pk = pk_field or self._get_or_create_table_pk(table_name)

            # Fetch columns
            with get_cursor(conn) as cursor:
                cursor.execute(
                    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                    "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
                    (self.connection_manager.config.database, table_name)
                )
                cols = {r[0] for r in cursor.fetchall()}

            # Split work
            sql_jobs: list[tuple[TableField, str]] = []
            py_jobs:  list[tuple[TableField, str]] = []

            for f in flist:
                if f.field_name not in cols:
                    raise ValueError(f"Column '{f.field_name}' not found in '{table_name}'")

                new_field = f"__{f.field_name}_{f.field_transform.value.lower()}__"
                if new_field not in cols:
                    with get_cursor(conn) as cursor:
                        cursor.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `{new_field}` VARCHAR(255)")
                    conn.commit()
                    cols.add(new_field)

                if f.field_transform == FieldTransform.SOUNDEX:
                    sql_jobs.append((f, new_field))
                else:
                    py_jobs.append((f, new_field))

            # SOUNDEX via SQL
            for f, new_field in sql_jobs:
                with get_cursor(conn) as cursor:
                    cursor.execute(
                        f"UPDATE `{table_name}` SET `{new_field}` = SOUNDEX(`{f.field_name}`)"
                    )
                conn.commit()

            # Python transforms batched
            if py_jobs:
                with get_cursor(conn) as cursor:
                    cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                    total_rows = cursor.fetchone()[0]

                batches = math.ceil(total_rows / batch_size)
                select_cols = ", ".join({f"`{effective_pk}`"} | {f"`{f.field_name}`" for f, _ in py_jobs})

                for i in range(batches):
                    offset = i * batch_size
                    with get_cursor(conn) as cursor:
                        cursor.execute(
                            f"SELECT {select_cols} FROM `{table_name}` LIMIT %s OFFSET %s",
                            (batch_size, offset)
                        )
                        rows = cursor.fetchall()
                        # capture column order once
                        colnames = [d[0] for d in cursor.description]

                    if not rows:
                        break

                    updates: dict[str, list[tuple[str | None, object]]] = {nf: [] for _, nf in py_jobs}
                    pk_idx = colnames.index(effective_pk)
                    for row in rows:
                        pk_val = row[pk_idx]
                        row_map = dict(zip(colnames, row))
                        for f, new_field in py_jobs:
                            src_val = row_map[f.field_name]
                            if f.field_transform == FieldTransform.INITIALISM:
                                transformed = to_initialism(src_val)
                            else:
                                transformed = to_phonetic(src_val)
                            updates[new_field].append((transformed, pk_val))

                    with get_cursor(conn) as cursor:
                        for new_field, data in updates.items():
                            cursor.executemany(
                                f"UPDATE `{table_name}` SET `{new_field}`=%s WHERE `{effective_pk}`=%s",
                                data
                            )
                    conn.commit()

            created[table_name] = [f"{f.field_name}_{f.field_transform.value.lower()}" for f in flist]

        logger.info("✅ Finished create_table_fields.")
        return created

    def drop_table_fields(self, fields: list["TableField"]) -> dict[str, list[str]]:
        """
        Drop the derived columns referenced by TableField objects.
        Uses TableField.field_transform to infer the column name:
        new_col = f"{field_name}_{field_transform.lower()}"
        If field_transform is None, it will try to drop `field_name` directly.

        Returns: {table_name: [dropped_cols]}
        """
        # Group by table
        by_table: dict[str, list[TableField]] = {}
        for f in fields:
            by_table.setdefault(f.table_name, []).append(f)

        conn = self.connection_manager.connect()
        dropped: dict[str, list[str]] = {}

        for table, flist in by_table.items():
            # get current cols
            with get_cursor(conn) as c:
                c.execute(
                    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                    "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
                    (self.connection_manager.config.database, table)
                )
                cols = {r[0] for r in c.fetchall()}

            # build list of real cols to drop
            to_drop: list[str] = []
            for f in flist:
                if f.field_transform:
                    col = f"{f.field_name}_{f.field_transform.value.lower()}"
                else:
                    col = f.field_name
                if col in cols:
                    to_drop.append(col)
                else:
                    logger.debug(f"Column '{col}' not found in '{table}', skipping.")

            if not to_drop:
                continue

            # one ALTER with multiple DROP COLUMN
            drops_sql = ", ".join(f"DROP COLUMN `{cname}`" for cname in to_drop)
            with get_cursor(conn) as c:
                c.execute(f"ALTER TABLE `{table}` {drops_sql}")
            conn.commit()

            dropped[table] = to_drop
            logger.info(f"Dropped columns on {table}: {', '.join(to_drop)}")

        return dropped

    def _get_or_create_table_pk(self, table_name: str) -> str:
        """
        Return a suitable PK/unique handle for batched updates.
        If none exists, create __tmp_pk__ as AUTO_INCREMENT PRIMARY KEY.
        """
        conn = self.connection_manager.connect()
        with get_cursor(conn) as c:
            c.execute("""
                SELECT COLUMN_NAME, COLUMN_KEY, EXTRA
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s
            """, (self.connection_manager.config.database, table_name))
            rows = c.fetchall()

        cols = {r[0]: (r[1], r[2]) for r in rows}  # name -> (COLUMN_KEY, EXTRA)

        # Prefer real PK
        for name, (key, _) in cols.items():
            if key == "PRI":
                return name

        # Next best: unique, not null
        for name, (key, _) in cols.items():
            if key == "UNI":
                return name

        # Create throwaway
        tmp = "__tmp_pk__"
        if tmp not in cols:
            with get_cursor(conn) as c2:
                c2.execute(
                    f"ALTER TABLE `{table_name}` ADD COLUMN `{tmp}` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY"
                )
            conn.commit()
        return tmp


    #########################################################
    # Table Dropping
    #########################################################
    def drop_table(self, table_name: str, skip_confirm: bool = False) -> None:
        """
        Delete a table from the database. Prompts for confirmation by default.
        Set skip_confirm=True to bypass confirmation.
        """
        clean_name = table_name.strip()
        if not skip_confirm:
            resp = input(
                f"Are you sure you want to delete table '{clean_name}'? This cannot be undone. [y/N]: "
            )
            if resp.strip().lower() not in ('y', 'yes'):
                logger.info(f"Deletion of table '{clean_name}' cancelled by user.")
                return

        conn = self.connection_manager.connect()
        current_db = self.connection_manager.config.database

        # Verify table exists
        with get_cursor(conn) as cursor:
            cursor.execute(
                "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
                "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s",
                (current_db, clean_name)
            )
            if not cursor.fetchone():
                logger.warning(f"Table '{clean_name}' does not exist; nothing to delete.")
                return

        # Drop the table
        with get_cursor(conn) as cursor:
            cursor.execute(f"DROP TABLE `{clean_name}`;")
        conn.commit()
        logger.info(f"Table '{clean_name}' deleted successfully.")


    #########################################################
    # Table Heuristics
    #########################################################
    def list_tables(self, database: str) -> list[str]:
        """
        List all tables in the specified database.
        """
        conn = self.connection_manager.connect()
        with get_cursor(conn) as cursor:
            cursor.execute(f"SHOW TABLES FROM {database};")
            return [row[0] for row in cursor.fetchall()]

    def get_table_size(self, table_name: str) -> int:
        """
        Get the size of a table in bytes.
        """
        conn = self.connection_manager.connect()
        with get_cursor(conn) as cursor:
            cursor.execute(f"SELECT SUM(DATA_LENGTH + INDEX_LENGTH) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
            return cursor.fetchone()[0]

