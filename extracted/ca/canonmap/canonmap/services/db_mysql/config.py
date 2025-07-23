# canonmap/services/db_mysql/config.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class CanonMapMySQLConfig:
    host: str
    user: str
    password: str
    port: int = 3306
    database: Optional[str] = None 