# src/canonmap/connectors/mysql_connector/connector.py

import logging
import time
from contextlib import contextmanager
from typing import Any, List, Optional

from mysql.connector.pooling import MySQLConnectionPool

from canonmap.connectors.mysql_connector.config import MySQLConfig


logger = logging.getLogger(__name__)


class MySQLConnector:
    """Manages a MySQL connection pool and provides connection contexts."""

    def __init__(self, config: MySQLConfig):
        self.config = config
        self._pool: Optional[MySQLConnectionPool] = None
        # Provide an instance logger used by utils for optional logging
        self.logger = logger

    def initialize_pool(self) -> None:
        if self._pool is None:
            self._pool = MySQLConnectionPool(**self.config.to_pool_dict())

    def get_pool(self) -> MySQLConnectionPool:
        if self._pool is None:
            self.initialize_pool()
        return self._pool

    @contextmanager
    def get_connection(self):
        conn = self.get_pool().get_connection()
        try:
            yield conn
        finally:
            conn.close()

    @contextmanager
    def transaction(self):
        """Begin a transaction: commit on success, rollback on exception."""
        conn = self.get_pool().get_connection()
        conn.autocommit = False
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def close_pool(self):
        """Close all pooled connections."""
        if self._pool is None:
            return
        logger.info("Pool cleanup completed")
        self._pool = None

    def execute_query(self, query: str, params: Optional[List[Any]] = None, allow_writes: bool = False) -> Any:
        query_upper = query.strip().upper()
        if not allow_writes and not query_upper.startswith("SELECT"):
            raise ValueError("Writes are disallowed; set allow_writes=True to proceed.")

        start = time.time()
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, params or [])
                if cursor.with_rows:
                    result = cursor.fetchall()
                else:
                    conn.commit()
                    result = {"affected_rows": cursor.rowcount}
                duration = time.time() - start
                logger.info("Query executed in %.4f sec", duration)
                return result
            finally:
                cursor.close()


