# canonmap/services/db_mysql/adapters/connection.py

import logging
from typing import Optional

import mysql.connector
from mysql.connector import MySQLConnection, Error

from canonmap.services.db_mysql.config import CanonMapMySQLConfig

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self, config: CanonMapMySQLConfig):
        self.config = config
        self.conn: Optional[MySQLConnection] = None

    def connect(self) -> MySQLConnection:
        if self.conn and self.conn.is_connected():
            logger.debug("Reusing existing MySQL connection")
            return self.conn

        config = {
            "host": self.config.host,
            "user": self.config.user,
            "password": self.config.password,
            "port": self.config.port,
        }

        try:
            self.conn = mysql.connector.connect(**config, allow_local_infile=True)
            if self.config.database:
                self.conn.database = self.config.database
            logger.info(f"Connected to MySQL server at {self.config.host}:{self.config.port}")
            return self.conn

        except Error as e:
            logger.error("Could not connect to MySQL: %s", e, exc_info=True)
            raise RuntimeError(f"Could not connect to MySQL: {e}") from e

    def close(self) -> None:
        if self.conn and self.conn.is_connected():
            self.conn.close()
            self.conn = None
            logger.info("MySQL connection closed")

    def connection_info(self) -> dict:
        status = "Connected" if (self.conn and self.conn.is_connected()) else "Disconnected"
        info = {
            "host": self.config.host,
            "port": self.config.port,
            "user": self.config.user,
            "database": self.config.database,
            "status": status,
        }
        # log a prettified multi-line summary
        for k, v in info.items():
            logger.info(f"  {k}: {v}")
        return info