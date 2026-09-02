#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from datetime import date, datetime
import re
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union, cast
import warnings

from sqlalchemy import BindParameter, ClauseElement, Executable, TextClause, bindparam, text
from sqlalchemy.dialects import sqlite
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.engine.result import IteratorResult, SimpleResultMetaData
from sqlalchemy.exc import StatementError
from sqlalchemy.sql import visitors
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy.sql.visitors import ExternallyTraversible
from strenum import StrEnum

from datarobot.models.data_store import DataStore
from datarobot.models.jdbc_data_preview import (
    JdbcPreview,
    JdbcPreviewData,
    get_parsed_jdbc_data_records_iter,
)


class QueryModeAmbiguousWarning(UserWarning):
    """
    Raised when the mode with which to execute a statement is ambiguous.
    QueryEngine will use best-efforts heuristic to guess the mode to execute a statement.
    """

    pass


warnings.filterwarnings("always", category=QueryModeAmbiguousWarning)


# Keywords whose statements are expected to return a result set.
# Covers most popular SQL dialects. Best-efforts heuristic.
_QUERY_KEYWORDS: frozenset[str] = frozenset({
    "SELECT",  # standard query — all dialects
    "WITH",  # CTEs (WITH … SELECT/INSERT/…); heuristically treated as a query
    "TABLE",  # PostgreSQL/MySQL shorthand for SELECT * FROM <table>
    "VALUES",  # standalone VALUES clause (PostgreSQL, SQL Server, SQLite)
    "SHOW",  # SHOW TABLES / SHOW COLUMNS / SHOW VARIABLES — MySQL, PostgreSQL, Snowflake, …
    "DESCRIBE",  # DESCRIBE <table> — MySQL, Snowflake, BigQuery, Oracle
    "DESC",  # alias for DESCRIBE — MySQL, Oracle, Snowflake
    "EXPLAIN",  # EXPLAIN / EXPLAIN ANALYZE — returns execution-plan rows in most dialects
    "CALL",  # stored-procedure calls that return a result set — MySQL, PostgreSQL, Snowflake
})

_SQL_COMMENT_RE = re.compile(
    r"/\*.*?\*/|--[^\n]*",
    re.DOTALL,
)
_FIRST_TOKEN_RE = re.compile(r"[A-Za-z_]\w*")
# Matches a RETURNING clause (PostgreSQL 17+, SQLite, MariaDB, …), which causes an otherwise
# non-query DML statement (INSERT/UPDATE/DELETE/MERGE) to return rows. Best-efforts heuristic:
# may false-positive if "RETURNING" appears inside a string literal or identifier.
_RETURNING_RE = re.compile(r"\bRETURNING\b", re.IGNORECASE)


def is_query_statement(sql: str) -> bool:
    """
    Check if a SQL statement is likely to produce a result set that should be
    routed via query mode. Best-efforts heuristic.

    Parameters
    ----------
    sql:
        SQL statement to check.

    Returns
    -------
    bool
        True if the statement is likely to return rows: either it starts with a keyword
        that always returns rows (SELECT, SHOW, EXPLAIN, …), or it is a DML statement
        (INSERT, UPDATE, DELETE, MERGE, …) with a trailing RETURNING clause.
        False if the statement is likely a DML/DDL side-effect with no result set
        (INSERT, UPDATE, DROP, plain MERGE, …).
    """
    cleaned = _SQL_COMMENT_RE.sub(" ", sql)
    match = _FIRST_TOKEN_RE.search(cleaned)
    if not match:
        return False
    if match.group(0).upper() in _QUERY_KEYWORDS:
        return True
    return bool(_RETURNING_RE.search(cleaned))


BoundParam = Optional[Union[str, int, float, bool, datetime, date]]


