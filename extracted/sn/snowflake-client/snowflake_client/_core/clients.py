from collections.abc import Callable
from dataclasses import (
    dataclass,
)

from fa_purity import (
    Cmd,
    FrozenDict,
    PureIter,
    ResultE,
)
from redshift_client.client import (
    GroupedRows,
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
    Table,
)
from redshift_client.sql_client import (
    Limit,
    RowData,
)

BluePrint = DbTableId
NewTable = DbTableId
Source = DbTableId
Target = DbTableId


@dataclass(frozen=True, kw_only=True)
class TableClient:
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
class SchemaClient:
    all_schemas: Cmd[ResultE[frozenset[SchemaId]]]
    table_ids: Callable[[SchemaId], Cmd[ResultE[frozenset[DbTableId]]]]
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
