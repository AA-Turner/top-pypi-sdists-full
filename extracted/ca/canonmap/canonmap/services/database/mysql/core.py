# canonmap/services/database/mysql/core.py

from canonmap.services.database.mysql.config import MySQLConfig
from canonmap.services.database.mysql.managers.database import DatabaseManager
from canonmap.services.database.mysql.managers.user import UserManager
from canonmap.services.database.mysql.managers.table import TableManager
from canonmap.services.database.mysql.managers.matcher import MatcherManager
from canonmap.services.database.mysql.managers.csv import CSVManager

class MySQLClient:
    def __init__(self, config: MySQLConfig):
        self.connection_manager = config
        self.database_manager = DatabaseManager(self.connection_manager)
        self.user_manager = UserManager(self.connection_manager)
        self.table_manager = TableManager(self.connection_manager)
        self.matcher_manager = MatcherManager(self.connection_manager)
        self.csv_manager = CSVManager(self.connection_manager)
