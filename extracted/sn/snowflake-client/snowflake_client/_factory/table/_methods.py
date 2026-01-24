from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    PureIter,
    PureIterFactory,
    Result,
    ResultE,
    ResultTransform,
    Unsafe,
    cast_exception,
)
from fa_purity.json import (
    JsonPrimitiveUnfolder,
    Primitive,
)
from redshift_client import (
    _utils,
)
from redshift_client.client._core import (
    GroupedRows,
    TableRow,
)
from redshift_client.core.column import (
    Column,
    ColumnId,
    ColumnObj,
)
from redshift_client.core.data_type.core import DataType, StaticTypes
from redshift_client.core.id_objs import (
    DbTableId,
    Identifier,
    SchemaId,
    TableId,
)
from redshift_client.core.table import (
    Table,
)
from redshift_client.sql_client import (
    DbPrimitive,
    DbPrimitiveFactory,
    Limit,
    QueryValues,
    RowData,
    Template,
)

from snowflake_client._core.cursor import (
    SnowflakeCursor,
)
from snowflake_client._core.query import (
    SnowflakeQuery,
)

from . import (
    _encode,
)
from ._assert import (
    to_column,
)


def _int_to_str(value: int) -> str:
    return str(value)


def _to_raw_schema(schema: SchemaId) -> str:
    return schema.name.to_str().upper()


def _to_raw_table(table: TableId) -> str:
    return table.name.to_str().upper()


def _to_raw_column(column: ColumnId) -> str:
    return column.name.to_str().upper()


def get(client: SnowflakeCursor, table: DbTableId) -> Cmd[ResultE[Table]]:
    stm = """
        SELECT ordinal_position,
            column_name,
            data_type,
            CASE WHEN character_maximum_length IS not null
                    THEN character_maximum_length
                    ELSE numeric_precision end AS max_length,
            numeric_scale,
            is_nullable,
            column_default AS default_value
        FROM information_schema.columns
        WHERE table_schema = %(table_schema)s
            AND table_name = %(table_name)s
        ORDER BY ordinal_position
    """
    args: dict[str, Primitive] = {
        "table_schema": _to_raw_schema(table.schema),
        "table_name": _to_raw_table(table.table),
    }
    exe = client.execute(
        SnowflakeQuery.new_query(stm),
        QueryValues(DbPrimitiveFactory.from_raw_prim_dict(FrozenDict(args))),
    )
    results = client.fetch_all

    def _extract(raw: FrozenList[RowData]) -> ResultE[Table]:
        columns_pairs = ResultTransform.all_ok(
            PureIterFactory.from_list(raw).map(lambda c: to_column(c.data)).to_list(),
        )
        columns = columns_pairs.map(lambda i: FrozenDict(dict(i)))
        order = columns_pairs.map(lambda i: PureIterFactory.from_list(i).map(lambda c: c[0]))
        return columns.bind(lambda c: order.bind(lambda o: Table.new(o.to_list(), c, frozenset())))

    return _utils.chain_results(exe, results).map(lambda r: r.bind(_extract))


def exist(client: SnowflakeCursor, table: DbTableId) -> Cmd[ResultE[bool]]:
    stm = """
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = %(table_schema)s
            AND table_name = %(table_name)s
        );
    """
    args: dict[str, Primitive] = {
        "table_schema": _to_raw_schema(table.schema),
        "table_name": _to_raw_table(table.table),
    }
    return _utils.chain_results(
        client.execute(
            SnowflakeQuery.new_query(stm),
            QueryValues(DbPrimitiveFactory.from_raw_prim_dict(FrozenDict(args))),
        ),
        client.fetch_one.map(
            lambda r: r.bind(
                lambda m: m.to_result()
                .alt(lambda _: cast_exception(TypeError("Expected not Empty")))
                .bind(
                    lambda e: _utils.get_index(e.data, 0).bind(
                        lambda v: v.map(
                            lambda p: JsonPrimitiveUnfolder.to_bool(p),
                            lambda _: Result.failure(
                                TypeError("Expected `JsonPrimitive` but got `datetime`"),
                                bool,
                            ).alt(cast_exception),
                        ),
                    ),
                ),
            ),
        ),
    )


def insert(
    client: SnowflakeCursor,
    table_id: DbTableId,
    table: Table,
    items: PureIter[RowData],
    limit: Limit,
) -> Cmd[ResultE[None]]:
    _fields = ",".join(f"{{field_{i}}}" for i, _ in enumerate(table.order))
    stm = f"""
        INSERT INTO {{schema}}.{{table}} ({_fields}) VALUES %s
    """  # noqa: S608
    identifiers: dict[str, str] = {
        "schema": _to_raw_schema(table_id.schema),
        "table": _to_raw_table(table_id.table),
    }
    for i, c in enumerate(table.order):
        identifiers[f"field_{i}"] = c.name.to_str()
    return client.values(
        SnowflakeQuery.dynamic_query(stm, FrozenDict(identifiers))
        .alt(Unsafe.raise_exception)
        .to_union(),
        items,
        limit,
    )


