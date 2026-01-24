from collections.abc import Callable

from fa_purity import (
    Cmd,
    FrozenDict,
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
from redshift_client.core.id_objs import (
    DbTableId,
    Identifier,
    SchemaId,
    TableId,
)
from redshift_client.sql_client import (
    DbPrimitiveFactory,
    QueryValues,
)

from snowflake_client._core.cursor import (
    SnowflakeCursor,
)
from snowflake_client._core.query import (
    SnowflakeQuery,
)


def _to_raw_schema(schema: SchemaId) -> str:
    return schema.name.to_str().upper()


def all_schemas(cursor: SnowflakeCursor) -> Cmd[ResultE[frozenset[SchemaId]]]:
    statement = "SELECT schema_name FROM information_schema.schemata"
    return _utils.chain_results(
        cursor.execute(SnowflakeQuery.new_query(statement), None),
        cursor.fetch_all.map(
            lambda r: r.map(
                lambda i: PureIterFactory.from_list(i).map(
                    lambda e: _utils.get_index(e.data, 0)
                    .bind(
                        lambda v: v.map(
                            lambda p: JsonPrimitiveUnfolder.to_str(p),
                            lambda _: Result.failure(
                                TypeError("Expected `JsonPrimitive` but got `datetime`"),
                                str,
                            ).alt(cast_exception),
                        ),
                    )
                    .map(lambda s: SchemaId(Identifier.new(s))),
                ),
            ).bind(lambda i: ResultTransform.all_ok(i.to_list()).map(lambda s: frozenset(s))),
        ),
    )


def table_ids(cursor: SnowflakeCursor, schema: SchemaId) -> Cmd[ResultE[frozenset[DbTableId]]]:
    statement = (
        "SELECT table_name FROM information_schema.tables WHERE table_schema = %(schema_name)s"
    )
    args: dict[str, Primitive] = {"schema_name": _to_raw_schema(schema)}
    return _utils.chain_results(
        cursor.execute(
            SnowflakeQuery.new_query(statement),
            QueryValues(DbPrimitiveFactory.from_raw_prim_dict(FrozenDict(args))),
        ),
        cursor.fetch_all.map(
            lambda r: r.map(
                lambda i: PureIterFactory.from_list(i).map(
                    lambda e: _utils.get_index(e.data, 0).bind(
                        lambda v: v.map(
                            lambda p: JsonPrimitiveUnfolder.to_str(p),
                            lambda _: Result.failure(
                                TypeError("Expected `JsonPrimitive` but got `datetime`"),
                                str,
                            ).alt(cast_exception),
                        ).map(lambda s: DbTableId(schema, TableId(Identifier.new(s)))),
                    ),
                ),
            ).bind(lambda i: ResultTransform.all_ok(i.to_list()).map(lambda s: frozenset(s))),
        ),
    )


def exist(cursor: SnowflakeCursor, schema: SchemaId) -> Cmd[ResultE[bool]]:
    statement = """
        SELECT EXISTS (
            SELECT 1 FROM information_schema.schemata
            WHERE schema_name = %(schema_name)s
        );
    """
    args: dict[str, Primitive] = {"schema_name": _to_raw_schema(schema)}
    get_result = cursor.fetch_one.map(
        lambda r: r.bind(
            lambda m: m.to_result()
            .alt(lambda _: cast_exception(TypeError("Expected not Empty")))
            .bind(
                lambda p: _utils.get_index(p.data, 0).bind(
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
    )
    return _utils.chain_results(
        cursor.execute(
            SnowflakeQuery.new_query(statement),
            QueryValues(DbPrimitiveFactory.from_raw_prim_dict(FrozenDict(args))),
        ),
        get_result,
    )


def delete(cursor: SnowflakeCursor, schema: SchemaId, cascade: bool) -> Cmd[ResultE[None]]:
    opt = "CASCADE" if cascade else "RESTRICT"
    stm: str = "DROP SCHEMA {schema_name} " + opt
    return cursor.execute(
        SnowflakeQuery.dynamic_query(stm, FrozenDict({"schema_name": _to_raw_schema(schema)}))
        .alt(Unsafe.raise_exception)
        .to_union(),
        None,
    )


def recreate(
    delete_schema: Callable[[SchemaId], Cmd[ResultE[None]]],
    create_schema: Callable[[SchemaId], Cmd[ResultE[None]]],
    cursor: SnowflakeCursor,
    schema: SchemaId,
) -> Cmd[ResultE[None]]:
    nothing = Cmd.wrap_value(Result.success(None, Exception))
    _exists = _utils.chain(
        exist(cursor, schema),
        lambda b: delete_schema(schema) if b else nothing,
    ).map(lambda r: r.bind(lambda x: x))
    return _utils.chain_results(_exists, create_schema(schema))


def move_tables(
    cursor: SnowflakeCursor,
    source: SchemaId,
    target: SchemaId,
    move_op: Callable[[DbTableId, DbTableId], Cmd[ResultE[None]]],
) -> Cmd[ResultE[None]]:
    _move_tables = _utils.chain(
        table_ids(cursor, source),
        lambda t: PureIterFactory.from_list(tuple(t))
        .map(lambda t: move_op(t, DbTableId(target, t.table)))
        .transform(lambda x: _utils.extract_fail(x)),
    ).map(lambda r: r.bind(lambda x: x))
    return _utils.chain(_move_tables, lambda _: delete(cursor, source, False)).map(
        lambda r: r.bind(lambda x: x),
    )


def rename(cursor: SnowflakeCursor, old: SchemaId, new: SchemaId) -> Cmd[ResultE[None]]:
    stm = "ALTER SCHEMA {from_schema} RENAME TO {to_schema}"
    return cursor.execute(
        SnowflakeQuery.dynamic_query(
            stm,
            FrozenDict(
                {
                    "from_schema": old.name.to_str(),
                    "to_schema": new.name.to_str(),
                },
            ),
        )
        .alt(Unsafe.raise_exception)
        .to_union(),
        None,
    )


def create(client: SnowflakeCursor, schema: SchemaId, if_not_exist: bool) -> Cmd[ResultE[None]]:
    not_exist = " IF NOT EXISTS " if if_not_exist else ""
    stm = f"CREATE SCHEMA {not_exist} {{schema}}"
    return client.execute(
        SnowflakeQuery.dynamic_query(stm, FrozenDict({"schema": schema.name.to_str()}))
        .alt(Unsafe.raise_exception)
        .to_union(),
        None,
    )
