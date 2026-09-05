"""
Thin DBAPI-2 wrapper around adbc_driver_flightsql.dbapi.

SQLAlchemy's DefaultDialect calls ``dialect.dbapi()`` (a classmethod) to get
the DBAPI module, then uses ``module.connect(**kwargs)`` to open connections.
We simply re-export ``adbc_driver_flightsql.dbapi`` so that all PEP-249
symbols (connect, Error, Warning, …) are available at the module level.
"""
from adbc_driver_flightsql.dbapi import (  # noqa: F401
    BINARY,
    DATETIME,
    NUMBER,
    ROWID,
    STRING,
    Connection,
    Cursor,
    DatabaseError,
    DataError,
    Date,
    DateFromTicks,
    Error,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    Time,
    TimeFromTicks,
    Timestamp,
    TimestampFromTicks,
    Warning,
    connect,
)

apilevel = "2.0"
threadsafety = 1
paramstyle = "qmark"
