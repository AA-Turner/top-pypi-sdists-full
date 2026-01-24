from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)

from cryptography.hazmat.backends import (
    default_backend,
)
from cryptography.hazmat.primitives import (
    serialization,
)
from fa_purity import (
    Cmd,
)
from snowflake.connector import (
    connect as snowflake_connect,
)

from snowflake_client._core import (
    SnowflakeConnection,
    SnowflakeCredentials,
    SnowflakeDatabase,
    SnowflakeWarehouse,
)

from .cursor import (
    SnowflakeCursorFactory,
)


@dataclass(frozen=True)
class ConnectionFactory:
    @staticmethod
    def snowflake_connection(
        database: SnowflakeDatabase,
        warehouse: SnowflakeWarehouse,
        creds: SnowflakeCredentials,
    ) -> Cmd[SnowflakeConnection]:
        def _action() -> SnowflakeConnection:
            private_key = serialization.load_pem_private_key(
                creds.private_key.encode("utf-8"),
                password=None,
                backend=default_backend(),  # type: ignore[misc]
            )
            pkb = private_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
            connection = snowflake_connect(
                user=creds.user,
                private_key=pkb,
                account=creds.account,
                database=database.name,
                warehouse=warehouse.name,
            )
            return SnowflakeConnection(
                Cmd.wrap_impure(lambda: connection.close()),
                Cmd.wrap_impure(lambda: connection.commit()),
                lambda log: Cmd.wrap_impure(lambda: connection.cursor()).map(
                    lambda c: SnowflakeCursorFactory.new_cursor(log, c),
                ),
            )

        return Cmd.wrap_impure(_action)