class IConnectionManager:
    """Interface for connection managers"""

    def query(
        self, sql: str, parameters: Optional[List[BoundParam]] = None, max_rows: int = 1000, **kwargs: Any
    ) -> JdbcPreviewData:
        """
        Execute a SQL query and return the result as a
        :class:`JdbcPreviewData <datarobot.models.jdbc_data_preview.JdbcPreviewData>` object.

        Parameters
        ----------
        sql:
            The SQL query to execute.
        parameters:
            Parameters to bind to the statement.
        max_rows:
            The maximum number of rows to return.
        kwargs:
            Additional keyword arguments for future-proofing.

        Returns
        -------
        :class:`JdbcPreviewData <datarobot.models.jdbc_data_preview.JdbcPreviewData>`:
            Data returned from the query.
        """
        raise NotImplementedError

    def execute_update(self, sql: str, parameters: Optional[List[BoundParam]] = None, **kwargs: Any) -> None:
        """
        Execute an SQL statement.

        Parameters
        ----------
        sql:
            The SQL statement to execute.
        parameters:
            Parameters to bind to the statement.
        kwargs:
            Additional keyword arguments for future-proofing.

        Raises
        ------
        StatementError:
            If the statement is not successful.
        """
        raise NotImplementedError


class JdbcConnectionManager(IConnectionManager):
    """Manage the connection parameters for a JDBC database connection."""

    def __init__(
        self,
        jdbc_url: Optional[str] = None,
        jdbc_params: Optional[Dict[str, str]] = None,
        jdbc_url_generator: Optional[Callable[[], str]] = None,
    ):
        if jdbc_url is None and jdbc_url_generator is None:
            raise ValueError("Either jdbc_url or jdbc_url_generator must be provided")
        if jdbc_url is not None and jdbc_url_generator is not None:
            raise ValueError("Only one of jdbc_url or jdbc_url_generator must be provided")

        if jdbc_url_generator is not None:
            self._get_jdbc_url = jdbc_url_generator
        else:
            assert jdbc_url is not None
            self._get_jdbc_url = lambda: jdbc_url
        self.jdbc_params = jdbc_params

    @property
    def jdbc_url(self) -> str:
        return self._get_jdbc_url()

    def query(
        self, sql: str, parameters: Optional[List[BoundParam]] = None, max_rows: int = 1000, **kwargs: Any
    ) -> JdbcPreviewData:
        return JdbcPreview.preview(
            jdbc_url=self.jdbc_url,
            parameters=self.jdbc_params,
            sql=sql,
            max_rows=max_rows,
            bind_parameters=parameters,
            **kwargs,
        )

    def execute_update(self, sql: str, parameters: Optional[List[BoundParam]] = None, **kwargs: Any) -> None:
        message = JdbcPreview.execute_update(
            jdbc_url=self.jdbc_url, parameters=self.jdbc_params, sql=sql, bind_parameters=parameters, **kwargs
        )
        if not DataStore.is_execute_update_success(message):
            raise StatementError(message=message, statement=sql, params=parameters, orig=None)


class DataStoreConnectionManager(IConnectionManager):
    """Manage the connection parameters for a DataStore connection."""

    def __init__(self, data_store_id: str, credential_id: Optional[str] = None):
        self.data_store: DataStore = DataStore.get(data_store_id)
        self.credential_id = credential_id

    def query(
        self, sql: str, parameters: Optional[List[BoundParam]] = None, max_rows: int = 1000, **kwargs: Any
    ) -> JdbcPreviewData:
        return self.data_store.preview_query(
            sql, credential_id=self.credential_id, bind_parameters=parameters, max_rows=max_rows, **kwargs
        )

    def execute_update(self, sql: str, parameters: Optional[List[BoundParam]] = None, **kwargs: Any) -> None:
        message = self.data_store.execute_update(
            sql, credential_id=self.credential_id, bind_parameters=parameters, **kwargs
        )
        if not DataStore.is_execute_update_success(message):
            raise StatementError(message=message, statement=sql, params=parameters, orig=None)


