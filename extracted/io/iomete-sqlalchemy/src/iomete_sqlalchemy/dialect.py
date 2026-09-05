"""
SQLAlchemy dialect for IOMETE via Arrow Flight SQL.

Connection URL format
---------------------
  iomete://<user>:<password>@<host>:<port>/<catalog>/<database>
    ?cluster=<cluster_name>
    &data_plane=<data_plane_name>
    [&tls=true]
    [&max_msg_size=134217728]

IOMETE uses a three-level namespace: catalog → database → table.
SQLAlchemy maps the second level to its ``schema`` parameter throughout
the reflection API — so wherever SQLAlchemy says "schema", IOMETE means
"database" (e.g. ``spark_catalog.default``).

Example
-------
  iomete://alice:secret@dev.iomete.cloud:443/spark_catalog/default
      ?cluster=dwh&data_plane=spark-resources
"""

from __future__ import annotations

import logging
import re
from urllib.parse import unquote_plus

from sqlalchemy import pool, text
from sqlalchemy.engine import URL
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.engine.interfaces import ReflectedColumn
from sqlalchemy.exc import DatabaseError
from sqlalchemy.sql.compiler import GenericTypeCompiler, IdentifierPreparer, SQLCompiler

from iomete_sqlalchemy import dbapi as iomete_dbapi
from iomete_sqlalchemy.types import spark_type_to_sqla

logger = logging.getLogger(__name__)

_NOT_FOUND_PATTERNS = (
    "TABLE_OR_VIEW_NOT_FOUND",
    "SCHEMA_NOT_FOUND",
    "NoSuchNamespaceException",
    "NoSuchDatabaseException",
)

def _is_not_found(exc: Exception) -> bool:
    """Return True if the exception message indicates a missing object.

    Used to distinguish expected "object does not exist" errors (which should
    result in graceful empty/None returns) from unexpected failures (which
    should be logged as warnings).
    """
    msg = str(exc)
    return any(pattern in msg for pattern in _NOT_FOUND_PATTERNS)


class SparkIdentifierPreparer(IdentifierPreparer):
    """Use backtick quoting for identifiers.

    Spark SQL does not accept ANSI double-quote identifiers (``"name"``);
    backticks (`` `name` ``) are the only supported quoting style.
    """

    def __init__(self, dialect):
        super().__init__(dialect, initial_quote="`", final_quote="`")

    def quote_schema(self, schema, force=None):
        """Quote each dot-separated part of the schema individually.

        SQLAlchemy encodes IOMETE's two-level schema as ``"catalog.database"``.
        The base implementation would quote this as a single token
        (`` `catalog.database` ``), which Spark rejects.  Splitting on ``.``
        and quoting each part produces `` `catalog`.`database` `` instead.
        """
        parts = schema.split(".")
        active_catalog = getattr(self.dialect, "_catalog", None)
        if len(parts) == 2 and active_catalog and parts[0] == active_catalog:
            parts = parts[1:]
        return ".".join(self.quote(part, force) for part in parts)


class SparkSQLCompiler(SQLCompiler):
    """Compiler overrides for Spark SQL dialect quirks.

    Spark requires integer literals for LIMIT/OFFSET (e.g. ``LIMIT 10``),
    not bind parameters (``LIMIT ?``). The base SQLCompiler emits bind params,
    so we override ``limit_clause`` to force ``literal_binds=True``.
    """

    def limit_clause(self, select, **kw):
        limit = select._limit_clause
        offset = select._offset_clause
        clause = ""
        if limit is not None:
            clause += "\n LIMIT " + self.process(limit, literal_binds=True)
        if offset is not None:
            clause += "\n OFFSET " + self.process(offset, literal_binds=True)
        return clause

    def fetch_clause(self, select, **kw):
        # Spark doesn't support FETCH FIRST n ROWS either
        return self.limit_clause(select, **kw)


