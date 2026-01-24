from dataclasses import (
    dataclass,
)

from fa_purity import (
    Cmd,
    FrozenDict,
    Maybe,
    PureIter,
    ResultE,
)
from fluidattacks_etl_utils.typing import (
    Callable,
    FrozenSet,
)
from redshift_client.client import (
    GroupedRows,
)
from redshift_client.client import (
    SchemaClient as RedshiftSchemaClient,
)
from redshift_client.client import (
    TableClient as RedshiftTableClient,
)
from redshift_client.core.column import (
    Column,
    ColumnObj,
)
from redshift_client.core.id_objs import (
    ColumnId,
    DbTableId,
    SchemaId,
    TableId,
)
from redshift_client.core.table import (
    DistStyle,
    SortKeys,
    Table,
    TableAttrs,
)
from redshift_client.sql_client import (
    Limit,
    RowData,
)
from snowflake_client import (
    SchemaClient,
    TableClient,
)

BluePrint = DbTableId
NewTable = DbTableId
Source = DbTableId
Target = DbTableId


@dataclass(frozen=True, kw_only=True)
class CommonTableClient:
    """Table client interface. See factory method documentation for further details."""

    get: Callable[[DbTableId], Cmd[ResultE[Table]]]
    exist: Callable[[DbTableId], Cmd[ResultE[bool]]]
    insert: Callable[[DbTableId, Table, PureIter[RowData], Limit], Cmd[ResultE[None]]]
    named_insert: Callable[[DbTableId, GroupedRows], Cmd[ResultE[None]]]
    rename: Callable[[DbTableId, str], Cmd[ResultE[TableId]]]
    delete: Callable[[DbTableId], Cmd[ResultE[None]]]
    delete_cascade: Callable[[DbTableId], Cmd[ResultE[None]]]
    add_column: Callable[[DbTableId, ColumnObj], Cmd[ResultE[None]]]
    add_columns: Callable[[DbTableId, FrozenDict[ColumnId, Column]], Cmd[ResultE[None]]]
    new: Callable[[DbTableId, Table], Cmd[ResultE[None]]]
    new_if_not_exist: Callable[[DbTableId, Table], Cmd[ResultE[None]]]
    create_like: Callable[[BluePrint, NewTable], Cmd[ResultE[None]]]
    move_data: Callable[[Source, Target], Cmd[ResultE[None]]]
    move: Callable[[Source, Target], Cmd[ResultE[None]]]
    migrate: Callable[[Source, Target], Cmd[ResultE[None]]]


@dataclass(frozen=True, kw_only=True)
class CommonSchemaClient:
    all_schemas: Cmd[ResultE[FrozenSet[SchemaId]]]
    table_ids: Callable[[SchemaId], Cmd[ResultE[FrozenSet[DbTableId]]]]
    exist: Callable[[SchemaId], Cmd[ResultE[bool]]]
    delete: Callable[[SchemaId], Cmd[ResultE[None]]]
    delete_cascade: Callable[[SchemaId], Cmd[ResultE[None]]]
    rename: Callable[[SchemaId, SchemaId], Cmd[ResultE[None]]]
    create: Callable[[SchemaId], Cmd[ResultE[None]]]
    create_if_not_exist: Callable[[SchemaId], Cmd[ResultE[None]]]
    recreate: Callable[[SchemaId], Cmd[ResultE[None]]]
    recreate_cascade: Callable[[SchemaId], Cmd[ResultE[None]]]
    migrate: Callable[[SchemaId, SchemaId], Cmd[ResultE[None]]]
    move: Callable[[SchemaId, SchemaId], Cmd[ResultE[None]]]


@dataclass(frozen=True)
class ClientAdapter:
    @staticmethod
    def snowflake_table_client_adapter(
        client: TableClient,
    ) -> CommonTableClient:
        return CommonTableClient(
            get=client.get,
            exist=client.exist,
            insert=client.insert,
            named_insert=client.named_insert,
            rename=client.rename,
            delete=client.delete,
            delete_cascade=client.delete_cascade,
            add_column=client.add_column,
            add_columns=client.add_columns,
            new=client.new,
            new_if_not_exist=client.new_if_not_exist,
            create_like=client.create_like,
            move_data=client.move_data,
            move=client.move,
            migrate=client.migrate,
        )

    @staticmethod
    def redshift_table_client_adapter(
        client: RedshiftTableClient,
    ) -> CommonTableClient:
        return CommonTableClient(
            get=client.get,
            exist=client.exist,
            insert=client.insert,
            named_insert=client.named_insert,
            rename=client.rename,
            delete=client.delete,
            delete_cascade=client.delete_cascade,
            add_column=client.add_column,
            add_columns=client.add_columns,
            new=lambda i, t: client.new(
                i,
                t,
                TableAttrs(DistStyle.AUTO, Maybe.empty(), True, SortKeys.auto()),
            ),
            new_if_not_exist=lambda i, t: client.new_if_not_exist(
                i,
                t,
                TableAttrs(DistStyle.AUTO, Maybe.empty(), True, SortKeys.auto()),
            ),
            create_like=client.create_like,
            move_data=client.move_data,
            move=client.move,
            migrate=client.migrate,
        )

    @staticmethod
    def _schema_client_adapter(
        client: SchemaClient | RedshiftSchemaClient,
    ) -> CommonSchemaClient:
        return CommonSchemaClient(
            all_schemas=client.all_schemas,
            table_ids=client.table_ids,
            exist=client.exist,
            delete=client.delete,
            delete_cascade=client.delete_cascade,
            rename=client.rename,
            create=client.create,
            create_if_not_exist=client.create_if_not_exist,
            recreate=client.recreate,
            recreate_cascade=client.recreate_cascade,
            migrate=client.migrate,
            move=client.move,
        )

    @classmethod
    def snowflake_schema_client_adapter(
        cls,
        client: SchemaClient,
    ) -> CommonSchemaClient:
        return cls._schema_client_adapter(client)

    @classmethod
    def redshift_schema_client_adapter(
        cls,
        client: RedshiftSchemaClient,
    ) -> CommonSchemaClient:
        return cls._schema_client_adapter(client)
