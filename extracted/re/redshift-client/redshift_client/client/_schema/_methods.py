from collections.abc import Callable

from fa_purity import (
    Cmd,
    FrozenDict,
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
from redshift_client.client._table import (
    new_table_client,
)
from redshift_client.core.id_objs import (
    DbTableId,
    Identifier,
    SchemaId,
    TableId,
)
from redshift_client.core.schema import (
    Quota,
    SchemaPolicy,
)
from redshift_client.sql_client import (
    DbPrimitiveFactory,
    Query,
    QueryValues,
    SqlCursor,
)


def all_schemas(client: SqlCursor) -> Cmd[ResultE[frozenset[SchemaId]]]:
    statement = """
        SELECT s.nspname AS table_schema
        FROM pg_catalog.pg_namespace s
        JOIN pg_catalog.pg_user u ON u.usesysid = s.nspowner
        ORDER BY table_schema
    """
    return _utils.chain_results(
        client.execute(Query.new_query(statement), None),
        client.fetch_all.map(
            lambda r: r.map(
                lambda i: PureIterFactory.from_list(i).map(
                    lambda e: _utils.get_index(e.data, 0)
                    .bind(
                        lambda v: v.map(
                            lambda p: JsonPrimitiveUnfolder.to_str(p),
                            lambda _: Result.failure(
                                TypeError(
                                    "Expected `JsonPrimitive` but got `datetime`",
                                ),
                                str,
                            ).alt(cast_exception),
                        ),
                    )
                    .map(lambda s: SchemaId(Identifier.new(s))),
                ),
            ).bind(
                lambda i: ResultTransform.all_ok(i.to_list()).map(
                    lambda s: frozenset(s),
                ),
            ),
        ),
    )


def table_ids(
    client: SqlCursor,
    schema: SchemaId,
) -> Cmd[ResultE[frozenset[DbTableId]]]:
    _stm = (
        "SELECT tables.table_name FROM information_schema.tables",
        "WHERE table_schema = %(schema_name)s",
    )
    stm = " ".join(_stm)
    args: dict[str, Primitive] = {"schema_name": schema.name.to_str()}
    return _utils.chain_results(
        client.execute(
            Query.new_query(stm),
            QueryValues(
                DbPrimitiveFactory.from_raw_prim_dict(FrozenDict(args)),
            ),
        ),
        client.fetch_all.map(
            lambda r: r.map(
                lambda i: PureIterFactory.from_list(i).map(
                    lambda e: _utils.get_index(e.data, 0).bind(
                        lambda v: v.map(
                            lambda p: JsonPrimitiveUnfolder.to_str(p),
                            lambda _: Result.failure(
                                TypeError(
                                    "Expected `JsonPrimitive` but got `datetime`",
                                ),
                                str,
                            ).alt(cast_exception),
                        ).map(
                            lambda s: DbTableId(
                                schema,
                                TableId(Identifier.new(s)),
                            ),
                        ),
                    ),
                ),
            ).bind(
                lambda i: ResultTransform.all_ok(i.to_list()).map(
                    lambda s: frozenset(s),
                ),
            ),
        ),
    )


def exist(client: SqlCursor, schema: SchemaId) -> Cmd[ResultE[bool]]:
    statement = """
        SELECT EXISTS (
            SELECT 1 FROM pg_namespace
            WHERE nspname = %(schema_name)s
        );
    """
    args: dict[str, Primitive] = {"schema_name": schema.name.to_str()}
    get_result = client.fetch_one.map(
        lambda r: r.bind(
            lambda m: m.to_result()
            .alt(lambda _: cast_exception(TypeError("Expected not Empty")))
            .bind(
                lambda p: _utils.get_index(p.data, 0).bind(
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
    )
    return _utils.chain_results(
        client.execute(
            Query.new_query(statement),
            QueryValues(
                DbPrimitiveFactory.from_raw_prim_dict(FrozenDict(args)),
            ),
        ),
        get_result,
    )


def delete(
    client: SqlCursor,
    schema: SchemaId,
    cascade: bool,
) -> Cmd[ResultE[None]]:
    opt = " CASCADE" if cascade else ""
    stm: str = "DROP SCHEMA {schema_name}" + opt
    return client.execute(
        Query.dynamic_query(
            stm,
            FrozenDict({"schema_name": schema.name.to_str()}),
        ),
        None,
    )


def rename(
    client: SqlCursor,
    old: SchemaId,
    new: SchemaId,
) -> Cmd[ResultE[None]]:
    stm = "ALTER SCHEMA {from_schema} RENAME TO {to_schema}"
    return client.execute(
        Query.dynamic_query(
            stm,
            FrozenDict(
                {
                    "from_schema": old.name.to_str(),
                    "to_schema": new.name.to_str(),
                },
            ),
        ),
        None,
    )


def create(
    client: SqlCursor,
    schema: SchemaId,
    if_not_exist: bool = False,
) -> Cmd[ResultE[None]]:
    not_exist = " IF NOT EXISTS " if if_not_exist else ""
    stm = f"CREATE SCHEMA {not_exist} {{schema}}"
    return client.execute(
        Query.dynamic_query(stm, FrozenDict({"schema": schema.name.to_str()})),
        None,
    )


def recreate(
    client: SqlCursor,
    schema: SchemaId,
    cascade: bool,
) -> Cmd[ResultE[None]]:
    nothing = Cmd.wrap_value(Result.success(None, Exception))
    _exists = _utils.chain(
        exist(client, schema),
        lambda b: delete(client, schema, cascade) if b else nothing,
    ).map(lambda r: r.bind(lambda x: x))
    return _utils.chain_results(_exists, create(client, schema))


def _move(
    client: SqlCursor,
    source: SchemaId,
    target: SchemaId,
    move_op: Callable[[DbTableId, DbTableId], Cmd[ResultE[None]]],
) -> Cmd[ResultE[None]]:
    move_tables = _utils.chain(
        table_ids(client, source),
        lambda t: PureIterFactory.from_list(tuple(t))
        .map(lambda t: move_op(t, DbTableId(target, t.table)))
        .transform(lambda x: _utils.extract_fail(x)),
    ).map(lambda r: r.bind(lambda x: x))
    return _utils.chain(
        move_tables,
        lambda _: delete(client, source, False),
    ).map(lambda r: r.bind(lambda x: x))


def migrate(
    client: SqlCursor,
    source: SchemaId,
    target: SchemaId,
) -> Cmd[ResultE[None]]:
    tb = new_table_client(client)
    return _move(client, source, target, tb.migrate)


def move(
    client: SqlCursor,
    source: SchemaId,
    target: SchemaId,
) -> Cmd[ResultE[None]]:
    tb = new_table_client(client)
    return _move(client, source, target, tb.move)


def set_policy(
    client: SqlCursor,
    schema: SchemaId,
    policy: SchemaPolicy,
) -> Cmd[ResultE[None]]:
    stm = "ALTER SCHEMA {schema} OWNER TO {owner}"
    stm2 = (
        f"ALTER SCHEMA {{schema}} QUOTA %(quota)s {policy.quota.unit.value}"
        if isinstance(policy.quota, Quota)
        else "ALTER SCHEMA {schema} QUOTA UNLIMITED"
    )
    set_owner = client.execute(
        Query.dynamic_query(
            stm,
            FrozenDict(
                {"schema": schema.name.to_str(), "owner": policy.owner},
            ),
        ),
        None,
    )
    id_args: dict[str, str] = {"schema": schema.name.to_str()}
    args: dict[str, Primitive] = (
        {"quota": policy.quota.value} if isinstance(policy.quota, Quota) else {}
    )
    set_quota = client.execute(
        Query.dynamic_query(stm2, FrozenDict(id_args)),
        QueryValues(DbPrimitiveFactory.from_raw_prim_dict(FrozenDict(args))),
    )
    return _utils.chain_results(set_owner, set_quota)
