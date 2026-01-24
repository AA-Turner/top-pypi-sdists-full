from __future__ import (
    annotations,
)

from collections.abc import Callable
from dataclasses import (
    dataclass,
    field,
)

from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    PureIter,
    PureIterFactory,
    Result,
    ResultE,
    ResultTransform,
    cast_exception,
)

from redshift_client._utils import (
    NonEmptySet,
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
from redshift_client.core.schema import (
    SchemaPolicy,
)
from redshift_client.core.table import (
    ManifestId,
    Table,
    TableAttrs,
)
from redshift_client.sql_client import (
    DbPrimitive,
    Limit,
    RowData,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class TableRow:
    """
    Ensure a key value map that match table columns.

    i.e.
    - all keys on the map belongs to a column in the table
    - all columns are listed on the map keys
    """

    _private: _Private = field(repr=False, hash=False, compare=False)
    table: Table
    row: FrozenDict[ColumnId, DbPrimitive]

    @staticmethod
    def new(
        table: Table,
        row: FrozenDict[ColumnId, DbPrimitive],
    ) -> ResultE[TableRow]:
        _columns = frozenset(table.order)
        _row_keys = frozenset(row.keys())

        missing_columns = (
            NonEmptySet.optional_non_empty(_columns - _row_keys)
            .to_result()
            .swap()
            .alt(
                lambda e: Exception(
                    f"All 'columns' must be in the 'row keys'. Missing: {e.to_set()}",
                ),
            )
        )
        missing_fields = (
            NonEmptySet.optional_non_empty(_row_keys - _columns)
            .to_result()
            .swap()
            .alt(
                lambda e: Exception(
                    f"All 'row keys' must be in 'columns'. Missing: {e.to_set()}",
                ),
            )
        )
        return missing_columns.bind(
            lambda _: missing_fields.map(
                lambda _: TableRow(_Private(), table, row),
            ),
        )


@dataclass(frozen=True)
class GroupedRows:
    _private: _Private = field(repr=False, hash=False, compare=False)
    table: Table
    rows: FrozenList[TableRow]

    @staticmethod
    def new(table: Table, rows: FrozenList[TableRow]) -> ResultE[GroupedRows]:
        def _valid(row: TableRow) -> ResultE[TableRow]:
            if row.table == table:
                return Result.success(row)
            return Result.failure(
                ValueError("TableRow does not belong to the current table"),
                TableRow,
            ).alt(cast_exception)

        return ResultTransform.all_ok(
            PureIterFactory.from_list(rows).map(_valid).to_list(),
        ).map(lambda r: GroupedRows(_Private(), table, r))


@dataclass(frozen=True)
class SchemaClient:
    all_schemas: Cmd[ResultE[frozenset[SchemaId]]]
    table_ids: Callable[[SchemaId], Cmd[ResultE[frozenset[DbTableId]]]]
    exist: Callable[[SchemaId], Cmd[ResultE[bool]]]
    delete: Callable[[SchemaId], Cmd[ResultE[None]]]
    delete_cascade: Callable[[SchemaId], Cmd[ResultE[None]]]
    _rename: Callable[[SchemaId, SchemaId], Cmd[ResultE[None]]]
    create: Callable[[SchemaId], Cmd[ResultE[None]]]
    create_if_not_exist: Callable[[SchemaId], Cmd[ResultE[None]]]
    recreate: Callable[[SchemaId], Cmd[ResultE[None]]]
    recreate_cascade: Callable[[SchemaId], Cmd[ResultE[None]]]
    _migrate: Callable[[SchemaId, SchemaId], Cmd[ResultE[None]]]
    _move: Callable[[SchemaId, SchemaId], Cmd[ResultE[None]]]
    set_policy: Callable[[SchemaId, SchemaPolicy], Cmd[ResultE[None]]]

    def rename(self, old: SchemaId, new: SchemaId) -> Cmd[ResultE[None]]:
        return self._rename(old, new)

    def migrate(
        self,
        source: SchemaId,
        target: SchemaId,
    ) -> Cmd[ResultE[None]]:
        """
        Move all tables from `source` to `target` overwriting `target` data.

        Deletes empty source after success.
        """
        return self._migrate(source, target)

    def move(self, source: SchemaId, target: SchemaId) -> Cmd[ResultE[None]]:
        """
        Move all tables from `source` to `target`.

        It does not overwrite target data.
        Deletes empty source after success.
        """
        return self._move(source, target)


@dataclass(frozen=True)
class AwsRole:
    role: str


@dataclass(frozen=True)
class S3Prefix:
    prefix: str


@dataclass(frozen=True)
class NanHandler:
    enabled: bool


BluePrint = DbTableId
NewTable = DbTableId
Source = DbTableId
Target = DbTableId


@dataclass(frozen=True)
class TableClient:
    """Table client interface. See factory method documentation for further details."""

    unload: Callable[[DbTableId, S3Prefix, AwsRole], Cmd[ResultE[ManifestId]]]
    load: Callable[
        [DbTableId, ManifestId, AwsRole, NanHandler],
        Cmd[ResultE[None]],
    ]
    get: Callable[[DbTableId], Cmd[ResultE[Table]]]
    exist: Callable[[DbTableId], Cmd[ResultE[bool]]]
    insert: Callable[
        [DbTableId, Table, PureIter[RowData], Limit],
        Cmd[ResultE[None]],
    ]
    named_insert: Callable[[DbTableId, GroupedRows], Cmd[ResultE[None]]]
    rename: Callable[[DbTableId, str], Cmd[ResultE[TableId]]]
    delete: Callable[[DbTableId], Cmd[ResultE[None]]]
    delete_cascade: Callable[[DbTableId], Cmd[ResultE[None]]]
    add_column: Callable[[DbTableId, ColumnObj], Cmd[ResultE[None]]]
    add_columns: Callable[
        [DbTableId, FrozenDict[ColumnId, Column]],
        Cmd[ResultE[None]],
    ]
    new: Callable[[DbTableId, Table, TableAttrs], Cmd[ResultE[None]]]
    new_if_not_exist: Callable[
        [DbTableId, Table, TableAttrs],
        Cmd[ResultE[None]],
    ]
    create_like: Callable[[BluePrint, NewTable], Cmd[ResultE[None]]]
    move_data: Callable[[Source, Target], Cmd[ResultE[None]]]
    move: Callable[[Source, Target], Cmd[ResultE[None]]]
    migrate: Callable[[Source, Target], Cmd[ResultE[None]]]
