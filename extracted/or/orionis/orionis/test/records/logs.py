import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from orionis.test.exceptions import OrionisTestPersistenceError, OrionisTestValueError
from orionis.test.contracts.logs import ITestLogs

class TestLogs(ITestLogs):

    def __init__(
        self,
        storage_path: str
    ) -> None:
        """
        Initialize a new instance of the TestLogs class, configuring the SQLite database path and connection.

        This constructor sets up the database file and table names, ensures the storage directory exists,
        and prepares the absolute path for the SQLite database file. The database connection is initialized
        as None and will be established when needed.

        Parameters
        ----------
        storage_path : str
            The directory path where the SQLite database file ('tests.sqlite') will be stored. If the directory
            does not exist, it will be created automatically.

        Returns
        -------
        None
            This method does not return a value.
        """

        # Set the database file and table names
        self.__db_name = 'tests.sqlite'
        self.__table_name = 'reports'

        # Create the full path to the database file
        db_path = Path(storage_path)
        db_path = db_path / self.__db_name

        # Ensure the parent directory exists
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Store the resolved absolute path to the database
        self.__db_path = db_path.resolve()

        # Initialize the database connection as None
        self._conn: Optional[sqlite3.Connection] = None

    def __connect(
        self
    ) -> None:
        """
        Establishes a connection to the SQLite database if not already connected.

        This method checks if a database connection is already established. If not, it attempts to create a new
        SQLite connection using the absolute path specified during initialization. If the connection attempt fails,
        it raises an OrionisTestPersistenceError with the error details.

        Raises
        ------
        OrionisTestPersistenceError
            If a database connection error occurs.

        Returns
        -------
        None
            This method does not return a value. It sets the self._conn attribute to an active SQLite connection
            if successful, or raises an exception if the connection fails.
        """

        # Only connect if there is no existing connection
        if self._conn is None:

            try:

                # Attempt to establish a new SQLite connection
                self._conn = sqlite3.connect(
                    database=str(self.__db_path),
                    timeout=5.0,
                    isolation_level=None,
                    check_same_thread=False,
                    autocommit=True
                )

                # Hability to use WAL mode for better concurrency
                self._conn.execute("PRAGMA journal_mode=WAL;")
                self._conn.execute("PRAGMA synchronous=NORMAL;")

            except (sqlite3.Error, Exception) as e:

                # Raise a custom exception if connection fails
                raise OrionisTestPersistenceError(f"Database connection error: {e}")

    def __createTableIfNotExists(
        self
    ) -> bool:
        """
        Ensures the existence of the test history table in the SQLite database.

        This method establishes a connection to the database and attempts to create the table
        specified by `self.__table_name` with the required schema if it does not already exist.
        The table includes columns for the report JSON, test statistics, and a timestamp.
        If a database error occurs during table creation, the transaction is rolled back and
        an OrionisTestPersistenceError is raised.

        Raises
        ------
        OrionisTestPersistenceError
            If the table creation fails due to a database error.

        Returns
        -------
        bool
            Returns True if the table was created successfully or already exists.
            Returns False only if an unexpected error occurs (which will typically raise an exception).
        """

        # Establish a connection to the database
        self.__connect()

        try:

            # Create a cursor to execute SQL commands
            cursor = self._conn.cursor()

            # Create the table with the required schema if it does not exist
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
            if self._conn:
                self._conn.rollback()

            # Raise a custom exception with the error details
            raise OrionisTestPersistenceError(f"Failed to create table: {e}")

        finally:

            # Close the database connection
            if self._conn:
                self.__close()
                self._conn = None

    def __insertReport(
        self,
        report: Dict
    ) -> bool:
        """
        Inserts a test report into the history database table.

        This method validates the provided report dictionary to ensure all required fields are present,
        serializes the report as JSON, and inserts it into the database table. If any required field is missing,
        or if a database error occurs during insertion, an appropriate exception is raised.

        Parameters
        ----------
        report : Dict
            A dictionary containing the report data. The dictionary must include the following keys:
            - total_tests
            - passed
            - failed
            - errors
            - skipped
            - total_time
            - success_rate
            - timestamp

        Raises
        ------
        OrionisTestPersistenceError
            If there is an error inserting the report into the database.
        OrionisTestValueError
            If required fields are missing from the report.

        Returns
        -------
        bool
            Returns True if the report was successfully inserted into the database.
            Returns False only if an unexpected error occurs (which will typically raise an exception).
        """

        # List of required fields for the report
        fields = [
            "json", "total_tests", "passed", "failed", "errors",
            "skipped", "total_time", "success_rate", "timestamp"
        ]

        # Check for missing required fields (excluding "json" which is handled separately)
        missing = []
        for key in fields:
            if key not in report and key != "json":
                missing.append(key)
        if missing:
            raise OrionisTestValueError(f"Missing report fields: {missing}")

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

            # Execute the insert query with the report data, serializing the entire report as JSON
            cursor = self._conn.cursor()

            # Ensure the 'json' field is serialized to JSON format
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

            # Commit the transaction to save the new report
            self._conn.commit()

            # Return True indicating the report was successfully inserted
            return True

        except sqlite3.Error as e:

            # Roll back the transaction if an error occurs during insertion
            if self._conn:
                self._conn.rollback()
            raise OrionisTestPersistenceError(f"Failed to insert report: {e}")

        finally:

            # Ensure the database connection is closed after the operation
            if self._conn:
                self.__close()
                self._conn = None

    def __getReports(
        self,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> List[Tuple]:
        """
        Retrieves a specified number of report records from the database, ordered by their ID.

        This method allows fetching either the earliest or latest test reports from the database,
        depending on the parameters provided. If `first` is specified, it retrieves the earliest
        reports in ascending order by ID. If `last` is specified, it retrieves the latest reports
        in descending order by ID. Only one of `first` or `last` can be provided at a time.

        Parameters
        ----------
        first : Optional[int], default=None
            The number of earliest reports to retrieve, ordered ascending by ID.
        last : Optional[int], default=None
            The number of latest reports to retrieve, ordered descending by ID.

        Returns
        -------
        List[Tuple]
            A list of tuples, where each tuple represents a report record retrieved from the database.
            Each tuple contains all columns from the reports table, including the serialized JSON report
            and associated statistics.

        Raises
        ------
        OrionisTestValueError
            If both 'first' and 'last' are specified, or if either is not a positive integer.
        OrionisTestPersistenceError
            If there is an error retrieving reports from the database.
        """

        # Ensure that only one of 'first' or 'last' is specified
        if first is not None and last is not None:
            raise OrionisTestValueError(
                "Cannot specify both 'first' and 'last' parameters. Use one or the other."
            )

        # Validate 'first' parameter if provided
        if first is not None:
            if not isinstance(first, int) or first <= 0:
                raise OrionisTestValueError("'first' must be an integer greater than 0.")

        # Validate 'last' parameter if provided
        if last is not None:
            if not isinstance(last, int) or last <= 0:
                raise OrionisTestValueError("'last' must be an integer greater than 0.")

        # Determine the order and quantity of records to retrieve
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

            # Fetch all matching records
            results = cursor.fetchall()

            # Return the list of report records
            return results

        except sqlite3.Error as e:

            # Raise a custom exception if retrieval fails
            raise OrionisTestPersistenceError(f"Failed to retrieve reports from '{self.__db_name}': {e}")

        finally:

            # Ensure the database connection is closed after the operation
            if self._conn:
                self.__close()
                self._conn = None

    def __resetDatabase(
        self
    ) -> bool:
        """
        Drops the reports table from the SQLite database, effectively resetting the test history.

        This method establishes a connection to the database and attempts to drop the table specified
        by `self.__table_name` if it exists. After dropping the table, it commits the changes and closes
        the connection. If an error occurs during the operation, an OrionisTestPersistenceError is raised.

        Raises
        ------
        OrionisTestPersistenceError
            If an SQLite error occurs while attempting to drop the table.

        Returns
        -------
        bool
            Returns True if the table was successfully dropped or did not exist.
            Returns False only if an unexpected error occurs (which will typically raise an exception).
        """

        # Establish a connection to the database
        self.__connect()

        try:

            # Create a cursor and execute the DROP TABLE statement
            cursor = self._conn.cursor()
            cursor.execute(f'DROP TABLE IF EXISTS {self.__table_name}')

            # Commit the transaction to apply the changes
            self._conn.commit()

            # Return True to indicate the reset was successful
            return True

        except sqlite3.Error as e:

            # Raise a custom exception if the reset fails
            raise OrionisTestPersistenceError(f"Failed to reset database: {e}")

        finally:

            # Ensure the database connection is closed after the operation
            if self._conn:
                self.__close()
                self._conn = None

    def __close(
        self
    ) -> None:
        """
        Closes the active SQLite database connection if it exists.

        This method checks whether a database connection is currently open. If so, it closes the connection
        to release any associated resources and sets the connection attribute to None to indicate that
        there is no active connection.

        Returns
        -------
        None
            This method does not return a value. It ensures that the database connection is properly closed.
        """

        # If a database connection exists, close it and set the connection attribute to None
        if self._conn:
            self._conn.close()
            self._conn = None

    def create(
        self,
        report: Dict
    ) -> bool:
        """
        Inserts a new test report into the history database after ensuring the reports table exists.

        This method first checks for the existence of the reports table in the SQLite database,
        creating it if necessary. It then attempts to insert the provided report dictionary into
        the table. The report must contain all required fields as defined by the schema.

        Parameters
        ----------
        report : Dict
            A dictionary containing the test report data. The dictionary must include all required
            fields such as total_tests, passed, failed, errors, skipped, total_time, success_rate, and timestamp.

        Returns
        -------
        bool
            Returns True if the report was successfully inserted into the database.
            Raises an exception if the operation fails due to missing fields or database errors.
        """

        # Ensure the reports table exists before inserting the report
        self.__createTableIfNotExists()

        # Insert the report into the database and return the result
        return self.__insertReport(report)

    def reset(
        self
    ) -> bool:
        """
        Drops the reports table from the SQLite database, effectively clearing all test history records.

        This method establishes a connection to the database and attempts to drop the table specified
        by `self.__table_name` if it exists. This operation removes all stored test reports, resetting
        the database to an empty state. If the table does not exist, the method completes without error.
        If an error occurs during the operation, an OrionisTestPersistenceError is raised.

        Returns
        -------
        bool
            Returns True if the reports table was successfully dropped or did not exist.
            Raises an exception if the operation fails due to a database error.
        """

        # Attempt to drop the reports table and reset the database
        return self.__resetDatabase()

    def get(
        self,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> List[Tuple]:
        """
        Retrieves test reports from the history database based on the specified parameters.

        This method allows fetching either the earliest or latest test reports from the database.
        If `first` is provided, it retrieves the earliest reports in ascending order by ID.
        If `last` is provided, it retrieves the latest reports in descending order by ID.
        Only one of `first` or `last` can be specified at a time; providing both will result in an error.

        Parameters
        ----------
        first : Optional[int], default=None
            The number of earliest reports to retrieve, ordered ascending by ID.
        last : Optional[int], default=None
            The number of latest reports to retrieve, ordered descending by ID.

        Returns
        -------
        List[Tuple]
            A list of tuples, where each tuple represents a report record retrieved from the database.
            Each tuple contains all columns from the reports table, including the serialized JSON report
            and associated statistics.

        Raises
        ------
        OrionisTestValueError
            If both 'first' and 'last' are specified, or if either is not a positive integer.
        OrionisTestPersistenceError
            If there is an error retrieving reports from the database.
        """

        # Delegate the retrieval logic to the internal __getReports method
        return self.__getReports(first, last)
