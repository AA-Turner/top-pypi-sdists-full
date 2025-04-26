import logging

from dap.api import DAPSession
from dap.integration.database import DatabaseConnection
from dap.replicator.sql_metatable_handler import get_table_names_in_namespace_from_meta
from dap.replicator.sql_op import SqlOp
from dap.replicator.sql_op_drop import SqlOpDrop
from dap.replicator.sql_op_init import SqlOpInit
from dap.replicator.sql_op_sync import SqlOpSync
from dap.version_upgrade.db_version_upgrader import VersionUpgrader

logger: logging.Logger = logging.getLogger(__name__)


class SQLReplicator:
    """
    Encapsulates logic that replicates changes acquired from DAP API in a SQL database.
    """

    _session: DAPSession
    _connection: DatabaseConnection

    def __init__(self, session: DAPSession, connection: DatabaseConnection) -> None:
        self._session = session
        self._connection = connection

    async def version_upgrade(
        self,
    ) -> None:
        async with self._connection.connection as base_connection:
            explorer = self._connection.engine.create_explorer(base_connection)
            await VersionUpgrader(
                explorer, base_connection, self._connection.dialect
            ).upgrade()

    async def initialize(
        self,
        namespace: str,
        table_name: str,
    ) -> None:
        logger.debug(f"initializing table: {namespace}.{table_name}")

        async with self._connection.connection as base_connection:
            explorer = self._connection.engine.create_explorer(base_connection)

            # Currently, in case of web logs, due to upstream 'at-least-once' logic,
            # sometimes we receive the same key twice or more times.
            # When we switch to the next-generation web logs that has no
            # duplicates by design, we can remove this line.
            use_upsert = namespace == "canvas_logs" and table_name == "web_logs"

            init_op: SqlOp = SqlOpInit(
                conn=base_connection,
                namespace=namespace,
                table_name=table_name,
                explorer=explorer,
                session=self._session,
                use_upsert=use_upsert,
            )

            await init_op.run()

    async def synchronize(
        self,
        namespace: str,
        table_name: str,
    ) -> None:
        logger.debug(f"synchronizing table: {namespace}.{table_name}")

        async with self._connection.connection as base_connection:
            explorer = self._connection.engine.create_explorer(base_connection)

            sync_op: SqlOp = SqlOpSync(
                conn=base_connection,
                namespace=namespace,
                table_name=table_name,
                explorer=explorer,
                session=self._session,
            )

            await sync_op.run()


class SQLDrop:
    """
    Encapsulates logic that drops table(s) from the SQL database.
    """

    _connection: DatabaseConnection

    def __init__(self, connection: DatabaseConnection) -> None:
        self._connection = connection

    async def drop(
        self,
        namespace: str,
        table_names: str,
    ) -> None:
        """
        Drops the given database tables.
        """

        async with self._connection.connection as base_connection:
            explorer = self._connection.engine.create_explorer(base_connection)
            await VersionUpgrader(
                explorer, base_connection, self._connection.dialect
            ).upgrade()

            table_names_to_delete = []
            if table_names == "all":
                table_names_to_delete = await get_table_names_in_namespace_from_meta(
                    base_connection, namespace
                )
                logger.info(
                    f"all local database tables in namespace {namespace} : {table_names_to_delete}"
                )
            else:
                table_names_to_delete = table_names.split(",")

            if len(table_names_to_delete) < 1:
                logger.warning(f"no tables to drop in namespace {namespace}")

            exceptions = []
            for idx, table_name in enumerate(table_names_to_delete):
                try:
                    drop_op: SqlOp = SqlOpDrop(
                        conn=base_connection,
                        namespace=namespace,
                        table_name=table_name,
                        explorer=explorer,
                    )
                    await drop_op.run()
                    logger.info(
                        f"Deleted table '{table_name}' ({idx + 1} of {len(table_names_to_delete)})"
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to delete table '{table_name}' ({idx + 1} of {len(table_names_to_delete)}): {e}"
                    )
                    exceptions.append(e)

            if len(exceptions) > 0:
                table_str = "table" if len(exceptions) == 1 else "tables"
                raise ExceptionGroup(
                    f"Failed to delete {len(exceptions)} {table_str} of {len(table_names_to_delete)}",
                    exceptions,
                )
