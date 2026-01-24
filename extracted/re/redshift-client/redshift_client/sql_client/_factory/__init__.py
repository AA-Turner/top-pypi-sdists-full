from dataclasses import (
    dataclass,
)

from fa_purity import (
    Cmd,
    ResultE,
)

from redshift_client.sql_client._core.connection import (
    Credentials,
    DatabaseId,
    DbConnection,
    IsolationLvl,
)

from . import (
    _temp_creds,
)
from ._connection import (
    RedshiftConnection,
)
from ._primitive import (
    DbPrimitiveFactory,
)
from ._temp_creds import (
    TempCredsUser,
)


@dataclass(frozen=True)
class ConnectionFactory:
    @staticmethod
    def redshift_connection(
        db_id: DatabaseId,
        creds: Credentials,
        readonly: bool,
        isolation: IsolationLvl,
        autocommit: bool,
    ) -> Cmd[DbConnection]:
        return RedshiftConnection.connect(
            db_id,
            creds,
            readonly,
            isolation,
            autocommit,
        )


@dataclass(frozen=True)
class LoginUtils:
    @staticmethod
    def get_temp_creds(user: TempCredsUser) -> Cmd[ResultE[Credentials]]:
        return _temp_creds.get_temp_creds(user)


__all__ = [
    "DbPrimitiveFactory",
    "TempCredsUser",
]
