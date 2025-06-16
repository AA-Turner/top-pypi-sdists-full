
"""
    Helper functions for working with Cosmic Frog models
"""

import os
import sys
import time
import uuid
import json
from typing import Dict, List, Optional, Tuple, Any
from contextlib import contextmanager
from io import StringIO
from collections.abc import Iterable
from pandas import DataFrame
from charset_normalizer import from_fp
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import text, inspect
from psycopg2 import sql
from psycopg2.errors import LockNotAvailable, DeadlockDetected
from .frog_platform import OptilogicClient
from .frog_log import get_logger
from .frog_notifications import ModelActivity, activity_signal
from .frog_activity_status import ActivityStatus
from .db_helpers import create_engine_with_retry
from .frog_utils import FrogUtils
from .frog_anura import AnuraSchema
from .frog_custom_tables_and_columns import CustomTablesAndColumns
from .frog_run_scenario import RunScenario, RunScenarioResponse, RESOURCE_SIZES, ENGINES, ModelRunOption
from .decorators import check_connection_type

# pylint: disable=logging-fstring-interpolation

# TODO:
# Profile parallel write for xlsx
# Add batching to standard table writing

# Define chunk size (number of rows to write per chunk)
CHUNK_SIZE = 1000000

# For key columns, replace Null with placeholder
# For matching on key columns only, will not be written to final table!
PLACEHOLDER_VALUE = ""  # replace with a value that does not appear in your data

CFLIB_IDLE_TRANSACTION_TIMEOUT = os.getenv("CFLIB_IDLE_TRANSACTION_TIMEOUT") or 1800
ATLAS_API_BASE_URL = os.getenv("ATLAS_API_BASE_URL", "https://api.optilogic.app/v0").strip("/")

# TODO:
# Delete a model destroys the connection? same goes for archive, ...
# can switch active model in between FrogModel class?
# After creating a model does that model become a model in class?

