# canonmap/services/database/mysql/managers/table.py
import logging
logger = logging.getLogger(__name__)

import re
import json
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
from typing import Union, Optional, List, Dict, Any

from canonmap.services.database.mysql.config import MySQLConfig
from canonmap.services.database.mysql.schemas import Table, TableField, FieldTransformType
from canonmap.services.database.mysql.cursor import get_cursor
from canonmap.services.database.mysql.utils.create_mysql_ddl import create_mysql_ddl
from canonmap.services.database.mysql.utils.create_table_data_from_csv import create_table_data_from_csv






import os
import re
import logging
from concurrent.futures import ProcessPoolExecutor

# ---- Pure utility transform functions (outside class!) ----
def to_initialism(text: str | None) -> str | None:
    if not text:
        return None
    parts = re.findall(r"[A-Za-z]+", text)
    return "".join(p[0].upper() for p in parts) if parts else None

def to_phonetic(text: str | None) -> str | None:
    if not text:
        return None
    try:
        from metaphone import doublemetaphone
    except ImportError:
        raise RuntimeError("metaphone package not installed")
    p, s = doublemetaphone(text)
    return p or s or None

def to_soundex_py(text: str | None) -> str | None:
    if not text:
        return None
    try:
        import jellyfish
    except ImportError:
        raise RuntimeError("jellyfish package not installed for SOUNDEX")
    return jellyfish.soundex(text)