class SparkTypeCompiler(GenericTypeCompiler):
    """DDL type compiler that maps SQLAlchemy types to Spark SQL DDL equivalents.

    Spark SQL quirks handled here:

    - ``DATETIME`` is unsupported; ``TIMESTAMP`` is the correct keyword.
    - ``VARCHAR(n)`` is valid in Spark 3.x, but bare ``VARCHAR`` without a length
      is never accepted — Spark has no unbounded VARCHAR type.  SQLAlchemy's
      ``String()`` (no length) must therefore map to ``STRING``, which is Spark's
      native unbounded string type.
    """

    def visit_DATETIME(self, type_, **kw):
        return "TIMESTAMP"

    def visit_datetime(self, type_, **kw):
        return "TIMESTAMP"

    def visit_VARCHAR(self, type_, **kw):
        if type_.length:
            return f"VARCHAR({type_.length})"
        return "STRING"

    def visit_NVARCHAR(self, type_, **kw):
        if type_.length:
            return f"VARCHAR({type_.length})"
        return "STRING"

    def visit_TEXT(self, type_, **kw):
        return "STRING"


class IOMETEDialect(DefaultDialect):
    # ── dialect identity ────────────────────────────────────────────────────
    name = "iomete"
    driver = "flightsql"
    preparer = SparkIdentifierPreparer
    statement_compiler = SparkSQLCompiler
    type_compiler_cls = SparkTypeCompiler

    # ── capabilities ────────────────────────────────────────────────────────
    supports_alter = False
    supports_empty_insert = False
    supports_native_boolean = True
    supports_multivalues_insert = True
    supports_statement_cache = True  # must be explicit — SQLAlchemy checks __dict__, not inheritance

    default_schema_name = "default"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._catalog: str | None = None

    # ── pooling ─────────────────────────────────────────────────────────────
    @classmethod
    def import_dbapi(cls):
        return iomete_dbapi

    # backwards-compat alias for SQLAlchemy < 2.0
    @classmethod
    def dbapi(cls):
        return cls.import_dbapi()

    # Use NullPool by default: Flight SQL connections are stateful gRPC
    # streams; connection pooling doesn't add value here.
    @classmethod
    def get_pool_class(cls, url):
        return pool.NullPool

    # ── URL → connect args ──────────────────────────────────────────────────
    def create_connect_args(self, url: URL):
        # url.database is "catalog/schema"; extract only the catalog part.
        database = url.database or ""
        catalog_part, _, _ = database.partition("/")
        self._catalog = catalog_part or None
        query_params = url.query

        def get_query_param(key: str, default: str | None = None) -> str | None:
            value = query_params.get(key, default)
            if isinstance(value, (list, tuple)):
                *_, value = value
            return unquote_plus(value) if value is not None else None

        tls = get_query_param("tls", "true").lower() not in ("false", "0", "no")
        scheme = "grpc+tls" if tls else "grpc"
        host = url.host or "localhost"
        port = url.port or 443
        uri = f"{scheme}://{host}:{port}"

        db_kwargs: dict[str, str] = {}
        if url.username:
            db_kwargs["username"] = unquote_plus(url.username)
        if url.password:
            db_kwargs["password"] = unquote_plus(str(url.password))

        cluster = get_query_param("cluster")
        if cluster:
            db_kwargs["adbc.flight.sql.rpc.call_header.cluster"] = cluster

        data_plane = get_query_param("data_plane")
        if data_plane:
            db_kwargs["adbc.flight.sql.rpc.call_header.data-plane"] = data_plane

        max_msg_size = get_query_param("max_msg_size", "134217728")
        db_kwargs["adbc.flight.sql.client_option.with_max_msg_size"] = max_msg_size

        if self._catalog:
            db_kwargs["adbc.flight.sql.rpc.call_header.schema"] = self._catalog

        return [], {"uri": uri, "db_kwargs": db_kwargs}

    # ── schema helpers ──────────────────────────────────────────────────────
    @staticmethod
    def _catalog_schema(schema: str | None) -> tuple[str | None, str | None]:
        """
        IOMETE uses a three-level namespace: catalog.database.table.
        SQLAlchemy's ``schema`` parameter encodes both levels as
        ``"catalog.database"`` (dot-separated), e.g. ``"spark_catalog.default"``.
        If only one token is given it is treated as the database name within
        the default catalog.
        """
        if not schema:
            return None, None
        catalog, sep, db = schema.partition(".")
        if sep:
            return catalog, db
        return None, catalog

    def _schema_qualifier(self, schema: str | None) -> str:
        catalog, db = self._catalog_schema(schema)
        if not db:
            return ""
        if catalog and catalog != self._catalog:
            return f"`{catalog}`.`{db}`"
        return f"`{db}`"

    def _full_name(self, schema: str | None, object_name: str) -> str:
        catalog, db = self._catalog_schema(schema)
        parts = []
        if catalog and catalog != self._catalog:
            parts.append(f"`{catalog}`")
        if db:
            parts.append(f"`{db}`")
        parts.append(f"`{object_name}`")
        return ".".join(parts)

    # ── dialect initialisation ──────────────────────────────────────────────
    def initialize(self, connection):
        pass  # nothing to probe at startup

    def do_executemany(self, cursor, statement, parameters, context=None):
        """Execute a DML statement one row at a time.

        IOMETE's Arrow Flight SQL server rejects multi-row batches, so each row is
        sent individually via ``cursor.executemany(statement, [row])``.
        https://github.com/iomete/spark/blob/18a173f3b11cdbf21cb20b2130572a57dbdb1941/iomete/arrow-server/src/main/java/com/iomete/spark/arrow/flight/sql/handlers/PreparedStatementHandler.java#L296
        TODO: remove this workaround once the server supports batch parameter binding.
        """
        for params in parameters:
            cursor.executemany(statement, [params])

    def do_execute(self, cursor, statement, parameters, context=None):
        is_write = context is not None and (context.isddl or context.is_crud)
        if is_write and parameters:
            # Parameterized DML — DoPut write path, synchronous.
            cursor.executemany(statement, [parameters])
            return

        cursor.execute(statement, parameters)
        if not cursor.description:
            # Row-less statement (USE, DDL, output-less DML). The ADBC driver fetches its result
            # stream in the background and cancels that fetch as soon as the cursor is closed
            # unread, and the server runs a prepared command only while that stream is read.
            # Draining here makes the statement actually run, and any error surface, before
            # execute() returns. Commands that return rows (e.g. Spark `SET key = value`, which
            # echoes a key/value row) are left for the caller to read; draining them here would
            # consume the caller's result.
            cursor.fetchall()

    def do_execute_no_params(self, cursor, statement, context=None):
        # Same path as do_execute so parameterless statements are drained as well.
        self.do_execute(cursor, statement, None, context)

    def do_rollback(self, dbapi_connection):
        pass

    # ── server version ──────────────────────────────────────────────────────
    def _get_server_version_info(self, connection):
        try:
            row = connection.execute(text("SELECT version()")).fetchone()
            if row:
                version_match = re.search(r"(\d+)\.(\d+)\.(\d+)", row[0])
                if version_match:
                    return tuple(int(x) for x in version_match.groups())
        except DatabaseError as e:
            logger.debug("Could not retrieve server version: %s", e)
        return 0, 0, 0

    # ── schema / table listing ──────────────────────────────────────────────
    def get_schema_names(self, connection, **kw) -> list[str]:
        """Return all schemas visible in the current catalog."""
        rows = connection.execute(text("SHOW SCHEMAS")).fetchall()
        return [row[0].strip("`") for row in rows]

    def get_table_names(self, connection, schema: str | None = None, **kw) -> list[str]:
        qualifier = self._schema_qualifier(schema)
        sql = f"SHOW TABLES{' IN ' + qualifier if qualifier else ''}"
        rows = connection.execute(text(sql)).fetchall()
        # Iomete SHOW TABLES returns (namespace, tableName, isTemporary)
        return [row[1] if len(row) > 1 else row[0] for row in rows]

    def get_view_definition(
        self,
        connection,
        view_name: str,
        schema: str | None = None,
        **kw,
    ) -> str | None:
        full_name = self._full_name(schema, view_name)
        try:
            rows = connection.execute(text(f"SHOW CREATE TABLE {full_name}")).fetchall()
            if rows:
                return "\n".join(row[0] for row in rows)
            return None
        except DatabaseError as e:
            if _is_not_found(e):
                logger.debug("get_view_definition(%r): not found: %s", view_name, e)
                return None
            logger.warning(
                "get_view_definition(%r) failed unexpectedly: %s", view_name, e
            )
            return None

    def get_view_names(self, connection, schema: str | None = None, **kw) -> list[str]:
        qualifier = self._schema_qualifier(schema)
        sql = f"SHOW VIEWS{' IN ' + qualifier if qualifier else ''}"
        try:
            rows = connection.execute(text(sql)).fetchall()
            return [row[1] if len(row) > 1 else row[0] for row in rows]
        except DatabaseError as e:
            logger.warning("get_view_names(schema=%r) failed: %s", schema, e)
            return []

    # ── column reflection ───────────────────────────────────────────────────
    def get_columns(
        self,
        connection,
        table_name: str,
        schema: str | None = None,
        **kw,
    ) -> list[ReflectedColumn]:
        full_name = self._full_name(schema, table_name)
        rows = connection.execute(text(f"DESCRIBE TABLE {full_name}")).fetchall()
        columns: list[ReflectedColumn] = []
        for row in rows:
            col_name = row[0]
            type_str = row[1] if len(row) > 1 else "string"
            comment = row[2] if len(row) > 2 else None

            # DESCRIBE sometimes includes partition/metadata separators
            if not col_name or col_name.startswith("#"):
                break

            col: ReflectedColumn = {
                "name": col_name,
                "type": spark_type_to_sqla(type_str),
                "nullable": True,  # DESCRIBE TABLE doesn't expose nullability; default to True
                "default": None,
                "autoincrement": False,
            }
            if comment:
                col["comment"] = comment
            columns.append(col)
        return columns

    # ── graceful stubs (Lakehouse has no PK / FK / index concepts) ──────────
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        return {"constrained_columns": [], "name": None}

    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        return []

    def get_indexes(self, connection, table_name, schema=None, **kw):
        return []

    def get_unique_constraints(self, connection, table_name, schema=None, **kw):
        return []

    def get_check_constraints(self, connection, table_name, schema=None, **kw):
        return []

    def get_table_comment(self, connection, table_name, schema=None, **kw):
        full_name = self._full_name(schema, table_name)
        try:
            rows = connection.execute(
                text(f"DESCRIBE TABLE EXTENDED {full_name}")
            ).fetchall()
            for row in rows:
                if row[0].strip().lower() == "comment":
                    comment = row[1].strip() if row[1] else None
                    return {"text": comment or None}
        except DatabaseError as e:
            if _is_not_found(e):
                logger.debug("get_table_comment(%r): not found: %s", table_name, e)
            else:
                logger.warning(
                    "get_table_comment(%r) failed unexpectedly: %s", table_name, e
                )
        return {"text": None}

    # ── existence checks ────────────────────────────────────────────────────
    def has_table(
        self, connection, table_name: str, schema: str | None = None, **kw
    ) -> bool:
        try:
            return table_name in self.get_table_names(connection, schema=schema)
        except DatabaseError as e:
            logger.warning("has_table(%r) check failed: %s", table_name, e)
            return False

    def has_schema(self, connection, schema_name: str, **kw) -> bool:
        try:
            return schema_name in self.get_schema_names(connection)
        except DatabaseError as e:
            logger.warning("has_schema(%r) check failed: %s", schema_name, e)
            return False

    # ── default schema detection ─────────────────────────────────────────────
    def _get_default_schema_name(self, connection):
        try:
            row = connection.execute(text("SELECT current_database()")).fetchone()
            if row:
                return row[0]
        except DatabaseError as e:
            logger.debug("Could not retrieve default schema name: %s", e)
        return self.default_schema_name
