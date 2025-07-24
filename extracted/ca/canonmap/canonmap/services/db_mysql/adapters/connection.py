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
            "user": self.config.user,
            "password": self.config.password,
        }

        # Use Unix socket if provided (for Cloud SQL)
        if self.config.unix_socket:
            config["unix_socket"] = self.config.unix_socket
            logger.info(f"Using Unix socket connection: {self.config.unix_socket}")
        else:
            # Use TCP connection
            config.update({
                "host": self.config.host,
                "port": self.config.port,
            })
            logger.info(f"Using TCP connection to {self.config.host}:{self.config.port}")

        try:
            self.conn = mysql.connector.connect(**config, allow_local_infile=True)
            if self.config.database:
                self.conn.database = self.config.database
            logger.info(f"Connected to MySQL server successfully")
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
            "user": self.config.user,
            "database": self.config.database,
            "status": status,
        }
        
        if self.config.unix_socket:
            info["unix_socket"] = self.config.unix_socket
        else:
            info.update({
                "host": self.config.host,
                "port": self.config.port,
            })
            
        # log a prettified multi-line summary
        for k, v in info.items():
            logger.info(f"  {k}: {v}")
        return info