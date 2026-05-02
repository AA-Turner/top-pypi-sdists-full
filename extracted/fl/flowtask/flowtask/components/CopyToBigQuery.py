import asyncio
from collections.abc import Callable
import datetime as dt
import math
import time
import pandas as pd
from asyncdb import AsyncDB
from asyncdb.exceptions import (
    StatementError,
    DataError
)
from pathlib import Path
from .CopyTo import CopyTo
from ..interfaces.dataframes import PandasDataframe
from ..exceptions import (
    ComponentError,
    DataNotFound
)
from querysource.conf import (
    BIGQUERY_CREDENTIALS,
    BIGQUERY_PROJECT_ID
)


class CopyToBigQuery(CopyTo, PandasDataframe):
    """
    CopyToBigQuery.

    Overview

        This component allows copying data into a BigQuery table,
        using write functionality from AsyncDB BigQuery driver.

        :widths: auto

        | tablename    |   Yes    | Name of the table in                                   |
        |              |          | BigQuery                                               |
        | schema       |   Yes    | Name of the dataset                                    |
        |              |          | where the table is located                             |
        | truncate     |   Yes    | This option indicates if the component should empty    |
        |              |          | before copying the new data to the table. If set to    |
        |              |          | true, the table will be truncated before saving data.  |
        | use_buffer   |   No     | When activated, this option allows optimizing the      |
        |              |          | performance of the task when dealing with large        |
        |              |          | volumes of data.                                       |
        | credentials  |   No     | Path to BigQuery credentials JSON file                 |
        |              |          |                                                        |
        | project_id   |   No     | Google Cloud Project ID                                |
        |              |          |                                                        |


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          CopyToBigQuery:
          schema: hisense
          tablename: product_availability_all
        ```
    """  # noqa: E501
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.pk = []
        self.truncate: bool = False
        self.delete_before_insert: bool = False
        self.use_merge: bool = False
        self.data = None
        self._engine = None
        self.tablename: str = ""
        self.schema: str = ""  # dataset in BigQuery terminology
        self.use_chunks = False
        self._chunksize: int = kwargs.pop('chunksize', 10000)
        self._connection: Callable = None
        self._project_id: str = kwargs.pop('project_id', BIGQUERY_PROJECT_ID)
        self._credentials: str = kwargs.pop('credentials', BIGQUERY_CREDENTIALS)
        self._record_columns: dict = kwargs.pop('record_columns', {})
        try:
            self.multi = bool(kwargs["multi"])
            del kwargs["multi"]
        except KeyError:
            self.multi = False
        super().__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        self._driver: str = 'bigquery'

    def default_connection(self):
        """default_connection.

        Default Connection to BigQuery.
        """
        try:
            credentials = self._credentials
            if isinstance(credentials, Path):
                credentials = str(credentials)
            params: dict = {
                "credentials": credentials,
                "project_id": self._project_id
            }
            self._connection = AsyncDB(
                'bigquery',
                params=params,
                loop=self._loop
            )
            return self._connection
        except Exception as err:
            raise ComponentError(
                f"Error configuring BigQuery Connection: {err!s}"
            ) from err

    def _build_record_schema(self) -> list:
        """Build schema including RECORD type columns."""
        type_mapping = {
            'object': 'STRING',
            'string': 'STRING',
            'int64': 'INTEGER',
            'float64': 'FLOAT',
            'Float64': 'FLOAT',
            'bool': 'BOOLEAN',
            'boolean': 'BOOLEAN',
            'datetime64[ns]': 'TIMESTAMP',
            'datetime64[ns, UTC]': 'TIMESTAMP',
            'datetime64[us, UTC]': 'TIMESTAMP',
            'date': 'DATE'
        }

        bq_schema = []
        for column, dtype in self.data.dtypes.items():
            # Check if this column has a custom RECORD schema
            if column in self._record_columns:
                bq_schema.append({
                    "name": column,
                    "type": "RECORD",
                    "mode": "REPEATED",
                    "fields": self._record_columns[column]
                })
            else:
                bq_type = type_mapping.get(str(dtype), 'STRING')
                bq_schema.append({
                    "name": column,
                    "type": bq_type,
                    "mode": "NULLABLE"
                })

        return bq_schema

    # Function to clean invalid float values
    def clean_floats(self, data):
        def sanitize_value(value):
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                return None
            return value

        if isinstance(data, dict):
            return {k: sanitize_value(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.clean_floats(item) for item in data]
        return data

    async def _create_table(self):
        """Create a Table in BigQuery if it doesn't exist."""
        from google.cloud import bigquery
        from google.cloud.exceptions import Conflict, NotFound

        try:
            async with await self._connection.connection() as conn:
                client = conn._connection
                table_ref = client.dataset(self.schema).table(self.tablename)

                # Check if we need to drop the table first
                if hasattr(self, 'create_table') and isinstance(self.create_table, dict):
                    if self.create_table.get('drop', False) is True:
                        self._logger.info(f"CopyTo: Dropping table {self.schema}.{self.tablename} (create_table['drop']=True)")
                        client.delete_table(table_ref, not_found_ok=True)

                
                # Check if table already exists
                try:
                    client.get_table(table_ref)
                    self._logger.info(f"CopyTo: Table {self.schema}.{self.tablename} already exists")
                    return
                except NotFound:
                    pass  # Table does not exist, proceed with creation

                # First ensure dataset exists
                await conn.create_dataset(self.schema)

                # Infer schema from DataFrame
                bq_schema = []
                type_mapping = {
                    'object': 'STRING',
                    'string': 'STRING',
                    'int64': 'INTEGER',
                    'Int64': 'INTEGER',
                    'int32': 'INTEGER',
                    'Int32': 'INTEGER',
                    'float64': 'FLOAT',
                    'Float64': 'FLOAT',
                    'bool': 'BOOLEAN',
                    'boolean': 'BOOLEAN',
                    'datetime64[ns]': 'TIMESTAMP',
                    'datetime64[ns, UTC]': 'TIMESTAMP',
                    'datetime64[us, UTC]': 'TIMESTAMP',
                    'date': 'DATE'
                }

                # Build DDL for debugging
                ddl_columns = []

                for column, dtype in self.data.dtypes.items():
                    bq_type = type_mapping.get(str(dtype), 'STRING')
                    # Create SchemaField object directly
                    field = bigquery.SchemaField(column, bq_type, mode="NULLABLE")
                    bq_schema.append(field)
                    ddl_columns.append(f"{column} {bq_type}")

                # Construct and print CREATE TABLE sentence
                ddl = f"CREATE TABLE `{self.schema}.{self.tablename}` (\n"
                ddl += ",\n".join([f"  {col}" for col in ddl_columns])
                ddl += "\n)"
                self._logger.debug(f"CopyTo: Table Sentence: \n{ddl}")

                # If create_table has clustering fields, get them
                clustering_fields = None
                if hasattr(self, 'create_table'):
                    if isinstance(self.create_table, dict) and 'pk' in self.create_table:
                        clustering_fields = self.create_table['pk']


                # Create table using underlying client to support clustering
                client = conn._connection
                table_ref = client.dataset(self.schema).table(self.tablename)
                table = bigquery.Table(table_ref, schema=bq_schema)
                
                if clustering_fields:
                    table.clustering_fields = clustering_fields

                try:
                    table = client.create_table(table)
                    self._logger.info(f"CopyTo: Created table {table.project}.{table.dataset_id}.{table.table_id}")
                except Conflict:
                    self._logger.info(f"CopyTo: Table {self.schema}.{self.tablename} already exists")

        except Exception as err:
            raise ComponentError(
                f"Error creating BigQuery table: {err}"
            ) from err

    async def _truncate_table(self):
        """Truncate the BigQuery table using the driver's built-in method."""
        async with await self._connection.connection() as conn:
            await self._connection.truncate_table(
                table_id=self.tablename,
                dataset_id=self.schema
            )

    async def _wait_for_load_job(self, load_job, description: str = "LoadJob"):
        """Wait for a BigQuery LoadJob with proper error checking."""
        while not load_job.done():
            await asyncio.sleep(2)
        if getattr(load_job, 'errors', None):
            raise ComponentError(
                f"{description} finished with errors: {load_job.errors}"
            )
        if getattr(load_job, 'error_result', None):
            raise ComponentError(
                f"{description} error_result: {load_job.error_result}"
            )
        self._logger.info(f"{description} completed successfully")
        return load_job

    def _normalize_records(
        self, records: list, column_types: dict, json_columns: set
    ) -> list:
        """Normalize DataFrame records for BigQuery NDJSON loading.

        Handles JSON columns, temporal type conversions, and NaN cleanup.
        """
        def normalize_value(value, column=None):
            col_type = column_types.get(column) if column_types else None
            if value is None:
                return None
            try:
                if pd.isna(value):
                    return None
            except (ValueError, TypeError):
                pass
            if column in json_columns and isinstance(value, (dict, list)):
                return value
            if col_type in ("DATETIME", "TIMESTAMP"):
                if isinstance(value, (int, float)):
                    ts = value / 1000 if value > 1_000_000_000_000 else value
                    dt_value = dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc)
                    if col_type == "DATETIME":
                        return dt_value.strftime("%Y-%m-%d %H:%M:%S")
                    return dt_value.isoformat()
                elif isinstance(value, (pd.Timestamp, dt.datetime)):
                    if col_type == "DATETIME":
                        return value.strftime("%Y-%m-%d %H:%M:%S")
                    return value.isoformat()
                elif isinstance(value, dt.date):
                    return dt.datetime.combine(
                        value, dt.time.min
                    ).strftime("%Y-%m-%d %H:%M:%S")
            elif col_type == "DATE":
                if isinstance(value, (int, float)):
                    ts = value / 1000 if value > 1_000_000_000_000 else value
                    return dt.datetime.fromtimestamp(
                        ts, tz=dt.timezone.utc
                    ).date().isoformat()
                elif isinstance(value, (pd.Timestamp, dt.datetime)):
                    return value.date().isoformat()
                elif isinstance(value, dt.date):
                    return value.isoformat()
                elif isinstance(value, str) and "T" in value:
                    return value.split("T", 1)[0]
            if isinstance(value, dict):
                return {k: normalize_value(v) for k, v in value.items()}
            if isinstance(value, list):
                return [normalize_value(v) for v in value]
            return value

        return [
            {k: normalize_value(v, column=k) for k, v in record.items()}
            for record in records
        ]

    def _prepare_record_data(self, records: list) -> list:
        """Prepare records for BigQuery, converting datetimes in nested structures."""
        import datetime as dt

        def convert_value(value):
            if isinstance(value, dt.datetime):
                return value.isoformat()
            elif isinstance(value, dict):
                return {k: convert_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [convert_value(item) for item in value]
            return value

        return [convert_value(record) for record in records]

    async def _copy_with_records(self):
        """Copy DataFrame to BigQuery with RECORD column support using JSON loading."""
        from google.cloud import bigquery
        # Convert DataFrame to list of dicts
        records = self.data.to_dict(orient='records')

        # Convert datetime objects in nested structures
        records = self._prepare_record_data(records)

        async with await self._connection.connection() as conn:
            client = conn._connection

            table_ref = f"{self._project_id}.{self.schema}.{self.tablename}"

            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            )

            load_job = client.load_table_from_json(
                records,
                table_ref,
                job_config=job_config
            )
            result = load_job.result()  # Wait for completion
            self._logger.info(f'CopyTo: Loaded {len(records)} rows into {table_ref}')

    async def _copy_with_json_loader(self, json_columns, column_types):
        """Copy DataFrame to BigQuery using NDJSON loader (for JSON column support)."""
        records = self.data.to_dict(orient='records')
        normalized_records = self._normalize_records(records, column_types, json_columns)

        self._logger.info(
            f'CopyTo: Normalized {len(normalized_records)} records for NDJSON loader'
        )

        async with await self._connection.connection() as conn:
            result = await conn.write(
                data=normalized_records,
                table_id=self.tablename,
                dataset_id=self.schema,
                use_pandas=False,
                if_exists="append"
            )
            self._logger.info(f'CopyTo: NDJSON loader result: {result}')

            if self._debug:
                count_q = f"SELECT COUNT(*) as count FROM `{self.schema}.{self.tablename}`"
                count_result, count_error = await conn.query(count_q)
                if count_result:
                    rows = list(count_result) if hasattr(count_result, '__iter__') else count_result
                    if rows and len(rows) > 0:
                        self._logger.debug(
                            f'CopyTo: Rows in table after INSERT: {rows[0].get("count", "unknown")}'
                        )
                elif count_error:
                    self._logger.warning(f'CopyTo: Error verifying row count: {count_error}')

    async def _load_to_staging(self, conn, temp_table, column_types, json_columns):
        """Load self.data to a staging table, handling JSON/RECORD columns."""
        use_pandas = True
        data = self.data

        if json_columns or self._record_columns:
            records = self.data.to_dict(orient='records')
            data = self._normalize_records(records, column_types, json_columns)
            use_pandas = False

        load_job = await conn.write(
            data=data,
            table_id=temp_table,
            dataset_id=self.schema,
            use_pandas=use_pandas,
            if_exists="append"
        )
        await self._wait_for_load_job(load_job, f"Staging load to {temp_table}")
        return load_job

    async def _delete_and_insert_safe(self, column_types, json_columns):
        """
        Transactional DELETE + INSERT using a staging table.

        Flow:
        1. LoadJob data -> temp table (FREE, target untouched if fails)
        2. BEGIN TRANSACTION
        3.   DELETE matching PKs from target
        4.   INSERT INTO target SELECT * FROM temp
        5. COMMIT (atomic: both succeed or both rollback)
        6. DROP temp table
        """
        temp_table = f"{self.tablename}_stg_{int(time.time())}"

        async with await self._connection.connection() as conn:
            try:
                # 1. Create empty clone of target table
                create_q = f"""
                    CREATE TABLE `{self.schema}.{temp_table}`
                    AS SELECT * FROM `{self.schema}.{self.tablename}` WHERE 1=0
                """
                _, err = await conn.query(create_q)
                if err:
                    raise ComponentError(f"Error creating staging table: {err}")

                # 2. Load data to staging (FREE LoadJob - target untouched if fails)
                await self._load_to_staging(
                    conn, temp_table, column_types, json_columns
                )

                # 3. Verify staging has data
                count_q = f"SELECT COUNT(*) as c FROM `{self.schema}.{temp_table}`"
                count_res, _ = await conn.query(count_q)
                rows = list(count_res) if count_res and hasattr(count_res, '__iter__') else []
                staged = rows[0].get("c", 0) if rows else 0
                if staged == 0:
                    raise ComponentError("Staging table is empty after load")
                self._logger.info(f"CopyTo: Staged {staged} rows in {temp_table}")

                # 4. Transactional DELETE + INSERT (atomic)
                pk_join = " AND ".join(
                    [f"T.{k} = S.{k}" for k in self.pk]
                )
                all_cols = ", ".join(self.data.columns)

                txn_sql = f"""
                    BEGIN TRANSACTION;

                    DELETE FROM `{self.schema}.{self.tablename}` T
                    WHERE EXISTS (
                        SELECT 1 FROM `{self.schema}.{temp_table}` S
                        WHERE {pk_join}
                    );

                    INSERT INTO `{self.schema}.{self.tablename}` ({all_cols})
                    SELECT {all_cols} FROM `{self.schema}.{temp_table}`;

                    COMMIT TRANSACTION;
                """

                self._logger.info("CopyTo: Executing transactional DELETE+INSERT")
                result, error = await conn.query(txn_sql)
                if error:
                    raise ComponentError(
                        f"Transactional DELETE+INSERT failed (auto-rollback): {error}"
                    )
                self._logger.info("CopyTo: Transaction committed successfully")

            finally:
                await conn.query(
                    f"DROP TABLE IF EXISTS `{self.schema}.{temp_table}`"
                )

    async def _merge_dataframe(self, column_types, json_columns):
        """
        Atomic MERGE: update existing rows + insert new rows in one DML.

        Flow:
        1. LoadJob data -> temp table (FREE, target untouched if fails)
        2. MERGE target USING temp ON pk match
        3. DROP temp table
        """
        if not self.pk:
            raise ComponentError(
                "MERGE requires pk (primary keys) to be defined"
            )

        temp_table = f"{self.tablename}_merge_{int(time.time())}"

        async with await self._connection.connection() as conn:
            try:
                # 1. Create empty clone of target table
                create_q = f"""
                    CREATE TABLE `{self.schema}.{temp_table}`
                    AS SELECT * FROM `{self.schema}.{self.tablename}` WHERE 1=0
                """
                _, err = await conn.query(create_q)
                if err:
                    raise ComponentError(
                        f"Error creating staging table for MERGE: {err}"
                    )

                # 2. Load data to staging
                await self._load_to_staging(
                    conn, temp_table, column_types, json_columns
                )

                # 3. Build and execute MERGE
                merge_keys = " AND ".join(
                    [f"T.{k} = S.{k}" for k in self.pk]
                )

                non_pk_cols = [
                    c for c in self.data.columns if c not in self.pk
                ]
                set_clause = ", ".join(
                    [f"T.{c} = S.{c}" for c in non_pk_cols]
                )

                all_cols = ", ".join(self.data.columns)
                source_cols = ", ".join(
                    [f"S.{c}" for c in self.data.columns]
                )

                merge_q = f"""
                    MERGE `{self.schema}.{self.tablename}` T
                    USING `{self.schema}.{temp_table}` S
                    ON {merge_keys}
                    WHEN MATCHED THEN UPDATE SET {set_clause}
                    WHEN NOT MATCHED THEN
                        INSERT ({all_cols}) VALUES ({source_cols})
                """

                self._logger.info(
                    f"CopyTo: Executing MERGE on {self.schema}.{self.tablename}"
                )
                result, error = await conn.query(merge_q)
                if error:
                    raise ComponentError(f"MERGE failed: {error}")
                self._logger.info("CopyTo: MERGE completed successfully")

            finally:
                await conn.query(
                    f"DROP TABLE IF EXISTS `{self.schema}.{temp_table}`"
                )

    async def _get_table_schema(self):
        """Get BigQuery table schema to properly convert DataFrame columns."""
        column_types = {}
        try:
            async with await self._connection.connection() as conn:
                schema_q = f"""
                    SELECT column_name, data_type
                    FROM {self.schema}.INFORMATION_SCHEMA.COLUMNS
                    WHERE table_name = '{self.tablename}'
                """
                schema_res, error = await conn.query(schema_q)
                if not error and schema_res:
                    column_types = {
                        row["column_name"]: row["data_type"] for row in schema_res
                    }
                    self._logger.info(f'CopyTo: Retrieved schema for {self.schema}.{self.tablename}')
        except Exception as err:
            self._logger.warning(f'CopyTo: Could not retrieve table schema: {err}')
        return column_types

    def _convert_dataframe_to_bigquery_types(self, df, column_types):
        """Convert DataFrame columns to match BigQuery schema types."""
        converted_df = df.copy()

        for col in converted_df.columns:
            if col not in column_types:
                continue

            bq_type = column_types[col]

            # Handle DATE type
            if bq_type == "DATE":
                if pd.api.types.is_datetime64_any_dtype(converted_df[col]):
                    converted_df[col] = pd.to_datetime(converted_df[col]).dt.date
                    self._logger.debug(f'CopyTo: Converted {col} to DATE (BigQuery schema type)')
                elif pd.api.types.is_integer_dtype(converted_df[col]):
                    # Unix timestamp to date
                    converted_df[col] = pd.to_datetime(converted_df[col], unit='s').dt.date

            # Handle DATETIME type
            elif bq_type == "DATETIME":
                if pd.api.types.is_datetime64_any_dtype(converted_df[col]):
                    converted_df[col] = converted_df[col].dt.tz_localize(None)

            # Handle TIMESTAMP type
            elif bq_type == "TIMESTAMP":
                if pd.api.types.is_datetime64_any_dtype(converted_df[col]):
                    converted_df[col] = converted_df[col].dt.tz_localize(None)

            # Handle STRING type
            elif bq_type == "STRING":
                if pd.api.types.is_datetime64_any_dtype(converted_df[col]):
                    converted_df[col] = converted_df[col].astype(str).replace('NaT', None)
                    self._logger.debug(f'CopyTo: Converted {col} to STRING (from datetime for BigQuery schema)')

        return converted_df

    async def _copy_dataframe(self):
        """Copy a pandas DataFrame to BigQuery."""
        try:
            # Get BigQuery table schema for proper type conversion
            column_types = await self._get_table_schema()

            # --- Data preparation (common to all strategies) ---
            # Clean NA/NaT values from string fields
            str_cols = self.data.select_dtypes(include=["string"])
            if not str_cols.empty:
                self.data[str_cols.columns] = str_cols.astype(object).where(
                    pd.notnull(str_cols), None
                )

            # Convert DataFrame columns to match BigQuery schema
            if column_types:
                if self._debug:
                    self._logger.debug("DataFrame to BigQuery Type Conversion:")
                    for col in self.data.columns:
                        df_type = str(self.data[col].dtype)
                        bq_type = column_types.get(col, "NOT IN SCHEMA")
                        if bq_type != "NOT IN SCHEMA" and col in self.pk:
                            self._logger.debug(
                                f"  PK {col}: DataFrame={df_type} -> BigQuery={bq_type}"
                            )

                self.data = self._convert_dataframe_to_bigquery_types(
                    self.data, column_types
                )

            # Clean datetime fields (fallback if no schema info)
            try:
                datetime_cols = self.data.select_dtypes(include=["datetime64"])
                if not datetime_cols.empty:
                    for col in datetime_cols.columns:
                        if col not in column_types:
                            self.data[col] = self.data[col].dt.tz_localize(None)
            except Exception as e:
                self._logger.warning(
                    f"CopyTo: Could not clean datetime fields: {e}"
                )

            # Detect JSON columns
            json_columns = set()
            if column_types:
                json_columns = {
                    col for col, dtype in column_types.items() if dtype == "JSON"
                }

            # --- Route to write strategy ---

            # MERGE strategy: atomic upsert via temp table + MERGE DML
            if self.use_merge and self.pk and not self.truncate:
                self._logger.info('CopyTo: Using MERGE strategy (atomic upsert)')
                await self._merge_dataframe(column_types, json_columns)
                return

            # DELETE+INSERT strategy: atomic via temp table + transaction
            if self.delete_before_insert and self.pk and not self.truncate:
                self._logger.info(
                    'CopyTo: Using transactional DELETE+INSERT strategy'
                )
                await self._delete_and_insert_safe(column_types, json_columns)
                return

            # Simple append (truncate already handled by CopyTo.run())
            if self._record_columns or json_columns:
                if json_columns:
                    self._logger.info(
                        f'CopyTo: Detected {len(json_columns)} JSON columns, '
                        'using NDJSON loader'
                    )
                await self._copy_with_json_loader(json_columns, column_types)
                return

            async with await self._connection.connection() as conn:
                result = await conn.write(
                    data=self.data,
                    table_id=self.tablename,
                    dataset_id=self.schema,
                    use_pandas=True,
                    if_exists="append"
                )
                self._logger.info(f'CopyTo: Write result: {result}')

                if self._debug:
                    count_q = f"SELECT COUNT(*) as count FROM `{self.schema}.{self.tablename}`"
                    count_result, count_error = await conn.query(count_q)
                    if count_result:
                        rows = list(count_result) if hasattr(count_result, '__iter__') else count_result
                        if rows and len(rows) > 0:
                            self._logger.debug(
                                f'CopyTo: Rows in table after INSERT: '
                                f'{rows[0].get("count", "unknown")}'
                            )
                    elif count_error:
                        self._logger.warning(
                            f'CopyTo: Error verifying row count: {count_error}'
                        )
        except StatementError as err:
            raise ComponentError(f"Statement error: {err}") from err
        except DataError as err:
            raise ComponentError(f"Data error: {err}") from err
        except Exception as err:
            raise ComponentError(f"{self.StepName} Error: {err!s}") from err

    async def _copy_iterable(self):
        """Copy an iterable to BigQuery."""
        try:
            async with await self._connection.connection() as conn:
                await conn.write(
                    data=self.data,
                    table_id=self.tablename,
                    dataset_id=self.schema,
                    use_pandas=False,
                    if_exists="append",
                    batch_size=self._chunksize
                )
        except Exception as err:
            raise ComponentError(
                f"Error copying iterable to BigQuery: {err}"
            ) from err