def _column_name(num: int, column: Column) -> str:
    column_name = "column" + _int_to_str(num)
    if column.data_type == DataType(StaticTypes.SUPER):
        return "PARSE_JSON(" + column_name + ")"
    return column_name


def _named_insert_with_variant(
    client: SnowflakeCursor,
    table_id: DbTableId,
    data: GroupedRows,
) -> Cmd[ResultE[None]]:
    _enumerated = PureIterFactory.from_list(data.table.order).enumerate(1)
    _template = _enumerated.map(lambda t: "%(field_" + _int_to_str(t[0]) + ")s")
    _field_map = FrozenDict(dict(_enumerated.map(lambda t: (t[1], "field_" + _int_to_str(t[0])))))
    _columns = ",".join(_enumerated.map(lambda t: _column_name(t[0], data.table.columns[t[1]])))
    stm = f"INSERT INTO {{schema}}.{{table}} SELECT {_columns} FROM VALUES %s"  # noqa: S608
    identifiers: dict[str, str] = {
        "schema": _to_raw_schema(table_id.schema),
        "table": _to_raw_table(table_id.table),
    }

    def _to_fields_map(item: TableRow) -> QueryValues:
        return QueryValues(FrozenDict({_field_map[k]: v for k, v in item.row.items()}))

    values = PureIterFactory.from_list(data.rows).map(_to_fields_map)
    return client.named_values(
        SnowflakeQuery.dynamic_query(stm, FrozenDict(identifiers))
        .alt(Unsafe.raise_exception)
        .to_union(),
        Template(_template.to_list()),
        values.to_list(),
    )


def _named_insert_no_variant(
    client: SnowflakeCursor,
    table_id: DbTableId,
    data: GroupedRows,
) -> Cmd[ResultE[None]]:
    _enumerated = PureIterFactory.from_list(data.table.order).enumerate(1)
    _field_placeholders = _enumerated.map(lambda t: "{field_" + _int_to_str(t[0]) + "}")
    _template = _enumerated.map(lambda t: "%(field_" + _int_to_str(t[0]) + ")s")
    _field_map = FrozenDict(dict(_enumerated.map(lambda t: (t[1], "field_" + _int_to_str(t[0])))))
    _fields = ",".join(_field_placeholders)
    stm = f"INSERT INTO {{schema}}.{{table}} ({_fields}) VALUES %s"  # noqa: S608
    identifiers: dict[str, str] = dict(
        _enumerated.map(lambda t: ("field_" + _int_to_str(t[0]), t[1].name.to_str())),
    ) | {
        "schema": _to_raw_schema(table_id.schema),
        "table": _to_raw_table(table_id.table),
    }

    def _to_fields_map(item: TableRow) -> QueryValues:
        return QueryValues(FrozenDict({_field_map[k]: v for k, v in item.row.items()}))

    values = PureIterFactory.from_list(data.rows).map(_to_fields_map)
    return client.named_values(
        SnowflakeQuery.dynamic_query(stm, FrozenDict(identifiers))
        .alt(Unsafe.raise_exception)
        .to_union(),
        Template(_template.to_list()),
        values.to_list(),
    )


def named_insert(
    client: SnowflakeCursor,
    table_id: DbTableId,
    data: GroupedRows,
) -> Cmd[ResultE[None]]:
    has_variant = any(
        i[1].data_type == DataType(StaticTypes.SUPER) for i in tuple(data.table.columns.items())
    )
    if has_variant:
        return _named_insert_with_variant(client, table_id, data)
    return _named_insert_no_variant(client, table_id, data)


def rename(client: SnowflakeCursor, table_id: DbTableId, new_name: str) -> Cmd[ResultE[TableId]]:
    stm = """
        ALTER TABLE {schema}.{table} RENAME TO {new_name}
    """
    identifiers: dict[str, str] = {
        "schema": _to_raw_schema(table_id.schema),
        "table": _to_raw_table(table_id.table),
        "new_name": new_name,
    }
    return client.execute(
        SnowflakeQuery.dynamic_query(stm, FrozenDict(identifiers))
        .alt(Unsafe.raise_exception)
        .to_union(),
        None,
    ).map(lambda r: r.map(lambda _: TableId(Identifier.new(new_name))))


def delete(client: SnowflakeCursor, table_id: DbTableId, cascade: bool) -> Cmd[ResultE[None]]:
    _cascade = "CASCADE" if cascade else ""
    stm = f"""
        DROP TABLE {{schema}}.{{table}} {_cascade}
    """
    identifiers: dict[str, str] = {
        "schema": _to_raw_schema(table_id.schema),
        "table": _to_raw_table(table_id.table),
    }
    return client.execute(
        SnowflakeQuery.dynamic_query(stm, FrozenDict(identifiers))
        .alt(Unsafe.raise_exception)
        .to_union(),
        None,
    )


