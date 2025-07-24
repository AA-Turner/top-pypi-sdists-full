# canonmap/services/db_mysql/config.py

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class CanonMapMySQLConfig:
    host: str
    user: str
    password: str
    port: int = 3306
    database: Optional[str] = None
    unix_socket: Optional[str] = None
    cloud_sql_instance: Optional[str] = None

    @classmethod
    def from_environment(cls, prefix: str = "DB_") -> "CanonMapMySQLConfig":
        """
        Create a CanonMapMySQLConfig from environment variables.
        
        For Cloud SQL on Cloud Run, set these environment variables:
        - DB_USER: MySQL username
        - DB_PASSWORD: MySQL password  
        - DB_NAME: Database name
        - DB_UNIX_SOCKET: Unix socket path (e.g., /cloudsql/PROJECT:REGION:INSTANCE)
        
        For regular MySQL connections:
        - DB_HOST: MySQL host
        - DB_PORT: MySQL port (default: 3306)
        """
        # Check for Cloud SQL Unix socket first
        unix_socket = os.getenv(f"{prefix}UNIX_SOCKET")
        
        if unix_socket:
            # Cloud SQL via Unix socket
            return cls(
                host="localhost",  # Not used with Unix socket
                user=os.getenv(f"{prefix}USER", ""),
                password=os.getenv(f"{prefix}PASSWORD", ""),
                database=os.getenv(f"{prefix}NAME"),
                unix_socket=unix_socket,
            )
        else:
            # Regular TCP connection
            return cls(
                host=os.getenv(f"{prefix}HOST", "localhost"),
                user=os.getenv(f"{prefix}USER", ""),
                password=os.getenv(f"{prefix}PASSWORD", ""),
                port=int(os.getenv(f"{prefix}PORT", "3306")),
                database=os.getenv(f"{prefix}NAME"),
            ) 