class QueryMode(StrEnum):
    """
    Mode with which to execute a SQL statement.
    Can be used to override the best-efforts heuristic for determining the mode.

    Examples
    --------
    Override QueryEngine's guess at determining the mode to ensure you get results back:

    .. code-block:: python

        >>> from datarobot.query_engine import QueryMode, QueryEngine
        >>> engine = QueryEngine.from_jdbc_connection(jdbc_url="jdbc:postgresql://localhost:5432/mydb")
        >>> results = engine.execute(
        ...     "UPDATE users SET status = 'active' WHERE name = 'John Doe' RETURNING id, name, status",
        ...     mode=QueryMode.QUERY, # overrides QueryEngine's guess of the mode to ensure you get results back
        ... )
        >>> results.all()
        [(1, "John Doe", "active")]
    """

    #: Assumed to return rows.
    QUERY = "query"
    #: Executes the statement without returning any results.
    EXECUTE_UPDATE = "execute_update"


class QueryEngine:
    """
    Execute SQL statements against a database through DataRobot. Supports statements as strings
    or SQLAlchemy constructs.

    Parameters
    ----------
    connection_manager:
        The connection manager to use to execute statements against a database.
    dialect:
        The SQL dialect to use to compile statements. Modifies how SQLAlchemy constructs are compiled to
        their database-specific SQL strings. Defaults to sqlite.dialect().
    paramstyle:
        The parameter style used to bind parameters to the statement. By default, "qmark" is used, which
        uses ``?`` placeholders for parameters. Named parameters will be substituted in the SQL string according
        to the parameter name.
    **kwargs:
        Additional keyword arguments for future-proofing.

    Notes
    -----
    When executing statements using SQLAlchemy constructs, ``dialect`` should be provided to
    ensure correct compilation.

    Examples
    --------
    Execute a query against a DataStore using QueryEngine:

    .. code-block:: python

        >>> from datarobot.query_engine import QueryEngine
        >>> engine = QueryEngine.from_data_store(
        ...     data_store_id="my_data_store_id",
        ...     credential_id="my_credential_id",
        ... )
        >>> result: IteratorResult = engine.execute(
        ...     "SELECT * FROM my_table WHERE name = :name AND status IN :statuses",
        ...     params={
        ...         "name": "John Doe",
        ...         "statuses": ["active", "pending"]
        ...     }
        ... )
        >>> result.all()
        [(1, "John Doe", "active"), (2, "Jane Doe", "pending")]

    Execute an update against a MS SQL Server database through a JDBC connection using QueryEngine
    and SQLAlchemy constructs. Note the ``dialect`` parameter is provided to ensure correct compilation:

    .. code-block:: python

        >>> from sqlalchemy import insert, table, bindparam, column
        >>> from sqlalchemy.dialects import mssql
        >>> USER_TABLE = table("users", column("name"), column("status"))
        >>> engine = QueryEngine.from_jdbc_connection(
        ...     jdbc_url="jdbc:sqlserver://localhost:1433;databaseName=mydb",
        ...     jdbc_params={"user": "sa", "password": "myPassword"},
        ...     dialect=mssql.dialect(),
        ... )
        >>> engine.execute(
        ...     insert(USER_TABLE).values(name="John Doe", status=bindparam("status")),
        ...     params={"status": "active"},
        ... )
    """

    def __init__(
        self,
        connection_manager: IConnectionManager,
        *,
        dialect: Optional[Dialect] = None,
        paramstyle: Optional[str] = None,
    ):
        self.connection_manager = connection_manager

        dialect = dialect or sqlite.dialect()
        paramstyle = paramstyle or "qmark"
        self.dialect = type(dialect)(paramstyle=paramstyle)  # type: ignore[call-arg]

    def _to_qmark_sql_and_bound_params(
        self,
        stmt: Union[str, Executable],
        params: Optional[Dict[str, Union[BoundParam, List[BoundParam], Tuple[BoundParam, ...]]]] = None,
        params_to_expand: Iterable[str] = (),
    ) -> Tuple[str, List[BoundParam]]:
        """
        Given a statement (string or SQLAlchemy construct) and named parameter dict, compile to a SQL string with
        placeholders and an ordered list of values, one for each placeholder.
        """
        sql_stmt: ClauseElement = text(stmt) if isinstance(stmt, str) else cast(ClauseElement, stmt)
        is_text = isinstance(sql_stmt, TextClause)

        if is_text and params:
            binds: List[BindParameter[Any]] = [
                bindparam(k, value=v, expanding=(k in params_to_expand)) for k, v in params.items()
            ]
            sql_stmt = cast(TextClause, sql_stmt).bindparams(*binds)
        elif params:  # SELECT, UPDATE, DELETE, INSERT, etc. constructs.
            params_to_expand = set(params_to_expand)

            def _bind_value(bp: BindParameter[Any]) -> None:
                if bp.key in params:
                    bp.value = params[bp.key]
                    bp.required = False
                    if bp.key in params_to_expand:
                        bp.expanding = True

            sql_stmt = cast(
                ClauseElement,
                visitors.cloned_traverse(cast(ExternallyTraversible, sql_stmt), {}, {"bindparam": _bind_value}),
            )

        compiled = cast(
            SQLCompiler, sql_stmt.compile(dialect=self.dialect, compile_kwargs={"render_postcompile": True})
        )
        bound = compiled.construct_params()

        sql = str(compiled)
        if not is_text:
            # compilation for some constructs adds newlines (ignore for text clauses)
            sql = sql.replace('\n', ' ')

        if bound is None or compiled.positiontup is None:
            return sql, []

        return sql, [bound[k] for k in compiled.positiontup]

    def execute(
        self,
        stmt: Union[str, Executable],
        params: Optional[Dict[str, Union[BoundParam, List[BoundParam], Tuple[BoundParam, ...]]]] = None,
        *,
        max_rows: int = 1000,
        mode: Optional[QueryMode] = None,
        **kwargs: Any,
    ) -> IteratorResult[Any]:
        """
        Execute a SQL statement against a database. Supports string statements and SQLAlchemy constructs.
        Supports named parameters only.

        Uses best-efforts to determine if the statement will return rows. Use ``mode`` to
        override this behavior. No results are returned for non-query statements.

        Notes
        -----
        If a parameter is a list or tuple, it will always be expanded. Replacement of a single parameter
        with a list or tuple is not supported. See examples below for more details.

        Parameters
        ----------
        stmt:
            The SQL statement to execute. Supports string statements and SQLAlchemy constructs.
        params:
            Named parameters to bind to the statement. Supports scalar, list, and tuple values.
        max_rows:
            The maximum number of rows to return. Only used for query-type statements.
        mode:
            The mode to execute the statement. Overrides best-efforts to determine the mode.
        **kwargs:
            Additional keyword arguments passed to ``query`` or ``execute_update``.

        Returns
        -------
        sqlalchemy.engine.result.IteratorResult
            The result of the statement.
            If the statement is a query, returns an IteratorResult with the result of the query.
            If the statement is an update, returns an IteratorResult with an empty result.

        Examples
        --------
        Execute plain SQL string:

        .. code-block:: python

            >>> from datarobot.query_engine import QueryEngine
            >>> engine = QueryEngine.from_jdbc_connection(jdbc_url="jdbc:postgresql://localhost:5432/mydb")
            >>> results = engine.execute("SELECT * FROM users")
            >>> results.all()
            [(1, "John Doe")]

        Execute SQL query with named parameters:

        .. code-block:: python

            >>> engine.execute("SELECT * FROM users WHERE name = :name", params={"name": "John Doe"})
            >>> # Compiles to: SELECT * FROM users WHERE name = ?

            >>> results.all()
            [(1, "John Doe")]

        Execute SQL query with named parameter that will be expanded. Note the expansion
        of the age parameter to ``(?, ?, ?)``:

        .. code-block:: python

            >>> engine.execute(
            ...     "SELECT * FROM users WHERE name = :name AND age IN :ages",
            ...     params={"name": "John Doe", "ages": (30, 40, 50)},
            ... )
            >>> # Compiles to: SELECT * FROM users WHERE name = ? AND age IN (?, ?, ?)
            >>> results.all()
            [(1, "John Doe", 30), (1, "John Doe", 40), (1, "John Doe", 50)]

        Execute SQL statement to insert record with named parameter and parameter that will be
        expanded:

        .. code-block:: python

            >>> engine.execute(
            ...     "INSERT INTO users (name, brothers) VALUES (:name, :brother_names)",
            ...     params={
            ...         "name": "John Doe",
            ...         "brother_names": ["Jim Doe", "Jack Doe"]
            ...     },
            ... )
            >>> # Compiles to: INSERT INTO users (name, brothers) VALUES (?, (?, ?))

        Execute SQLAlchemy select with named and bound parameters:

        .. code-block:: python

            >>> from sqlalchemy import select, bindparam, column, table
            >>> USER_TABLE = table("users", column("name"), column("status"))
            >>> results = engine.execute(
            ...     select(USER_TABLE)
            ...         .where(USER_TABLE.c.name == "John Doe")
            ...         .where(USER_TABLE.c.status == bindparam("status")),
            ...     params={"status": "active"},
            ... )
            >>> results.all()
            [("John Doe", "active")]

        Execute SQLAlchemy insert statement with bound parameter:

        .. code-block:: python

            >>> from sqlalchemy import insert
            >>> USER_TABLE = table("users", column("name"), column("status"))
            >>> results = engine.execute(
            ...     insert(USER_TABLE).values(name="John Doe", status=bindparam("status")),
            ...     params={"status": "active"},
            ... )
        """
        params_to_expand = []
        if params:
            for param, value in params.items():
                if isinstance(value, (list, tuple)):
                    params_to_expand.append(param)

        sql, bound_params = self._to_qmark_sql_and_bound_params(
            stmt=stmt, params=params, params_to_expand=params_to_expand
        )
        sql_params = bound_params or None

        if mode is None:
            warning_message = (
                "QueryMode not set, QueryEngine will guess the mode with which to execute the statement. "
                "Pass mode=QueryMode.QUERY or mode=QueryMode.EXECUTE_UPDATE to avoid this warning."
            )
            warnings.warn(warning_message, QueryModeAmbiguousWarning, stacklevel=2)

        is_read = mode == QueryMode.QUERY if mode is not None else is_query_statement(sql)
        if is_read:
            payload = self.connection_manager.query(sql, max_rows=max_rows, parameters=sql_params, **kwargs)
            metadata = SimpleResultMetaData(payload.columns)
            return IteratorResult(
                metadata, get_parsed_jdbc_data_records_iter(payload.records, payload.columns, payload.result_schema)
            )

        self.connection_manager.execute_update(sql, parameters=sql_params, **kwargs)
        return IteratorResult(SimpleResultMetaData([]), iter(()))

    @classmethod
    def from_jdbc_connection(
        cls,
        jdbc_url: Optional[str] = None,
        jdbc_url_generator: Optional[Callable[[], str]] = None,
        jdbc_params: Optional[Dict[str, str]] = None,
        dialect: Optional[Dialect] = None,
        paramstyle: Optional[str] = None,
        **kwargs: Any,
    ) -> QueryEngine:
        """
        Create a QueryEngine from credentials for a JDBC database connection.

        Parameters
        ----------
        jdbc_url:
            The JDBC URL of the database.
        jdbc_params:
            The JDBC parameters to use for the connection.
        jdbc_url_generator:
            A function that returns a JDBC URL. Used to generate a JDBC URL for each connection if required.
        **kwargs:
            Additional keyword arguments to pass to the QueryEngine constructor.

        Other Parameters
        ----------------
        dialect: sqlalchemy.dialects.Dialect
            The SQL dialect to use to compile statements. Modifies how SQLAlchemy constructs are compiled to
            their database-specific SQL strings.
        paramstyle: str
            The parameter style used to bind parameters to the statement. By default, "qmark" is used, which
            uses ``?`` placeholders for parameters. Named parameters will be substituted in the SQL string according
            to the parameter name.

        Notes
        -----
        When constructing a QueryEngine to execute statements using SQLAlchemy constructs, ``dialect`` should be
        provided to ensure correct compilation. For example, for MS SQL Server, pass ``dialect=mssql.dialect()``.

        Examples
        --------
        Create a QueryEngine from a JDBC URL:

        .. code-block:: python

            >>> from datarobot.query_engine import QueryEngine
            >>> engine = QueryEngine.from_jdbc_connection(
            ...     jdbc_url="jdbc:postgresql://localhost:5432/mydb",
            ...     jdbc_params={"user": "postgres", "password": "postgres"},
            ... )

        Create a QueryEngine with a JDBC URL that has to be generated dynamically:

        .. code-block:: python

            >>> engine = QueryEngine.from_jdbc_connection(
            ...     jdbc_url_generator=my_function_here",
            ...     jdbc_params={"user": "postgres", "password": "postgres"},
            ... )

        Create a QueryEngine with a JDBC URL for an MS SQL Server:

        .. code-block:: python

            >>> from sqlalchemy.dialects import mssql
            >>> engine = QueryEngine.from_jdbc_connection(
            ...     jdbc_url="jdbc:sqlserver://localhost:1433;databaseName=mydb",
            ...     jdbc_params={"user": "sa", "password": "myPassword"},
            ...     dialect=mssql.dialect(),
            ... )
        """
        return cls(
            JdbcConnectionManager(jdbc_url=jdbc_url, jdbc_params=jdbc_params, jdbc_url_generator=jdbc_url_generator),
            dialect=dialect,
            paramstyle=paramstyle,
            **kwargs,
        )

    @classmethod
    def from_data_store(
        cls,
        data_store_id: str,
        credential_id: Optional[str] = None,
        dialect: Optional[Dialect] = None,
        paramstyle: Optional[str] = None,
        **kwargs: Any,
    ) -> QueryEngine:
        """
        Create a QueryEngine for a DataStore database connection.

        Notes
        -----
        Not all DataStores support statement execution through QueryEngine (e.g. Blob Storage).

        Parameters
        ----------
        data_store_id:
            The ID of the DataStore to use for the connection.
        credential_id:
            The ID of the credential to use for the connection. If not provided,
            the default credential for the DataStore will be used.
        **kwargs:
            Additional keyword arguments to pass to the QueryEngine constructor.

        Other Parameters
        ----------------
        dialect: sqlalchemy.dialects.Dialect
            The SQL dialect to use to compile statements. Modifies how SQLAlchemy constructs are compiled to
            their database-specific SQL strings.
        paramstyle: str
            The parameter style used to bind parameters to the statement. By default, "qmark" is used, which
            uses ``?`` placeholders for parameters. Named parameters will be substituted in the SQL string according
            to the parameter name.

        Notes
        -----
        When constructing a QueryEngine to execute statements using SQLAlchemy constructs, ``dialect`` should be
        provided to ensure correct compilation. For example, for MS SQL Server, pass ``dialect=mssql.dialect()``.

        Examples
        --------
        Create a QueryEngine for a DataStore using default sqlite SQL dialect:

        .. code-block:: python

            >>> from datarobot.query_engine import QueryEngine
            >>> engine = QueryEngine.from_data_store(
            ...     data_store_id="my_data_store_id",
            ...     credential_id="my_credential_id"
            ... )

        Create a QueryEngine for an MS SQL Server DataStore:

        .. code-block:: python

            >>> from sqlalchemy.dialects import mssql
            >>> engine = QueryEngine.from_data_store(
            ...     data_store_id="my_data_store_id",
            ...     credential_id="my_credential_id",
            ...     dialect=mssql.dialect(),
            ... )
        """
        return cls(
            DataStoreConnectionManager(data_store_id, credential_id), dialect=dialect, paramstyle=paramstyle, **kwargs
        )
