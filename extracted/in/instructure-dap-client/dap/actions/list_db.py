import json
from datetime import datetime, timezone
from typing import Optional

from pysqlsync.model.id_types import PrefixedId, QualifiedId

from .. import ui
from ..api import DAPClient
from ..dap_types import Credentials
from ..integration.database import DatabaseConnection
from ..replicator import meta_schema
from ..replicator.sql_metatable_handler import (
    get_table_meta_record,
    get_table_names_in_namespace_from_meta,
)


def _count_from_clause(
    dialect: str, target_schema: Optional[str], target_table: str
) -> str:
    if dialect == "mysql":
        # MySQL has no schemas; pysqlsync uses namespace__table (ANSI_QUOTES mode is always enabled)
        return str(PrefixedId(target_schema, target_table))
    else:
        # PostgreSQL and MSSQL use schema.table
        return str(QualifiedId(target_schema, target_table))


def cell(value: str | None, fallback: str = "-") -> tuple[ui.MsgType, str]:
    if value is not None:
        return (ui.MsgType.TITLE, value)
    return (ui.MsgType.INFO, fallback)


def calculate_age(timestamp: datetime) -> str:
    # timestamp is naive but represents UTC time, so get current UTC time for comparison
    now = (
        datetime.now(timezone.utc).replace(tzinfo=None)
        if timestamp.tzinfo is None
        else datetime.now(timestamp.tzinfo)
    )
    age_seconds = int((now - timestamp).total_seconds())
    days, remainder = divmod(age_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 0:
        return f"{days}d {hours}h" if hours > 0 else f"{days}d"
    elif hours > 0:
        return f"{hours}h {minutes}m" if minutes > 0 else f"{hours}h"
    elif minutes > 0:
        return f"{minutes}m {seconds}s" if seconds > 0 else f"{minutes}m"
    else:
        return f"{seconds}s"


async def list_db(
    base_url: str,
    credentials: Credentials,
    connection_string: str,
    namespace: str,
    tracking: Optional[bool] = None,
    omit_not_replicated: bool = False,
    omit_record_count: bool = False,
) -> None:
    dap_tables_names = []
    async with DAPClient(
        base_url=base_url, credentials=credentials, tracking=tracking
    ) as session:
        dap_tables_names = await session.get_tables(namespace)
        if not omit_record_count:
            ui.info("Querying table record counts...")
        db_connection = DatabaseConnection(connection_string)
        async with db_connection.connection as base_connection:
            explorer = db_connection.engine.create_explorer(base_connection)
            await explorer.synchronize(modules=[meta_schema])
            db_table_names = await get_table_names_in_namespace_from_meta(
                base_connection, namespace
            )
            db_table_meta_records: dict[str, Optional[meta_schema.table_sync]] = {}
            for table_name in sorted(db_table_names):
                meta = await get_table_meta_record(
                    base_connection, namespace, table_name
                )
                if meta is not None:
                    db_table_meta_records[table_name] = meta
            if not omit_not_replicated:
                for table_name in sorted(dap_tables_names):
                    if table_name not in db_table_meta_records:
                        db_table_meta_records[table_name] = None

            db_table_record_counts = {}
            for table_name, meta in db_table_meta_records.items():
                if meta is not None and not omit_record_count:
                    from_clause = _count_from_clause(
                        db_connection.dialect, meta.target_schema, meta.target_table
                    )
                    count = await base_connection.query_one(
                        int,
                        f"SELECT COUNT(*) FROM {from_clause}",
                    )
                    db_table_record_counts[table_name] = count

            title_str = f"Local database replication status of tables in namespace [bold]{namespace}[/bold]"
            columns = [
                ui.TableColumn("Name", style="bold"),
                *(
                    []
                    if omit_record_count
                    else [ui.TableColumn("Records", style="bold", justify="right")]
                ),
                ui.TableColumn("Data as of"),
                ui.TableColumn("Staleness"),
                ui.TableColumn("Schema", justify="right"),
                ui.TableColumn("Use command"),
            ]
            ui.print_table(
                title=title_str,
                columns=columns,
                rows=[
                    [
                        cell(table_name if meta is not None else None, table_name),
                        *(
                            []
                            if omit_record_count
                            else [
                                cell(
                                    str(db_table_record_counts[table_name])
                                    if table_name in db_table_record_counts
                                    else None
                                )
                            ]
                        ),
                        cell(
                            meta.timestamp.replace(tzinfo=timezone.utc)
                            .astimezone()
                            .isoformat()
                            if meta is not None
                            else None,
                            "Not replicated",
                        ),
                        cell(
                            calculate_age(meta.timestamp) if meta is not None else None
                        ),
                        cell(str(meta.schema_version) if meta is not None else None),
                        cell("syncdb" if meta is not None else None, "initdb"),
                    ]
                    for table_name, meta in db_table_meta_records.items()
                ],
            )
            if not ui.is_interactive():
                rows = []
                for table_name, meta in db_table_meta_records.items():
                    row: dict = {
                        "name": table_name,
                        "timestamp": meta.timestamp.replace(tzinfo=timezone.utc)
                        .astimezone()
                        .isoformat()
                        if meta is not None
                        else None,
                        "staleness": calculate_age(meta.timestamp)
                        if meta is not None
                        else None,
                        "schema": meta.schema_version if meta is not None else None,
                        "command": "syncdb" if meta is not None else "initdb",
                    }
                    if not omit_record_count:
                        row["records"] = db_table_record_counts.get(table_name)
                    rows.append(row)
                print(json.dumps(rows, indent=2))

            if session.tracking_data:
                session.tracking_data.set_cmd_info("listdb", namespace, None)
                session.tracking_data.db_dialect = db_connection.dialect
                session.tracking_data.db_version = await db_connection.get_version(
                    db_connection.dialect, base_connection
                )
