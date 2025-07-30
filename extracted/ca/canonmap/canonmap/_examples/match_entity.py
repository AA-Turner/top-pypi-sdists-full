import logging
import os

from dotenv import load_dotenv

from canonmap import (
    CanonMap, 
    MySQLClient, 
    MySQLConfig, 
    Database, 
    make_console_handler,
    TableField,
    Table,
    EntityMappingRequest,
    EntityMappingResponse
)
from canonmap.services.database.mysql.managers.matcher import MatcherManager
from canonmap.services.database.mysql.managers.database import DatabaseManager
from canonmap.services.database.mysql.managers.table import TableManager

load_dotenv(override=True)

make_console_handler("INFO", set_root=True)
logger = logging.getLogger(__name__)

mysql_config = MySQLConfig(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    # host=os.getenv("DB_HOST"),
    # port=os.getenv("DB_PORT"),
    unix_socket=os.getenv("GCP_CLOUD_SQL_UNIX_SOCKET"),
)
mysql_client = MySQLClient(config=mysql_config)
cm = CanonMap(mysql_client=mysql_client)

database = Database(database_name="<your database name here>")
test_table = Table(table_name="<your table name here>")
database_manager: DatabaseManager = cm.mysql_client.database_manager
table_manager: TableManager = cm.mysql_client.table_manager
matcher: MatcherManager = cm.mysql_client.matcher_manager
cm.mysql_client.connection_manager.database = database.database_name
cm.mysql_client.connection_manager.connect()


def main() -> EntityMappingResponse:
    select_field = TableField(table_name=test_table, field_name="<your field name here>")
    match_request = EntityMappingRequest(
        entity_name="<your entity name here>",
        select_field=select_field,
    )
    result: EntityMappingResponse = matcher.match(request=match_request)
    return result

if __name__ == "__main__":
    result = main()
    logger.info(result)