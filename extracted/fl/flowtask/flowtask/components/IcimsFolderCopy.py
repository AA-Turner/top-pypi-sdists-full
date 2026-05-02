import os
import shutil
import asyncio
from navconfig.logging import logging
from asyncdb.exceptions import ProviderError
from asyncdb.drivers.pg import pg
from .flow import FlowComponent
from ..exceptions import ComponentError, DataNotFound
from querysource.conf import default_dsn, DB_TIMEOUT
import pandas as pd


class IcimsFolderCopy(FlowComponent):
    """
    IcimsFolderCopy.

    Copies folders from one directory to another based on data retrieved from a PostgreSQL database.
    Supports three modes: copying all folders,
    copying based on the associate's name, or copying based on the associate's ID.

    Properties:
    | Name              | Required    | Summary                                         |
    |  driver           |   Yes       | pg (default asyncdb PostgreSQL driver)          |
    |  source_directory |   Yes       | Directory where folders are located             |
    |  destination_dir  |   Yes       | Directory where folders will be copied to       |
    |  by_name          |   No        | Person's name to filter by                      |
    |  by_associate_id  |   No        | Associate ID to filter by                       |

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          IcimsFolderCopy:
          # attributes here
        ```
    """
    _version = "1.0.0"

    def __init__(self, loop: asyncio.AbstractEventLoop = None, job=None, stat=None, **kwargs):
        self.source_directory = kwargs.get("source_directory")
        self.destination_directory = kwargs.get("destination_directory")
        self.driver = kwargs.get("driver", "pg")
        self.by_name = kwargs.get("by_name", None)
        self.by_associate_id = kwargs.get("by_associate_id", None)

        # Automatically load environment-based credentials
        self.dsn = default_dsn
        self.timeout = DB_TIMEOUT

        # Initialize FlowComponent
        FlowComponent.__init__(self, loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs) -> bool:
        """Prepare component for execution."""
        await super(IcimsFolderCopy, self).start(**kwargs)
        return True

    async def run(self):
        """Execute the folder copying process based on database results using Pandas."""
        try:
            db = pg(dsn=self.dsn, timeout=self.timeout)
        except ProviderError as e:
            raise ComponentError(f"Error connecting to database: {e}")

        try:
            # Establish connection and assign it to _connection
            self._connection = await db.connection()

            if not self._connection.is_connected():
                raise ComponentError(f"DB Error: driver {self.driver} is not connected.")

            query_to_run = ""

            if self.by_name:
                associate_query = (
                    f"SELECT associate_id, full_name FROM icims.forms_list "
                    f"WHERE full_name LIKE '%{self.by_name}%' "
                    f"GROUP BY associate_id, full_name"
                )
                query_to_run = associate_query
                logging.info(f"Running query: {query_to_run}")
                associate_result = await self._connection.query(associate_query)

            elif self.by_associate_id:
                associate_query = (
                    f"SELECT associate_id, full_name FROM icims.forms_list "
                    f"WHERE associate_id = '{self.by_associate_id}' "
                    f"GROUP BY associate_id, full_name"
                )
                query_to_run = associate_query
                logging.info(f"Running query: {query_to_run}")
                associate_result = await self._connection.query(associate_query)

            elif hasattr(self, "query"):
                # Custom query provided
                query_to_run = self.query
                logging.info(f"Running custom query: {query_to_run}")
                associate_result = await self._connection.query(query_to_run)
            else:
                raise ComponentError("Either by_name, by_associate_id, or a custom query is required for this operation.")

            # Flatten and filter out None
            associate_result = [item for sublist in associate_result if sublist is not None for item in sublist]

            # Dynamically extract field names and values
            data = [{k: v for k, v in row.items()} for row in associate_result]

            # Convert to DataFrame
            df = pd.DataFrame(data)

            # Handle missing values
            df.dropna(subset=["associate_id"], inplace=True)

            # Extract folder codes as a list
            folder_codes = df["associate_id"].tolist()

            # Copy folders
            copied_count = self.copy_folders(folder_codes)

            # Check if no folders were copied
            if copied_count == 0:
                raise ComponentError("No folders were copied. Please check the source or the query results.")

        except ProviderError as e:
            raise ComponentError(f"Error querying database: {e}") from e
        except Exception as e:
            self._logger.error(e)
            raise
        return True


    def copy_folders(self, folder_codes):
        """Copy folders and handle missing folders gracefully."""
        copied_count = 0
        failed_folders = []

        for code in folder_codes:
            src_folder = os.path.join(self.source_directory, code)
            dest_folder = os.path.join(self.destination_directory, code)

            if os.path.exists(src_folder):
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)

                for root, dirs, files in os.walk(src_folder):
                    for file in files:
                        src_file = os.path.join(root, file)
                        rel_path = os.path.relpath(src_file, src_folder)
                        dest_file = os.path.join(dest_folder, rel_path)

                        os.makedirs(os.path.dirname(dest_file), exist_ok=True)

                        try:
                            shutil.copy2(src_file, dest_file)
                        except shutil.Error as e:
                            self._logger.error(f"Error copying file {src_file}: {e}")
                copied_count += 1
            else:
                failed_folders.append(code)
                logging.warning(f"Folder {code} does not exist in the source directory.")

        if failed_folders:
            self._logger.error(f"Failed to find folders for the following associate_ids: {failed_folders}")

        logging.info(f"Total folders copied or merged: {copied_count} out of {len(folder_codes)} requested.")
        return copied_count

    async def close(self, connection=None):
        """Close the database connection."""
        if not connection:
            connection = getattr(self, '_connection', None)  # Safely get the connection
        try:
            if connection is not None:
                await connection.close()
                logging.info("Database connection closed successfully.")
            else:
                logging.warning("No active connection to close.")
        except Exception as err:
            self._logger.error(f"Error closing database connection: {err}")
