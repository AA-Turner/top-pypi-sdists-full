from typing import Optional

from ..api import DAPClient
from ..dap_types import Credentials
from ..integration.database import DatabaseConnection
from ..replicator.sql import SQLReplicator


async def sync_db(
    base_url: str,
    credentials: Credentials,
    connection_string: str,
    namespace: str,
    table_names: str,
    tracking: Optional[bool] = None,
) -> None:
    db_connection = DatabaseConnection(connection_string)
    async with DAPClient(base_url, credentials, tracking) as session:
        sql_replicator = SQLReplicator(session, db_connection)

        await sql_replicator.version_upgrade()

        async def replicate_table_fn(namespace: str, table: str) -> None:
            await sql_replicator.synchronize(namespace, table)

        await session.execute_operation_on_tables(namespace, table_names, "syncdb", replicate_table_fn)
