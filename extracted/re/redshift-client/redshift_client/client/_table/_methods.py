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
from fa_purity.json import (
    JsonPrimitiveUnfolder,
    Primitive,
)

from redshift_client import (
    _utils,
)
from redshift_client.client._core import (
    AwsRole,
    GroupedRows,
    NanHandler,
    S3Prefix,
    TableRow,
)
from redshift_client.core.column import (
    Column,
    ColumnId,
    ColumnObj,
)
from redshift_client.core.id_objs import (
    DbTableId,
    Identifier,
    TableId,
)
from redshift_client.core.table import (
    ManifestId,
    Table,
)
from redshift_client.sql_client import (
    DbPrimitive,
    DbPrimitiveFactory,
    Limit,
    Query,
    QueryValues,
    RowData,
    SqlCursor,
    Template,
)

from . import (
    _encode,
)
from ._assert import (
    to_column,
)


def _int_to_str(value: int) -> str:
    return str(value)


def unload(
    client: SqlCursor,
    table: DbTableId,
    prefix: S3Prefix,
    role: AwsRole,
) -> Cmd[ResultE[ManifestId]]:
    """
    Unload data from a table to s3.

    prefix: a s3 uri prefix
    role: an aws role id-arn
    """
    stm = """
        UNLOAD ('SELECT * FROM {schema}.{table}')
        TO %(prefix)s iam_role %(role)s MANIFEST ESCAPE
    """
    args: dict[str, Primitive] = {
        "prefix": prefix.prefix,
        "role": role.role,
    }
    return client.execute(
        Query.dynamic_query(
            stm,
            FrozenDict(
                {
                    "schema": table.schema.name.to_str(),
                    "table": table.table.name.to_str(),
                },
            ),
        ),
        QueryValues(DbPrimitiveFactory.from_raw_prim_dict(FrozenDict(args))),
    ).map(lambda r: r.map(lambda _: ManifestId(f"{prefix}manifest")))


def load(
    client: SqlCursor,
    table: DbTableId,
    manifest: ManifestId,
    role: AwsRole,
    nan_handler: NanHandler,
) -> Cmd[ResultE[None]]:
    """
    Load data into a table from a manifest.

    If `nan_handler` is disabled, ensure that the table does not contain NaN values on float columns
    """
    nan_fix = "NULL AS 'nan'" if nan_handler.enabled else ""
    stm = f"""
        COPY {{schema}}.{{table}} FROM %(manifest_file)s
        iam_role %(role)s MANIFEST ESCAPE {nan_fix}
    """
    args: dict[str, Primitive] = {
        "manifest_file": manifest.uri,
        "role": role.role,
    }
    return client.execute(
        Query.dynamic_query(
            stm,
            FrozenDict(
                {
                    "schema": table.schema.name.to_str(),
                    "table": table.table.name.to_str(),
                },
            ),
        ),
        QueryValues(DbPrimitiveFactory.from_raw_prim_dict(FrozenDict(args))),
    )


def get(client: SqlCursor, table: DbTableId) -> Cmd[ResultE[Table]]:
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
        "table_schema": table.schema.name.to_str(),
        "table_name": table.table.name.to_str(),
    }
    exe = client.execute(
        Query.new_query(stm),
        QueryValues(DbPrimitiveFactory.from_raw_prim_dict(FrozenDict(args))),
    )
    results = client.fetch_all

    def _extract(raw: FrozenList[RowData]) -> ResultE[Table]:
        columns_pairs = ResultTransform.all_ok(
            PureIterFactory.from_list(raw).map(lambda c: to_column(c.data)).to_list(),
        )
        columns = columns_pairs.map(lambda i: FrozenDict(dict(i)))
        order = columns_pairs.map(
            lambda i: PureIterFactory.from_list(i).map(lambda c: c[0]),
        )
        return columns.bind(
            lambda c: order.bind(
                lambda o: Table.new(o.to_list(), c, frozenset()),
            ),
        )

    return _utils.chain_results(exe, results).map(lambda r: r.bind(_extract))


def exist(client: SqlCursor, table: DbTableId) -> Cmd[ResultE[bool]]:
    stm = """
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = %(table_schema)s
            AND table_name = %(table_name)s
        );
    """
    args: dict[str, Primitive] = {
        "table_schema": table.schema.name.to_str(),
        "table_name": table.table.name.to_str(),
    }
    return _utils.chain_results(
        client.execute(
            Query.new_query(stm),
            QueryValues(
                DbPrimitiveFactory.from_raw_prim_dict(FrozenDict(args)),
            ),
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
                                TypeError(
                                    "Expected `JsonPrimitive` but got `datetime`",
                                ),
                                bool,
                            ).alt(cast_exception),
                        ),
                    ),
                ),
            ),
        ),
    )


def insert(
    client: SqlCursor,
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
        "schema": table_id.schema.name.to_str(),
        "table": table_id.table.name.to_str(),
    }
    for i, c in enumerate(table.order):
        identifiers[f"field_{i}"] = c.name.to_str()
    return client.values(
        Query.dynamic_query(stm, FrozenDict(identifiers)),
        items,
        limit,
    )


