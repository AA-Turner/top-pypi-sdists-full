import logging

from pysqlsync.base import ClassRef

from dap.replicator import meta_schema
from dap.replicator.sql_metatable_handler import (
    drop_delete_table_metadata,
    get_table_meta_record,
)
from dap.replicator.sql_op import SqlOp

logger: logging.Logger = logging.getLogger(__name__)


class SqlOpDrop(SqlOp):
    async def run(self) -> None:
        await self.explorer.synchronize(modules=[meta_schema, self.namespace_module])

        logger.debug(
            f"Start operation - Drop table. Namespace: {self.namespace}, table: {self.table_name}, conn: {self.conn}"
        )
        logger.debug("fetch meta-data about table whose data to replicate")
        table_meta = await get_table_meta_record(
            self.conn, self.namespace, self.table_name
        )
        if not table_meta:
            raise ValueError("Table not initialized. Please run initdb first.")

        table_id = self.conn.get_table_id(
            ClassRef(module=self.namespace_module, entity_name=self.table_name)
        )

        meta_table = self.conn.get_table(meta_schema.table_sync)
        await drop_delete_table_metadata(
            conn=self.conn,
            table_metadata_row=table_meta,
            metadata_table=meta_table,
        )

        await self.conn.drop_table_if_exists(table_id)
