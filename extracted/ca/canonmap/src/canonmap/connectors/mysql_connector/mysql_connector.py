# src/canonmap/connectors/mysql_connector/mysql_connector.py

import logging
from typing import Optional, Dict, List, Union
import threading

from mysql.connector import pooling, Error as MySQLError

from canonmap.connectors.base import BaseConnector
from canonmap.connectors.mysql_connector.config import MySQLConnectorConfig

logger = logging.getLogger(__name__)

class MySQLConnector(BaseConnector):
    """
    MySQL Connector with connection pooling for CanonMap.
    
    Usage:
        connector = MySQLConnector(config)
        connector.connect()
        result = connector.run_query("SELECT ...")
        connector.close()
    """
    def __init__(
        self, 
        config: MySQLConnectorConfig, 
        pool_size: int = 5, 
        pool_name: str = "canonmap_mysql_pool"
    ):
        self.config = config.model_copy()
        self.pool_size = pool_size
        self.pool_name = pool_name
        self.pool: Optional[pooling.MySQLConnectionPool] = None
        self._lock = threading.Lock()
        self._connected = False

    def connect(self) -> None:
        """Establish connection pool (idempotent)."""
        with self._lock:
            if self.pool is not None and self._connected:
                return
            try:
                mysql_params = self.config.model_dump(exclude_none=True, exclude={"connection_method"})
                self.pool = pooling.MySQLConnectionPool(
                    pool_name=self.pool_name,
                    pool_size=self.pool_size,
                    **mysql_params
                )
                self._connected = True
                logger.info(f"Pool created with {self.pool_size} connections")
            except MySQLError as e:
                logger.error(f"Failed to create pool: {e}")
                raise MySQLError(f"Failed to create pool: {e}")

    def connect_to_database(self, database: str) -> None:
        """Reconnect to a different database (re-create pool)."""
        # (re)initialize connection pool using new database param
        config = self.config.model_copy()
        config.database = database
        self.config = config
        self.close()      # close existing pool if open
        self.connect()    # re-init with new database

    def run_query(self, query: str, params: Optional[Union[List, Dict]] = None) -> List[Dict]:
        """
        Run a query and return results as list of dicts.
        """
        if self.pool is None or not self._connected:
            raise MySQLError("Connector not connected. Call connect() first.")
        conn = None
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            # If SELECT, fetch results
            if cursor.with_rows:
                result = cursor.fetchall()
            else:
                result = []
                conn.commit()
            cursor.close()
            logger.info(f"Query executed successfully: {query}")
            return result
        except MySQLError as e:
            logger.error(f"MySQL query error: {e}")
            raise MySQLError(f"MySQL query error: {e}")
        finally:
            if conn is not None:
                conn.close()

    def close(self):
        """
        There is no explicit pool close in mysql-connector, but 
        for consistency, set pool to None and mark disconnected.
        """
        with self._lock:
            self.pool = None
            self._connected = False
            logger.info("Pool closed")

    def is_alive(self) -> bool:
        """
        Check if pool is alive by pinging the DB.
        """
        if not self.pool:
            return False
        try:
            conn = self.pool.get_connection()
            conn.ping(reconnect=True, attempts=1, delay=0)
            conn.close()
            logger.info("Pool is alive")
            return True
        except Exception as e:
            logger.error(f"Pool is not alive: {e}")
            return False
