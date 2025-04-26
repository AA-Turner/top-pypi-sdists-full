import logging
import os
from typing import AsyncIterator, Type

import aiofiles
from pysqlsync.base import BaseContext
from pysqlsync.data.exchange import AsyncTextReader
from pysqlsync.model.properties import get_primary_key_name_type
from strong_typing.inspection import DataclassInstance

from dap.dap_types import IncrementalQuery, Format, Mode
from dap.integration.database_errors import (
    MissingMetaActionInSync,
)
from dap.replicator import meta_schema
from dap.replicator.sql_metatable_handler import (
    get_table_meta_record,
    sync_upsert_table_metadata,
)
from dap.replicator.sql_op import (
    _TabularLabelMapping,
    SqlOp,
    UTC_TIMEZONE,
    fetch_schema_for_table,
)

logger: logging.Logger = logging.getLogger(__name__)
META_ACTION_NAME = "_action"
INSERT_BATCH_SIZE: int = 100000


class SqlOpSync(SqlOp):
    async def run(self) -> None:
        if not self.session:
            raise ValueError("missing required parameters")
        entity_type, schema, versioned_schema = await fetch_schema_for_table(
            self.session, self.namespace, self.table_name
        )
        await self.explorer.synchronize(modules=[meta_schema, self.namespace_module])

        logger.debug(
            f"Start operation - Synchronize. Namespace: {self.namespace}, table: {self.table_name}, conn: {self.conn}"
        )
        logger.debug("fetch meta-data about table whose data to replicate")
        table_meta = await get_table_meta_record(
            self.conn, self.namespace, self.table_name
        )
        if not table_meta:
            raise ValueError("table not initialized, use `initdb`")

        logger.debug("fetching incremental data for table from DAP API...")
        result = await self.session.get_table_data(
            self.namespace,
            self.table_name,
            IncrementalQuery(
                format=Format.TSV,
                mode=Mode.condensed,
                since=table_meta.timestamp.replace(tzinfo=UTC_TIMEZONE),
                until=None,
            ),
        )

        async with aiofiles.tempfile.TemporaryDirectory() as temp_dir:
            await self.session.download_objects(result.objects, temp_dir, decompress=True)
            await self.sync_insert_data_from_files_to_db(
                self.conn, entity_type, temp_dir
            )
            await sync_upsert_table_metadata(
                self.conn,
                self.namespace,
                result,
                schema,
                table_meta,
                self.table_name,
                versioned_schema,
            )

    @staticmethod
    async def sync_insert_data_from_files_to_db(
        conn: BaseContext, entity_type: Type[DataclassInstance], temp_dir: str
    ) -> None:
        logger.debug(
            "sync: insert data from resources saved to disk into database table"
        )

        mapping = SqlOpSync._get_sync_tabular_mapping(entity_type)

        file_names = []
        for filename in os.listdir(temp_dir):
            if filename.endswith(".tsv"):
                file_names.append(filename)
        file_names.sort()
        total_files = len(file_names)

        for index, filename in enumerate(file_names):
            logger.debug(f"processing file {index+1} of {total_files}")

            filepath = os.path.join(temp_dir, filename)

            async with aiofiles.open(filepath, mode="rb") as f:
                reader = AsyncTextReader(f, mapping.labels_to_types)
                await reader.read_header()
                columns, field_types = reader.columns, reader.field_types
                records = reader.records()

                logger.debug(f"inserting/updating data from {filepath} into database table")

                async for recordBatch in SqlOpSync._getRecordBatches(records):
                    await SqlOpSync.upsert_rows(
                        columns=columns,
                        conn=conn,
                        entity_type=entity_type,
                        field_types=field_types,
                        filepath=filepath,
                        mapping=mapping,
                        rows=recordBatch,
                    )

    @staticmethod
    async def upsert_rows(
        columns: tuple,
        conn: BaseContext,
        entity_type: Type[DataclassInstance],
        field_types: tuple,
        filepath: str,
        mapping: _TabularLabelMapping,
        rows: list[tuple],
    ) -> None:
        logger.debug(f"insert/update data from {filepath} into database table")
        table = conn.get_table(entity_type)
        field_names = tuple(mapping.labels_to_fields[c] for c in columns)
        if META_ACTION_NAME not in field_names:
            raise MissingMetaActionInSync(META_ACTION_NAME, field_names)
        meta_action_index = field_names.index(META_ACTION_NAME)
        # get the value for each row on column meta_action_index,
        # and check if it's "D" or "U" and based on that sort it to a separate list
        delete_rows = [row for row in rows if row[meta_action_index] == "D"]
        update_rows = [row for row in rows if row[meta_action_index] == "U"]
        # delete from each row the column which index is meta_action_index
        delete_rows = [
            row[:meta_action_index] + row[meta_action_index + 1:]
            for row in delete_rows
        ]
        update_rows = [
            row[:meta_action_index] + row[meta_action_index + 1:]
            for row in update_rows
        ]
        # delete meta_action_index from field_names and field_types
        field_names = (
            field_names[:meta_action_index] + field_names[meta_action_index + 1:]
        )
        field_types = (
            field_types[:meta_action_index] + field_types[meta_action_index + 1:]
        )
        # get the key type and key values of the table and the key values of the rows
        primary_name, primary_type = get_primary_key_name_type(entity_type)
        primary_name_index = field_names.index(primary_name)
        delete_keys = [row[primary_name_index] for row in delete_rows]
        await conn.upsert_rows(
            table,
            field_names=field_names,
            field_types=field_types,
            records=update_rows,
        )
        await conn.delete_rows(
            table,
            key_type=primary_type,
            key_values=delete_keys,
        )

    @staticmethod
    def _get_sync_tabular_mapping(
        entity_type: type[DataclassInstance],
    ) -> _TabularLabelMapping:
        mapping = _TabularLabelMapping(
            labels_to_types={"meta.ts": type(None), "meta.action": str},
            labels_to_fields={"meta.ts": "", "meta.action": META_ACTION_NAME},
        )
        return SqlOp.get_tabular_mapping(entity_type, mapping)
    
    @staticmethod
    async def _getRecordBatches(records: AsyncIterator[tuple]) -> AsyncIterator[list[tuple]]:
        batch = []
        async for record in records:
            batch.append(record)
            if len(batch) == INSERT_BATCH_SIZE:
                yield batch
                batch = []
        if batch:
            yield batch
