import inspect

from fa_purity import FrozenDict, FrozenList
from redshift_client.client import (
    GroupedRows,
    TableRow,
)
from redshift_client.core.column import ColumnId
from redshift_client.core.table import Table
from redshift_client.sql_client import (
    DbPrimitive,
)

from .bug import Bug


def assert_table_row(
    table: Table,
    rows: FrozenDict[ColumnId, DbPrimitive],
    name: str,
    context: FrozenList[str],
) -> TableRow:
    return (
        TableRow.new(table, rows)
        .alt(
            lambda e: Bug.new(
                name,
                inspect.currentframe(),
                e,
                context,
            ).explode(),
        )
        .to_union()
    )


def assert_grouped_row(
    table: Table,
    rows: FrozenList[TableRow],
    name: str,
    context: FrozenList[str],
) -> GroupedRows:
    return (
        GroupedRows.new(
            table,
            rows,
        )
        .alt(
            lambda e: Bug.new(
                name,
                inspect.currentframe(),
                e,
                context,
            ).explode(),
        )
        .to_union()
    )
