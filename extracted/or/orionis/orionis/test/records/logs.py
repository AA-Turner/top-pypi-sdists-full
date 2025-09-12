import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from orionis.test.contracts.logs import ITestLogs
from orionis.test.exceptions import OrionisTestPersistenceError, OrionisTestValueError

class TestLogs(ITestLogs):

    def __init__(
        self,
        storage_path: str | Path,
        db_name: str = 'tests.sqlite',
        table_name: str = 'reports'
    ) -> None:
        """
        Initialize a TestLogs instance, configuring the SQLite database location and connection.

        Parameters
        ----------
        storage_path : str or Path
            Directory path where the SQLite database file will be stored. If the directory does not exist,
            it will be created automatically.
        db_name : str, optional
            Name of the SQLite database file. Defaults to 'tests.sqlite'.
        table_name : str, optional
            Name of the table used to store test reports. Defaults to 'reports'.

        Returns
        -------
        None
            This method does not return any value.

        Notes
        -----
        The database connection is not established during initialization; it is set to None and will be
        created when needed. The database path is resolved to an absolute path.
        """

        # Store the database file and table names as private attributes
        self.__db_name = db_name
        self.__table_name = table_name

        # Convert storage_path to Path object if it is a string
        db_path = Path(storage_path) if isinstance(storage_path, str) else storage_path

        # Append the database file name to the directory path
        db_path = db_path / self.__db_name

        # Ensure the parent directory for the database exists
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Store the absolute path to the database file
        self.__db_path = db_path.resolve()

        # Initialize the database connection attribute to None
        self._conn: Optional[sqlite3.Connection] = None

    def __connect(
        self
    ) -> None:
        """
        Establish a connection to the SQLite database if not already connected.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It sets up the database connection as a side effect.

        Raises
        ------
        OrionisTestPersistenceError
            If a database connection error occurs.

        Notes
        -----
        This method initializes the SQLite connection only if it is not already established.
        It configures the connection for improved concurrency using WAL mode and sets the synchronous
        mode to NORMAL for better performance. The connection is stored in the `_conn` attribute.
        """

        # Only connect if there is no existing connection
        if self._conn is None:

            try:

                # Attempt to establish a new SQLite connection with custom settings
                self._conn = sqlite3.connect(
                    database=str(self.__db_path),
                    timeout=5.0,
                    isolation_level=None,
                    check_same_thread=False,
                    autocommit=True
                )

                # Enable Write-Ahead Logging for better concurrency
                self._conn.execute("PRAGMA journal_mode=WAL;")

                # Set synchronous mode to NORMAL for performance
                self._conn.execute("PRAGMA synchronous=NORMAL;")

            except (sqlite3.Error, Exception) as e:

                # Raise a custom exception if connection fails
                raise OrionisTestPersistenceError(
                    f"Failed to connect to SQLite database at '{self.__db_path}': {e}"
                )

    def __createTableIfNotExists(
        self
    ) -> bool:
        """
        Ensures that the reports table exists in the SQLite database, creating it if necessary.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            Returns True if the table was created or already exists.

        Raises
        ------
        OrionisTestPersistenceError
            Raised if table creation fails due to a database error.

        Notes
        -----
        This method establishes a connection to the SQLite database and attempts to create the reports
        table with the required schema if it does not already exist. The schema includes fields for
        storing the report as JSON, test statistics, and a timestamp. The method commits the transaction
        if successful, rolls back on error, and always closes the connection at the end.
        """
        # Establish a connection to the database
        self.__connect()

        try:
            # Create a cursor to execute SQL commands
            cursor = self._conn.cursor()

            # Create the reports table with the required schema if it does not exist
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.__table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    json TEXT NOT NULL,
                    total_tests INTEGER,
                    passed INTEGER,
                    failed INTEGER,
                    errors INTEGER,
                    skipped INTEGER,
                    total_time REAL,
                    success_rate REAL,
                    timestamp TEXT
                )
            ''')

            # Commit the transaction to save changes
            self._conn.commit()

            # Return True indicating the table exists or was created successfully
            return True

        except sqlite3.Error as e:

            # Roll back the transaction if an error occurs
            if isinstance(self._conn, sqlite3.Connection):
                self._conn.rollback()

            # Raise a custom exception with the error details
            raise OrionisTestPersistenceError(
                f"Failed to create or verify table '{self.__table_name}' in database '{self.__db_name}' at '{self.__db_path}': {e}"
            )

        finally:

            # Always close the database connection after the operation
            if isinstance(self._conn, sqlite3.Connection):
                self.__close()
                self._conn = None

    def __insertReport(
        self,
        report: Dict
    ) -> bool:
        """
        Inserts a test report into the reports table in the SQLite database.

        Parameters
        ----------
        report : dict
            Dictionary containing the report data. Must include the following keys:
            'total_tests', 'passed', 'failed', 'errors', 'skipped', 'total_time', 'success_rate', 'timestamp'.
            The entire report will be serialized and stored in the 'json' column.

        Returns
        -------
        bool
            Returns True if the report was successfully inserted into the database.

        Raises
        ------
        OrionisTestPersistenceError
            If an error occurs while inserting the report into the database.
        OrionisTestValueError
            If any required fields are missing from the report.

        Notes
        -----
        This method validates the presence of all required fields in the report dictionary (except 'json', which is
        handled by serializing the entire report). The report is inserted as a new row in the reports table, with the
        full dictionary stored as a JSON string in the 'json' column and individual fields mapped to their respective
        columns. The database connection is managed internally and closed after the operation.
        """

        # List of required fields for the report (excluding 'json', which is handled separately)
        fields = [
            "json", "total_tests", "passed", "failed", "errors",
            "skipped", "total_time", "success_rate", "timestamp"
        ]

        # Check for missing required fields in the report dictionary
        missing = []
        for key in fields:
            if key not in report and key != "json":
                missing.append(key)

        # If any required fields are missing, raise an exception
        if missing:
            raise OrionisTestValueError(
                f"The report is missing the following required fields: {', '.join(missing)}"
            )

        # Establish a connection to the database
        self.__connect()

        try:

            # Prepare the SQL query to insert the report data
            query = f'''
                INSERT INTO {self.__table_name} (
                    json, total_tests, passed, failed, errors,
                    skipped, total_time, success_rate, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''

            # Create a cursor for executing the SQL statement
            cursor = self._conn.cursor()

            # Insert the report data, serializing the entire report as JSON for the 'json' column
            cursor.execute(query, (
                json.dumps(report),
                report["total_tests"],
                report["passed"],
                report["failed"],
                report["errors"],
                report["skipped"],
                report["total_time"],
                report["success_rate"],
                report["timestamp"]
            ))

            # Commit the transaction to persist the new report
            self._conn.commit()

            # Return True to indicate successful insertion
            return True

        except sqlite3.Error as e:

            # Roll back the transaction if an error occurs during insertion
            if isinstance(self._conn, sqlite3.Connection):
                self._conn.rollback()

            # Raise a custom exception with the error details
            raise OrionisTestPersistenceError(
                f"Failed to insert report into table '{self.__table_name}' in database '{self.__db_name}' at '{self.__db_path}': {e}"
            )

        finally:

            # Ensure the database connection is closed after the operation
            if isinstance(self._conn, sqlite3.Connection):
                self.__close()
                self._conn = None

    def __getReports(
        self,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> List[Tuple]:
        """
        Retrieve a specified number of report records from the database, either the earliest or latest entries.

        Parameters
        ----------
        first : int or None, optional
            The number of earliest reports to retrieve, ordered by ascending ID. Must be a positive integer.
        last : int or None, optional
            The number of latest reports to retrieve, ordered by descending ID. Must be a positive integer.

        Returns
        -------
        List[Tuple]
            A list of tuples, where each tuple represents a row from the reports table. Each tuple contains:
            (id, json, total_tests, passed, failed, errors, skipped, total_time, success_rate, timestamp).

        Raises
        ------
        OrionisTestValueError
            If both 'first' and 'last' are specified, or if either is not a positive integer.
        OrionisTestPersistenceError
            If there is an error retrieving reports from the database.

        Notes
        -----
        Only one of 'first' or 'last' can be specified at a time. If neither is provided, no records are returned.
        The method ensures proper connection management and closes the database connection after retrieval.
        """

        # Ensure that only one of 'first' or 'last' is specified
        if first is not None and last is not None:
            raise OrionisTestValueError(
                "You cannot specify both 'first' and 'last' parameters at the same time. Please provide only one."
            )

        # Validate 'first' parameter if provided
        if first is not None:
            if not isinstance(first, int) or first <= 0:
                raise OrionisTestValueError("'first' must be a positive integer greater than zero.")

        # Validate 'last' parameter if provided
        if last is not None:
            if not isinstance(last, int) or last <= 0:
                raise OrionisTestValueError("'last' must be a positive integer greater than zero.")

        # Determine the order and quantity of records to retrieve
        # If 'last' is specified, order by descending ID; otherwise, ascending
        order = 'DESC' if last is not None else 'ASC'
        quantity = first if first is not None else last

        # Establish a connection to the database
        self.__connect()

        try:

            # Create a cursor to execute SQL commands
            cursor = self._conn.cursor()

            # Prepare the SQL query to select the desired reports
            query = f"SELECT * FROM {self.__table_name} ORDER BY id {order} LIMIT ?"
            cursor.execute(query, (quantity,))

            # Fetch all matching records from the database
            results = cursor.fetchall()

            # Return the list of report records as tuples
            return results

        except sqlite3.Error as e:

            # Raise a custom exception if retrieval fails
            raise OrionisTestPersistenceError(
                f"An error occurred while retrieving reports from table '{self.__table_name}' in database '{self.__db_name}' at '{self.__db_path}': {e}"
            )

        finally:

            # Ensure the database connection is closed after the operation
            if isinstance(self._conn, sqlite3.Connection):
                self.__close()
                self._conn = None

    def __resetDatabase(
        self
    ) -> bool:
        """
        Drops the reports table from the SQLite database, effectively clearing all stored test history.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            Returns True if the reports table was successfully dropped or did not exist. If the operation
            completes without raising an exception, the database is considered reset.

        Raises
        ------
        OrionisTestPersistenceError
            If an SQLite error occurs while attempting to drop the table.

        Notes
        -----
        This method establishes a connection to the SQLite database and attempts to drop the reports table
        specified by `self.__table_name`. If the table does not exist, the operation completes silently.
        The database connection is closed after the operation, regardless of success or failure.
        """

        # Establish a connection to the database
        self.__connect()

        try:

            # Create a cursor and execute the DROP TABLE statement to remove the reports table
            cursor = self._conn.cursor()
            cursor.execute(f'DROP TABLE IF EXISTS {self.__table_name}')

            # Commit the transaction to apply the changes
            self._conn.commit()

            # Return True to indicate the reset was successful or the table did not exist
            return True

        except sqlite3.Error as e:

            # Raise a custom exception if the reset fails
            raise OrionisTestPersistenceError(
                f"Failed to reset the reports table '{self.__table_name}' in database '{self.__db_name}' at '{self.__db_path}': {e}"
            )

        finally:

            # Ensure the database connection is closed after the operation
            if isinstance(self._conn, sqlite3.Connection):
                self.__close()
                self._conn = None

    def __close(
        self
    ) -> None:
        """
        Close the active SQLite database connection if it exists.

        This method safely closes the current SQLite database connection if it is open.
        It ensures that resources are released and the connection attribute is reset to None.
        This is important for preventing resource leaks and maintaining proper connection management
        within the TestLogs class.

        Returns
        -------
        None
            This method does not return any value. The side effect is that the database connection
            is closed and the internal connection attribute is set to None.

        Notes
        -----
        This method should be called after database operations to ensure the connection is properly closed.
        It checks if the `_conn` attribute is an active `sqlite3.Connection` before attempting to close it.
        """

        # Check if there is an active SQLite connection before closing
        if isinstance(self._conn, sqlite3.Connection):

            # Close the database connection to release resources
            self._conn.close()

            # Reset the connection attribute to None
            self._conn = None

    def create(
        self,
        report: Dict
    ) -> bool:
        """
        Inserts a new test report into the database after ensuring the reports table exists.

        Parameters
        ----------
        report : dict
            Dictionary containing the test report data. Must include all required fields:
            'total_tests', 'passed', 'failed', 'errors', 'skipped', 'total_time', 'success_rate', 'timestamp'.
            The entire report will be serialized and stored in the 'json' column.

        Returns
        -------
        bool
            True if the report was successfully inserted into the database; otherwise, raises an exception.

        Raises
        ------
        OrionisTestPersistenceError
            If a database error occurs during table creation or report insertion.
        OrionisTestValueError
            If required fields are missing from the report dictionary.

        Notes
        -----
        This method first ensures that the reports table exists in the database. It then validates and inserts
        the provided report dictionary as a new row, storing the full report as a JSON string and mapping individual
        fields to their respective columns. The database connection is managed internally and closed after the operation.
        """

        # Ensure the reports table exists before attempting to insert the report
        self.__createTableIfNotExists()

        # Insert the report into the database and return True if successful
        return self.__insertReport(report)

    def reset(
        self
    ) -> bool:
        """
        Drops the reports table from the SQLite database, effectively clearing all stored test history.

        This method attempts to remove the reports table specified by `self.__table_name` from the database.
        If the table does not exist, the operation completes without error. The database connection is managed
        internally and closed after the operation.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            Returns True if the reports table was successfully dropped or did not exist. If the operation
            completes without raising an exception, the database is considered reset.

        Raises
        ------
        OrionisTestPersistenceError
            If an SQLite error occurs while attempting to drop the table.

        Notes
        -----
        This method is useful for clearing all test report history from the database, such as during test
        environment resets or cleanup operations.
        """

        # Attempt to drop the reports table and reset the database.
        # Returns True if successful or if the table did not exist.
        return self.__resetDatabase()

    def get(
        self,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> List[Tuple]:
        """
        Retrieve a specified number of test report records from the database.

        Parameters
        ----------
        first : int or None, optional
            The number of earliest reports to retrieve, ordered by ascending ID. Must be a positive integer.
            If specified, returns the oldest reports.
        last : int or None, optional
            The number of latest reports to retrieve, ordered by descending ID. Must be a positive integer.
            If specified, returns the most recent reports.

        Returns
        -------
        List[Tuple]
            A list of tuples, where each tuple represents a row from the reports table:
            (id, json, total_tests, passed, failed, errors, skipped, total_time, success_rate, timestamp).
            If neither `first` nor `last` is provided, an empty list is returned.

        Raises
        ------
        OrionisTestValueError
            If both 'first' and 'last' are specified, or if either is not a positive integer.
        OrionisTestPersistenceError
            If there is an error retrieving reports from the database.

        Notes
        -----
        Only one of `first` or `last` can be specified at a time. The method delegates the retrieval
        logic to the internal `__getReports` method, which handles database connection management and
        query execution.
        """

        # Delegate the retrieval logic to the internal __getReports method.
        # This ensures proper validation and database access.
        return self.__getReports(first, last)