def named_insert(
    client: SqlCursor,
    table_id: DbTableId,
    data: GroupedRows,
) -> Cmd[ResultE[None]]:
    _enumerated = PureIterFactory.from_list(data.table.order).enumerate(1)
    _field_placeholders = _enumerated.map(
        lambda t: "{field_" + _int_to_str(t[0]) + "}",
    )
    _template = _enumerated.map(
        lambda t: "%(field_" + _int_to_str(t[0]) + ")s",
    )
    _field_map = FrozenDict(
        dict(_enumerated.map(lambda t: (t[1], "field_" + _int_to_str(t[0])))),
    )
    _fields = ",".join(_field_placeholders)
    stm = f"INSERT INTO {{schema}}.{{table}} ({_fields}) VALUES %s"  # noqa: S608
    identifiers: dict[str, str] = dict(
        _enumerated.map(
            lambda t: ("field_" + _int_to_str(t[0]), t[1].name.to_str()),
        ),
    ) | {
        "schema": table_id.schema.name.to_str(),
        "table": table_id.table.name.to_str(),
    }

    def _to_fields_map(item: TableRow) -> QueryValues:
        return QueryValues(
            FrozenDict({_field_map[k]: v for k, v in item.row.items()}),
        )

    values = PureIterFactory.from_list(data.rows).map(_to_fields_map)
    return client.named_values(
        Query.dynamic_query(stm, FrozenDict(identifiers)),
        Template(_template.to_list()),
        values.to_list(),
    )


def rename(
    client: SqlCursor,
    table_id: DbTableId,
    new_name: str,
) -> Cmd[ResultE[TableId]]:
    stm = """
        ALTER TABLE {schema}.{table} RENAME TO {new_name}
    """
    identifiers: dict[str, str] = {
        "schema": table_id.schema.name.to_str(),
        "table": table_id.table.name.to_str(),
        "new_name": new_name,
    }
    return client.execute(
        Query.dynamic_query(stm, FrozenDict(identifiers)),
        None,
    ).map(lambda r: r.map(lambda _: TableId(Identifier.new(new_name))))


def delete(
    client: SqlCursor,
    table_id: DbTableId,
    cascade: bool,
) -> Cmd[ResultE[None]]:
    _cascade = "CASCADE" if cascade else ""
    stm = f"""
        DROP TABLE {{schema}}.{{table}} {_cascade}
    """
    identifiers: dict[str, str] = {
        "schema": table_id.schema.name.to_str(),
        "table": table_id.table.name.to_str(),
    }
    return client.execute(
        Query.dynamic_query(stm, FrozenDict(identifiers)),
        None,
    )


def add_column(
    client: SqlCursor,
    table_id: DbTableId,
    column: ColumnObj,
) -> Cmd[ResultE[None]]:
    stm = f"""
        ALTER TABLE {{table_schema}}.{{table_name}}
        ADD COLUMN {{column_name}}
        {_encode.encode_data_type(column.column.data_type)} DEFAULT %(default_val)s
    """
    identifiers: dict[str, str] = {
        "table_schema": table_id.schema.name.to_str(),
        "table_name": table_id.table.name.to_str(),
        "column_name": column.id_obj.name.to_str(),
    }
    args: dict[str, DbPrimitive] = {
        "default_val": column.column.default,
    }
    return client.execute(
        Query.dynamic_query(stm, FrozenDict(identifiers)),
        QueryValues(FrozenDict(args)),
    )


def add_columns(
    client: SqlCursor,
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
    client: SqlCursor,
    blueprint: DbTableId,
    new_table: DbTableId,
) -> Cmd[ResultE[None]]:
    stm = """
        CREATE TABLE {new_schema}.{new_table} (
            LIKE {blueprint_schema}.{blueprint_table}
        )
    """
    identifiers: dict[str, str] = {
        "blueprint_schema": blueprint.schema.name.to_str(),
        "blueprint_table": blueprint.table.name.to_str(),
        "new_schema": new_table.schema.name.to_str(),
        "new_table": new_table.table.name.to_str(),
    }
    return client.execute(
        Query.dynamic_query(stm, FrozenDict(identifiers)),
        None,
    )


def move_data(
    client: SqlCursor,
    source: DbTableId,
    target: DbTableId,
) -> Cmd[ResultE[None]]:
    """
    Move data from source to target.

    - After the operation source will be empty.
    - Both tables must exists.
    """
    stm = """
        ALTER TABLE {target_schema}.{target_table}
        APPEND FROM {source_schema}.{source_table}
    """
    identifiers: dict[str, str] = {
        "source_schema": source.schema.name.to_str(),
        "source_table": source.table.name.to_str(),
        "target_schema": target.schema.name.to_str(),
        "target_table": target.table.name.to_str(),
    }
    return client.execute(
        Query.dynamic_query(stm, FrozenDict(identifiers)),
        None,
    )


def move(
    client: SqlCursor,
    source: DbTableId,
    target: DbTableId,
) -> Cmd[ResultE[None]]:
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


def migrate(
    client: SqlCursor,
    source: DbTableId,
    target: DbTableId,
) -> Cmd[ResultE[None]]:
    """
    Migrate tables.

    - delete target if exist
    - move source into target (see move method)
    """
    nothing: Cmd[ResultE[None]] = Cmd.wrap_value(Result.success(None))
    _delete = _utils.chain(
        exist(client, target),
        lambda b: delete(client, target, True) if b else nothing,
    ).map(lambda r: r.bind(lambda v: v))
    return _utils.chain_results(_delete, move(client, source, target))
