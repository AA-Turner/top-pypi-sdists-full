# scrapy_ingest/database/connection.py

import logging
import sqlite3
from datetime import datetime
from typing import Optional, Any, Sequence
from urllib.parse import quote, unquote, urlparse

from ..config.sqlite_path import sqlite_path_from_url
from ..constants import CLIENT_NAME
from ..exceptions import DependencyError, IngestConnectionError


class _CursorWrapper:
    """sqlite3 cursors lack a context manager; other drivers may support one."""

    __slots__ = ("_cur",)

    def __init__(self, cur):
        self._cur = cur

    def __enter__(self):
        return self._cur

    def __exit__(self, exc_type, exc, tb):
        self._cur.close()
        return False

    def __getattr__(self, name):
        return getattr(self._cur, name)


class DBConnection:
    """
    Database connection manager (singleton) for PostgreSQL, MySQL, and SQLite.
    Supports a DSN/URL or settings-based configuration and exposes
    ``connect/execute/commit/rollback/close``.
    """

    _instance: Optional["DBConnection"] = None
    _connection = None
    _db_url: Optional[str] = None
    _dialect: str = "postgres"
    _logger = logging.getLogger(__name__)

    def __new__(cls, db_url: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
            if db_url:
                cls._instance._db_url = db_url
            cls._instance._initialize_connection()
        return cls._instance

    @classmethod
    def open(cls, db_url: Optional[str] = None) -> "DBConnection":
        """Independent connection (safe for multi-threaded dashboard reads)."""
        conn = object.__new__(cls)
        conn._db_url = db_url
        conn._connection = None
        conn._dialect = "postgres"
        conn._initialize_connection()
        return conn

    @classmethod
    def reset_singleton(cls):
        if cls._instance is not None:
            try:
                cls._instance.close()
            except Exception:
                pass
        cls._instance = None

    @staticmethod
    def _is_mysql_url(url):
        if not url or "://" not in str(url):
            return False
        scheme = str(url).split("://", 1)[0].lower().split("+")[0]
        return scheme in ("mysql", "mariadb")

    @staticmethod
    def _is_sqlite_url(url):
        if not url or "://" not in str(url):
            return False
        scheme = str(url).split("://", 1)[0].lower().split("+")[0]
        return scheme == "sqlite"

    def _normalize_dsn(self, dsn: str) -> str:
        """URL-encode credentials if the password contains reserved characters."""
        if self._is_sqlite_url(dsn):
            return dsn
        try:
            if "://" not in dsn:
                return dsn
            scheme, rest = dsn.split("://", 1)
            if "/" in rest:
                netloc, tail = rest.split("/", 1)
                tail = "/" + tail
            else:
                netloc, tail = rest, ""
            if "@" in netloc:
                userinfo, hostport = netloc.rsplit("@", 1)
                if ":" in userinfo:
                    user, pwd = userinfo.split(":", 1)
                    if any(c in pwd for c in "@:$ /\\"):
                        user_enc = quote(unquote(user), safe="")
                        pwd_enc = quote(pwd, safe="")
                        netloc = f"{user_enc}:{pwd_enc}@{hostport}"
            return f"{scheme}://{netloc}{tail}"
        except Exception:
            return dsn

    def _is_open(self):
        conn = self._connection
        if conn is None:
            return False
        if self._dialect == "sqlite":
            return True
        if hasattr(conn, "closed"):
            return conn.closed == 0
        return bool(getattr(conn, "open", False))

    def _adapt_sql(self, sql: str) -> str:
        if self._dialect == "sqlite":
            return sql.replace("%s", "?")
        return sql

    def _connect_postgres(self, dsn=None, **kwargs):
        import psycopg2

        kwargs.setdefault("application_name", CLIENT_NAME)
        if dsn:
            return psycopg2.connect(dsn, **kwargs)
        return psycopg2.connect(**kwargs)

    def _connect_mysql(self, dsn=None, **kwargs):
        try:
            import pymysql
        except ImportError as exc:
            raise DependencyError(
                "MySQL support requires PyMySQL. Reinstall scrapy-ingest to get it."
            ) from exc
        if dsn:
            parsed = urlparse(dsn)
            kwargs = {
                "host": parsed.hostname or "localhost",
                "port": parsed.port or 3306,
                "user": unquote(parsed.username or ""),
                "password": unquote(parsed.password or ""),
                "database": unquote((parsed.path or "").lstrip("/").split("?")[0]),
                "charset": "utf8mb4",
            }
        kwargs.setdefault("autocommit", False)
        return pymysql.connect(**kwargs)

    def _connect_sqlite(self, dsn):
        path = sqlite_path_from_url(dsn)
        path.parent.mkdir(parents=True, exist_ok=True)

        def _adapt_datetime(val):
            return val.isoformat(sep=" ", timespec="seconds")

        sqlite3.register_adapter(datetime, _adapt_datetime)
        conn = sqlite3.connect(str(path), timeout=30.0, check_same_thread=False)
        conn.execute("PRAGMA foreign_keys = ON")
        # DELETE journal: single ingest.db file (no -wal / -shm). Fine for typical crawls.
        conn.execute("PRAGMA journal_mode = DELETE")
        conn.execute("PRAGMA busy_timeout = 30000")
        return conn

    def _connect_error_types(self):
        errors = [sqlite3.Error]
        try:
            from psycopg2 import OperationalError as PgError

            errors.append(PgError)
        except ImportError:
            pass
        try:
            from pymysql import OperationalError as MyError

            errors.append(MyError)
        except ImportError:
            pass
        return tuple(errors) or (Exception,)

    def _initialize_connection(self):
        """Initialize the connection once (or reconnect if closed)."""
        if self._is_open():
            return

        source = "unknown"
        try:
            if self._db_url:
                source = "db_url"
                dsn = self._normalize_dsn(self._db_url)
                if self._is_sqlite_url(dsn):
                    self._dialect = "sqlite"
                    self._connection = self._connect_sqlite(dsn)
                elif self._is_mysql_url(dsn):
                    self._dialect = "mysql"
                    self._connection = self._connect_mysql(dsn)
                else:
                    self._dialect = "postgres"
                    self._connection = self._connect_postgres(dsn)
            else:
                from scrapy.utils.project import get_project_settings

                settings = get_project_settings()
                source = "Scrapy settings"
                db_type = str(settings.get("DB_TYPE") or "postgres").strip().lower()
                kwargs = {
                    "host": settings.get("DB_HOST"),
                    "port": settings.get("DB_PORT"),
                    "user": settings.get("DB_USER"),
                    "password": settings.get("DB_PASSWORD"),
                }
                if db_type in ("mysql", "mariadb"):
                    self._dialect = "mysql"
                    kwargs["database"] = settings.get("DB_NAME")
                    self._connection = self._connect_mysql(**kwargs)
                else:
                    self._dialect = "postgres"
                    kwargs["dbname"] = settings.get("DB_NAME")
                    self._connection = self._connect_postgres(**kwargs)
            if self._dialect != "sqlite" and hasattr(self._connection, "autocommit"):
                try:
                    self._connection.autocommit = False
                except Exception:
                    pass
        except self._connect_error_types() as e:
            self._logger.error(
                "Failed to connect to database via %s: %s. "
                "Verify DB settings or DSN (host, port, dbname).",
                source,
                str(e),
            )
            raise IngestConnectionError(
                f"Failed to connect to database via {source}: {e}"
            ) from e
        except Exception as e:
            self._logger.error(
                "Failed to connect to database via %s: %s. "
                "Verify DB settings or DSN (host, port, dbname).",
                source,
                str(e),
            )
            raise IngestConnectionError(
                f"Failed to connect to database via {source}: {e}"
            ) from e

    def connect(self) -> bool:
        try:
            self._initialize_connection()
            return True
        except IngestConnectionError:
            return False

    def cursor(self):
        if not self._is_open():
            self._initialize_connection()
        return _CursorWrapper(self._connection.cursor())

    def execute(self, sql: str, params: Sequence[Any] = None):
        """Execute a SQL statement.
        Returns the first row if the statement produces a result set,
        otherwise returns None.
        """
        sql = self._adapt_sql(sql)
        with self.cursor() as cur:
            if params is not None:
                cur.execute(sql, params)
            else:
                cur.execute(sql)
            if cur.description is not None:
                return cur.fetchone()
            return None

    def executemany(self, sql: str, params_seq):
        sql = self._adapt_sql(sql)
        with self.cursor() as cur:
            cur.executemany(sql, params_seq)

    def fetchall(self, sql: str, params: Sequence[Any] = ()):
        sql = self._adapt_sql(sql)
        with self.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()

    def commit(self):
        if self._connection:
            self._connection.commit()

    def rollback(self):
        if self._connection:
            self._connection.rollback()

    def close(self):
        if self._connection is not None:
            try:
                self._connection.close()
            except Exception:
                pass
            self._connection = None


DatabaseConnection = DBConnection
