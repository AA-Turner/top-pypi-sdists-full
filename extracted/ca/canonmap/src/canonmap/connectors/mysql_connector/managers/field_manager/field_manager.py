import logging
import os
from typing import List, Callable
from concurrent.futures import ThreadPoolExecutor

from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.connectors.mysql_connector.managers.field_manager.validators.models import TableField, FieldTransformType
from canonmap.connectors.mysql_connector.managers.field_manager.validators.requests import (
    CreateFieldRequest,
    CreateFieldsRequest,
    CreateHelperFieldsRequest,
    DropHelperFieldsRequest,
    CreateHelperFieldRequest,
    DropHelperFieldRequest,
    CreateIndexFieldsRequest,
    CreateIndexFieldRequest,
    DropIndexFieldsRequest,
    DropIndexFieldRequest,
    AttachPrimaryKeyToFieldRequest,
    DropPrimaryKeyFromFieldRequest,
    CreateHelperFieldsAllTransformsRequest,
    CreateHelperFieldAllTransformsRequest,
    DropHelperFieldAllTransformsRequest,
    DropHelperFieldsAllTransformsRequest,
    DropFieldRequest,
    DropFieldsRequest,
    )
from canonmap.connectors.mysql_connector.managers.field_manager.transformers import (
    to_initialism,
    to_phonetic,
    to_soundex_py,
)
from canonmap.connectors.mysql_connector.validators.models import IfExists
from canonmap.exceptions import FieldManagerError

logger = logging.getLogger(__name__)

TRANSFORM_MAP: dict[FieldTransformType, Callable[[str | None], str | None]] = {
    FieldTransformType.INITIALISM: to_initialism,
    FieldTransformType.PHONETIC: to_phonetic,
    FieldTransformType.SOUNDEX: to_soundex_py,
}

