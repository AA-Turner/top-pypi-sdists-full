#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""
JDBC DBAPI 2.0 compatible interface using JPype.

This module provides a Python DB-API 2.0 compatible interface for JDBC connections
using JPype to call Java JDBC directly.

Usage:
    from snowflake.snowpark_connect.relation.jdbc_utils import connect

    conn = connect("com.mysql.jdbc.Driver", "jdbc:mysql://localhost/test", {"user": "root", "password": "secret"})
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
"""

import datetime
import os
import threading
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, Union

import jpype

# =============================================================================
# DB-API 2.0 Module Interface - Global Variables
# =============================================================================

# Module interface version
apilevel = "2.0"

# Thread safety level: 1 = Threads may share the module, but not connections
threadsafety = 1

# Parameter marker style
paramstyle = "qmark"


# =============================================================================
# DB-API 2.0 Type Objects
# =============================================================================


class _DBAPITypeObject:
    """
    DB-API 2.0 Type Object for comparing database types.
    Used in cursor.description to indicate column types.
    """

    def __init__(self, *values) -> None:
        """
        Initialize DBAPI Type object
        :param values: Type values
        """
        self.values = frozenset(values)
        self._name = None

    def __eq__(self, other):
        if other in self.values:
            return True
        if isinstance(other, _DBAPITypeObject):
            return bool(self.values & other.values)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.values)

    def __repr__(self):
        return f"DBAPITypeObject({self._name or self.values})"


# DB-API 2.0 Type Objects
# JDBC type names that map to each DB-API type
STRING = _DBAPITypeObject(
    "CHAR",
    "NCHAR",
    "VARCHAR",
    "NVARCHAR",
    "LONGVARCHAR",
    "LONGNVARCHAR",
    "CLOB",
    "NCLOB",
    "SQLXML",
)
STRING._name = "STRING"

BINARY = _DBAPITypeObject("BINARY", "VARBINARY", "LONGVARBINARY", "BLOB")
BINARY._name = "BINARY"

NUMBER = _DBAPITypeObject("INTEGER", "BIGINT", "SMALLINT", "TINYINT")
NUMBER._name = "NUMBER"

FLOAT = _DBAPITypeObject("FLOAT", "REAL", "DOUBLE")
FLOAT._name = "FLOAT"

DECIMAL = _DBAPITypeObject("DECIMAL", "NUMERIC")
DECIMAL._name = "DECIMAL"

DATE = _DBAPITypeObject("DATE")
DATE._name = "DATE"

TIME = _DBAPITypeObject("TIME", "TIME_WITH_TIMEZONE")
TIME._name = "TIME"

DATETIME = _DBAPITypeObject("TIMESTAMP", "TIMESTAMP_WITH_TIMEZONE")
DATETIME._name = "DATETIME"

ROWID = _DBAPITypeObject("ROWID")
ROWID._name = "ROWID"

# Mapping from JDBC type name to DB-API type object
# These are standard JDBC types from java.sql.Types
_JDBC_TYPE_TO_DBAPI = {
    # String types
    "CHAR": STRING,
    "NCHAR": STRING,
    "VARCHAR": STRING,
    "NVARCHAR": STRING,
    "LONGVARCHAR": STRING,
    "LONGNVARCHAR": STRING,
    "CLOB": STRING,
    "NCLOB": STRING,
    "SQLXML": STRING,
    # Binary types
    "BINARY": BINARY,
    "VARBINARY": BINARY,
    "LONGVARBINARY": BINARY,
    "BLOB": BINARY,
    # Integer types
    "INTEGER": NUMBER,
    "BIGINT": NUMBER,
    "SMALLINT": NUMBER,
    "TINYINT": NUMBER,
    # Float types
    "FLOAT": FLOAT,
    "REAL": FLOAT,
    "DOUBLE": FLOAT,
    # Decimal types
    "DECIMAL": DECIMAL,
    "NUMERIC": DECIMAL,
    # Date/Time types
    "DATE": DATE,
    "TIME": TIME,
    "TIME_WITH_TIMEZONE": TIME,
    "TIMESTAMP": DATETIME,
    "TIMESTAMP_WITH_TIMEZONE": DATETIME,
    # Other standard JDBC types
    "ROWID": ROWID,
    "BIT": NUMBER,  # BIT is often used as boolean/integer
    "BOOLEAN": NUMBER,
    "JAVA_OBJECT": STRING,  # Generic object, convert to string
    "OTHER": STRING,  # Database-specific types, convert to string
    "ARRAY": STRING,  # Arrays, convert to string representation
    "STRUCT": STRING,  # Structured types, convert to string
    "REF": STRING,  # References, convert to string
    "DATALINK": STRING,  # URLs/links, convert to string
    "DISTINCT": STRING,  # Distinct types, convert to string
    "REF_CURSOR": STRING,  # Cursor references, convert to string
    "NULL": STRING,  # Null type placeholder
}


# =============================================================================
# DB-API 2.0 Exceptions
# =============================================================================


class Error(Exception):
    """Base class for all database errors."""

    pass


class Warning(Exception):
    """Exception for important warnings."""

    pass


class InterfaceError(Error):
    """Exception for errors related to the database interface."""

    pass


class DatabaseError(Error):
    """Exception for errors related to the database."""

    pass


class DataError(DatabaseError):
    """Exception for errors due to problems with processed data."""

    pass


class OperationalError(DatabaseError):
    """Exception for errors related to database operation."""

    pass


class IntegrityError(DatabaseError):
    """Exception for database integrity errors."""

    pass


class InternalError(DatabaseError):
    """Exception for internal database errors."""

    pass


class ProgrammingError(DatabaseError):
    """Exception for programming errors."""

    pass


class NotSupportedError(DatabaseError):
    """Exception for not supported operations."""

    pass


# =============================================================================
# DB-API 2.0 Constructors
# =============================================================================


def Date(year: int, month: int, day: int) -> datetime.date:
    """Construct a date value."""
    return datetime.date(year, month, day)


def Time(hour: int, minute: int, second: int) -> datetime.time:
    """Construct a time value."""
    return datetime.time(hour, minute, second)


def Timestamp(
    year: int, month: int, day: int, hour: int, minute: int, second: int
) -> datetime.datetime:
    """Construct a timestamp value."""
    return datetime.datetime(year, month, day, hour, minute, second)


def DateFromTicks(ticks: float) -> datetime.date:
    """Construct a date value from a POSIX timestamp."""
    return datetime.date.fromtimestamp(ticks)


def TimeFromTicks(ticks: float) -> datetime.time:
    """Construct a time value from a POSIX timestamp."""
    return datetime.datetime.fromtimestamp(ticks).time()


def TimestampFromTicks(ticks: float) -> datetime.datetime:
    """Construct a timestamp value from a POSIX timestamp."""
    return datetime.datetime.fromtimestamp(ticks)


def Binary(data: bytes) -> bytes:
    """Construct a binary value."""
    return bytes(data)


# =============================================================================
# Internal State - JDBC Type Mappings
# =============================================================================

# Mapping JDBC type attribute name to attribute value
_jdbc_type_name_to_const: Optional[Dict[str, int]] = None

# Mapping from JDBC type attribute constant value to attribute name
_jdbc_type_const_to_name: Optional[Dict[int, str]] = None

# JDBC type to converter method
_jdbc_type_converters: Optional[Dict[int, callable]] = None

# Java byte array helper
_java_array_byte = None

# Driver class names that have already been registered with DriverManager via
# an isolated URLClassLoader.  Avoids re-registering on every connection call.
_isolated_drivers_registered: Set[str] = set()
_isolated_drivers_lock = threading.Lock()

# Environment variable written by snowpark-submit's SparkConnectJobRunner.
# Contains colon-separated jar paths (already adjusted to in-container form).
# Named differently from CLASSPATH so JPype does NOT auto-add these paths to
# the JVM bootstrap classpath at startJVM() time.
_SCOS_JDBC_DRIVER_JARS_ENV = "SCOS_JDBC_DRIVER_JARS"


# =============================================================================
# Connection Class
# =============================================================================


class Connection:
    """
    DB-API 2.0 Connection object wrapping a JDBC Connection.
    """

    # DB-API 2.0 exception attributes on Connection class
    Error = Error
    Warning = Warning
    InterfaceError = InterfaceError
    DatabaseError = DatabaseError
    DataError = DataError
    OperationalError = OperationalError
    IntegrityError = IntegrityError
    InternalError = InternalError
    ProgrammingError = ProgrammingError
    NotSupportedError = NotSupportedError

    def __init__(self, jdbc_connection) -> None:
        """
        Initialize the connection wrapper.

        Args:
            jdbc_connection: The underlying Java JDBC Connection object
        """
        self._jdbc_conn = jdbc_connection
        self._closed = False
        self._timeout = 0

    @property
    def jconn(self):
        """
        Return the underlying Java JDBC Connection object.
        """
        return self._jdbc_conn

    @property
    def timeout(self) -> int:
        """Get/set the query timeout in seconds."""
        return self._timeout

    @timeout.setter
    def timeout(self, value: int):
        """Set the query timeout in seconds."""
        self._timeout = value if value is not None else 0

    def close(self) -> None:
        """
        Close the connection.

        Raises Error if connection is already closed.
        """
        if self._closed:
            raise Error("Connection is already closed")
        try:
            if self._jdbc_conn is not None:
                self._jdbc_conn.close()
        except Exception:
            pass  # Ignore errors during close
        finally:
            self._closed = True

    def commit(self) -> None:
        """Commit any pending transaction."""
        self._check_closed()
        try:
            self._jdbc_conn.commit()
        except Exception as e:
            _handle_sql_exception_from(e)

    def rollback(self) -> None:
        """Rollback any pending transaction."""
        self._check_closed()
        try:
            self._jdbc_conn.rollback()
        except Exception as e:
            _handle_sql_exception_from(e)

    def cursor(self) -> "Cursor":
        """Return a new Cursor object using this connection."""
        self._check_closed()
        return Cursor(self)

    def _check_closed(self) -> None:
        """Raise an error if the connection is closed."""
        if self._closed:
            raise InterfaceError("Connection is closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


# =============================================================================
# Cursor Class
# =============================================================================


class Cursor:
    """
    DB-API 2.0 Cursor object wrapping a JDBC Statement/ResultSet.

    This implementation provides compatible attribute aliases:
    - _prep: alias for the JDBC PreparedStatement/Statement
    - _rs: alias for the JDBC ResultSet
    - _meta: alias for the JDBC ResultSetMetaData
    """

    def __init__(self, connection: Connection) -> None:
        """
        Initialize the cursor.

        Args:
            connection: The parent Connection object
        """
        self._connection = connection
        self._jdbc_stmt = None
        self._jdbc_rs = None
        self._jdbc_meta = None  # Store ResultSetMetaData
        self._description = None
        self._rowcount = -1
        self._closed = False
        self._arraysize = 1
        self._column_converters = None

    # -------------------------------------------------------------------------
    # DB-API compatible attribute aliases
    # -------------------------------------------------------------------------
    @property
    def _prep(self):
        """Alias for the JDBC Statement/PreparedStatement."""
        return self._jdbc_stmt

    @_prep.setter
    def _prep(self, value):
        self._jdbc_stmt = value

    @property
    def _rs(self):
        """Alias for the JDBC ResultSet."""
        return self._jdbc_rs

    @_rs.setter
    def _rs(self, value):
        self._jdbc_rs = value

    @property
    def _meta(self):
        """Alias for the JDBC ResultSetMetaData."""
        return self._jdbc_meta

    @_meta.setter
    def _meta(self, value):
        self._jdbc_meta = value

    # -------------------------------------------------------------------------
    # DB-API 2.0 properties
    # -------------------------------------------------------------------------
    @property
    def description(self) -> Optional[Tuple[Tuple, ...]]:
        """
        Return column description as sequence of 7-item sequences:
        (name, type_code, display_size, internal_size, precision, scale, null_ok)
        """
        return self._description

    @property
    def rowcount(self) -> int:
        """Return the number of rows affected by the last execute."""
        return self._rowcount

    @property
    def arraysize(self) -> int:
        """Get the number of rows to fetch at a time with fetchmany()."""
        return self._arraysize

    @arraysize.setter
    def arraysize(self, value: int):
        """Set the number of rows to fetch at a time with fetchmany()."""
        self._arraysize = value if value > 0 else 1

    def close(self) -> None:
        """Close the cursor."""
        if self._closed:
            return
        self._closed = True
        self._close_last()

    def _close_last(self) -> None:
        """
        Close the current ResultSet and Statement.
        """
        if self._jdbc_rs is not None:
            try:
                self._jdbc_rs.close()
            except Exception:
                pass
            self._jdbc_rs = None
        if self._jdbc_stmt is not None:
            try:
                self._jdbc_stmt.close()
            except Exception:
                pass
            self._jdbc_stmt = None
        self._jdbc_meta = None
        self._description = None

    def _close_resultset(self) -> None:
        """Close the current ResultSet if any."""
        if self._jdbc_rs is not None:
            try:
                self._jdbc_rs.close()
            except Exception:
                pass
            self._jdbc_rs = None
            self._jdbc_meta = None

    def _close_statement(self) -> None:
        """Close the current Statement if any."""
        if self._jdbc_stmt is not None:
            try:
                self._jdbc_stmt.close()
            except Exception:
                pass
            self._jdbc_stmt = None

    def execute(self, operation: str, parameters: Sequence = None) -> "Cursor":
        """
        Execute a database operation (query or command).

        Args:
            operation: SQL query or command to execute
            parameters: Optional sequence of parameters for the query

        Returns:
            self
        """
        self._check_closed()
        self._close_resultset()
        self._close_statement()
        self._description = None
        self._rowcount = -1
        self._column_converters = None

        try:
            jdbc_conn = self._connection._jdbc_conn

            if parameters:
                # Use PreparedStatement for parameterized queries
                self._jdbc_stmt = jdbc_conn.prepareStatement(operation)
                self._set_parameters(parameters)

                # Set timeout if specified
                if self._connection.timeout > 0:
                    self._jdbc_stmt.setQueryTimeout(self._connection.timeout)

                # Set fetch size hint if arraysize is set
                if self._arraysize > 1:
                    self._jdbc_stmt.setFetchSize(self._arraysize)

                has_result = self._jdbc_stmt.execute()
            else:
                # Use Statement for simple queries
                self._jdbc_stmt = jdbc_conn.createStatement()

                # Set timeout if specified
                if self._connection.timeout > 0:
                    self._jdbc_stmt.setQueryTimeout(self._connection.timeout)

                # Set fetch size hint if arraysize is set
                if self._arraysize > 1:
                    self._jdbc_stmt.setFetchSize(self._arraysize)

                has_result = self._jdbc_stmt.execute(operation)

            if has_result:
                self._jdbc_rs = self._jdbc_stmt.getResultSet()
                self._jdbc_meta = self._jdbc_rs.getMetaData()
                self._build_description()
            else:
                self._rowcount = self._jdbc_stmt.getUpdateCount()

        except Exception as e:
            _handle_sql_exception_from(e)

        return self

    def executemany(
        self, operation: str, seq_of_parameters: Sequence[Sequence]
    ) -> "Cursor":
        """
        Execute a database operation multiple times with different parameters.

        Uses JDBC batch execution for better performance.

        Args:
            operation: SQL query or command to execute
            seq_of_parameters: Sequence of parameter sequences

        Returns:
            self
        """
        self._check_closed()
        self._close_resultset()
        self._close_statement()
        self._description = None
        self._rowcount = -1
        self._column_converters = None

        if not seq_of_parameters:
            return self

        try:
            jdbc_conn = self._connection._jdbc_conn

            # Use PreparedStatement with batch execution
            self._jdbc_stmt = jdbc_conn.prepareStatement(operation)

            # Set timeout if specified
            if self._connection.timeout > 0:
                self._jdbc_stmt.setQueryTimeout(self._connection.timeout)

            # Add each parameter set to the batch
            for parameters in seq_of_parameters:
                self._set_parameters(parameters)
                self._jdbc_stmt.addBatch()

            # Execute the batch and sum up affected rows
            update_counts = self._jdbc_stmt.executeBatch()
            self._rowcount = sum(int(count) for count in update_counts)

        except Exception as e:
            _handle_sql_exception_from(e)

        return self

    def fetchone(self) -> Optional[Tuple]:
        """
        Fetch the next row of a query result set.

        Returns:
            A single tuple, or None when no more data is available
        """
        self._check_closed()
        if self._jdbc_rs is None:
            raise InterfaceError("No result set available")

        try:
            if self._jdbc_rs.next():
                return self._fetch_row()
            return None
        except Exception as e:
            _handle_sql_exception_from(e)

    def fetchmany(self, size: int = None) -> List[Tuple]:
        """
        Fetch the next set of rows of a query result.

        Args:
            size: Number of rows to fetch (default: arraysize)

        Returns:
            A list of tuples

        Note:
            This method sets the fetch size hint on the ResultSet before fetching
            rows and resets it to 0 afterwards.
        """
        self._check_closed()
        if self._jdbc_rs is None:
            raise InterfaceError("No result set available")

        if size is None:
            size = self._arraysize

        rows = []
        try:
            # Set fetch size hint on ResultSet
            self._jdbc_rs.setFetchSize(size)

            for _ in range(size):
                if self._jdbc_rs.next():
                    rows.append(self._fetch_row())
                else:
                    break

            # Reset fetch size
            self._jdbc_rs.setFetchSize(0)
        except Exception as e:
            _handle_sql_exception_from(e)

        return rows

    def fetchall(self) -> List[Tuple]:
        """
        Fetch all remaining rows of a query result.

        Returns:
            A list of tuples
        """
        self._check_closed()
        if self._jdbc_rs is None:
            raise InterfaceError("No result set available")

        rows = []
        try:
            while self._jdbc_rs.next():
                rows.append(self._fetch_row())
        except Exception as e:
            _handle_sql_exception_from(e)

        return rows

    def setinputsizes(self, sizes: Sequence) -> None:
        """No-op for DB-API 2.0 compatibility."""
        pass

    def setoutputsize(self, size: int, column: int = None) -> None:
        """No-op for DB-API 2.0 compatibility."""
        pass

    def _check_closed(self) -> None:
        """Raise an error if the cursor is closed."""
        if self._closed:
            raise InterfaceError("Cursor is closed")

    def _set_parameters(self, parameters: Sequence) -> None:
        """Set parameters on the PreparedStatement."""
        for i, param in enumerate(parameters, start=1):
            if param is None:
                self._jdbc_stmt.setNull(i, jpype.java.sql.Types.NULL)
            elif isinstance(param, bool):
                self._jdbc_stmt.setBoolean(i, param)
            elif isinstance(param, int):
                self._jdbc_stmt.setLong(i, param)
            elif isinstance(param, float):
                self._jdbc_stmt.setDouble(i, param)
            elif isinstance(param, str):
                self._jdbc_stmt.setString(i, param)
            elif isinstance(param, bytes):
                self._jdbc_stmt.setBytes(i, param)
            elif isinstance(param, datetime.datetime):
                ts = jpype.java.sql.Timestamp(int(param.timestamp() * 1000))
                self._jdbc_stmt.setTimestamp(i, ts)
            elif isinstance(param, datetime.date):
                d = jpype.java.sql.Date(param.year - 1900, param.month - 1, param.day)
                self._jdbc_stmt.setDate(i, d)
            elif isinstance(param, datetime.time):
                t = jpype.java.sql.Time(param.hour, param.minute, param.second)
                self._jdbc_stmt.setTime(i, t)
            else:
                self._jdbc_stmt.setObject(i, param)

    def _build_description(self) -> None:
        """Build the cursor description from ResultSet metadata."""
        if self._jdbc_rs is None:
            self._description = None
            return

        try:
            meta = self._jdbc_rs.getMetaData()
            col_count = meta.getColumnCount()

            desc = []
            converters = []

            for i in range(1, col_count + 1):
                name = meta.getColumnName(i)
                jdbc_type_code = meta.getColumnType(i)
                jdbc_type_name = _jdbc_type_const_to_name.get(jdbc_type_code, "OTHER")
                dbapi_type = _JDBC_TYPE_TO_DBAPI.get(jdbc_type_name, STRING)
                display_size = meta.getColumnDisplaySize(i)
                internal_size = display_size
                precision = meta.getPrecision(i)
                scale = meta.getScale(i)
                nullable = meta.isNullable(i) != 0  # 0 = columnNoNulls

                desc.append(
                    (
                        name,
                        dbapi_type,
                        display_size,
                        internal_size,
                        precision,
                        scale,
                        nullable,
                    )
                )

                # Get converter for this column type
                converter = _jdbc_type_converters.get(jdbc_type_code, _from_jdbc_object)
                converters.append(converter)

            self._description = tuple(desc)
            self._column_converters = converters

        except Exception as e:
            _handle_sql_exception_from(e)

    def _fetch_row(self) -> Tuple:
        """Fetch a single row from the ResultSet and convert to Python types."""
        if self._column_converters is None:
            self._build_description()

        row = []
        for i, converter in enumerate(self._column_converters, start=1):
            try:
                value = converter(self._jdbc_rs, i)
                row.append(value)
            except Exception:
                # Fallback to getObject if converter fails
                row.append(self._jdbc_rs.getObject(i))

        return tuple(row)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def __iter__(self):
        return self

    def __next__(self):
        row = self.fetchone()
        if row is None:
            raise StopIteration
        return row


# =============================================================================
# Module-Level Functions
# =============================================================================


def _get_jdbc_driver_jar_paths() -> List[str]:
    """Return jar paths from SCOS_JDBC_DRIVER_JARS env var (set by snowpark-submit)."""
    raw = os.environ.get(_SCOS_JDBC_DRIVER_JARS_ENV, "")
    if not raw:
        return []
    return [p.strip() for p in raw.split(os.path.pathsep) if p.strip()]


def _ensure_driver_loaded(jclassname: str) -> None:
    """Ensure the JDBC driver class is registered with DriverManager.

    Strategy:
    1. If the class is already loadable via the system classloader (e.g. added
       via spark.jars / CLASSPATH before JVM start), do nothing — it self-
       registers via the JDBC 4.0 ServiceLoader mechanism on first load.
    2. Otherwise, build an isolated URLClassLoader whose parent is the JVM
       platform classloader.  This means only JDK platform modules (java.sql,
       javax.sql, …) are inherited; none of SCOS's own Jackson, Scala, Hadoop,
       etc. jars are visible to the driver, eliminating classpath collision risk.
       (Using null/bootstrap would work in Java 8 but java.sql is a platform
       module in Java 9+ and requires the platform classloader.)
    3. Wrap the loaded driver instance in a JPype @JImplements proxy so that
       DriverManager.isDriverAllowed() accepts it (the check uses
       Class.forName(driver.class.getName(), callerClassLoader) and rejects
       drivers whose class is not visible from the caller's loader — the proxy
       class is created by JPype's own loader which is always accessible).
    """
    with _isolated_drivers_lock:
        if jclassname in _isolated_drivers_registered:
            return

        # Fast path: driver already on the system classloader (spark.jars / CLASSPATH).
        try:
            jpype.JClass(jclassname)
            _isolated_drivers_registered.add(jclassname)
            return
        except Exception:
            pass

        jar_paths = _get_jdbc_driver_jar_paths()
        if not jar_paths:
            raise InterfaceError(
                f"JDBC driver class '{jclassname}' not found on the server classpath "
                f"and {_SCOS_JDBC_DRIVER_JARS_ENV} is not set. "
                "Pass the driver jar via --jars or bundle it in the application fat jar."
            )

        File = jpype.JClass("java.io.File")
        URL = jpype.JClass("java.net.URL")
        URLClassLoader = jpype.JClass("java.net.URLClassLoader")

        url_array = jpype.JArray(URL)([File(p).toURI().toURL() for p in jar_paths])
        platform_cl = jpype.JClass("java.lang.ClassLoader").getPlatformClassLoader()
        loader = URLClassLoader(url_array, platform_cl)

        try:
            driver_class = loader.loadClass(jclassname)
        except Exception as e:
            raise InterfaceError(
                f"Failed to load JDBC driver class '{jclassname}' from {jar_paths}: {e}"
            )

        try:
            driver_instance = driver_class.getDeclaredConstructor().newInstance()
        except Exception as e:
            raise InterfaceError(
                f"Failed to instantiate JDBC driver '{jclassname}': {e}"
            )

        # DriverManager.isDriverAllowed() tries to load the driver's class via the
        # caller's classloader.  A driver loaded from an isolated URLClassLoader is
        # invisible to the system classloader, so the check fails and getConnection
        # never routes to that driver.  Wrapping in a @JImplements proxy sidesteps
        # this: JPype creates the proxy class in its own loader (a child of the
        # system loader), so it IS visible and the check passes.
        @jpype.JImplements("java.sql.Driver")
        class _DriverShim:
            @jpype.JOverride
            def connect(self, url, info):
                return driver_instance.connect(url, info)

            @jpype.JOverride
            def acceptsURL(self, url):
                return driver_instance.acceptsURL(url)

            @jpype.JOverride
            def getMajorVersion(self):
                return driver_instance.getMajorVersion()

            @jpype.JOverride
            def getMinorVersion(self):
                return driver_instance.getMinorVersion()

            @jpype.JOverride
            def jdbcCompliant(self):
                return driver_instance.jdbcCompliant()

            @jpype.JOverride
            def getPropertyInfo(self, url, info):
                return driver_instance.getPropertyInfo(url, info)

            @jpype.JOverride
            def getParentLogger(self):
                return driver_instance.getParentLogger()

        jpype.java.sql.DriverManager.registerDriver(_DriverShim())
        _isolated_drivers_registered.add(jclassname)


def connect(
    jclassname: str,
    url: str,
    driver_args: Union[Dict[str, str], Sequence] = None,
    jars: Sequence[str] = None,
    libs: Sequence[str] = None,
) -> Connection:
    """
    Create a connection to a JDBC database.

    Args:
        jclassname: The JDBC driver class name (e.g., "com.mysql.jdbc.Driver")
        url: The JDBC URL (e.g., "jdbc:mysql://localhost/test")
        driver_args: Either a dictionary of connection properties (user, password, etc.)
                    or a sequence [user, password]
        jars: Optional list of JAR files to add to classpath
        libs: Optional list of native library paths

    Returns:
        A Connection object

    Example:
        conn = connect(
            "com.mysql.jdbc.Driver",
            "jdbc:mysql://localhost/test",
            {"user": "root", "password": "secret"}
        )
    """
    jdbc_conn = _jdbc_connect(jclassname, url, driver_args, jars, libs)
    return Connection(jdbc_conn)


def _jdbc_connect(jclassname, url, driver_args, jars, libs):
    """Internal function to create a JDBC connection using JPype."""
    global _java_array_byte

    # JVM must already be started by SCOS
    if not jpype.isJVMStarted():
        raise InterfaceError(
            "JVM is not started. SCOS should have already started the JVM before "
            "calling jdbc_utils. Please ensure the JVM is initialized first."
        )

    # Attach thread to JVM if not already attached
    if not jpype.isThreadAttachedToJVM():
        jpype.attachThreadToJVM()
        jpype.java.lang.Thread.currentThread().setContextClassLoader(
            jpype.java.lang.ClassLoader.getSystemClassLoader()
        )

    # Initialize JDBC type mappings if not done yet
    if _jdbc_type_name_to_const is None:
        _init_jdbc_types_from_jvm()

    # Initialize byte array helper
    if _java_array_byte is None:

        def _java_array_byte(data):
            return jpype.JArray(jpype.JByte, 1)(data)

    _ensure_driver_loaded(jclassname)

    # Build connection arguments
    if isinstance(driver_args, dict):
        Properties = jpype.java.util.Properties
        info = Properties()
        for k, v in driver_args.items():
            if v is not None:
                info.setProperty(str(k), str(v))
        connection_args = [info]
    elif driver_args:
        connection_args = list(driver_args)
    else:
        connection_args = []

    # Create the connection
    try:
        return jpype.java.sql.DriverManager.getConnection(url, *connection_args)
    except Exception as e:
        raise DatabaseError(f"Failed to connect to database: {e}")


def _init_jdbc_types_from_jvm() -> None:
    """Initialize JDBC type mappings from the JVM."""
    global _jdbc_type_name_to_const
    global _jdbc_type_const_to_name

    jdbc_types = jpype.java.sql.Types
    jdbc_types_map = {}

    for field in jdbc_types.class_.getFields():
        if jpype.java.lang.reflect.Modifier.isStatic(field.getModifiers()):
            const = field.get(None)
            jdbc_types_map[field.getName()] = const

    _jdbc_type_name_to_const = jdbc_types_map
    _jdbc_type_const_to_name = {v: k for k, v in jdbc_types_map.items()}
    _init_jdbc_type_converters(jdbc_types_map)


def _init_jdbc_type_converters(jdbc_types_map: Dict[str, int]) -> None:
    """Initialize converters for JDBC types to Python objects."""
    global _jdbc_type_converters
    _jdbc_type_converters = {}

    for type_name, converter in _DEFAULT_JDBC_CONVERTERS.items():
        if type_name in jdbc_types_map:
            const_val = jdbc_types_map[type_name]
            _jdbc_type_converters[const_val] = converter


def _handle_sql_exception_from(e: Exception) -> None:
    """Handle a JDBC SQLException and re-raise as appropriate DB-API exception."""
    SQLException = jpype.java.sql.SQLException

    if isinstance(e, SQLException):
        raise DatabaseError(str(e)) from e
    elif isinstance(e, (InterfaceError, DatabaseError)):
        raise
    else:
        raise InterfaceError(str(e)) from e


# =============================================================================
# JDBC Type Converters - Convert Java types to Python
# =============================================================================


def _from_jdbc_object(rs, col: int) -> Any:
    """Default converter - get object as-is."""
    java_val = rs.getObject(col)
    if java_val is None:
        return None
    # Convert common Java types to Python
    if isinstance(java_val, (str, int, float, bool)):
        return java_val
    return java_val


def _from_jdbc_string(rs, col: int) -> Optional[str]:
    """Convert JDBC string types to Python string."""
    return rs.getString(col)


def _from_jdbc_date(rs, col: int) -> Optional[str]:
    """Convert JDBC Date to Python string (ISO format)."""
    java_val = rs.getDate(col)
    if java_val is None:
        return None
    return str(java_val)[:10]


def _from_jdbc_time(rs, col: int) -> Optional[str]:
    """Convert JDBC Time to Python string."""
    java_val = rs.getTime(col)
    if java_val is None:
        return None
    return str(java_val)


def _from_jdbc_datetime(rs, col: int) -> Optional[str]:
    """Convert JDBC Timestamp to Python datetime string."""
    java_val = rs.getTimestamp(col)
    if java_val is None:
        return None
    # Parse the timestamp with nanoseconds
    d = datetime.datetime.strptime(str(java_val)[:19], "%Y-%m-%d %H:%M:%S")
    nanos = str(java_val.getNanos())
    if len(nanos) >= 6:
        d = d.replace(microsecond=int(nanos[:6]))
    return str(d)


def _from_jdbc_binary(rs, col: int) -> Optional[bytes]:
    """Convert JDBC binary types to Python bytes."""
    java_val = rs.getBytes(col)
    if java_val is None:
        return None
    return bytes(java_val)


def _from_jdbc_boolean(rs, col: int) -> Optional[bool]:
    """Convert JDBC boolean to Python bool."""
    java_val = rs.getObject(col)
    if java_val is None:
        return None
    if isinstance(java_val, bool):
        return java_val
    if hasattr(java_val, "booleanValue"):
        return java_val.booleanValue()
    return bool(java_val)


def _from_jdbc_int(rs, col: int) -> Optional[int]:
    """Convert JDBC integer types to Python int."""
    java_val = rs.getObject(col)
    if java_val is None:
        return None
    if isinstance(java_val, int):
        return java_val
    if hasattr(java_val, "intValue"):
        return java_val.intValue()
    if hasattr(java_val, "longValue"):
        return java_val.longValue()
    return int(java_val)


def _from_jdbc_bigint(rs, col: int) -> Optional[int]:
    """Convert JDBC BIGINT to Python int."""
    java_val = rs.getObject(col)
    if java_val is None:
        return None
    if isinstance(java_val, int):
        return java_val
    if hasattr(java_val, "longValue"):
        return java_val.longValue()
    return int(java_val)


def _from_jdbc_double(rs, col: int) -> Optional[float]:
    """Convert JDBC float/double types to Python float."""
    java_val = rs.getObject(col)
    if java_val is None:
        return None
    if isinstance(java_val, float):
        return java_val
    if hasattr(java_val, "doubleValue"):
        return java_val.doubleValue()
    return float(java_val)


def _from_jdbc_decimal(rs, col: int) -> Optional[Union[int, float]]:
    """Convert JDBC DECIMAL/NUMERIC to Python int or float based on scale."""
    java_val = rs.getObject(col)
    if java_val is None:
        return None
    if hasattr(java_val, "scale"):
        scale = java_val.scale()
        if scale == 0:
            return java_val.longValue()
        else:
            return java_val.doubleValue()
    elif isinstance(java_val, (int, float)):
        return java_val
    else:
        return float(java_val)


# Default converters for JDBC types
# These are standard JDBC types from java.sql.Types
_DEFAULT_JDBC_CONVERTERS = {
    # String types
    "CHAR": _from_jdbc_string,
    "VARCHAR": _from_jdbc_string,
    "LONGVARCHAR": _from_jdbc_string,
    "NCHAR": _from_jdbc_string,
    "NVARCHAR": _from_jdbc_string,
    "LONGNVARCHAR": _from_jdbc_string,
    "CLOB": _from_jdbc_string,
    "NCLOB": _from_jdbc_string,
    "SQLXML": _from_jdbc_string,
    # Binary types
    "BINARY": _from_jdbc_binary,
    "VARBINARY": _from_jdbc_binary,
    "LONGVARBINARY": _from_jdbc_binary,
    "BLOB": _from_jdbc_binary,
    # Boolean types
    "BIT": _from_jdbc_boolean,
    "BOOLEAN": _from_jdbc_boolean,
    # Integer types
    "TINYINT": _from_jdbc_int,
    "SMALLINT": _from_jdbc_int,
    "INTEGER": _from_jdbc_int,
    "BIGINT": _from_jdbc_bigint,
    # Float types
    "REAL": _from_jdbc_double,
    "FLOAT": _from_jdbc_double,
    "DOUBLE": _from_jdbc_double,
    # Decimal types
    "DECIMAL": _from_jdbc_decimal,
    "NUMERIC": _from_jdbc_decimal,
    # Date/Time types
    "DATE": _from_jdbc_date,
    "TIME": _from_jdbc_time,
    "TIME_WITH_TIMEZONE": _from_jdbc_time,
    "TIMESTAMP": _from_jdbc_datetime,
    "TIMESTAMP_WITH_TIMEZONE": _from_jdbc_datetime,
    # Other standard JDBC types - use generic object converter
    # JAVA_OBJECT and OTHER may contain complex objects (e.g., Neo4j's ArrayList)
    # that need to be returned as-is for the caller to handle
    "JAVA_OBJECT": _from_jdbc_object,
    "OTHER": _from_jdbc_object,
    "ARRAY": _from_jdbc_object,
    "STRUCT": _from_jdbc_object,
    "REF": _from_jdbc_object,
    "DATALINK": _from_jdbc_string,
    "DISTINCT": _from_jdbc_object,
    "REF_CURSOR": _from_jdbc_object,
}


# =============================================================================
# Utility Functions for Backward Compatibility
# =============================================================================


def detach_thread_from_jvm() -> None:
    """Detach the current thread from the JVM."""
    if jpype.isThreadAttachedToJVM():
        jpype.detachThreadFromJVM()