class TableManager:
    def __init__(self, connection_manager: MySQLConfig):
        self.connection_manager = connection_manager
        self.autocommit = connection_manager.autocommit

    #########################################################
    # Table Creation
    #########################################################
    def create_table(
        self,
        table_name: str,
        csv_path: Optional[Union[str, Path]] = None,
        data: Optional[Union[str, List[Dict[str, Any]]]] = None,
        chunk_size: int = 1000,
        if_exists: str = "skip",
    ) -> None:
        """
        Create a table by inferring schema from `data`, and optionally load `data`:

          • The schema is always inferred from the structure of `data`.
          • If `data` is provided, infer a CREATE TABLE from its keys/types, execute that, then insert rows.

        :param table_name: Name of the table.
        :param data:   Either a JSON string or a List[dict] to insert into the new table.
        :param chunk_size: Rows per INSERT batch.
        :param if_exists:  "skip" | "replace" | "error" – handle existing table.
        """
        if csv_path is None and data is None:
            raise ValueError("Must provide `data` to infer schema and create table")

        # 1) Normalize data: handle CSV, JSON, or List[dict]
        # If a CSV path is passed in as data, convert it to a list of dicts
        if csv_path is not None:
            data = create_table_data_from_csv(csv_path)
        # If data is a JSON string, parse it
        elif isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                raise ValueError(f"`data` provided as string but is not valid JSON: {e}")
        # Now data should be None or List[Dict[str, Any]]

        # 2) Infer DDL from data
        resp = create_mysql_ddl(table_name=table_name, data=data)

        # 3) Execute CREATE TABLE (with if_exists logic)
        stmts = [s.strip() for s in resp.ddl.split(";") if s.strip()]
        conn = self.connection_manager.connect()
        created, skipped = [], []

        with get_cursor(conn) as cursor:
            for stmt in stmts:
                up = stmt.upper()
                tbl = None
                if up.startswith("CREATE TABLE"):
                    m = re.search(
                        r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"]?(\w+)[`"]?\s*\(',
                        stmt, re.IGNORECASE
                    )
                    tbl = m.group(1) if m else table_name

                    cursor.execute(
                        "SELECT 1 FROM INFORMATION_SCHEMA.TABLES "
                        "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
                        (self.connection_manager.database, tbl)
                    )
                    exists = cursor.fetchone() is not None

                    if exists:
                        if if_exists == "skip":
                            skipped.append(tbl)
                            logger.info(f"Table '{tbl}' exists, skipping.")
                            continue
                        if if_exists == "error":
                            raise ValueError(f"Table '{tbl}' already exists.")
                        logger.info(f"Table '{tbl}' exists, dropping first.")
                        cursor.execute(f"DROP TABLE `{tbl}`")
                        created.append(tbl)
                    else:
                        created.append(tbl)

                cursor.execute(stmt)
        conn.commit()

        # 4) Populate data if provided
        if data is not None:
            cols = list(data[0].keys())
            cols_sql = ", ".join(f"`{c}`" for c in cols)
            ph = ", ".join(["%s"] * len(cols))
            total = 0

            with get_cursor(conn) as cursor:
                for i in range(0, len(data), chunk_size):
                    batch = data[i : i + chunk_size]
                    vals = [tuple(row[c] for c in cols) for row in batch]
                    sql = f"INSERT INTO `{table_name}` ({cols_sql}) VALUES ({ph})"
                    cursor.executemany(sql, vals)
                    total += len(vals)

            conn.commit()
            logger.info(f"Inserted {total} row(s) into '{table_name}'")

        # 5) Final logging
        if created:
            logger.info(f"Created tables: {', '.join(created)}")
        if skipped:
            logger.info(f"Skipped tables: {', '.join(skipped)}")
        if not created and not skipped:
            logger.info("No CREATE TABLE statements executed.")






    def create_table_fields(
        self,
        fields: list["TableField"],
        field_transform: FieldTransformType,
        pk_field: str | None = None,
        recreate_existing_fields: bool = False,
        chunk_size: int = 10000,
    ) -> dict[str, list[str]]:
        """
        Efficiently bulk-create derived columns with transforms.
        Uses MySQL SOUNDEX natively if possible, otherwise Python multiprocess for phonetic transforms.
        Handles large mapping tables in batches for best performance.
        """
        try:
            from metaphone import doublemetaphone
        except ImportError:
            doublemetaphone = None
        try:
            import jellyfish
        except ImportError:
            jellyfish = None

        logger = logging.getLogger(__name__)

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

        def to_soundex_py(text: str | None) -> str | None:
            if not text:
                return None
            if jellyfish is None:
                raise RuntimeError("jellyfish package not installed for SOUNDEX")
            return jellyfish.soundex(text)

        valid = {
            FieldTransformType.INITIALISM: to_initialism,
            FieldTransformType.PHONETIC: to_phonetic,
            FieldTransformType.SOUNDEX: to_soundex_py,
        }
        if field_transform not in valid:
            raise ValueError(f"Invalid transform '{field_transform}'")
        transform_fn = valid[field_transform]
        max_workers = os.cpu_count() or 4

        by_table: dict[str, list["TableField"]] = {}
        for f in fields:
            table_name = f.table_name.table_name if hasattr(f.table_name, 'table_name') else f.table_name
            by_table.setdefault(table_name, []).append(f)

        conn = self.connection_manager.connect()
        created: dict[str, list[str]] = {}

        for table_name, flist in by_table.items():
            logger.info(f"Starting transform for table '{table_name}' ({field_transform.name}).")
            with get_cursor(conn) as cursor:
                cursor.execute(
                    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                    "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
                    (self.connection_manager.database, table_name)
                )
                existing_cols = {row[0] for row in cursor.fetchall()}

            new_fields: list[tuple["TableField", str]] = []
            for f in flist:
                if f.field_name not in existing_cols:
                    raise ValueError(f"Field '{f.field_name}' not found in '{table_name}'")
                new_name = f"__{f.field_name}_{field_transform.value.lower()}__"
                if new_name in existing_cols and not recreate_existing_fields:
                    logger.info(f"Column '{new_name}' already exists on '{table_name}', skipping.")
                    continue
                if new_name not in existing_cols:
                    with get_cursor(conn) as cursor:
                        cursor.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `{new_name}` VARCHAR(255)")
                    if self.autocommit:
                        conn.commit()
                    existing_cols.add(new_name)
                    logger.info(f"Added column '{new_name}' to '{table_name}'")
                new_fields.append((f, new_name))

            for f, new_name in new_fields:
                logger.info(f"Starting transform for '{table_name}.{new_name}' ({field_transform.name})")
                cond = f"`{new_name}` IS NULL OR `{new_name}` = ''" if not recreate_existing_fields else "1=1"
                # -- MySQL-native SOUNDEX --
                if field_transform == FieldTransformType.SOUNDEX:
                    try:
                        # Test SOUNDEX availability in separate cursor context
                        with get_cursor(conn) as cursor:
                            cursor.execute(f"SELECT SOUNDEX('test')")
                            cursor.fetchall()  # Consume the result
                        
                        # Execute the actual UPDATE in separate cursor context
                        with get_cursor(conn) as cursor:
                            cursor.execute(
                                f"UPDATE `{table_name}` SET `{new_name}` = SOUNDEX(`{f.field_name}`) WHERE {cond}"
                            )
                        if self.autocommit:
                            conn.commit()
                        logger.info(f"MySQL-native SOUNDEX done for '{table_name}.{new_name}'")
                        created.setdefault(table_name, []).append(new_name)
                        continue
                    except Exception as e:
                        logger.warning("MySQL-native SOUNDEX not available, fallback to Python: %s", e)

                # -- Efficient Python fallback for initialism/phonetic --
                with get_cursor(conn) as cursor:
                    cursor.execute(
                        f"SELECT DISTINCT `{f.field_name}` FROM `{table_name}` WHERE {cond}"
                    )
                    distinct_vals = [r[0] for r in cursor.fetchall()]
                if not distinct_vals:
                    logger.info(f"No values to update for '{new_name}' in '{table_name}'")
                    continue

                # *** BRANCH: Use threads/processes only for C-extensions ***
                if field_transform == FieldTransformType.INITIALISM:
                    # Pure Python: GIL-bound, don't thread!
                    logger.info(f"Transforming {len(distinct_vals)} values for initialism (single-thread)...")
                    results = [transform_fn(val) for val in distinct_vals]
                else:
                    # Use threads for C-extension phonetic/soundex
                    logger.info(f"Transforming {len(distinct_vals)} values using {max_workers} threads...")
                    with ThreadPoolExecutor(max_workers=max_workers) as pool:
                        results = list(pool.map(transform_fn, distinct_vals))

                mapping = [(orig, transformed) for orig, transformed in zip(distinct_vals, results) if transformed not in (None, '')]
                if not mapping:
                    logger.info(f"No non-empty transforms for '{new_name}' in '{table_name}'")
                    continue

                temp_table = f"tmp_map_{f.field_name}_{field_transform.value.lower()}"
                with get_cursor(conn) as cursor:
                    # Check if temp table exists before dropping
                    cursor.execute(
                        "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES "
                        "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
                        (self.connection_manager.database, temp_table)
                    )
                    if cursor.fetchone()[0] > 0:
                        cursor.execute(f"DROP TABLE `{temp_table}`")
                    
                    cursor.execute(f"CREATE TABLE `{temp_table}` (orig VARCHAR(255), transformed VARCHAR(255))")
                    # Batch insert for big mapping lists
                    for i in range(0, len(mapping), chunk_size):
                        chunk = mapping[i:i+chunk_size]
                        cursor.executemany(
                            f"INSERT INTO `{temp_table}` (orig, transformed) VALUES (%s, %s)", chunk
                        )
                    cursor.execute(
                        f"""
                        UPDATE `{table_name}` t
                        JOIN `{temp_table}` m ON t.`{f.field_name}` = m.orig
                        SET t.`{new_name}` = m.transformed
                        WHERE {cond}
                        """
                    )
                    cursor.execute(f"DROP TABLE `{temp_table}`")
                    if self.autocommit:
                        conn.commit()

                logger.info(f"Bulk-updated '{new_name}' for {len(mapping)} distinct values in '{table_name}'")
                created.setdefault(table_name, []).append(new_name)

        logger.info("✅ Finished create_table_fields.")
        return created








    def create_primary_key(self, field: TableField, autocommit: bool = None) -> None:
        """
        Add a PRIMARY KEY constraint on the specified column for an existing table.
        If the column doesn't exist, it will be created as an auto-increment primary key.

        Args:
            field: The TableField specifying the table and column
            autocommit: If True, skip user confirmation prompts. 
                               If None, uses the instance default.

        Raises an error if the table already has a primary key,
        or if the specified column already is a primary key.
        """
        conn = self.connection_manager.connect()
        schema = self.connection_manager.database

        # Use method parameter if provided, otherwise use instance default
        should_autoconfirm = autocommit if autocommit is not None else self.autocommit
        
        # Extract table name from Table object
        table_name = field.table_name.table_name if hasattr(field.table_name, 'table_name') else field.table_name
        
        # Check if a primary key already exists
        with get_cursor(conn) as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS "
                "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND CONSTRAINT_TYPE='PRIMARY KEY'",
                (schema, table_name)
            )
            if cursor.fetchone()[0] > 0:
                logger.warning(f"Table '{table_name}' already has a primary key. Drop it before adding a new one.")
                return

        # Check if field exists
        with get_cursor(conn) as cursor:
            cursor.execute(
                "SELECT COLUMN_NAME, COLUMN_KEY FROM INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_NAME=%s",
                (schema, table_name, field.field_name)
            )
            result = cursor.fetchone()
            
            if not result:
                # Field doesn't exist, create it as auto-increment primary key
                if not should_autoconfirm:
                    resp = input(f"Field '{field.field_name}' doesn't exist. Create it as an auto-increment primary key? [y/N]: ")
                    if resp.strip().lower() not in ('y', 'yes'):
                        logger.info(f"Primary key creation cancelled for table '{table_name}'.")
                        return
                
                cursor.execute(
                    f"ALTER TABLE `{table_name}` "
                    f"ADD COLUMN `{field.field_name}` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY"
                )
                if self.autocommit:
                    conn.commit()
                logger.info(f"Created auto-increment primary key field '{field.field_name}' for table '{table_name}'.")
                return
            elif result[1] == "PRI":
                logger.info(f"Field '{field.field_name}' is already the primary key of '{table_name}'.")
                return
            else:
                # Field exists but is not a primary key
                if not should_autoconfirm:
                    resp = input(f"Are you sure you want to add a primary key on field '{field.field_name}' of table '{table_name}'? [y/N]: ")
                    if resp.strip().lower() not in ('y', 'yes'):
                        logger.info(f"Primary key creation cancelled for table '{table_name}'.")
                        return
                # Add the primary key constraint
                cursor.execute(
                    f"ALTER TABLE `{table_name}` "
                    f"ADD PRIMARY KEY (`{field.field_name}`)"
                )
                if self.autocommit:
                    conn.commit()
                logger.info(f"Added primary key on existing field '{field.field_name}' for table '{table_name}'.")

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
            """, (self.connection_manager.database, table_name))
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
            if self.autocommit:
                conn.commit()
        return tmp

    #########################################################
    # Table Dropping
    #########################################################
    def drop_table(self, table_name: str, autocommit: bool = None) -> None:
        """
        Delete a table from the database. Prompts for confirmation by default.
        Set autocommit=True to bypass confirmation.
        """
        clean_name = table_name.strip()
        
        # Use method parameter if provided, otherwise use instance default
        should_autoconfirm = autocommit if autocommit is not None else self.autocommit
        
        if not should_autoconfirm:
            resp = input(
                f"Are you sure you want to delete table '{clean_name}'? This cannot be undone. [y/N]: "
            )
            if resp.strip().lower() not in ('y', 'yes'):
                logger.info(f"Deletion of table '{clean_name}' cancelled by user.")
                return

        conn = self.connection_manager.connect()
        current_db = self.connection_manager.database

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
        if self.autocommit:
            conn.commit()
        logger.info(f"Table '{clean_name}' deleted successfully.")

    def drop_table_fields(self, fields: list["TableField"], autocommit: bool = None) -> dict[str, list[str]]:
        """
        Drop the specified fields from tables.
        Asks for user confirmation per table before dropping.
        
        Args:
            fields: List of TableField objects whose .field_name attribute is the field to drop.
            autocommit: If True, skip user confirmation prompts. 
                               If None, uses the instance default.
        Returns:
            A dict mapping table_name to list of dropped field names.
        """
        # Normalize input to a list of TableField
        if not isinstance(fields, (list, tuple)):
            fields = [fields]
        # Group fields by table
        by_table: dict[str, list[str]] = {}
        for f in fields:
            # Extract table name from Table object
            table_name = f.table_name.table_name if hasattr(f.table_name, 'table_name') else f.table_name
            by_table.setdefault(table_name, []).append(f.field_name)

        # Use method parameter if provided, otherwise use instance default
        should_autoconfirm = autocommit if autocommit is not None else self.autocommit
        
        conn = self.connection_manager.connect()
        dropped: dict[str, list[str]] = {}

        for table_name, col_list in by_table.items():   
            # Confirm with user
            if not should_autoconfirm:
                resp = input(f"Are you sure you want to drop fields {col_list} from table '{table_name}'? [y/N]: ")
                if resp.strip().lower() not in ('y', 'yes'):
                    logger.info(f"Dropping fields cancelled for table '{table_name}'.")
                    continue

            # Verify fields exist
            with get_cursor(conn) as cursor:
                cursor.execute(
                    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                    "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
                    (self.connection_manager.database, table_name)
                )
                existing_cols = {row[0] for row in cursor.fetchall()}

            to_drop = [col for col in col_list if col in existing_cols]
            if not to_drop:
                logger.info(f"No matching fields to drop for table '{table_name}'.")
                continue

            # Build and execute ALTER TABLE
            drops_sql = ", ".join(f"DROP COLUMN `{col}`" for col in to_drop)
            with get_cursor(conn) as cursor:
                cursor.execute(f"ALTER TABLE `{table_name}` {drops_sql}")
            if self.autocommit:
                conn.commit()

            dropped[table_name] = to_drop
            logger.info(f"Dropped fields on '{table_name}': {', '.join(to_drop)}")

        return dropped

    def drop_helper_fields(self, table_name: str, autocommit: bool = None) -> List[str]:
        """
        Drop any helper fields from the given table that:
        - start with "__" and end with "__"
        - contain one of: "initialism", "phonetic", or "soundex"
        Returns a list of dropped field names.
        """
        # Use method parameter if provided, otherwise use instance default
        should_autoconfirm = autocommit if autocommit is not None else self.autocommit
        
        # Prompt user for confirmation before dropping helper fields
        if not should_autoconfirm:
            resp = input(f"Are you sure you want to drop all helper fields from table '{table_name}'? [y/N]: ")
            if resp.strip().lower() not in ('y', 'yes'):
                logger.info(f"Dropping helper fields cancelled for table '{table_name}'.")
                return []

        conn = self.connection_manager.connect()
        schema = self.connection_manager.database
        # Fetch all fields for the table
        with get_cursor(conn) as cursor:
            cursor.execute(
                "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
                (schema, table_name)
            )
            cols = [row[0] for row in cursor.fetchall()]

        # Identify helper fields to drop
        helper_keywords = ("initialism", "phonetic", "soundex")
        to_drop = [
            col for col in cols
            if col.startswith("__") and col.endswith("__")
               and any(keyword in col for keyword in helper_keywords)
        ]

        if not to_drop:
            logger.info(f"No helper fields to drop for table '{table_name}'.")
            return []

        # Build and execute a single ALTER TABLE to drop all helper fields
        drops_sql = ", ".join(f"DROP COLUMN `{col}`" for col in to_drop)
        with get_cursor(conn) as cursor:
            cursor.execute(f"ALTER TABLE `{table_name}` {drops_sql}")
        if self.autocommit:
            conn.commit()

        logger.info(f"Dropped helper fields on '{table_name}': {', '.join(to_drop)}")
        return to_drop


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

    def create_index(
        self,
        index_fields: List[TableField],
        index_name: Optional[str] = None,
        index_type: str = "BTREE",
        unique: bool = False,
        if_exists: str = "error",
        replace_existing: bool = False,
        autocommit: bool = None,
    ) -> str:
        """
        Create an index on the specified table and fields.
        
        Args:
            index_fields: List of TableField objects specifying the table and fields to index
            index_name: Optional custom name for the index. If None, auto-generated
            index_type: Index type (BTREE, HASH, etc.) - defaults to BTREE
            unique: Whether to create a unique index
            if_exists: How to handle existing index - "error", "skip", or "replace"
            replace_existing: If True and index exists, drop and recreate it (overrides if_exists behavior).
            autocommit: If True, skip user confirmation prompts. If None, uses instance default.
            
        Returns:
            The name of the created index
            
        Raises:
            ValueError: If table doesn't exist or fields don't exist
            
        Examples:
            # Single field index
            field = TableField(table_name=Table(table_name="users"), field_name="email")
            cm.table_manager.create_index([field])
            
            # Composite index
            fields = [
                TableField(table_name=Table(table_name="orders"), field_name="user_id"),
                TableField(table_name=Table(table_name="orders"), field_name="order_date")
            ]
            cm.table_manager.create_index(fields)
        """
        # Use method parameter if provided, otherwise use instance default
        should_autoconfirm = autocommit if autocommit is not None else self.autocommit
        
        if not index_fields:
            raise ValueError("At least one TableField must be specified for index creation")
        
        # Validate all TableField objects are for the same table
        table_names = set()
        field_names = []
        
        for field in index_fields:
            # Extract table name from Table object
            table_name = field.table_name.table_name if hasattr(field.table_name, 'table_name') else field.table_name
            table_names.add(table_name)
            field_names.append(field.field_name)
        
        if len(table_names) > 1:
            raise ValueError("All TableField objects must be for the same table")
        
        table_name = list(table_names)[0]
        fields = field_names
        
        conn = self.connection_manager.connect()
        schema = self.connection_manager.database
        
        # Verify table exists
        with get_cursor(conn) as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES "
                "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
                (schema, table_name)
            )
            if cursor.fetchone()[0] == 0:
                raise ValueError(f"Table '{table_name}' does not exist in database '{schema}'")
        
        # Verify all fields exist
        with get_cursor(conn) as cursor:
            cursor.execute(
                "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
                (schema, table_name)
            )
            existing_cols = {row[0] for row in cursor.fetchall()}
        
        missing_fields = [f for f in fields if f not in existing_cols]
        if missing_fields:
            raise ValueError(f"Fields not found in table '{table_name}': {', '.join(missing_fields)}")
        
        # Generate index name if not provided
        if index_name is None:
            prefix = "idx_unique" if unique else "idx"
            field_suffix = "_".join(fields)
            index_name = f"{prefix}_{table_name}_{field_suffix}"
            # Ensure index name doesn't exceed MySQL limit (64 characters)
            if len(index_name) > 64:
                index_name = f"{prefix}_{field_suffix}"[:64]
        
        # Check if index already exists
        with get_cursor(conn) as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS "
                "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND INDEX_NAME=%s",
                (schema, table_name, index_name)
            )
            index_exists = cursor.fetchone()[0] > 0
        
        if index_exists:
            if replace_existing:
                logger.info(f"Index '{index_name}' already exists, dropping and recreating.")
                with get_cursor(conn) as cursor:
                    cursor.execute(f"DROP INDEX `{index_name}` ON `{table_name}`")
                if self.autocommit:
                    conn.commit()
            elif if_exists == "error":
                raise ValueError(f"Index '{index_name}' already exists on table '{table_name}'")
            elif if_exists == "skip":
                logger.info(f"Index '{index_name}' already exists on table '{table_name}', skipping.")
                return index_name
            elif if_exists == "replace":
                logger.info(f"Index '{index_name}' already exists, dropping and recreating.")
                with get_cursor(conn) as cursor:
                    cursor.execute(f"DROP INDEX `{index_name}` ON `{table_name}`")
                if self.autocommit:
                    conn.commit()
            else:
                raise ValueError(f"Invalid if_exists value: {if_exists}")
        
        # Build the CREATE INDEX statement
        fields_sql = ", ".join(f"`{field}`" for field in fields)
        unique_keyword = "UNIQUE" if unique else ""
        
        create_sql = f"CREATE {unique_keyword} INDEX `{index_name}` ON `{table_name}` ({fields_sql}) USING {index_type}"
        
        # Confirm with user if not auto-confirming
        if not should_autoconfirm:
            index_type_desc = "unique" if unique else "non-unique"
            resp = input(
                f"Create {index_type_desc} index '{index_name}' on table '{table_name}' "
                f"for fields {fields}? [y/N]: "
            )
            if resp.strip().lower() not in ('y', 'yes'):
                logger.info(f"Index creation cancelled for table '{table_name}'.")
                return index_name
        
        # Execute the CREATE INDEX
        with get_cursor(conn) as cursor:
            cursor.execute(create_sql)
        if self.autocommit:
            conn.commit()
        
        index_type_desc = "unique" if unique else "non-unique"
        logger.info(f"Created {index_type_desc} index '{index_name}' on table '{table_name}' for fields: {', '.join(fields)}")
        
        return index_name

    def drop_index(
        self,
        table_name: str,
        index_name: str,
        autocommit: bool = None,
    ) -> None:
        """
        Drop an index from the specified table.
        
        Args:
            table_name: Name of the table
            index_name: Name of the index to drop
            autocommit: If True, skip user confirmation prompts. If None, uses instance default.
        """
        # Use method parameter if provided, otherwise use instance default
        should_autoconfirm = autocommit if autocommit is not None else self.autocommit
        
        conn = self.connection_manager.connect()
        schema = self.connection_manager.database
        
        # Verify index exists
        with get_cursor(conn) as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS "
                "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND INDEX_NAME=%s",
                (schema, table_name, index_name)
            )
            if cursor.fetchone()[0] == 0:
                logger.warning(f"Index '{index_name}' does not exist on table '{table_name}'")
                return
        
        # Confirm with user if not auto-confirming
        if not should_autoconfirm:
            resp = input(f"Drop index '{index_name}' from table '{table_name}'? [y/N]: ")
            if resp.strip().lower() not in ('y', 'yes'):
                logger.info(f"Index drop cancelled for table '{table_name}'.")
                return
        
        # Drop the index
        with get_cursor(conn) as cursor:
            cursor.execute(f"DROP INDEX `{index_name}` ON `{table_name}`")
        if self.autocommit:
            conn.commit()
        
        logger.info(f"Dropped index '{index_name}' from table '{table_name}'")

    def delete_indexes(
        self,
        index_fields: List[TableField],
        autocommit: bool = None,
    ) -> Dict[str, List[str]]:
        """
        Delete indexes from tables based on a list of TableField objects.
        
        Args:
            index_fields: List of TableField objects representing indexes to delete
            autocommit: If True, skip user confirmation prompts. If None, uses instance default.
            
        Returns:
            Dictionary mapping table_name to list of deleted index names
            
        Note:
            This method deletes indexes based on field names, not index names.
            It will delete ALL indexes that include the specified fields.
        """
        # Use method parameter if provided, otherwise use instance default
        should_autoconfirm = autocommit if autocommit is not None else self.autocommit
        
        if not index_fields:
            logger.warning("No index fields provided for deletion")
            return {}
        
        # Group fields by table
        by_table: Dict[str, List[str]] = {}
        for field in index_fields:
            # Extract table name from Table object
            table_name = field.table_name.table_name if hasattr(field.table_name, 'table_name') else field.table_name
            by_table.setdefault(table_name, []).append(field.field_name)
        
        conn = self.connection_manager.connect()
        schema = self.connection_manager.database
        deleted: Dict[str, List[str]] = {}
        
        for table_name, field_list in by_table.items():
            # Get all indexes for this table
            with get_cursor(conn) as cursor:
                cursor.execute(
                    """
                    SELECT INDEX_NAME, COLUMN_NAME
                    FROM INFORMATION_SCHEMA.STATISTICS
                    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                    ORDER BY INDEX_NAME, SEQ_IN_INDEX
                    """,
                    (schema, table_name)
                )
                index_data = cursor.fetchall()
            
            # Group indexes by name and their columns
            index_columns: Dict[str, List[str]] = {}
            for index_name, column_name in index_data:
                if index_name not in index_columns:
                    index_columns[index_name] = []
                index_columns[index_name].append(column_name)
            
            # Find indexes that contain any of the specified fields
            indexes_to_delete = []
            for index_name, columns in index_columns.items():
                # Skip PRIMARY KEY indexes
                if index_name == 'PRIMARY':
                    continue
                
                # Check if any of the specified fields are in this index
                if any(field in columns for field in field_list):
                    indexes_to_delete.append(index_name)
            
            if not indexes_to_delete:
                logger.info(f"No matching indexes found for fields {field_list} in table '{table_name}'")
                continue
            
            # Confirm with user if not auto-confirming
            if not should_autoconfirm:
                resp = input(
                    f"Delete indexes {indexes_to_delete} from table '{table_name}' "
                    f"for fields {field_list}? [y/N]: "
                )
                if resp.strip().lower() not in ('y', 'yes'):
                    logger.info(f"Index deletion cancelled for table '{table_name}'.")
                    continue
            
            # Delete the indexes
            deleted_indexes = []
            with get_cursor(conn) as cursor:
                for index_name in indexes_to_delete:
                    try:
                        cursor.execute(f"DROP INDEX `{index_name}` ON `{table_name}`")
                        deleted_indexes.append(index_name)
                        logger.info(f"Dropped index '{index_name}' from table '{table_name}'")
                    except Exception as e:
                        logger.warning(f"Failed to drop index '{index_name}' from table '{table_name}': {e}")
            
            if self.autocommit:
                conn.commit()
            
            if deleted_indexes:
                deleted[table_name] = deleted_indexes
        
        return deleted

    def get_table_indexes(self, table_name: str) -> List[TableField]:
        """
        Retrieve index information for the given table.
        Returns a dict mapping index_name to {"unique": bool, "fields": [field1, field2, ...]}.
        """
        conn = self.connection_manager.connect()
        schema = self.connection_manager.database
        # Check if table exists before fetching indexes
        with get_cursor(conn) as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
                (schema, table_name)
            )
            if cursor.fetchone()[0] == 0:
                logger.warning(f"Table '{table_name}' does not exist in database '{schema}'.")
                return {}
        with get_cursor(conn) as cursor:
            cursor.execute(
                """
                SELECT INDEX_NAME, NON_UNIQUE, SEQ_IN_INDEX, COLUMN_NAME
                FROM INFORMATION_SCHEMA.STATISTICS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                ORDER BY INDEX_NAME, SEQ_IN_INDEX
                """,
                (schema, table_name)
            )
            rows = cursor.fetchall()
        indexes: List[TableField] = []
        for index_name, non_unique, seq, col in rows:
            indexes.append(TableField(table_name=Table(table_name=table_name), field_name=col))
        return indexes

    def _get_recommended_index_fields(self, table_name: str) -> List[str]:
        """
        Get recommended fields for indexing based on common patterns.
        Returns a list of field names that would benefit from indexing.
        """
        conn = self.connection_manager.connect()
        schema = self.connection_manager.database
        
        # Get table structure
        with get_cursor(conn) as cursor:
            cursor.execute(
                """
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_KEY, EXTRA
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION
                """,
                (schema, table_name)
            )
            columns = cursor.fetchall()
        
        if not columns:
            return []
        
        recommended_fields = []
        
        # Common patterns for indexing
        for col_name, data_type, is_nullable, column_key, extra in columns:
            # Skip if already has a key (PRIMARY, UNIQUE, etc.)
            if column_key:
                continue
                
            # Skip auto-increment fields (usually already indexed)
            if extra and 'auto_increment' in extra.lower():
                continue
            
            # Common field patterns that benefit from indexing
            col_lower = col_name.lower()
            
            # ID fields (common foreign keys)
            if any(pattern in col_lower for pattern in ['_id', 'id_', 'id']):
                recommended_fields.append(col_name)
                continue
            
            # Name fields
            if any(pattern in col_lower for pattern in ['name', 'title', 'label']):
                recommended_fields.append(col_name)
                continue
            
            # Date/time fields
            if any(pattern in col_lower for pattern in ['date', 'time', 'created', 'updated', 'modified']):
                recommended_fields.append(col_name)
                continue
            
            # Email fields
            if 'email' in col_lower:
                recommended_fields.append(col_name)
                continue
            
            # Code/identifier fields
            if any(pattern in col_lower for pattern in ['code', 'ref', 'number', 'sku']):
                recommended_fields.append(col_name)
                continue
            
            # Status/enum fields (usually low cardinality but frequently queried)
            if any(pattern in col_lower for pattern in ['status', 'type', 'category', 'state']):
                recommended_fields.append(col_name)
                continue
        
        # Limit to reasonable number of indexes (avoid over-indexing)
        return recommended_fields[:5]  # Max 5 recommended indexes
