import logging

from canonmap.services.database.mysql.core import MySQLClient

logger = logging.getLogger(__name__)


class CanonMap:
    def __init__(self, mysql_client: MySQLClient):
        # autocommit = mysql_client.config.autocommit
        # if autocommit:
        #     autocommit_user_confirmation = input("Are you sure you want to enable autocommit?\n This will commit all changes to the database immediately.\n (NOTICE: This message will be the last confirmation you will see before the changes are autocommitted.)\n [y/N]: ")
        #     if autocommit_user_confirmation.lower() != "y":
        #         raise ValueError("Autocommit is disabled")


        self.mysql_client = mysql_client
        # self.autocommit = mysql_client.config.autocommit
    #     self.mysql_client.table_manager.autocommit = autocommit
    #     self.mysql_client.database_manager.autocommit = autocommit

    # @property
    # def connection_manager(self):
    #     return self.mysql_client.connection_manager

    # @property
    # def database_manager(self):
    #     return self.mysql_client.database_manager

    # @property
    # def table_manager(self):
    #     return self.mysql_client.table_manager

    # @property
    # def matcher_manager(self):
    #     return self.mysql_client.matcher_manager
