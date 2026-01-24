from __future__ import (
    annotations,
)

import logging
from dataclasses import (
    dataclass,
)

from fa_purity import (
    Cmd,
    Coproduct,
    Result,
    ResultE,
)
from fluidattacks_etl_utils.secrets import (
    ObservesSecrets,
    ObservesSecretsFactory,
)
from fluidattacks_etl_utils.secrets import SnowflakeCredentials as SecretsSnowflakeCredentials
from fluidattacks_etl_utils.typing import (
    Callable,
    TypeVar,
)
from snowflake_client import (
    ClientFactory,
    ConnectionFactory,
    SchemaClient,
    SnowflakeConnection,
    SnowflakeCredentials,
    SnowflakeCursor,
    SnowflakeDatabase,
    SnowflakeWarehouse,
    TableClient,
)

from fluidattacks_connection_manager import (
    _utils,
)

from . import _setup
from ._core import (
    ConnectionConf,
    Databases,
    Roles,
    SetupException,
    Warehouses,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")
_F = TypeVar("_F")


@dataclass(frozen=True)
class DbClients:
    connection: SnowflakeConnection
    new_table_client: Callable[[SnowflakeCursor], TableClient]
    new_schema_client: Callable[[SnowflakeCursor], SchemaClient]


@dataclass(frozen=True)
class ConnectionManager:
    snowflake_connection: Callable[[ConnectionConf], Cmd[Result[SnowflakeConnection, _F]]]
    execute_with_snowflake: Callable[
        [Callable[[DbClients], Cmd[Result[_T, _F]]], ConnectionConf],
        Cmd[Result[_T, Coproduct[_F, SetupException]]],
    ]


def _snowflake_connection(
    creds: SnowflakeCredentials,
    conf: ConnectionConf,
) -> Cmd[Result[SnowflakeConnection, _F]]:
    return ConnectionFactory.snowflake_connection(
        SnowflakeDatabase(conf.database.value),
        SnowflakeWarehouse(conf.warehouse.value),
        SnowflakeCredentials(
            user=creds.user,
            private_key=creds.private_key,
            account=creds.account,
        ),
    ).map(lambda c: Result.success(c))


def _execute_with_snowflake(
    new_connection: Callable[[ConnectionConf], Cmd[Result[SnowflakeConnection, _F]]],
    action: Callable[[DbClients], Cmd[Result[_T, _F]]],
    conf: ConnectionConf,
) -> Cmd[Result[_T, Coproduct[_F, SetupException]]]:
    return _utils.chain_cmd_result(
        new_connection(conf).map(lambda r: r.alt(Coproduct.inl)),
        lambda db: SnowflakeConnection.connect_and_execute(
            Cmd.wrap_value(db),
            lambda c: _utils.chain_cmd_result(
                _setup.setup_connection(c, conf, LOG).map(lambda r: r.alt(Coproduct.inr)),
                lambda _: action(
                    DbClients(
                        c,
                        ClientFactory.new_table_client,
                        ClientFactory.new_schema_client,
                    ),
                ).map(lambda r: r.alt(Coproduct.inl)),
            ),
        ),
    )


def _creds_adapter(creds: SecretsSnowflakeCredentials) -> SnowflakeCredentials:
    return SnowflakeCredentials(
        creds.user,
        creds.private_key,
        creds.account,
    )


def _manager_from_creds(creds: SnowflakeCredentials) -> ConnectionManager:
    return ConnectionManager(
        lambda conf: _snowflake_connection(creds, conf),
        lambda action, conf: _execute_with_snowflake(
            lambda conf: _snowflake_connection(creds, conf),
            action,
            conf,
        ),
    )


def _observes_manager(secrets: ObservesSecrets) -> ConnectionManager:
    return ConnectionManager(
        lambda conf: secrets.snowflake_etl_access.map(_creds_adapter).bind(
            lambda c: _snowflake_connection(c, conf),
        ),
        lambda action, conf: _execute_with_snowflake(
            lambda conf: secrets.snowflake_etl_access.map(_creds_adapter).bind(
                lambda c: _snowflake_connection(c, conf),
            ),
            action,
            conf,
        ),
    )


@dataclass(frozen=True)
class ConnectionManagerFactory:
    @staticmethod
    def custom_manager(creds: SnowflakeCredentials) -> ConnectionManager:
        return _manager_from_creds(creds)

    @staticmethod
    def observes_manager() -> Cmd[ResultE[ConnectionManager]]:
        return ObservesSecretsFactory.new().map(lambda r: r.map(_observes_manager))


__all__ = [
    "ConnectionConf",
    "Databases",
    "Roles",
    "SetupException",
    "Warehouses",
]
