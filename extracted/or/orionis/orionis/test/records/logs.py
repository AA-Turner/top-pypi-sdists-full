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
        Initialize the TestLogs instance, setting up the SQLite database path and connection.

        Parameters
        ----------
        storage_path : str
            Directory path where the SQLite database file ('tests.sqlite') will be stored. The directory
            will be created if it does not exist.

        Returns
        -------
        None
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
        Establish a connection to the SQLite database if not already connected.

        Raises
        ------
        OrionisTestPersistenceError
            If a database connection error occurs.

        Returns
        -------
        None
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
        Ensure the reports table exists in the SQLite database.

        Returns
        -------
        bool
            True if the table was created or already exists.

        Raises
        ------
        OrionisTestPersistenceError
            If table creation fails due to a database error.
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
        Insert a test report into the reports table.

        Parameters
        ----------
        report : dict
            Dictionary containing the report data. Must include keys:
            'total_tests', 'passed', 'failed', 'errors', 'skipped', 'total_time', 'success_rate', 'timestamp'.

        Returns
        -------
        bool
            True if the report was successfully inserted.

        Raises
        ------
        OrionisTestPersistenceError
            If there is an error inserting the report into the database.
        OrionisTestValueError
            If required fields are missing from the report.
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
        Retrieve a specified number of report records from the database.

        Parameters
        ----------
        first : int or None, optional
            Number of earliest reports to retrieve, ordered by ascending ID.
        last : int or None, optional
            Number of latest reports to retrieve, ordered by descending ID.

        Returns
        -------
        list of tuple
            List of tuples representing report records.

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
        Drop the reports table from the SQLite database.

        Returns
        -------
        bool
            True if the table was successfully dropped or did not exist.

        Raises
        ------
        OrionisTestPersistenceError
            If an SQLite error occurs while attempting to drop the table.
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
        Close the active SQLite database connection if it exists.

        Returns
        -------
        None
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
        Insert a new test report into the database after ensuring the reports table exists.

        Parameters
        ----------
        report : dict
            Dictionary containing the test report data. Must include all required fields.

        Returns
        -------
        bool
            True if the report was successfully inserted.

        Raises
        ------
        OrionisTestPersistenceError
            If the operation fails due to database errors.
        OrionisTestValueError
            If required fields are missing from the report.
        """
        # Ensure the reports table exists before inserting the report
        self.__createTableIfNotExists()

        # Insert the report into the database and return the result
        return self.__insertReport(report)

    def reset(
        self
    ) -> bool:
        """
        Drop the reports table from the SQLite database, clearing all test history records.

        Returns
        -------
        bool
            True if the reports table was successfully dropped or did not exist.

        Raises
        ------
        OrionisTestPersistenceError
            If the operation fails due to a database error.
        """
        # Attempt to drop the reports table and reset the database
        return self.__resetDatabase()

    def get(
        self,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> List[Tuple]:
        """
        Retrieve test reports from the database.

        Parameters
        ----------
        first : int or None, optional
            Number of earliest reports to retrieve, ordered by ascending ID.
        last : int or None, optional
            Number of latest reports to retrieve, ordered by descending ID.

        Returns
        -------
        list of tuple
            List of tuples representing report records.

        Raises
        ------
        OrionisTestValueError
            If both 'first' and 'last' are specified, or if either is not a positive integer.
        OrionisTestPersistenceError
            If there is an error retrieving reports from the database.
        """
        # Delegate the retrieval logic to the internal __getReports method
        return self.__getReports(first, last)
