from ..integration.database import DatabaseConnection
from ..replicator.sql import SQLDrop


async def drop_db(connection_string: str, namespace: str, table_names: str) -> None:
    db_connection = DatabaseConnection(connection_string)
    await SQLDrop(db_connection).drop(namespace, table_names)
