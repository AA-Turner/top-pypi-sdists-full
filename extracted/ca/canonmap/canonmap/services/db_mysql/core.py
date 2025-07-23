# canonmap/services/db_mysql/core.py

from canonmap.services.db_mysql.adapters.connection import ConnectionManager
from canonmap.services.db_mysql.managers.database import DatabaseManager
from canonmap.services.db_mysql.managers.user import UserManager
from canonmap.services.db_mysql.managers.table import TableManager
from canonmap.services.db_mysql.config import CanonMapMySQLConfig
from canonmap.services.db_mysql.managers.matcher import MatcherManager
from canonmap.services.db_mysql.managers.csv import CSVManager

class CanonMapMySQLClient:
    def __init__(self, config: CanonMapMySQLConfig):
        self.connection_manager = ConnectionManager(config)
        self.database_manager = DatabaseManager(self.connection_manager)
        self.user_manager = UserManager(self.connection_manager)
        self.table_manager = TableManager(self.connection_manager)
        self.matcher_manager = MatcherManager(self.connection_manager)
        self.csv_manager = CSVManager(self.connection_manager)