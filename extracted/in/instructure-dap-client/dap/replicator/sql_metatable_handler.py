import logging
from typing import Dict, Optional

from pysqlsync.base import BaseContext
from pysqlsync.formation.object_types import Table
from pysqlsync.model.data_types import quote
from pysqlsync.model.key_types import DEFAULT
from strong_typing.core import JsonType
from strong_typing.serialization import json_dump_string

from dap.dap_types import GetTableDataResult, VersionedSchema
from dap.replicator import meta_schema
from dap.replicator.sql_op import UTC_TIMEZONE

logger: logging.Logger = logging.getLogger(__name__)


async def get_table_names_in_namespace_from_meta(
    conn: BaseContext, namespace: str
) -> list[str]:
    "Retrieves the names of tables in the namespace from the meta-table."

    meta_table = conn.get_table(meta_schema.table_sync)
    records = await conn.query_all(
        str,
        "SELECT source_table\n"
        f"FROM {meta_table.name}\n"
        f"WHERE source_namespace = {quote(namespace)}",
    )
    return records


async def get_table_meta_record(
    conn: BaseContext, namespace: str, table_name: str
) -> Optional[meta_schema.table_sync]:
    "Retrieves the synchronization record for a table."

    table = conn.get_table(meta_schema.table_sync)
    records = await conn.query_all(
        meta_schema.table_sync,
        "SELECT id, source_namespace, source_table, timestamp, schema_version, target_schema, target_table, schema_description_format, schema_description\n"
        f"FROM {table.name}\n"
        f"WHERE source_namespace = {quote(namespace)} AND source_table = {quote(table_name)}",
    )
    if records:
        return records[0]
    else:
        return None


async def initdb_insert_table_metadata(
    conn: BaseContext,
    namespace: str,
    table_data: GetTableDataResult,
    schema: Dict[str, JsonType],
    table_name: str,
    versioned_schema: VersionedSchema,
) -> None:
    logger.debug(f"insert meta-data about table {table_name} that has been replicated")
    await conn.insert_data(
        meta_schema.table_sync,
        [
            meta_schema.table_sync(
                id=DEFAULT,
                source_namespace=namespace,
                source_table=table_name,
                timestamp=table_data.timestamp.astimezone(UTC_TIMEZONE).replace(
                    tzinfo=None
                ),
                schema_version=versioned_schema.version,
                target_schema=namespace,
                target_table=table_name,
                schema_description_format="json",
                schema_description=json_dump_string(schema),
            )
        ],
    )


async def sync_upsert_table_metadata(
    conn: BaseContext,
    namespace: str,
    table_data: GetTableDataResult,
    schema: JsonType,
    table_meta: Optional[meta_schema.table_sync],
    table_name: str,
    versioned_schema: VersionedSchema,
) -> None:
    logger.debug(f"update meta-data about table {table_name} that has been replicated")
    if table_meta is None:
        raise AssertionError("Internal error: ‘table_meta’ must not be null. Please report this issue.")

    await conn.upsert_data(
        meta_schema.table_sync,
        [
            meta_schema.table_sync(
                id=table_meta.id,
                source_namespace=namespace,
                source_table=table_name,
                timestamp=table_data.timestamp.astimezone(UTC_TIMEZONE).replace(
                    tzinfo=None
                ),
                schema_version=versioned_schema.version,
                target_schema=namespace,
                target_table=table_name,
                schema_description_format="json",
                schema_description=json_dump_string(schema),
            )
        ],
    )


async def drop_delete_table_metadata(
    conn: BaseContext, table_metadata_row: meta_schema.table_sync, metadata_table: Table
) -> None:
    logger.debug(
        f"drop meta-data about table {table_metadata_row.source_namespace}.{table_metadata_row.target_table}"
    )
    await conn.delete_rows(metadata_table, int, [table_metadata_row.id])
