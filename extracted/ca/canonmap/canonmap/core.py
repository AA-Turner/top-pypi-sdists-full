# canonmap/core.py
import logging

from canonmap.services.db_mysql.core import CanonMapMySQLClient
from canonmap.utils.logger import configure_logging

configure_logging("INFO")
logger = logging.getLogger(__name__)

class CanonMap:
    def __init__(self, mysql_client: CanonMapMySQLClient):
        self.mysql_client = mysql_client
