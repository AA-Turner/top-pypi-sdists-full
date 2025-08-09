# src/canonmap/connectors/mysql_connector/config.py

import os
from typing import Dict, Optional

from pydantic import BaseModel

from canonmap.exceptions import MySQLConnectorError


class MySQLConfig(BaseModel):
    host: str
    user: str
    password: str
    database: str
    pool_name: str = "mypool"
    pool_size: int = 5

    def to_pool_dict(self) -> dict:
        return self.dict()

    @classmethod
    def from_env(cls) -> "MySQLConfig":
        """
        Build config from environment variables and provide a clear error if any are missing.

        Expected env vars:
          - MYSQL_HOST
          - MYSQL_USER
          - MYSQL_PASSWORD
          - MYSQL_DATABASE
        Optional:
          - MYSQL_POOL_NAME (default: mypool)
          - MYSQL_POOL_SIZE (default: 5)
        """
        required_keys = ["MYSQL_HOST", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE"]
        env_values: Dict[str, Optional[str]] = {k: os.getenv(k) for k in required_keys}
        missing = [k for k, v in env_values.items() if not v]
        if missing:
            raise MySQLConnectorError(
                "Missing required environment variables for MySQL configuration: "
                + ", ".join(missing)
                + "\nPlease create a .env with these keys or export them before starting the app."
            )

        pool_name = os.getenv("MYSQL_POOL_NAME", "mypool")
        try:
            pool_size = int(os.getenv("MYSQL_POOL_SIZE", "5"))
        except ValueError:
            pool_size = 5

        return cls(
            host=env_values["MYSQL_HOST"],
            user=env_values["MYSQL_USER"],
            password=env_values["MYSQL_PASSWORD"],
            database=env_values["MYSQL_DATABASE"],
            pool_name=pool_name,
            pool_size=pool_size,
        )