def add_column(
    client: SnowflakeCursor,
    table_id: DbTableId,
    column: ColumnObj,
) -> Cmd[ResultE[None]]:
    stm = f"""
        ALTER TABLE {{table_schema}}.{{table_name}}
        ADD COLUMN {{column_name}}
        {_encode.encode_data_type(column.column.data_type)} DEFAULT %(default_val)s
    """
    identifiers: dict[str, str] = {
        "table_schema": _to_raw_schema(table_id.schema),
        "table_name": _to_raw_table(table_id.table),
        "column_name": _to_raw_column(column.id_obj),
    }
    args: dict[str, DbPrimitive] = {
        "default_val": column.column.default,
    }
    return client.execute(
        SnowflakeQuery.dynamic_query(stm, FrozenDict(identifiers))
        .alt(Unsafe.raise_exception)
        .to_union(),
        QueryValues(FrozenDict(args)),
    )


def add_columns(
    client: SnowflakeCursor,
    table: DbTableId,
    columns: FrozenDict[ColumnId, Column],
) -> Cmd[ResultE[None]]:
    return (
        PureIterFactory.from_list(tuple(columns.items()))
        .map(lambda c: ColumnObj(c[0], c[1]))
        .map(lambda c: add_column(client, table, c))
        .transform(lambda x: _utils.extract_fail(x))
    )


def create_like(
    client: SnowflakeCursor,
    blueprint: DbTableId,
    new_table: DbTableId,
) -> Cmd[ResultE[None]]:
    stm = """
        CREATE TABLE {new_schema}.{new_table}
        LIKE {blueprint_schema}.{blueprint_table}
    """
    identifiers: dict[str, str] = {
        "blueprint_schema": _to_raw_schema(blueprint.schema),
        "blueprint_table": _to_raw_table(blueprint.table),
        "new_schema": _to_raw_schema(new_table.schema),
        "new_table": _to_raw_table(new_table.table),
    }
    return client.execute(
        SnowflakeQuery.dynamic_query(stm, FrozenDict(identifiers))
        .alt(Unsafe.raise_exception)
        .to_union(),
        None,
    )


def schema_rename(
    client: SnowflakeCursor,
    source: DbTableId,
    target: DbTableId,
) -> Cmd[ResultE[None]]:
    """Move/rename a table between schemas."""
    stm = """
        ALTER TABLE {source_schema}.{source_table}
        RENAME TO {target_schema}.{target_table}
    """
    identifiers: dict[str, str] = {
        "source_schema": _to_raw_schema(source.schema),
        "source_table": _to_raw_table(source.table),
        "target_schema": _to_raw_schema(target.schema),
        "target_table": _to_raw_table(target.table),
    }
    return client.execute(
        SnowflakeQuery.dynamic_query(stm, FrozenDict(identifiers))
        .alt(Unsafe.raise_exception)
        .to_union(),
        None,
    )


def move_data(client: SnowflakeCursor, source: DbTableId, target: DbTableId) -> Cmd[ResultE[None]]:
    """
    Move table data from source to target.

    - Both tables must exists
    """
    stm = """
    INSERT INTO {target_schema}.{target_table} SELECT * FROM {source_schema}.{source_table};
    """
    identifiers: dict[str, str] = {
        "source_schema": source.schema.name.to_str(),
        "source_table": source.table.name.to_str(),
        "target_schema": target.schema.name.to_str(),
        "target_table": target.table.name.to_str(),
    }
    return client.execute(
        SnowflakeQuery.dynamic_query(stm, FrozenDict(identifiers))
        .alt(Unsafe.raise_exception)
        .to_union(),
        None,
    )


def move(client: SnowflakeCursor, source: DbTableId, target: DbTableId) -> Cmd[ResultE[None]]:
    """
    Move tables.

    - create target if not exist
    - move_data (append) data from source into target
    - delete source table (that will be empty)
    """
    nothing: Cmd[ResultE[None]] = Cmd.wrap_value(Result.success(None))
    create = _utils.chain(
        exist(client, target),
        lambda b: create_like(client, source, target) if not b else nothing,
    ).map(lambda r: r.bind(lambda v: v))
    return _utils.chain_results(
        _utils.chain_results(create, move_data(client, source, target)),
        delete(client, source, True),
    )


def migrate(client: SnowflakeCursor, source: DbTableId, target: DbTableId) -> Cmd[ResultE[None]]:
    """
    Migrate tables.

    - delete target if exist
    - rename source into target
    """
    nothing: Cmd[ResultE[None]] = Cmd.wrap_value(Result.success(None))
    _delete = _utils.chain(
        exist(client, target),
        lambda b: delete(client, target, True) if b else nothing,
    ).map(lambda r: r.bind(lambda v: v))
    return _utils.chain_results(_delete, move(client, source, target))