class FrogModel:
    """
    FrogModel class with helper functions for accessing Cosmic Frog models
    """

    # This allows app key to be set once for all instances, makes utilities easier to write
    class_app_key = None

    # Helper method for setting up app key
    @classmethod
    def __set_app_key__(
        cls,
        app_key: Optional[str],
        raise_if_not_found: Optional[bool] = True
    ) -> str:
        """
        Helper method for setting up app key.

        There are 4 ways to set the app key:
        1) Passed in argument when opening a model e.g. FrogModel(app_key="my_app_key", model_name="my_model")
        2) Set via class variable (used for all instances of FrogModel, used in utilities)
        3) Via Enviroment var, in Andromeda (if running in Andromeda)
        4) Via app.key file (when running locally, place file in folder with your script)

        Args:
            app_key: Optional app key

        Returns:
            App key
        
        """
        try:
            found_app_key = app_key or cls.class_app_key or os.environ.get("OPTILOGIC_JOB_APPKEY")

            if not found_app_key:
                initial_script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
                file_path = os.path.join(initial_script_dir, "app.key")
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as file:
                        found_app_key = file.read().strip()

            if not found_app_key and raise_if_not_found:
                raise ValueError("App key not found. Please provide a valid app key.")

            return found_app_key
        except Exception as e:
            # cls.log.exception(f"Error setting app key: {e}", exc_info=True)
            raise ValueError(f"Error setting app key: {e}")

    def __init__(
        self,
        model_name: Optional[str] = None,
        connection_string: Optional[str] = None,
        engine: Optional[sqlalchemy.engine.Engine] = None,
        application_name: str = "CosmicFrog User Library",
        app_key: Optional[str] = None,
        model_creation: bool = False,
    ) -> None:
        self.log = get_logger()
        self.model_name = model_name
        self.engine = None
        self.connection = None # Used for managing transactions
        self.transactions = []
        self.activity_signal = activity_signal
        self._app_key = self.__class__.__set_app_key__(app_key, raise_if_not_found=False)

        self.connection_type = None # "app_key", "engine", "connection_string"
        self.oc = None
        self.custom_tables_helper = None
        self.run_scenario_helper = None

        # Model connection can happen in 3 ways:
        # 1) A model name is supplied (required app key) - connection string will be fetched
        # 2) A pre-connected engine is supplied
        # 3) A model connection string is supplied


        if self._app_key and not self.model_name:
            raise ValueError("Model name has to be provided when app key is set")

        if model_name and not (connection_string or engine):
            self.oc = OptilogicClient(appkey=self._app_key)
            success, connection_string = self.oc.get_connection_string(model_name)

            if not success:
                raise ValueError(f"Cannot get connection string for frog model: {model_name}")

            self.engine = create_engine_with_retry(self.log, connection_string, application_name, model_creation=model_creation)
            self.custom_tables_helper = CustomTablesAndColumns(
                model_name=self.model_name,
                app_key=self._app_key,
                log=self.log
            )
            self.run_scenario_helper = RunScenario(frog_model=self)

            self.connection_type = "app_key"
        elif engine:
            self.engine = engine
            self.connection_type = "engine"
        elif connection_string:
            self.engine = create_engine_with_retry(self.log, connection_string, application_name)
            self.connection_type = "connection_string"

        # Identify Anura version
        self.anura_version = self.get_anura_version()

    def __enter__(self):
        self.start_transaction()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # No exceptions occurred, so commit the transaction
            self.commit_transaction()
        else:
            # An exception occurred, so roll back the transaction
            self.rollback_transaction()

    # Note: The following are for user managed transactions (do not use for library internal transactions)
    def start_transaction(self) -> None:
        """Start a new transaction."""
        if self.connection is None:
            self.connection = self.engine.connect()

        if self.transactions:
            self.transactions.append(self.connection.begin_nested())
        else:
            self.transactions.append(self.connection.begin())

    def commit_transaction(self) -> None:
        """Commit the outermost transaction."""
        if self.transactions:
            transaction = self.transactions.pop()
            transaction.commit()

            if not self.transactions:
                self.connection.close()
                self.connection = None

    def rollback_transaction(self) -> None:
        """Rollback the outermost transaction."""
        if self.transactions:
            transaction = self.transactions.pop()
            transaction.rollback()

            if not self.transactions:
                self.connection.close()
                self.connection = None

    @contextmanager
    def begin(self):
        """Context manager for model connections, used to manage both user and system transactions"""
        connection = None
        try:
            # Decide the context based on the transaction state
            if self.transactions:  # If user has opened a transaction, then nest one
                connection = self.transactions[-1].connection
                transaction = connection.begin_nested()
            else:  # else start a new one
                connection = self.engine.connect()
                transaction = connection.begin()

            # IMPORTANT DETAIL -> yields the connection, not the transaction
            yield connection

            transaction.commit()  # commit the transaction if everything goes well

        except LockNotAvailable:
            self.log.warning("Rolling back, unable to execute due to existing locks on model")
            transaction.rollback()

        except DeadlockDetected:
            self.log.warning("Rolling back, DEADLOCK was detected during operation on model")
            transaction.rollback()

        except Exception:
            self.log.exception(
                "Error, rolling back transaction due to exception",
                exc_info=True,
                stack_info=True,
            )
            transaction.rollback()
            raise
        finally:
            # If the connection was created in this method, close it.
            if not self.transactions:
                connection.close()

    def get_anura_version(self):
        """Return the current Anura schema version"""
        df = self.read_sql("SELECT current_schema()")
        return df.iloc[0, 0]

    def get_anura_master_table_mappings(self):
        """Return a dictionary of Anura table mappings"""
        return AnuraSchema.get_anura_master_table_mappings(self.anura_version)

    def get_tablelist(
        self,
        input_only: bool = False,
        output_only: bool = False,
        technology_filter: str = None,
        original_names: bool = False,
    ) -> List[str]:
        """Get a list of commonly used Anura tables, with various filtering options.

        Args:
        input_only:         Return only input tables
        output_only:        Return only output tables
        technology_filter:  Return tables matching technology (e.g. "NEO")
        original_names:     Return original (UI) names (e.g. "CustomerDemand" rather than "customerdemand")
        """
        assert not (input_only and output_only), "input_only and output_only cannot both be True"

        if technology_filter:
            filtered_data = [
                field
                for field in AnuraSchema.get_anura_masterlist(self.anura_version)
                if (
                    (technology_filter.upper() in field["Technology"].upper())
                    and (
                        (input_only and not field["Category"].startswith("Output"))
                        or (output_only and field["Category"].startswith("Output"))
                        or (not input_only and not output_only)
                    )
                )
            ]

            return [
                field["Table"].lower() if not original_names else field["Table"]
                for field in filtered_data
            ]

        lower_case = not original_names

        # Common un filtered cases
        if input_only:
            return AnuraSchema.get_anura_input_table_names(self.anura_version, lower_case)

        if output_only:
            return AnuraSchema.get_anura_output_table_names(self.anura_version, lower_case)

        return AnuraSchema.get_anura_table_names(self.anura_version, lower_case)

    def get_columns(self, table_name: str) -> List[str]:
        """List Anura columns for the given table

        Args:
        table_name: The target table to fetch columns for
        """

        lower_name = table_name.lower()

        return AnuraSchema.get_anura_columns(self.anura_version, lower_name)

    def get_key_columns(self, table_name: str) -> List[str]:
        """List Anura 'key' columns for the given table

        Args:
        table_name: The target table to fetch keys for
        """

        lower_name = table_name.lower()

        return AnuraSchema.get_anura_keys(self.anura_version, lower_name)

    # Dump data to a model table
    def write_table(
        self, table_name: str, data: pd.DataFrame | Iterable, overwrite: bool = False
    ) -> None:
        """Pushes data into a model table from a data frame or iterable object

        Args:
        table_name: The target table
        data:       The data to be written
        overwrite:  Set to true to overwrite current table contents
        """

        table_name = table_name.lower().strip()

        self.log.info("write_table, writing to: %s", table_name)

        # TODO: Should be under same transaction as the write
        if overwrite:
            self.clear_table(table_name)

        if isinstance(data, pd.DataFrame) is False:
            data = pd.DataFrame(data)

        data.columns = data.columns.astype(str).str.lower().map(str.strip)

        # Initial implementation - pull everything into a df and dump with to_sql
        with self.begin() as connection:
            data.to_sql(
                table_name,
                con=connection,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=CHUNK_SIZE,
            )

        # Note: tried a couple of ways to dump the generator rows directly, but didn't
        # give significant performance over dataframe (though may be better for memory)
        # Decided to leave as is for now

    def read_table(self, table_name: str, id_col: bool = False) -> DataFrame:
        """Read a single model table and return as a DataFrame

        Args:
            table_name: Table name to be read (supporting custom tables)
            id_col: Indicates whether the table id column should be returned

        Returns:
            Single dataframe holding table contents
        """

        table_name = table_name.lower().strip()

        with self.begin() as connection:
            result = pd.read_sql(table_name, con=connection)
            if "id" in result.columns and not id_col:
                result.drop(columns=["id"], inplace=True)
            return result

    # Read all, or multiple Anura tables
    def read_tables(
        self, table_list: List[str] = None, id_col: bool = False
    ) -> Dict[str, pd.DataFrame]:
        """Read multiple Anura tables and return as a dictionary, indexed by table name

        Args:
            table_list: List of table names to be read (supporting custom tables)
            id_col: Indicates whether the table id column should be returned

        Returns:
            Dictionary of tables, where key is table name and value is dataframe of contents
        """

        result = {}

        for t in table_list:
            result[t] = self.read_table(t, id_col=id_col)

        return result

    # Read all, or multiple Anura tables
    def write_tables(self, tables: Dict[str, pd.DataFrame], overwrite: bool = False) -> None:
        """Write multiple Anura tables from a dictionary, as returned by read_tables()

        Args:
            tables: Dictionary of table data indexed by table name
            overwrite: Set to true to overwrite current table contents

        """

        for key in tables:
            self.write_table(key, tables[key], overwrite)

    def clear_table(self, table_name: str, send_signal: bool = False):
        """Clear table of all content

        Args:
            table_name: Name of table to be cleared

        Returns:
            None
        """

        table_name = table_name.lower().strip()

        # delete any existing data data from the table
        self.exec_sql(f"TRUNCATE {table_name}")

        # Event send to FE for clearing table
        if self.connection_type == "app_key":
            try:
                if send_signal:
                    self.activity_signal(
                        self.log,
                        message={
                            "table": table_name,
                        },
                        signal_topic="CLEAR TABLE",
                        app_key=self._app_key,
                        model_name=self.model_name,
                    )
            except Exception as e:
                self.log.exception(f"Error sending signal to clear table: {e}", exc_info=True)


        return True

    # Read from model using raw sql query
    def read_sql(self, query: str, params: Optional[dict] = None) -> DataFrame:
        """
        Executes a sql query on the model and returns the results in a dataframe

        When using % in query string, use %% to escape
        
        Example:

        SELECT * FROM optimizationproductionsummary WHERE productname LIKE 'example_%%';

        Args:
            query: SQL query to be run

        Returns:
            Dataframe containing results of query
        """
        with self.begin() as connection:
            if params:
                # If params are provided, execute query with parameters
                return pd.read_sql_query(query, con=connection, params=params)
            # Backward compatibility: execute query without parameters
            return pd.read_sql_query(query, con=connection)

    # Execute raw sql on model
    def exec_sql(self, query: str | sql.Composed) -> None:
        """
        Executes a sql query on the model

        Args:
            query: SQL query to be run

        Returns:
            None
        """
        with self.begin() as connection:
            connection.execute(text(query))
    
    # Upsert from a csv file to a model table
    def upsert_csv(
        self,
        table_name: str,
        filename: str,
        _activity: ModelActivity = None,
        _correlation_id: str = "",
        overwrite: bool = False,
    ) -> Tuple[int, int]:
        total_updated = 0
        total_inserted = 0

        upsertResults = self.upsert_csv_ext(table_name, filename, _activity, _correlation_id, overwrite)

        if not upsertResults:
            return 0, 0
        
        # flatten data to comply with existing function calls
        for updated, inserted, _, _ in upsertResults:
            total_updated += updated
            total_inserted += inserted

        return total_updated, total_inserted

    # Upsert from a csv file to a model table
    def upsert_csv_ext(
        self,
        table_name: str,
        filename: str,
        _activity: ModelActivity = None,
        _correlation_id: str = "",
        overwrite: bool = False,
    ) -> List[Tuple[int, int, str, str]]:
        """
        Upsert a csv file to a Cosmic Frog model table

        If model is not connected via app key, custom tables and custom columns will not be supported

        Args:
            table_name: Name of the target Anura table
            filename: Name of csv file to be imported
            overwrite: Set to true to overwrite current table contents and perform insert only. Default is False

        Returns:
            Array(updated_rows, inserted_rows, error, table_name)
        """
        upsertResults = []
        self.log.info(f"uploading {filename} to {table_name} for model {self.model_name}")
        try:
            file_size = os.path.getsize(filename)

            if file_size <= 0:
                self.log.warning("CSV file has no rows")
                return [(0, 0, "CSV file has no rows", table_name)]

            with open(filename, "rb") as file_handle:
                # Read a small chunk to detect encoding
                detected = from_fp(file_handle, chunk_size=CHUNK_SIZE).best()
                detected_encoding = detected.encoding if detected else "utf-8"  # Default to UTF-8 if unsure

                # Reset file pointer
                file_handle.seek(0)

                batch_number = 0
                for chunk in pd.read_csv(
                    file_handle, chunksize=CHUNK_SIZE, dtype=str, skipinitialspace=True, encoding=detected_encoding
                ):

                    # Get the current file position in bytes
                    current_position = file_handle.tell()

                    chunk.replace("", np.nan, inplace=True)
                    updated, inserted, error = self.upsert_ext(
                        table_name,
                        chunk,
                        _correlation_id=_correlation_id,
                        activity=_activity,
                        overwrite=overwrite,
                        batch_number=batch_number,
                    )
                    upsertResults.append((updated, inserted, error, table_name))
                    batch_number += 1

                    if _activity:
                        # TODO: Support async here

                        progress_pct = (current_position / file_size) * 100

                        _activity.update_activity(
                            ActivityStatus.STARTED,
                            last_message=f"Uploading csv to {table_name}",
                            progress=int(progress_pct),
                        )

            return upsertResults
        except Exception as e:
            errorString = f"File upsert failed: {e}"
            self.log.exception(errorString, exc_info=True)
            if _activity:
                _activity.update_activity(
                    ActivityStatus.FAILED,
                    last_message=errorString,
                    progress=100,
                )

    # Upsert from an xls file to a model table
    def upsert_excel(
        self, filename: str, _activity: ModelActivity = None, _correlation_id: str = "", overwrite: bool = False,
    ) -> Tuple[int, int]:
        total_updated = 0
        total_inserted = 0

        upsertResults = self.upsert_excel_ext( filename, _activity, _correlation_id, overwrite)
        if not upsertResults:
            return 0, 0

        # flatten data to comply with existing function calls
        for updated, inserted, _, _ in upsertResults:
            total_updated += updated
            total_inserted += inserted

        return total_updated, total_inserted

    # Upsert from a excel file to a model table
    # returns a list of table names with errors and aggregated updated and inserted counts for tables without errors
    def upsert_excel_ext_agg(self, filename: str, _activity: ModelActivity = None, _correlation_id: str = "", overwrite: bool = False, ) -> List[Tuple[int, int, str, str]]:
        upsertResponse = []
        total_updated = 0
        total_inserted = 0

        upsertResults = self.upsert_excel_ext(filename, _activity, _correlation_id, overwrite)

        if not upsertResults:
            return [(0, 0, "", "")]
        
        # aggregate data for all records without errors
        for updated, inserted, error, table_name in upsertResults:
            if not error:
                total_updated += updated
                total_inserted += inserted
            else:
                upsertResponse.append((updated, inserted, error, table_name))

        # append aggregated data
        upsertResponse.append((total_updated, total_inserted, "", ""))

        return upsertResponse

    # Upsert from an xls file to a model table
    def upsert_excel_ext(
        self, filename: str, _activity: ModelActivity = None, _correlation_id: str = "", overwrite: bool = False,
    ) -> List[Tuple[int, int, str, str]]:
        """
        Upsert an xlsx file to a Cosmic Frog model table

        If model is not connected via app key, custom tables and custom columns will not be supported

        Args:
            table_name: Name of the target Anura table
            filename: Name of xlsx file to be imported
            overwrite: Set to true to overwrite current table contents and perform insert only. Default is False

        Returns:
            Array(updated_rows, inserted_rows, error, table_name)
        """

        # TODO: If an issue could consider another way to load/stream from xlsx maybe?

        upsertResults = []
        try:
            with pd.ExcelFile(filename) as xls:
                file_name_without_extension = (
                    os.path.basename(filename).replace(".xlsx", "").replace(".xls", "")
                )

                total_sheets = len(xls.sheet_names)

                if total_sheets == 0:
                    self.log.warning("Excel file has no sheets")
                    return [(0, 0, "Excel file has no sheets", "")]

                # For each sheet in the file
                for count, sheet_name in enumerate(xls.sheet_names):
                    if _activity:
                        progress_pct = (count / total_sheets) * 100

                        # TODO: Support async here
                        _activity.update_activity(
                            ActivityStatus.STARTED,
                            last_message=f"Uploading {sheet_name}",
                            progress=int(progress_pct),
                            tags=f"Upload, Upsert, {sheet_name}" # Hardcoded Upload, Upsert, should be as helper somewhere
                        )

                    table_to_upload = (
                        file_name_without_extension
                        if sheet_name[:5].lower() == "sheet"
                        else sheet_name
                    )

                    # Read the entire sheet into a DataFrame
                    # Note: For xlsx there is an upper limit of ~1million rows per sheet, so not chunking here

                    # TODO: Consider parallelism
                    df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)

                    # Check if there are columns in the file
                    if len(df.columns) == 0:
                        self.log.info("No columns in the file")
                        return [(0, 0, "No columns in the file", table_to_upload)]

                    df.columns = df.columns.str.lower().map(str.strip)

                    df.replace("", np.nan, inplace=True)

                    updated, inserted, error = self.upsert_ext(
                        table_to_upload,
                        df,
                        _correlation_id=_correlation_id,
                        activity=_activity,
                        overwrite=overwrite,
                    )
                    upsertResults.append((updated, inserted, error, table_to_upload))

            return upsertResults
        except Exception as e:
            self.log.exception(f"Error upserting xlsx to model: {e}", exc_info=True)
            if _activity:
                _activity.update_activity(
                    ActivityStatus.FAILED,
                    last_message="File upsert failed",
                    progress=100,
                )

    def get_table_columns_from_model(self, table_name: str, id_col: bool = False) -> List[str]:
        """
        Fetches all columns direct from database (including custom)

        This gets all actual columns in the model table, including user custom columns
        """
        table_name = table_name.lower().strip()

        # Create an Inspector object
        inspector = inspect(self.engine)

        # Get the column names for a specific table
        column_names = inspector.get_columns(table_name)

        column_names = [column["name"] for column in column_names]

        if not id_col:
            column_names.remove("id")

        return [name.lower().strip() for name in column_names]

    def _get_combined_key_columns_for_upsert(self, table_name: str, is_anura_table=False):
        """"
        Get combined key columns for upsert

        If connection is via app key, custom columns will be included

        Args:
            table_name: Name of the target table
            is_anura_table: Indicates if the table is an Anura table

        Returns:
            List of combined key columns

        """
        pk_custom_columns = []
        if self.connection_type == "app_key" and self.custom_tables_helper:
            pk_custom_columns = self.custom_tables_helper.get_pk_custom_columns(table_name)

        self.log.info(f"Custom Column PKs: {pk_custom_columns}")
        if is_anura_table:
            # for anura tables: anura PK + notes + custom PKs
            anura_keys = AnuraSchema.get_anura_keys(self.anura_version, table_name)

            custom_key_columns = ["notes"]

            return anura_keys + custom_key_columns + pk_custom_columns
        else:
            # custom tables only custom PKs
            return pk_custom_columns

    def __generate_index_sql(self, index_name, table_name, key_column_list) -> str:
        """
        Creates an appropriate index for Anura tables.
        Coalesce is used to support
        """
        coalesced_columns = ", ".join(
            [f"COALESCE({column}, '{PLACEHOLDER_VALUE}')" for column in key_column_list]
        )

        return f"CREATE INDEX {index_name} ON {table_name}({coalesced_columns});"

    def _create_upsert_index_for_table(
        self, table_name: str, cursor, combined_key_columns=None, is_anura_table=False
    ) -> str:
        """
        Creates an index to aid update/insert performance for upsert
        """

        if combined_key_columns is None:
            combined_key_columns = self._get_combined_key_columns_for_upsert(
                table_name, is_anura_table
            )

        upsert_index_name = "cf_upsert_index_" + str(uuid.uuid4()).replace("-", "")
        index_sql = self.__generate_index_sql(upsert_index_name, table_name, combined_key_columns)

        start_time = time.time()
        cursor.execute(index_sql)
        end_time = time.time()
        self.log.info(
            f"Index creation took {end_time - start_time} seconds for {table_name}",
        )

        return upsert_index_name

    def upsert(
        self,
        table_name: str,
        data: pd.DataFrame,
        _correlation_id: str = "",  # Optional: correlation id for logging / tracing (for internal use)
        activity: ModelActivity = None,  # Optional: activity object for progress updates
        overwrite: bool = False, # Optional: clean table and then perform insert only
    ) -> Tuple[int, int]:
        total_updated, total_inserted, _  = self.upsert_ext( table_name, data, _correlation_id, activity, overwrite )
        return total_updated, total_inserted

    def upsert_ext(
        self,
        table_name: str,
        data: pd.DataFrame,
        _correlation_id: str = "",  # Optional: correlation id for logging / tracing (for internal use)
        activity: ModelActivity = None,  # Optional: activity object for progress updates
        overwrite: bool = False, # Optional: clean table and then perform insert only
        batch_number: int = 0, # Optional: for batched calls
    ) -> Tuple[int, int, str]:
        """
        Upsert a pandas dataframe to a Cosmic Frog model table

        Args:
            table_name: Name of the target Anura table (Input or Custom table)
            data: A Pandas dataframe containing the data to upsert

        Returns:
            updated_rows, inserted_rows
        """

        if len(data) <= 0:
            self.log.warning("Aborting upsert. Input dataframe is empty: %s", table_name)
            return 0, 0, "Input dataframe is empty"
        
        table_name = table_name.strip().lower()

        data.columns = data.columns.str.lower().map(str.strip)

        anura_tables = self.get_tablelist(input_only=True)
        anura_abbreviated_names = AnuraSchema.get_anura_abreviated_table_names(self.anura_version, True)

        is_anura_table = any(s.lower() == table_name for s in anura_tables)
        is_custom_table = False

        # Check if abbreviated anura table name if table name not found in anura tables
        if not is_anura_table and table_name in anura_abbreviated_names.keys():
            table_name = anura_abbreviated_names[table_name]
            is_anura_table = True

        # If table name still not found check custom tables
        if not is_anura_table:
            custom_tables = []
            if self.connection_type == "app_key" and self.custom_tables_helper:
                custom_tables = self.custom_tables_helper.get_custom_tables()
            else:
                self.log.warning("Custom tables not supported for this connection type")
                return 0,0, "Custom tables not supported for this connection type"

            is_custom_table = any(s.lower() == table_name for s in custom_tables)

            # if not recognised as custom table check if maybe shortened custom table
            if not is_custom_table and len(table_name) == 32:
                custom_table_abbr = [s[:32].lower() for s in custom_tables]
                if table_name in custom_table_abbr:
                    is_custom_table = True

        # if not found in anura tables, abbreviated names, custom tables or abbreviated custom tables return
        if not is_anura_table and not is_custom_table:
            # Skip it
            self.log.warning(
                "Table name not recognised as an Anura, Abbreviated name or Custom table. Input tables supported only. (skipping): %s",
                table_name,
            )
            return 0, 0, "Table name not recognised as an Anura, Abbreviated name or Custom table."

        self.log.info("Importing to table: %s", table_name)
        self.log.info("Source data has %s rows", len(data))

        # Behavior rules:
        # Key columns - get used to match (Note: possible future requirement, some custom columns may also be key columns)
        # Other Anura columns - get updated
        # Other Custom columns - get updated
        # Other columns (neither Anura or Custom) - get ignored

        all_column_names = self.get_table_columns_from_model(table_name)
        if "id" in all_column_names:
            all_column_names.remove("id")

        # 1) Anura key cols - defined in Anura
        # 2) Custom key cols - Coming from Platform APIs
        # 3) Update cols - The rest

        combined_key_columns = self._get_combined_key_columns_for_upsert(table_name, is_anura_table)
        # Skip Key columns that are not in present in input data
        combined_key_columns = [col for col in combined_key_columns if col in data.columns]

        #  Skip update columns that are not present in the input data
        update_columns = [col for col in all_column_names if col not in combined_key_columns]
        update_columns = [col for col in update_columns if col in data.columns.tolist()]
        
        # All checks have been made, early return and import only if its overwrite
        self.log.info("Checking if table should be overwritten: %s", overwrite)
        if overwrite:
            self.log.info("Overwriting table: %s", table_name)
            if batch_number == 0:
                # clear tables only for first batch
                self.clear_table(table_name, True)
                self.log.info("Table cleared: %s", table_name)
            return self._insert_only(table_name, data, _correlation_id, combined_key_columns, all_column_names, activity)

        # if there are no update columns, just perform an insert
        if len(update_columns) == 0:
            self.log.info("No columns to update, proceeding with insert.")
            return self._insert_only(table_name, data, _correlation_id, combined_key_columns, all_column_names, activity)

        # Skipping unrecognised columns (Do not trust column names from user data)
        cols_to_drop = [col for col in data.columns if col not in all_column_names]

        for col in cols_to_drop:
            self.log.info("Skipping unknown column in %s: %s", table_name, col)

        data = data.drop(cols_to_drop, axis=1)

        before_rows = len(data)

        if len(combined_key_columns) > 0:
            data = data.drop_duplicates(combined_key_columns)

        after_rows = len(data)
        if after_rows < before_rows:
            self.log.info(
                f"Cannot upsert duplicate rows: Removed {before_rows - after_rows} duplicates from upsert input data"
            )

        # Sometimes no columns match up (including for malformed
        # xlsx files saved in 3rd party tools)
        if len(data.columns) == 0:
            self.log.warning("No columns to import")
            return 0, 0, "No columns to import"

        updated_rows = 0
        inserted_rows = 0

        # Want to either make a transaction, or a nested transaction depending on the
        # presence or absence of a user transaction (if one exists then nest another,
        # else create a root)
        with self.begin() as connection:

            # Create temporary table
            temp_table_name = "temp_table_" + str(uuid.uuid4()).replace("-", "")
            self.log.info("Moving data to temporary table: %s", temp_table_name)

            # Note: this will also clone custom columns
            create_temp_table_sql = f"""
                /* {_correlation_id} cflib.upsert */
                CREATE TEMPORARY TABLE {temp_table_name} AS
                SELECT *
                FROM {table_name}
                WITH NO DATA;
                """

            connection.execute(text(create_temp_table_sql))

            # Copy data from df to temporary table
            copy_sql = sql.SQL(
                "COPY {table} ({fields}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
            ).format(
                table=sql.Identifier(temp_table_name),
                fields=sql.SQL(", ").join(map(sql.Identifier, data.columns)),
            )

            # For key columns (only) convert to a placeholder value
            for column in combined_key_columns:
                if column in data.columns:
                    data[column] = data[column].fillna(PLACEHOLDER_VALUE)

            with connection.connection.cursor() as cursor:
                start_time = time.time()
                cursor.copy_expert(copy_sql, StringIO(data.to_csv(index=False)))
                self.log.info(
                    f"Copy data to {temp_table_name} took {time.time() - start_time} seconds"
                )
                del data

                # Now upsert from temporary table to final table

                # Note: Looked at ON CONFLICT for upsert here, but not possible without
                # defining constraints on target table so doing insert and update separately

                all_columns_list = ", ".join([f'"{col_name}"' for col_name in all_column_names])

                if combined_key_columns:
                    update_column_list = ", ".join(
                        [
                            f'"{col_name}" = "{temp_table_name}"."{col_name}"'
                            for col_name in update_columns
                        ]
                    )
                    key_condition = " AND ".join(
                        [
                            f'COALESCE("{table_name}"."{key_col}", \'{PLACEHOLDER_VALUE}\') = COALESCE("{temp_table_name}"."{key_col}", \'{PLACEHOLDER_VALUE}\')'
                            for key_col in combined_key_columns
                        ]
                    )

                    cursor.execute(
                        f"SET idle_in_transaction_session_timeout = '{CFLIB_IDLE_TRANSACTION_TIMEOUT}s';"
                    )  # Idle transaction timeout in seconds

                    # Pre-locking is used here to prevent collision with other table usage or multiple upserts
                    # Will fail fast (exception) if all locks cannot be obtained
                    lock_query = f"""
                        /* {_correlation_id} cflib.upsert.lock */
                        SELECT 1
                        FROM {table_name}
                        FOR UPDATE NOWAIT;
                    """
                    start_time = time.time()
                    cursor.execute(lock_query)
                    updated_rows = cursor.rowcount
                    self.log.info(
                        f"Locking query took {time.time() - start_time} seconds for {table_name}"
                    )

                    # TODO: Indexing is based on the key columns required - this varies per upsert in some cases, due to
                    # allowing custom columns to be part of the index
                    _upsert_index_name = self._create_upsert_index_for_table(
                        table_name, cursor, combined_key_columns, is_anura_table
                    )

                    # Update rows in the table that match the input data
                    update_query = f"""
                        /* {_correlation_id} cflib.upsert.update */
                        UPDATE {table_name}
                        SET {update_column_list}
                        FROM {temp_table_name}
                        WHERE {key_condition};
                    """

                    start_time = time.time()
                    cursor.execute(update_query)
                    updated_rows = cursor.rowcount
                    self.log.info(
                        f"Updated {updated_rows} rows in {table_name} in {time.time() - start_time} seconds"
                    )

                    # Remove rows that matched from temp table (safest approach in presence of duplicates in target)
                    delete_query = f"""
                        /* {_correlation_id} cflib.upsert.delete */
                        DELETE FROM {temp_table_name}
                        USING {table_name}
                        WHERE {key_condition}
                    """

                    start_time = time.time()
                    cursor.execute(delete_query)
                    deleted_rows = cursor.rowcount
                    self.log.info(
                        f"Deleted {deleted_rows} rows in {time.time() - start_time} seconds for temp_table"
                    )

                    temp_columns_list = ", ".join(
                        [f'"{temp_table_name}"."{col_name}"' for col_name in all_column_names]
                    )

                    insert_query = f"""
                        /* {_correlation_id} cflib.upsert.insert */
                        INSERT INTO {table_name} ({all_columns_list})
                        SELECT {temp_columns_list}
                        FROM {temp_table_name}
                    """

                    start_time = time.time()
                    cursor.execute(insert_query)
                    inserted_rows = cursor.rowcount
                    self.log.info(
                        f"Inserted {inserted_rows} into {table_name} in {time.time() - start_time} seconds"
                    )

                    # Finally remove the index created for upsert
                    cursor.execute(f"DROP INDEX IF EXISTS {_upsert_index_name};")

                # If no key columns, then just insert
                else:
                    insert_query = f"""
                        /* {_correlation_id} cflib.upsert.insert_only */
                        INSERT INTO {table_name} ({all_columns_list})
                        SELECT {all_columns_list}
                        FROM {temp_table_name}
                    """

                    updated_rows = 0
                    self.log.info(f"Running insert query for {table_name}")
                    cursor.execute(insert_query)
                    inserted_rows = cursor.rowcount

                self.log.info("Updated rows  = %s for %s", updated_rows, table_name)
                self.log.info("Inserted rows = %s for %s", inserted_rows, table_name)

        # fire event for updating count in tables on UI
        # event moved here as then it works with abbreviated names
        if activity:
            insert_message = f"TABLE INSERT {table_name} {inserted_rows} {self.model_name}"
            self.log.debug(f"Signalling: {insert_message}")
            activity_signal(
                self.log,
                message={
                    "table": table_name,
                    "count": inserted_rows,
                },
                signal_topic="TABLE INSERT",
                app_key=self._app_key,
                model_name=self.model_name,
                correlation_id=_correlation_id,
            )

        return updated_rows, inserted_rows, ""

    # Consider optimising this, as there is no need for temp tables on insert only
    # Ideas:
    # 1) Use binary format with copy command
    # 2) bypass temp table usage
    # 3) parallelize import in batches?
    def _insert_only(self, table_name, data, _correlation_id, combined_key_columns, all_column_names, activity):
        try:
            with self.begin() as connection:
                temp_table_name = "temp_table_" + str(uuid.uuid4()).replace("-", "")
                self.log.info("Moving data to temporary table: %s", temp_table_name)

                create_temp_table_sql = f"""
                    /* {_correlation_id} cflib.insert */
                    CREATE TEMPORARY TABLE {temp_table_name} AS
                    SELECT *
                    FROM {table_name}
                    WITH NO DATA;
                    """

                connection.execute(text(create_temp_table_sql))

                copy_sql = sql.SQL(
                    "COPY {table} ({fields}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
                ).format(
                    table=sql.Identifier(temp_table_name),
                    fields=sql.SQL(", ").join(map(sql.Identifier, data.columns)),
                )

                for column in combined_key_columns:
                    if column in data.columns:
                        data[column] = data[column].fillna(PLACEHOLDER_VALUE)

                with connection.connection.cursor() as cursor:
                    start_time = time.time()
                    cursor.copy_expert(copy_sql, StringIO(data.to_csv(index=False)))
                    self.log.info(
                        f"Copy data to {temp_table_name} took {time.time() - start_time} seconds"
                    )
                    del data

                    all_columns_list = ", ".join([f'"{col_name}"' for col_name in all_column_names])

                    insert_query = f"""
                        /* {_correlation_id} cflib.insert_only */
                        INSERT INTO {table_name} ({all_columns_list})
                        SELECT {all_columns_list}
                        FROM {temp_table_name}
                    """

                    self.log.info(f"Running insert query for {table_name}")
                    cursor.execute(insert_query)
                    inserted_rows = cursor.rowcount

                    self.log.info("Inserted rows = %s for %s", inserted_rows, table_name)
        except Exception as e:
            return 0, 0, str(e)
        
        if activity:
            insert_message = f"TABLE INSERT {table_name} {inserted_rows} {self.model_name}"
            self.log.debug(f"Signalling: {insert_message}")
            activity_signal(
                self.log,
                message={
                    "table": table_name,
                    "count": inserted_rows,
                },
                signal_topic="TABLE INSERT",
                app_key=self._app_key,
                model_name=self.model_name,
                correlation_id=_correlation_id,
            )

        return 0, inserted_rows, ""


    ### START Custom Table & Custom Columns API: ###
    @check_connection_type("app_key")
    def create_table(self, table_name: str) -> Dict[str, str]:
        """
        Create a custom table in the model

        Args:
            table_name: str -- Name of the table to create

        Returns:
            dict: A dictionary containing 'status' and 'message'.
        """
        return self.custom_tables_helper.create_table(table_name)

    @check_connection_type("app_key")
    def rename_table(self, table_name: str, new_table_name: str) -> Dict[str, str]:
        """
        Rename a custom table in the model

        Args:
            table_name: str -- Name of the table to rename
            new_table_name: str -- New name for the table
        
        Returns:
            dict: A dictionary containing 'status' and 'message'.
        """
        return self.custom_tables_helper.rename_table(table_name, new_table_name)

    @check_connection_type("app_key")
    def delete_table(self, table_name: str) -> Dict[str, str]:
        """
        Delete a custom table in the model

        Args:
            table_name: str -- Name of the table to delete
        
        Returns:
            dict: A dictionary containing 'status' and 'message'.
        """
        return self.custom_tables_helper.delete_table(table_name)

    @check_connection_type("app_key")
    def get_all_custom_tables(self) -> List[str]:
        """
        Get all custom tables in the model

        Returns:
            list: A list of custom table names.
        """
        return self.custom_tables_helper.get_custom_tables()

    @check_connection_type("app_key")
    def get_all_custom_columns(self, table_name: str) -> Dict[str, str]:
        """
        Get all custom columns for a certain table

        Args:
            table_name: str -- Name of the table to get custom columns for

        Returns:
            dict: A dictionary containing 'status' and 'message'.
        """
        return self.custom_tables_helper.get_all_custom_columns(table_name)

    @check_connection_type("app_key")
    def create_custom_column(self, table_name: str, column_name: str, data_type: str = "text", key_column: bool = False, pseudo: bool = True) -> Dict[str, str]:
        """
        Create a custom column in a custom table

        Args:
            table_name: str -- Name of the table to create the column in
            column_name: str -- Name of the column to create
            data_type: str -- Data type of the column (e.g. text, integer, float, date, boolean)
            key_column: bool -- Will be included as part of the unique record identification when importing (updating, inserting) data to the table
            pseudo: bool -- Data of any type can be freely imported and will behave as the defined data type in UI (Grids, Maps, Dashboards)

        Returns:
            dict: A dictionary containing 'status' and 'message'.
        """
        return self.custom_tables_helper.create_custom_column(table_name, column_name, data_type, key_column, pseudo)


    @check_connection_type("app_key")
    def bulk_create_custom_columns(self, columns: List[Dict[str, str]]) -> Dict[str, str]:
        """
        Bulk create custom columns.

        Each column should be a dictionary with the following keys:
            - table_name: str
            - column_name: str
            - data_type: str (Optional) - Default is 'text'
            - key_column: bool (Optional) - Default is False
            - pseudo: bool (Optional) - Default is True

        Example Args:
            columns = [
                {
                    "table_name": "Facilities",
                    "column_name": "Custom1",
                    "data_type": "integer",
                },
                {
                    "table_name": "Facilities",
                    "column_name": "Custom2"
                },
                {
                    "table_name": "Customers",
                    "column_name": "Custom3",
                }
            ]

        Args:
            columns: list -- List of columns to create
        
        Returns:
            dict: A dictionary containing 'status', 'message', 'added', 'skipped', and 'errors'.
        """
        return self.custom_tables_helper.bulk_create_custom_columns(columns)


    @check_connection_type("app_key")
    def delete_custom_column(self, table_name: str, column_name: str) -> Dict[str, str]:
        """
        Delete a custom column in a custom table

        Args:
            table_name: str -- Name of the table to delete the column from
            column_name: str -- Name of the column to delete
        
        Returns:
            dict: A dictionary containing 'status' and 'message'.
        """
        return self.custom_tables_helper.delete_custom_column(table_name, column_name)

    @check_connection_type("app_key")
    def edit_custom_column(self, table_name: str, column_name: str, new_column_name: str = None, data_type: str = None, key_column: bool = None) -> Dict[str, str]:
        """
        Edit a custom column in a custom table

        Args:
            table_name: str -- Name of the table to edit the column in
            column_name: str -- Name of the column to edit
            new_column_name: str -- New name of the column
            data_type: str -- New data type of the column (e.g. text, integer, float, date, boolean)
            key_column: bool -- Will be included as part of the unique record identification when importing (updating, inserting) data to the table
            pseudo: bool -- Data of any type can be freely imported and will behave as the defined data type in UI (Grids, Maps, Dashboards)

        Returns:
            dict: A dictionary containing 'status' and 'message'.
        """
        return self.custom_tables_helper.edit_custom_column(table_name, column_name, new_column_name, data_type, key_column)

    ### END Custom Table & Custom Columns API ###

    ### START Run Scenario API: ###

    @check_connection_type("app_key")
    def run_scenario(
        self,
        scenarios: [str] = ["Baseline"],
        workspace: str = "Studio",
        engine: None | ENGINES = None,
        run_neo_with_infeasibility: bool = False,
        resource_size: RESOURCE_SIZES = "s",
        tags: str = "",
        version: str = "",
        fire_and_forget: bool = False,
        _correlation_id: str = None,
        check_configuration_before_run: bool = False
    ) -> RunScenarioResponse:
        """
        Run scenarios within a model.
        Can run all scenarios in a model by passing ["All"].
        If scenario names are not passed, will run the Baseline scenario (default).
        Scenario names are case sensitive.

        If engine is not passed, will run on the default
        engine from the scenario table (technology column).
        If technology is not set in the scenario table, will default to "neo".
        If technology is set to unknown value, will return an error.

        By default function will run the scenario on resource size S, which can be
        changed by passing resource_size parameter.

        By default function will await all of the scenarios to complete. Pass
        `fire_and_forget=True` to run in the background.

        If not sure about configuration before running, pass
        `check_configuration_before_run=True` to return the final config
        without actually running anything.

        If running with infeasibility check, set run_neo_with_infeasibility=True;
        engine parameter will be ignored and set to "neo".

        Args:
            scenarios (list[str]): Name(s) of the scenario(s) to run. Default ["Baseline"]
            workspace (str): Workspace to run the scenario in - Default "Studio"
            engine (str | None): Engine(s) to run on - Default is derived from scenario table
            run_neo_with_infeasibility (bool): If True, forcibly run "neo" with infeasibility check
            resource_size (str): Resource size to run the scenario on - default "s"
            tags (str): Tags to run the scenario with
            version (str): Version of the sovler to run
            fire_and_forget (bool): If True, do not monitor the job. Default False
            _correlation_id (str | None): Correlation ID for logs/tracing. If None, auto-generated
            check_configuration_before_run (bool): If True, only return the config, do not run anything.

        Returns:
            RunScenarioResponse: a dict describing success/failure status, job keys, etc.
        """

        return self.run_scenario_helper.run(
            scenarios=scenarios,
            workspace=workspace,
            engine=engine,
            run_neo_with_infeasibility=run_neo_with_infeasibility,
            resource_size=resource_size,
            tags=tags,
            version=version,
            fire_and_forget=fire_and_forget,
            _correlation_id=_correlation_id,
            check_configuration_before_run=check_configuration_before_run
        )


    @check_connection_type("app_key")
    def run_multiple_scenarios_with_custom_configuration(
        self,
        scenarios_with_custom_configuration: list[dict],
        workspace: str = "Studio",
        fire_and_forget: bool = False,
        _correlation_id: str = None,
    ) -> RunScenarioResponse:
        """
            Run multiple scenarios with different configurations.

            Args:
                scenarios_with_custom_configuration (list[dict]): List of dictionaries containing scenario name, engine, and resource size
                                                                 {scenario_name: str, engine: str, resource_size: str}
                workspace (str): Workspace to run the scenario in - Default "Studio"
                fire_and_forget (bool): If True, do not monitor the job. Default False
            
            Returns:
                RunScenarioResponse: a dict describing success/failure status, job keys, etc.
        """
        return self.run_scenario_helper.run_multiple_scenarios_with_custom_configuration(
            scenarios_with_custom_configuration, workspace, fire_and_forget, _correlation_id
        )

    @check_connection_type("app_key")
    def stop_scenario(
        self, scenario_name: Optional[str] = '', job_key: Optional[str] = '', workspace: str = "Studio"
    ) -> Dict[str, str]:
        """
        Stop a running scenario. Scenario name or job key is required. Scenario name is case sensitive. Will stop multiple jobs if multiple jobs are running with the same scenario name.

        Args:
            scenario_name: str -- Name of the scenario to stop
            job_key: str -- Key of the job to stop
            workspace: str -- Workspace where the scenario is running - Default Studio
        
        Returns:
            dict: A dictionary containing 'status' and 'message

        """
        return self.run_scenario_helper.stop_scenario(scenario_name, job_key, workspace)


    @check_connection_type("app_key")
    def check_scenario_status(
        self,
        scenario_name: Optional[str] = '',
        job_key: Optional[str]= '',
        history: str = '7',
        workspace: str = "Studio"
    ) -> Dict[str, str]:
        """
        Check the status of a running scenario. Scenario name or job key is required. Scenario name is case sensitive.

        For scenario name it will return statusCounts for all jobs with the scenario name. Example:

        "data": {
            "submitted": 1,
            "starting": 2,
            "started": 3,
            "running": 4,
            "done": 5,
            "stopping": 6,
            "stopped": 7,
            "canceling": 8,
            "cancelled": 9,
            "error": 10
        }

        Args:
            scenario_name: str -- Name of the scenario to check
            job_key: str -- Key of the job to check
            history: str -- Number of days to check the history for (default: 7). For all history, use all
            workspace: str -- Workspace where the scenario is running - Default Studio
        
        Returns:
            dict: A dictionary containing 'status' and 'message'. When using scenario name, it will also contain 'statusCounts' and 'jobs'
        """

        return self.run_scenario_helper.check_scenario_status(
            scenario_name, job_key, history, workspace
        )

    @check_connection_type("app_key")
    def get_job_logs(self, job_key: str, workspace: str = "Studio") -> Dict[str, str]:
        """
        Get the logs of a job. Used for finished jobs.

        Args:
            job_key: str -- The key of the job
            workspace: str -- The workspace of the job
        
        Returns:
            dict: A dictionary containing the status, message, and logs
        """
        return self.run_scenario_helper.get_job_logs(job_key, workspace)


    @check_connection_type("app_key")
    def all_scenarios_preview(self) -> dict:
        """
        Get all scenarios in the model

        Returns:
            dict: A dictionary containing the status, message, and data
        """
        return self.run_scenario_helper.all_scenarios_preview()


    @check_connection_type("app_key")
    def job_records(
        self, job_key: str, workspace: str = "Studio", _correlation_id: str = "", keys: Optional[str] = None
    ) -> dict:
        """
        Fetch the job records for a job.
        Will return all records if keys are not specified.
        Works when job is running.

        Args:
            job_key: str -- Key of the job
            workspace: str -- Workspace where the job is running - Default Studio
            _correlation_id: str -- Correlation id for logging / tracing (for internal use)
            keys: str -- Keys of the records to fetch

        Returns:
            dict: A dictionary containing the status, message, and records
        """
        return self.run_scenario_helper.job_records(job_key, workspace, _correlation_id, keys)


    @check_connection_type("app_key")
    def get_all_jobs_for_solver_job(
        self, job_key: str, workspace: str = "Studio", _correlation_id: str = ""
    ) -> dict:
        """
        Fetch all job records for a solver job.
        Works when job is running.

        Args:
            job_key: str -- Key of the job
            workspace: str -- Workspace where the job is running - Default Studio
            _correlation_id: str -- Correlation id for logging / tracing (for internal use)

        Returns:
            dict: A dictionary containing the status, message, and records
        """
        return self.run_scenario_helper.get_all_jobs_for_solver_job(job_key, workspace, _correlation_id)


    @check_connection_type("app_key")
    def tail_job_records(
        self, job_key: str, workspace: str = "Studio", _correlation_id: str = ""
    ) -> dict:
        """
            Tail the job records for a job.
            If job is running, will tail the logs until the job is completed.
            If job is completed, will print all of the records

            Args:
                job_key: str -- Key of the job
                workspace: str -- Workspace where the job is running - Default Studio
                _correlation_id: str -- Correlation id for logging / tracing (for internal use)
            Returns:
                dict: A dictionary containing the status, message, and records
        """
        return self.run_scenario_helper.tail_job_records(job_key, workspace, _correlation_id)


    @check_connection_type("app_key")
    def get_scenario_run_error_log(
        self, job_key: str, workspace: str = "Studio", _correlation_id: str = ""
    ) -> dict:
        """
        Fetch the error logs for a job.

        Args:
            job_key: str -- Key of the job
            workspace: str -- Workspace where the job is running - Default Studio
            _correlation_id: str -- Correlation id for logging / tracing (for internal use)
        
        Returns:
            dict: A dictionary containing the status, message, and error logs
        """

        return self.run_scenario_helper.get_scenario_run_error_log(job_key, workspace, _correlation_id)

    @check_connection_type("app_key")
    def all_running_scenarios(self, workspace: str = "Studio", _correlation_id: str = "") -> dict:
        """"
        Fetch all running scenarios in a workspace.

        Args:
            workspace: str -- Workspace to fetch the running scenarios from - Default Studio
            _correlation_id: str -- Correlation id for logging / tracing (for internal use)

        Returns:
            dict: A dictionary containing the status, message and jobs
        """
        return self.run_scenario_helper.all_running_scenarios(workspace, _correlation_id)

    ### END Run Scenario API ###

    ### START Model Run Options API: ###
    @check_connection_type("app_key")
    def get_all_run_parameters(self, engine: Optional[str] = '', _correlation_id = None) -> dict:
        """
        Get the model run options

        Returns:
            dict: A dictionary containing the model run options
        """
        return self.run_scenario_helper.get_all_run_parameters(
            engine,
            _correlation_id
        )

    @check_connection_type("app_key")
    def add_run_parameter(self, model_run_option: ModelRunOption, _correlation_id = None) -> dict:
        """
        Add a model run option

        Args:
            model_run_option: ModelRunOption -- The model run option to add
                option: str - The name of the run parameter
                status: str - The status of the run parameter, default: Include. Options: Include, Exclude. If Exclude, the run parameter will not be used in the scenario run and not be shown in the UI
                value: str - The value of the run parameter, default: "", has to follow the datatype rules
                technology: str - The technology of the run parameter, default: neo. Options: neo, neo_with_infeasibility, throg, triad, dendro, hopper, dart
                description: str - The description of the run parameter, default: ""
                datatype: str - The datatype of the run parameter, default: String. Options: String, int, double, [True, False], [custom1, custom2]
                uidisplaycategory: str - The UI display category of the run parameter, default: Basic. Options: Basic, Advanced. Basic means it will be shown in the CF UI
                uidisplayname: str - The CF UI display name of the run parameter, default: option. If not set, it will be the same as the option if not provided
                uidisplayorder: int - The order of the run parameter in the CF UI, default: highest order + 1, cannot be the same as another run parameter

        Returns:
            dict: A dictionary containing the status and message
        """
        return self.run_scenario_helper.add_run_parameter(
            model_run_option,
            _correlation_id
        )

    @check_connection_type("app_key")
    def update_run_parameter_value(self, option: str, value: str, _correlation_id = None) -> dict:
        """
        Update the value of a model run option

        Args:
            option: str -- The name of the run parameter
            value: str -- The new value of the run parameter

        Returns:
            dict: A dictionary containing the status and message
        """
        return self.run_scenario_helper.update_run_parameter_value(
            option,
            value,
            _correlation_id
        )

    @check_connection_type("app_key")
    def delete_run_parameter(self, option: str, _correlation_id = None) -> dict:
        """
        Delete a model run option

        Args:
            option: str -- The name of the run parameter

        Returns:
            dict: A dictionary containing the status and message
        """
        return self.run_scenario_helper.delete_run_parameter(
            option,
            _correlation_id
        )
    ### END Model Run Options API ###

    ### START Model Methods API: ###
    @staticmethod
    def all_models(app_key: Optional[str] = None) -> dict:
        """
        Get all models
        To get all archived models, use the archived_models method

        Args:
            app_key: Optional[str] -- The app key

        Returns:
            dict: A dictionary containing the status, message, and data
        """

        try:
            resolved_app_key = FrogModel.__set_app_key__(app_key)
            oc = OptilogicClient(appkey=resolved_app_key)
            all_models = oc.api.databases()
            return {"status": "success", "message": "Models fetched successfully", "data": all_models}
        except ValueError as ve:
            return {"status": "error", "message": str(ve)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def create_model(
        name: str,
        desc: Optional[str] = None,
        template: str = 'anura_clean',
        backups: bool = True,
        labels: Optional[Dict[str, Any]] = None,
        tags: Optional[str] = None,
        # schema_status: Optional[
        #     Literal[
        #         'legacy',
        #         'stable',
        #     ]
        # ] = None,
        template_id: Optional[float] = None,
        app_key: Optional[str] = None,
    ) -> dict:
        """
        Create a model. If the model is created successfully,
        a FrogModel object is returned, else a dictionary containing
        the status and message is returned.

        Args:
            name: str -- Name of the model
            desc: Optional[str] -- Description of the model
            template: str -- Template to use for the model (use FrogModel.all_available_model_templates to get available templates), default: anura_clean which is empty model
            backups: bool -- Enable backups for the model, default: True
            labels: Optional[Dict[str, Any]] -- Labels for the model, default: None
            tags: Optional[str] -- Tags for the model, default: None
            template_id: Optional[float] -- Template ID for the model (use FrogModel.all_available_model_templates to get available templates), default: None
            app_key: Optional[str] -- The app key
        
        Returns:
            FrogModel | dict: A FrogModel object if the model is created successfully, else a dictionary containing the status and message
        """
        if not name:
            return {"status": "error", "message": "Model name is required"}

        try:
            resolved_app_key = FrogModel.__set_app_key__(app_key)
            oc = OptilogicClient(appkey=resolved_app_key)
            response = oc.api.database_create(
                name=name,
                desc=desc,
                template=template,
                backups=backups,
                labels=labels,
                tags=tags,
                # schema_status=schema_status,
                template_id=template_id
            )

            if response.get('result', 'error') == 'error':
                return {"status": "error", "message": response.get('message', '')}

            new_model_instance = FrogModel(name, app_key=resolved_app_key, model_creation=True)
            print(f"Model created successfully with ID: {response.get('storageId', '')}")

            return new_model_instance
        except ValueError as ve:
            return {"status": "error", "message": str(ve)}
        except Exception as e:
            return {"status": "error", "message": str(e)}


    @staticmethod
    def delete_model(model_name: str, app_key: Optional[str] = None) -> dict:
        """
        Delete the model

        Returns:
            dict: A dictionary containing the status and message
        """

        resolved_app_key = FrogModel.__set_app_key__(app_key)
        oc = OptilogicClient(appkey=resolved_app_key)
        return oc.delete_model_api(model_name)


    @check_connection_type("app_key")
    def delete(self) -> dict:
        """
        Delete the model

        Returns:
            dict: A dictionary containing the status and message
        """
        oc = OptilogicClient(appkey=self._app_key)
        return oc.delete_model_api(self.model_name)


    @check_connection_type("app_key")
    def edit_model(self, new_name: Optional[str] = '', description: Optional[str] = '') -> Dict[str, str]:
        """
        Edit the model name or description

        Args:
            new_name: str -- New name for the model
            description: str -- New description for the model
        
        Returns:
            dict: A dictionary containing the status and message
        """

        import requests

        if not new_name and not description:
            return {"status": "error", "message": "New name or description is required for updating the model"}

        try:
            url = f'{ATLAS_API_BASE_URL}/storage/{self.model_name}'
            headers = {'X-App-Key': self._app_key}
            data = {}

            if new_name:
                data['name'] = new_name
            else:
                data['name'] = self.model_name

            if description:
                data['description'] = description
            else:
                oc = OptilogicClient(appkey=self._app_key)
                response = oc.api.database(name=self.model_name)
                data['description'] = response.get('description', '')

            response = requests.request('PATCH', url, headers=headers, data=json.dumps(data), timeout=60)
            res = response.json()

            if res.get('result', 'error') == 'error':
                return {"status": "error", "message": res.get('message', '')}

            self.model_name = new_name # update the model name in the object
            return {"status": "success", "message": f"Model {self.model_name} updated successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


    @staticmethod
    def all_available_model_templates(app_key: Optional[str] = None):
        """
        Get all available model templates

        Args:
            app_key: Optional[str] -- The app key

        Returns:
            dict: A dictionary containing the status, message, and data
        """

        try:
            resolved_app_key = FrogModel.__set_app_key__(app_key)
            oc = OptilogicClient(appkey=resolved_app_key)
            response = oc.api.database_templates()
            if response.get('result', 'error') == 'error':
                return {"status": "error", "message": response.get('message', '')}

            return {"status": "success", "message": "Model templates fetched successfully", "data": response['templates']}
        except ValueError as ve:
            return {"status": "error", "message": str(ve)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @check_connection_type("app_key")
    def share(
        self,
        target_user: str,
    ) -> Dict[str, str]:
        """
        Share the model with another user

        Args:
            target_user: str -- Username or email address of the user to share the model with
        
        Returns:
            dict: A dictionary containing the status and message
        """
        import requests

        if target_user is None:
            return {"status": "error", "message": "Target user is required. Username or email address of the user who will be assigned ownership of the storage device"}

        try:
            url = f'{ATLAS_API_BASE_URL}/storage/{self.model_name}/share/access?targetUser={target_user}'
            headers = {'X-App-Key': self._app_key}
            response = requests.request('POST', url, headers=headers, timeout=60)
            res = response.json()
            print(res)
            if res.get('result', 'error') == 'error':
                return {"status": "error", "message": res.get('message', '')}

            return {"status": "success", "message": f"Model {self.model_name} shared successfully with {target_user}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @check_connection_type("app_key")
    def remove_share_access(
        self,
        target_user: str,
    ) -> Dict[str, str]:
        """
        Remove share access from a user

        Args:
            target_user: str -- Username or email address of the user who will be removed from ownership of the storage device
        
        Returns:
            dict: A dictionary containing the status and message
        """
        import requests
    
        if target_user is None:
            return {"status": "error", "message": "Target user is required. Username or email address of the user who will be removed from ownership of the storage device"}

        try:
            url = f'{ATLAS_API_BASE_URL}/storage/{self.model_name}/share/access?targetUser={target_user}'
            headers = {'X-App-Key': self._app_key}
            response = requests.request('DELETE', url, headers=headers, timeout=60)
            res = response.json()
            if res.get('result', 'error') == 'error':
                return {"status": "error", "message": res.get('message', '')}

            return {"status": "success", "message": f"Removed share access from {target_user} for model {self.model_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @check_connection_type("app_key")
    def clone(self, new_name: str) -> Dict[str, str]:
        """
        Clone the model

        Args:
            new_name: str -- New name for the cloned model
        
        Returns:
            dict: A dictionary containing the status and message
        """
        if not new_name:
            return {"status": "error", "message": "New name is required"}

        try:
            oc = OptilogicClient(appkey=self._app_key)
            response = oc.api.database_clone(name=self.model_name, new_name=new_name)

            if response.get('result', 'error') == 'error':
                return {"status": "error", "message": response.get('message', '')}

            return {"status": "success", "message": f"Model {self.model_name} cloned successfully to {new_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @check_connection_type("app_key")
    def archive(self) -> Dict[str, str]:
        """
        Archive the model

        Returns:
            dict: A dictionary containing the status and message
        """
        try:
            oc = OptilogicClient(appkey=self._app_key)
            response = oc.api.database_archive(name=self.model_name)

            if response.get('result', 'error') == 'error':
                return {"status": "error", "message": response.get('message', '')}

            return {"status": "success", "message": f"Model {self.model_name} archived successfully as {self.model_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def archive_restore(app_key: Optional[str] = None, model_name: str = '', model_id: str = '') -> Dict[str, str]:
        """"
        Restore an archived model.

        To see all archived models, use the FrogModel.archived_models() method.

        Use either model_name or model_id to restore the model.

        If multiple models with the same name are archived, use the model_id to restore the correct model.

        Args:
            app_key: Optional[str] -- The app key
            model_name: str -- Name of the model to restore
            model_id: str -- ID of the model to restore (storage_id)

        Returns:
            dict: A dictionary containing the status and message
        """

        if not model_name and not model_id:
            return {"status": "error", "message": "Model name or model id is required"}

        try:
            resolved_app_key = FrogModel.__set_app_key__(app_key)
            oc = OptilogicClient(appkey=resolved_app_key)
            model_name = model_id if model_id else model_name
            response = oc.api.database_archive_restore(name=model_name)

            if response.get('result', 'error') == 'error':
                return {"status": "error", "message": response.get('message', '')}

            return {"status": "success", "message": f"Model {model_name} restored successfully"}
        except ValueError as ve:
            return {"status": "error", "message": str(ve)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def archived_models(app_key: Optional[str] = None) -> Dict[str, str]:
        """
        Get all archived models

        Args:
            app_key: Optional[str] -- The app key

        Returns:
            dict: A dictionary containing the status, message, and data
        """

        try:
            resolved_app_key = FrogModel.__set_app_key__(app_key)
            oc = OptilogicClient(appkey=resolved_app_key)
            response = oc.api.database_archived()

            if response.get('result', 'error') == 'error':
                return {"status": "error", "message": response.get('message', '')}

            return {"status": "success", "message": "Archived models fetched successfully", "data": response.get('storages', [])}
        except ValueError as ve:
            return {"status": "error", "message": str(ve)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    ### END Model Methods API ###

    ## Backup

    ### Start Geocoding API ###

    @check_connection_type("app_key")
    def geocode_table(
        self,
        table_name: str,
        geoprovider: str = "MapBox",
        geoapikey: str = None,
        ignore_low_confidence: bool = True,
        fire_and_forget: bool = True,
    ):
        """
        Wrapper function for geocoding an Cosmic Frog table (in place)

        Args:
            table_name: Name of the target Anura table (Customers, Facilities, Suppliers)
            geoprovider: Geocoding provider to use (default: MapBox)
            geoapikey: API key for geocoding provider if none is provided, the default key will be used for MapBox only
            ignore_low_confidence: Ignore low confidence geocodes
            fire_and_forget: Run geocoding in the background or wait for completion, if already in progress it can wait for completion
        """

        return FrogUtils.geocode_table(
            self.model_name,
            table_name,
            self._app_key,
            geoprovider=geoprovider,
            geoapikey=geoapikey,
            ignore_low_confidence=ignore_low_confidence,
            fire_and_forget=fire_and_forget
        )

    ### End Geocoding API ###