class FieldManager:
    def __init__(self, connection_manager: MySQLConnector):
        self.connection_manager = connection_manager

    #### GENERAL FIELD MANAGEMENT ####
    def create_field(
        self,
        request: CreateFieldRequest,
    ):
        table_name = request.field.table.name
        database_name = request.field.table.database.name

        # Connect to correct DB if not already
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        self._process_create_field(table_name, request)

    def create_fields(
        self,
        request: CreateFieldsRequest,
    ):
        """
        Create fields (columns) in the database for all specified TableFields. Can process in parallel for efficiency.
        """
        fields: List[TableField] = request.fields
        data_type = request.data_type
        parallel = getattr(request, "parallel", False)
        if not fields:
            raise ValueError("At least one TableField must be specified.")

        database_name = fields[0].table.database.name
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        if parallel:
            from concurrent.futures import ThreadPoolExecutor
            max_workers = os.cpu_count() or 4
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                list(pool.map(
                    lambda f: self._process_create_field(f.table.name, request),
                    fields
                ))
        else:
            for field in fields:
                self._process_create_field(field.table.name, request)

    def drop_field(
        self,
        request: DropFieldRequest,
    ):
        """
        Drop a field (column) from a table.
        Parameters:
            request: DropFieldRequest model.
        """
        field: TableField = request.field
        table_name = field.table.name
        database_name = field.table.database.name

        # Connect to correct DB if not already
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        self._process_drop_field(table_name, field)

    def drop_fields(
        self,
        request: DropFieldsRequest,
    ):
        """
        Drop multiple fields (columns) from tables, optionally in parallel.
        Parameters:
            request: DropFieldsRequest model.
        """
        fields = request.fields
        parallel = getattr(request, "parallel", False)
        if not fields:
            raise ValueError("At least one TableField must be specified.")

        database_name = fields[0].table.database.name
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        if parallel:
            from concurrent.futures import ThreadPoolExecutor
            max_workers = os.cpu_count() or 4
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                list(pool.map(
                    lambda f: self.drop_field(DropFieldRequest(field=f)),
                    fields
                ))
        else:
            for field in fields:
                self.drop_field(DropFieldRequest(field=field))

    def _process_create_field(
        self,
        table_name: str,
        field_request: CreateFieldRequest,
    ):
        conn = self.connection_manager.pool.get_connection()
        try:
            with conn.cursor() as cur:
                # Check if the column exists
                cur.execute("""
                    SELECT COUNT(*) FROM information_schema.columns
                    WHERE table_schema = %s AND table_name = %s AND column_name = %s
                """, (self.connection_manager.config.database, table_name, field_request.field.name))
                (col_exists,) = cur.fetchone()
                if not col_exists:
                    col_ddl = field_request.ddl_sql()
                    cur.execute(
                        f"ALTER TABLE `{table_name}` ADD COLUMN {col_ddl}"
                    )
                    conn.commit()
                    logger.info(f"Added field '{field_request.field.name}' ({col_ddl}) to {table_name}")
                else:
                    logger.info(f"Field '{field_request.field.name}' already exists in {table_name}, skipping.")
        except Exception as e:
            raise FieldManagerError(f"Error creating field '{field_request.field.name}' in '{table_name}': {str(e)}")
        finally:
            conn.close()

    def _process_drop_field(
        self,
        table_name: str,
        field: TableField,
    ):
        conn = self.connection_manager.pool.get_connection()
        try:
            with conn.cursor() as cur:
                # Check if the column exists
                cur.execute("""
                    SELECT COUNT(*) FROM information_schema.columns
                    WHERE table_schema = %s AND table_name = %s AND column_name = %s
                """, (self.connection_manager.config.database, table_name, field.name))
                (col_exists,) = cur.fetchone()
                if col_exists:
                    cur.execute(f"ALTER TABLE `{table_name}` DROP COLUMN `{field.name}`")
                    conn.commit()
                    logger.info(f"Dropped column '{field.name}' from '{table_name}'")
                else:
                    logger.info(f"Column '{field.name}' does not exist in '{table_name}', skipping.")
        except Exception as e:
            raise FieldManagerError(f"Error dropping field '{field.name}' from '{table_name}': {str(e)}")
        finally:
            conn.close()



    #### HELPER FIELD MANAGEMENT ####
    def create_helper_field(
        self,
        request: CreateHelperFieldRequest,
    ):
        """
        Create a transformed helper field (e.g., initialism, phonetic, soundex) in the database for a single field.
        This is the recommended public entry point for single helper field creation.

        Parameters:
            request: CreateHelperFieldRequest model.
        """
        field: TableField = request.field
        transform_type = request.transform_type
        chunk_size = request.chunk_size
        if_helper_exists = getattr(request, "if_helper_exists", IfExists.ERROR)
        if transform_type not in TRANSFORM_MAP:
            raise ValueError(f"Unsupported transform type: {transform_type}")
        transform_fn = TRANSFORM_MAP[transform_type]

        table_name = field.table.name
        database_name = field.table.database.name
        # Connect to correct DB if not already
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        self._process_create_helper_field(table_name, field, transform_fn, transform_type, chunk_size=chunk_size, if_helper_exists=if_helper_exists)

    def create_helper_fields(
        self,
        request: CreateHelperFieldsRequest,
    ):
        """
        Create transformed helper fields (e.g., initialism, phonetic, soundex) in the database
        for all specified fields. Can process in parallel for efficiency.

        Parameters:
            request: CreateHelperFieldsRequest model.
        """
        fields: List[TableField] = request.fields
        transform_type = request.transform_type
        chunk_size = request.chunk_size
        parallel = request.parallel
        if_helper_exists = getattr(request, "if_helper_exists", IfExists.ERROR)
        if not fields:
            raise ValueError("At least one TableField must be specified.")
        if transform_type not in TRANSFORM_MAP:
            raise ValueError(f"Unsupported transform type: {transform_type}")

        database_name = fields[0].table.database.name
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        if parallel:
            from concurrent.futures import ThreadPoolExecutor
            max_workers = os.cpu_count() or 4
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                list(pool.map(
                    lambda f: self.create_helper_field(
                        CreateHelperFieldRequest(field=f, transform_type=transform_type, chunk_size=chunk_size, if_helper_exists=if_helper_exists)
                    ),
                    fields
                ))
        else:
            for field in fields:
                self.create_helper_field(
                    CreateHelperFieldRequest(field=field, transform_type=transform_type, chunk_size=chunk_size, if_helper_exists=if_helper_exists)
                )

    def create_helper_field_all_transforms(
        self,
        request: CreateHelperFieldAllTransformsRequest,
    ):
        """
        For a single TableField, create ALL supported transformed helper fields
        (initialism, phonetic, soundex) in the database.

        Args:
            field: TableField to process
            chunk_size: Chunk size for updates
            parallel: If True, parallelize across transform types
        """
        field: TableField = request.field
        chunk_size = request.chunk_size
        parallel = request.parallel
        if_helper_exists = getattr(request, "if_helper_exists", IfExists.ERROR)

        transform_types = list(TRANSFORM_MAP.keys())
        database_name = field.table.database.name

        # Make sure we're on the correct DB
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        tasks = [
            CreateHelperFieldRequest(field=field, transform_type=transform_type, chunk_size=chunk_size, if_helper_exists=if_helper_exists)
            for transform_type in transform_types
        ]

        if parallel:
            from concurrent.futures import ThreadPoolExecutor
            max_workers = os.cpu_count() or 4
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                list(pool.map(self.create_helper_field, tasks))
        else:
            for req in tasks:
                self.create_helper_field(req)

    def create_helper_fields_all_transforms(
        self,
        request: CreateHelperFieldsAllTransformsRequest,
    ):
        fields: List[TableField] = request.fields
        chunk_size: int = request.chunk_size
        parallel: bool = request.parallel
        if_helper_exists = getattr(request, "if_helper_exists", IfExists.ERROR)

        if not fields:
            raise ValueError("At least one TableField must be specified.")

        # All supported transform types
        transform_types = list(TRANSFORM_MAP.keys())
        database_name = fields[0].table.database.name

        # Make sure we're on the correct DB
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        tasks = []
        for field in fields:
            for transform_type in transform_types:
                tasks.append(
                    CreateHelperFieldRequest(field=field, transform_type=transform_type, chunk_size=chunk_size, if_helper_exists=if_helper_exists)
                )

        if parallel:
            from concurrent.futures import ThreadPoolExecutor
            max_workers = os.cpu_count() or 4
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                list(pool.map(self.create_helper_field, tasks))
        else:
            for req in tasks:
                self.create_helper_field(req)

    def drop_helper_field(
        self,
        request: DropHelperFieldRequest,
    ):
        """
        Drop a transformed helper field (e.g., initialism, phonetic, soundex) from the database for a single field.
        This is the recommended public entry point for single helper field drop.

        Parameters:
            request: DropHelperFieldRequest model.
        """
        field: TableField = request.field
        transform_type = request.transform_type
        table_name = field.table.name
        database_name = field.table.database.name

        # Connect to correct DB if not already
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        self._process_drop_helper_field(table_name, field, transform_type)

    def drop_helper_fields(
        self,
        request: DropHelperFieldsRequest,
    ):
        """
        Drop transformed helper fields (e.g., initialism, phonetic, soundex) from the database
        for all specified fields. Can process in parallel for efficiency.

        Parameters:
            request: DropHelperFieldsRequest model.
        """
        fields: List[TableField] = request.fields
        transform_type = request.transform_type
        parallel = request.parallel
        if not fields:
            raise ValueError("At least one TableField must be specified.")
        database_name = fields[0].table.database.name
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        if parallel:
            from concurrent.futures import ThreadPoolExecutor
            max_workers = os.cpu_count() or 4
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                list(pool.map(
                    lambda f: self._process_drop_helper_field(
                        f.table.name, f, transform_type
                    ),
                    fields
                ))
        else:
            for field in fields:
                self._process_drop_helper_field(
                    field.table.name, field, transform_type
                )

    def drop_helper_field_all_transforms(
        self,
        request: DropHelperFieldAllTransformsRequest,
    ):
        """
        For a single TableField, drop ALL supported transformed helper fields
        (initialism, phonetic, soundex) from the database.

        Args:
            field: TableField to process
            parallel: If True, parallelize across transform types
        """
        field: TableField = request.field
        parallel = request.parallel

        transform_types = list(TRANSFORM_MAP.keys())
        database_name = field.table.database.name
        table_name = field.table.name

        # Make sure we're on the correct DB
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        # Create helper field names for all transform types
        helper_field_names = [f"__{field.name}_{transform_type.value}__" for transform_type in transform_types]

        if parallel:
            from concurrent.futures import ThreadPoolExecutor
            max_workers = os.cpu_count() or 4
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                list(pool.map(
                    lambda name: self._process_drop_helper_field_by_name(table_name, name),
                    helper_field_names
                ))
        else:
            for helper_field_name in helper_field_names:
                self._process_drop_helper_field_by_name(table_name, helper_field_name)

    def drop_helper_fields_all_transforms(
        self,
        request: DropHelperFieldsAllTransformsRequest,
    ):
        """
        For multiple TableFields, drop ALL supported transformed helper fields
        (initialism, phonetic, soundex) from the database.

        Args:
            fields: List of TableFields to process
            parallel: If True, parallelize across fields and transform types
        """
        fields: List[TableField] = request.fields
        parallel = request.parallel

        if not fields:
            raise ValueError("At least one TableField must be specified.")

        # All supported transform types
        transform_types = list(TRANSFORM_MAP.keys())
        database_name = fields[0].table.database.name

        # Make sure we're on the correct DB
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        # Create helper field names for all fields and transform types
        tasks = []
        for field in fields:
            table_name = field.table.name
            for transform_type in transform_types:
                helper_field_name = f"__{field.name}_{transform_type.value}__"
                tasks.append((table_name, helper_field_name))

        if parallel:
            from concurrent.futures import ThreadPoolExecutor
            max_workers = os.cpu_count() or 4
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                list(pool.map(
                    lambda task: self._process_drop_helper_field_by_name(task[0], task[1]),
                    tasks
                ))
        else:
            for table_name, helper_field_name in tasks:
                self._process_drop_helper_field_by_name(table_name, helper_field_name)

    def _process_drop_helper_field_by_name(
        self,
        table_name: str,
        helper_field_name: str,
    ):
        """
        Internal helper to drop a single helper field (column) from a table by name.
        """
        conn = self.connection_manager.pool.get_connection()
        try:
            with conn.cursor() as cur:
                # Get existing columns to check if the helper field exists
                cur.execute("""
                    SELECT column_name FROM information_schema.columns
                    WHERE table_schema = %s AND table_name = %s
                """, (self.connection_manager.config.database, table_name))
                existing_columns = {row[0] for row in cur.fetchall()}
                if helper_field_name in existing_columns:
                    alter_sql = f"ALTER TABLE `{table_name}` DROP COLUMN `{helper_field_name}`"
                    cur.execute(alter_sql)
                    conn.commit()
                    logger.info(f"Dropped helper field '{helper_field_name}' from {table_name}")
                else:
                    logger.info(f"No helper field '{helper_field_name}' to drop from {table_name}")
        except Exception as e:
            raise FieldManagerError(f"Error dropping helper field '{helper_field_name}' from '{table_name}': {str(e)}")
        finally:
            conn.close()

    def _process_create_helper_field(
        self,
        table_name: str,
        field: TableField,
        transform_fn: Callable,
        transform_type: FieldTransformType,
        chunk_size: int = 10000,
        if_helper_exists: IfExists = IfExists.ERROR,
    ):
        assert if_helper_exists in (IfExists.REPLACE, IfExists.ERROR, IfExists.SKIP, IfExists.FILL_EMPTY)
        helper_field_name = f"__{field.name}_{transform_type.value}__"
        conn = self.connection_manager.pool.get_connection()
        try:
            with conn.cursor() as cur:
                # Check if the helper column exists
                cur.execute("""
                    SELECT COUNT(*) FROM information_schema.columns
                    WHERE table_schema = %s AND table_name = %s AND column_name = %s
                """, (self.connection_manager.config.database, table_name, helper_field_name))
                (col_exists,) = cur.fetchone()
                
                # Handle based on if_helper_exists
                if col_exists:
                    if if_helper_exists == IfExists.ERROR:
                        raise FieldManagerError(f"Helper column '{helper_field_name}' already exists in '{table_name}'.")
                    elif if_helper_exists == IfExists.SKIP:
                        logger.info(f"Helper column '{helper_field_name}' exists in '{table_name}', skipping.")
                        return
                    elif if_helper_exists == IfExists.REPLACE:
                        logger.info(f"Dropping and recreating helper column '{helper_field_name}' in '{table_name}'.")
                        cur.execute(f"ALTER TABLE `{table_name}` DROP COLUMN `{helper_field_name}`")
                        conn.commit()
                        # Then proceed to create
                        cur.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `{helper_field_name}` VARCHAR(255)")
                        conn.commit()
                    elif if_helper_exists == IfExists.FILL_EMPTY:
                        logger.info(f"Filling empty cells for helper column '{helper_field_name}' in '{table_name}'.")
                        # Don't drop/recreate, just update empty ones later
                else:
                    cur.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `{helper_field_name}` VARCHAR(255)")
                    conn.commit()
            
            with conn.cursor() as cur:
                # Find PK col
                cur.execute("""
                    SELECT column_name
                    FROM information_schema.key_column_usage
                    WHERE table_schema = %s AND table_name = %s AND constraint_name = 'PRIMARY'
                    LIMIT 1
                """, (self.connection_manager.config.database, table_name))
                pk_result = cur.fetchone()
                if not pk_result:
                    raise RuntimeError(f"No primary key found for table {table_name}")
                pk_col = pk_result[0]

                # Select distinct source values (and, if FILL_EMPTY, only those with empty helper col)
                if if_helper_exists == IfExists.FILL_EMPTY and col_exists:
                    cur.execute(f"""
                        SELECT DISTINCT t.`{field.name}`
                        FROM `{table_name}` t
                        WHERE t.`{helper_field_name}` IS NULL OR t.`{helper_field_name}` = ''
                    """)
                else:
                    cur.execute(f"SELECT DISTINCT `{field.name}` FROM `{table_name}`")
                distinct_vals = [r[0] for r in cur.fetchall() if r[0] is not None]
                if not distinct_vals:
                    logger.info(f"No values found in {table_name}.{field.name} (nothing to transform).")
                    return

            # Transform in parallel (if C-extension)
            max_workers = os.cpu_count() or 4
            if transform_type == FieldTransformType.INITIALISM:
                results = [transform_fn(val) for val in distinct_vals]
            else:
                with ThreadPoolExecutor(max_workers=max_workers) as pool:
                    results = list(pool.map(transform_fn, distinct_vals))

            mapping = [(orig, transformed) for orig, transformed in zip(distinct_vals, results) if transformed]
            if not mapping:
                logger.info(f"No non-empty transforms for {helper_field_name} in {table_name}")
                return

            temp_table = f"tmp_map_{field.name}_{transform_type.value.lower()}"
            with conn.cursor() as cur:
                # 4. Create/drop temp table
                cur.execute(
                    "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES "
                    "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s",
                    (self.connection_manager.config.database, temp_table)
                )
                if cur.fetchone()[0] > 0:
                    cur.execute(f"DROP TABLE `{temp_table}`")
                cur.execute(f"CREATE TABLE `{temp_table}` (orig VARCHAR(255), transformed VARCHAR(255))")

                # 5. Batch insert mappings
                for i in range(0, len(mapping), chunk_size):
                    chunk = mapping[i:i+chunk_size]
                    cur.executemany(
                        f"INSERT INTO `{temp_table}` (orig, transformed) VALUES (%s, %s)", chunk
                    )

                # 6. UPDATE main table in bulk using JOIN
                update_condition = ""
                if if_helper_exists == IfExists.FILL_EMPTY and col_exists:
                    update_condition = f"WHERE t.`{helper_field_name}` IS NULL OR t.`{helper_field_name}` = ''"
                cur.execute(
                    f"""
                    UPDATE `{table_name}` t
                    JOIN `{temp_table}` m ON t.`{field.name}` = m.orig
                    SET t.`{helper_field_name}` = m.transformed
                    {update_condition}
                    """
                )
                cur.execute(f"DROP TABLE `{temp_table}`")
                conn.commit()
                logger.info(f"Bulk-updated '{helper_field_name}' for {len(mapping)} distinct values in '{table_name}'")
        except Exception as e:
            raise FieldManagerError(f"Error creating helper field '{helper_field_name}' in '{table_name}': {e}")
        finally:
            conn.close()

    def _process_drop_helper_field(
        self,
        table_name: str,
        field: TableField,
        transform_type: FieldTransformType,
    ):
        """
        Internal helper to drop a single helper field (column) from a table.
        """
        helper_field_name = f"__{field.name}_{transform_type.value}__"
        conn = self.connection_manager.pool.get_connection()
        try:
            with conn.cursor() as cur:
                # Get existing columns to check if the helper field exists
                cur.execute("""
                    SELECT column_name FROM information_schema.columns
                    WHERE table_schema = %s AND table_name = %s
                """, (self.connection_manager.config.database, table_name))
                existing_columns = {row[0] for row in cur.fetchall()}
                if helper_field_name in existing_columns:
                    alter_sql = f"ALTER TABLE `{table_name}` DROP COLUMN `{helper_field_name}`"
                    cur.execute(alter_sql)
                    conn.commit()
                    logger.info(f"Dropped helper field '{helper_field_name}' from {table_name}")
                else:
                    logger.info(f"No helper field '{helper_field_name}' to drop from {table_name}")
        except Exception as e:
            raise FieldManagerError(f"Error dropping helper field '{helper_field_name}' from '{table_name}': {str(e)}")
        finally:
            conn.close()



    #### INDEX FIELD MANAGEMENT ####
    def create_index_field(
        self,
        request: CreateIndexFieldRequest,
    ) -> str:
        """
        Create an index on the specified field or fields (composite index).
        This is the recommended public entry point for single or composite index creation,
        ensuring consistency and modularity.

        Parameters:
            request: CreateIndexFieldRequest model.

        Returns:
            The name of the created (or existing) index.
        """
        index_field: TableField = request.index_field
        index_name = request.index_name
        index_type = request.index_type
        unique = request.unique
        if_exists = request.if_exists

        # Ensure all fields are for the same table
        table_name = index_field.table.name
        if index_field.table.name != table_name:
            raise ValueError("TableField objects must refer to the same table.")
        field_names = [index_field.name]

        # Connect to correct DB if not already
        database_name = index_field.table.database.name
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        return self._process_create_index_fields(
            table_name=table_name,
            field_names=field_names,
            index_name=index_name,
            index_type=index_type,
            unique=unique,
            if_exists=if_exists,
        )

    def create_index_fields(
        self,
        request: CreateIndexFieldsRequest,
    ) -> List[str]:
        """
        Create indexes for multiple index requests.
        This method processes a list of index requests, each potentially on multiple fields,
        using the create_index_field helper for consistency.

        Parameters:
            request: CreateIndexFieldsRequest model.

        Returns a list of created index names.
        """ 
        index_requests: List[TableField] = request.index_fields
        index_name = request.index_name
        index_type = request.index_type
        unique = request.unique
        if_exists = request.if_exists

        created_indexes = []

        # If index_requests is a list of TableField or list of lists of TableField
        # We normalize to a list of lists of TableField for uniform processing
        # If index_requests is a flat list of TableField, treat as one group
        if not index_requests:
            raise ValueError("At least one TableField or group of TableFields must be specified.")

        # Detect if index_requests is a list of TableField or list of lists
        # If first element is TableField, treat as one group
        if isinstance(index_requests[0], TableField):
            # Single group
            idx_name = index_name
            created_index = self.create_index_field(
                CreateIndexFieldRequest(
                    index_fields=index_requests,
                    index_name=idx_name,
                    index_type=index_type,
                    unique=unique,
                    if_exists=if_exists,
                )
            )
            created_indexes.append(created_index)
        else:
            # Multiple groups
            for i, group in enumerate(index_requests):
                idx_name = None
                if index_name:
                    # Append index number to base name to keep unique
                    idx_name = f"{index_name}_{i+1}"
                created_index = self.create_index_field(
                    CreateIndexFieldRequest(
                        index_fields=group,
                        index_name=idx_name,
                        index_type=index_type,
                        unique=unique,
                        if_exists=if_exists,
                    )
                )
                created_indexes.append(created_index)

        return created_indexes

    def drop_index_field(
         self,
         request: DropIndexFieldRequest,
     ) -> str:
         index_field: TableField = request.index_field
         index_name = request.index_name

         # Ensure all fields are for the same table
         table_name = index_field.table.name
         field_names = [index_field.name]

         # Connect to correct DB if not already
         database_name = index_field.table.database.name
         if self.connection_manager.config.database != database_name:
             logger.info(f"Switching to database: {database_name}")
             self.connection_manager.connect_to_database(database_name)
         else:
             logger.info(f"Already connected to database: {database_name}")

         return self._process_drop_index_fields(
             table_name=table_name,
             field_names=field_names,
             index_name=index_name,
         )

    def drop_index_fields(
        self,
        request: DropIndexFieldsRequest,
    ) -> List[str]:
        """
        Drop indexes for multiple index requests.
        This method processes a list of index requests, each potentially on multiple fields,
        using the drop_index_field helper for consistency.

        Parameters:
            request: DropIndexFieldsRequest model.

        Returns a list of dropped index names.
        """ 
        index_requests: List[TableField] = request.index_fields
        index_name = request.index_name
        if_exists = request.if_exists
        parallel = request.parallel

        dropped_indexes = []

        # If index_requests is a list of TableField or list of lists of TableField
        # We normalize to a list of lists of TableField for uniform processing
        # If index_requests is a flat list of TableField, treat as one group
        if not index_requests:
            raise ValueError("At least one TableField or group of TableFields must be specified.")

        # Detect if index_requests is a list of TableField or list of lists
        # If first element is TableField, treat as one group
        if isinstance(index_requests[0], TableField):
            # Single group
            idx_name = index_name
            dropped_index = self.drop_index_field(
                DropIndexFieldRequest(
                    index_field=index_requests[0],
                    index_name=idx_name,
                    if_exists=if_exists,
                )
            )
            dropped_indexes.append(dropped_index)
        else:
            # Multiple groups
            for i, group in enumerate(index_requests):
                idx_name = None
                if index_name:
                    # Append index number to base name to keep unique
                    idx_name = f"{index_name}_{i+1}"
                dropped_index = self.drop_index_field(
                    DropIndexFieldRequest(
                        index_field=group[0],
                        index_name=idx_name,
                        if_exists=if_exists,
                    )
                )
                dropped_indexes.append(dropped_index)

        return dropped_indexes

    def _process_drop_index_fields(
        self,
        table_name: str,
        field_names: list[str],
        index_name: str = None,
    ) -> str:
        """
        Internal helper to drop an index on a given table/fields group.
        """
        schema = self.connection_manager.config.database
        conn = self.connection_manager.pool.get_connection()

        try:
            with conn.cursor() as cur:
                # Check table existence
                cur.execute(
                    "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=%s AND table_name=%s",
                    (schema, table_name)
                )
                if cur.fetchone()[0] == 0:
                    raise ValueError(f"Table '{table_name}' does not exist in database '{schema}'")

                # Determine/generate index name if not provided
                if not index_name:
                    field_suffix = "_".join(field_names)
                    index_name = f"idx_{table_name}_{field_suffix}"[:64]

                # Check if index exists
                cur.execute(
                    "SELECT COUNT(*) FROM information_schema.statistics WHERE table_schema=%s AND table_name=%s AND index_name=%s",
                    (schema, table_name, index_name)
                )
                exists = cur.fetchone()[0] > 0

                # Handle IfExists enum
                if not exists:
                    raise ValueError(f"Index '{index_name}' does not exist.")

                # Drop index
                cur.execute(f"DROP INDEX `{index_name}` ON `{table_name}`")
                conn.commit()
                logger.info(f"Dropped index '{index_name}' from '{table_name}'")
                return index_name
        except Exception as e:
            raise FieldManagerError(f"Error dropping index '{index_name or 'unnamed'}' from '{table_name}': {str(e)}")
        finally:
            conn.close()

    def _process_create_index_fields(
        self,
        table_name: str,
        field_names: list[str],
        index_name: str = None,
        index_type: str = "BTREE",
        unique: bool = False,
        if_exists: IfExists = IfExists.ERROR,
    ) -> str:
        """
        Internal helper to create an index on a given table/fields group.
        """
        schema = self.connection_manager.config.database
        conn = self.connection_manager.pool.get_connection()

        try:
            with conn.cursor() as cur:
                # Check table existence
                cur.execute(
                    "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=%s AND table_name=%s",
                    (schema, table_name)
                )
                if cur.fetchone()[0] == 0:
                    raise ValueError(f"Table '{table_name}' does not exist in database '{schema}'")

                # Check all columns exist
                cur.execute(
                    "SELECT column_name FROM information_schema.columns WHERE table_schema=%s AND table_name=%s",
                    (schema, table_name)
                )
                existing_cols = {row[0] for row in cur.fetchall()}
                missing = [f for f in field_names if f not in existing_cols]
                if missing:
                    raise ValueError(f"Fields not found in '{table_name}': {', '.join(missing)}")

                # Determine/generate index name
                if not index_name:
                    prefix = "idx_unique" if unique else "idx"
                    field_suffix = "_".join(field_names)
                    index_name = f"{prefix}_{table_name}_{field_suffix}"[:64]

                # Check if index exists
                cur.execute(
                    "SELECT COUNT(*) FROM information_schema.statistics WHERE table_schema=%s AND table_name=%s AND index_name=%s",
                    (schema, table_name, index_name)
                )
                exists = cur.fetchone()[0] > 0

                # Handle IfExists enum
                if exists:
                    if if_exists == IfExists.ERROR:
                        raise ValueError(f"Index '{index_name}' already exists.")
                    elif if_exists == IfExists.SKIP:
                        logger.info(f"Index '{index_name}' exists; skipping.")
                        return index_name
                    elif if_exists == IfExists.REPLACE:
                        logger.info(f"Index '{index_name}' exists; dropping for replacement.")
                        cur.execute(f"DROP INDEX `{index_name}` ON `{table_name}`")
                    elif if_exists == IfExists.APPEND:
                        logger.info(f"Index '{index_name}' exists; APPEND not relevant for indexes, skipping.")
                        return index_name
                    else:
                        raise ValueError(f"Invalid if_exists value: {if_exists}")

                # Create index
                fields_sql = ", ".join(f"`{f}`" for f in field_names)
                uniq = "UNIQUE" if unique else ""
                create_sql = f"CREATE {uniq} INDEX `{index_name}` ON `{table_name}` ({fields_sql}) USING {index_type}"
                cur.execute(create_sql)
                conn.commit()
                logger.info(f"Created {uniq or 'non-unique'} index '{index_name}' on '{table_name}' for {', '.join(field_names)}")
                return index_name
        except Exception as e:
            raise FieldManagerError(f"Error creating index '{index_name or 'unnamed'}' on '{table_name}': {str(e)}")
        finally:
            conn.close()



    #### CONSTRAINT MANAGEMENT ####
    def attach_primary_key_to_field(
        self,
        request: AttachPrimaryKeyToFieldRequest,
    ):
        field: TableField = request.field
        table_name = field.table.name
        database_name = field.table.database.name
        field_name = field.name

        # Connect to correct DB if not already
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        conn = self.connection_manager.pool.get_connection()
        try:
            with conn.cursor() as cur:
                # Check if PK already exists
                cur.execute("""
                    SELECT COUNT(*) FROM information_schema.key_column_usage
                    WHERE table_schema = %s AND table_name = %s AND constraint_name = 'PRIMARY'
                """, (database_name, table_name))
                if cur.fetchone()[0] > 0:
                    raise ValueError(f"Table '{table_name}' already has a primary key.")

                # Alter table to add PK
                cur.execute(
                    f"ALTER TABLE `{table_name}` ADD PRIMARY KEY (`{field_name}`)"
                )
                conn.commit()
                logger.info(f"Attached PRIMARY KEY to `{table_name}`.`{field_name}`.")
        finally:
            conn.close()

    def drop_primary_key_from_field(
        self,
        request: DropPrimaryKeyFromFieldRequest,
    ):
        field: TableField = request.field
        table_name = field.table.name
        database_name = field.table.database.name

        # Connect to correct DB if not already
        if self.connection_manager.config.database != database_name:
            logger.info(f"Switching to database: {database_name}")
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")

        conn = self.connection_manager.pool.get_connection()
        try:
            with conn.cursor() as cur:
                # Check if PK exists
                cur.execute("""
                    SELECT COUNT(*) FROM information_schema.key_column_usage
                    WHERE table_schema = %s AND table_name = %s AND constraint_name = 'PRIMARY'
                """, (database_name, table_name))
                if cur.fetchone()[0] == 0:
                    raise ValueError(f"Table '{table_name}' does not have a primary key.")

                # Drop primary key constraint
                cur.execute(f"ALTER TABLE `{table_name}` DROP PRIMARY KEY")
                conn.commit()
                logger.info(f"Dropped PRIMARY KEY constraint from `{table_name}`.")
        finally:
            conn.close()
