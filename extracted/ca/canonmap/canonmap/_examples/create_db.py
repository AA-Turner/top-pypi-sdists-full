import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from canonmap import (
    CanonMap, 
    MySQLClient, 
    MySQLConfig, 
    Database, 
    TableField,
    Table,
    FieldTransformType,
    make_console_handler,
)
from canonmap.services.database.mysql.managers.database import DatabaseManager
from canonmap.services.database.mysql.managers.table import TableManager
from canonmap.services.database.mysql.utils.create_table_data_from_csv import create_table_data_from_csv

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
database_manager: DatabaseManager = cm.mysql_client.database_manager
table_manager: TableManager = cm.mysql_client.table_manager

def main():
    #### CREATE NEW DATABASE ####
    database_to_create = Database(database_name="test_db")
    database_manager.create_database(database=database_to_create)

    #### CREATE NEW TABLE (with data) ####
    table_to_create = Table(table_name="test_table")
    table_data = create_table_data_from_csv(csv_path=Path("./combine.csv"))
    table_manager.create_table(table_name=table_to_create.table_name, data=table_data)

    #### CREATE INDEX ON TABLE ####
    table_field_to_index = TableField(table_name=table_to_create, field_name="name")
    table_manager.create_index(index_fields=[table_field_to_index])

    #### TRANSFORM FIELD ####
    table_field_to_transform = TableField(table_name=table_to_create, field_name="name")
    for field_transform in [FieldTransformType.INITIALISM, FieldTransformType.PHONETIC, FieldTransformType.SOUNDEX]:
        table_manager.create_table_fields(fields=[table_field_to_transform], field_transform=field_transform)

if __name__ == "__main__":
    result = main()
    logger.info(result)