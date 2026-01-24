from logging import (
    Logger,
)

from fa_purity import (
    Cmd,
    FrozenDict,
    Result,
    ResultE,
    Unsafe,
)
from snowflake_client import (
    SnowflakeConnection,
    SnowflakeCursor,
    SnowflakeQuery,
)

from fluidattacks_connection_manager import (
    _utils,
)

from ._core import ConnectionConf, SetupException


def _setup_db(
    cursor: SnowflakeCursor,
    conf: ConnectionConf,
) -> Cmd[ResultE[None]]:
    return cursor.execute(
        SnowflakeQuery.dynamic_query(
            "USE DATABASE {database}",
            FrozenDict({"database": conf.database.value}),
        )
        .alt(Unsafe.raise_exception)
        .to_union(),
        None,
    )


def _setup_warehouse(
    cursor: SnowflakeCursor,
    conf: ConnectionConf,
) -> Cmd[ResultE[None]]:
    return cursor.execute(
        SnowflakeQuery.dynamic_query(
            "USE WAREHOUSE {warehouse}",
            FrozenDict({"warehouse": conf.warehouse.value}),
        )
        .alt(Unsafe.raise_exception)
        .to_union(),
        None,
    )


def _setup_role(
    cursor: SnowflakeCursor,
    conf: ConnectionConf,
) -> Cmd[ResultE[None]]:
    return cursor.execute(
        SnowflakeQuery.dynamic_query(
            "USE ROLE {role}",
            FrozenDict({"role": conf.role.value}),
        )
        .alt(Unsafe.raise_exception)
        .to_union(),
        None,
    )


def setup_connection(
    connection: SnowflakeConnection,
    conf: ConnectionConf,
    log: Logger,
) -> Cmd[Result[SnowflakeCursor, SetupException]]:
    return connection.cursor(log).bind(
        lambda c: _utils.chain_cmd_result(
            _setup_role(c, conf),
            lambda _: _utils.chain_cmd_result(
                _setup_db(c, conf),
                lambda _: _setup_warehouse(c, conf),
            ),
        ).map(
            lambda r: r.map(lambda _: c).alt(lambda e: SetupException(e)),
        ),
    )
