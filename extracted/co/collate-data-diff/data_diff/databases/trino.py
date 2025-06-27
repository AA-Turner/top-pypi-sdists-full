from typing import Any, ClassVar, Type

import attrs
from requests import Session

from data_diff.abcs.database_types import TemporalType, ColType_UUID
from data_diff.databases import presto
from data_diff.databases.base import import_helper
from data_diff.databases.base import TIMESTAMP_PRECISION_POS, BaseDialect


@import_helper("trino")
def import_trino():
    import trino

    return trino


class Dialect(presto.Dialect):
    name = "Trino"

    def normalize_timestamp(self, value: str, coltype: TemporalType) -> str:
        if coltype.rounds:
            s = f"date_format(cast({value} as timestamp({coltype.precision})), '%Y-%m-%d %H:%i:%S.%f')"
        else:
            s = f"date_format(cast({value} as timestamp(6)), '%Y-%m-%d %H:%i:%S.%f')"

        return (
            f"RPAD(RPAD({s}, {TIMESTAMP_PRECISION_POS + coltype.precision}, '.'), {TIMESTAMP_PRECISION_POS + 6}, '0')"
        )

    def normalize_uuid(self, value: str, coltype: ColType_UUID) -> str:
        return f"TRIM({value})"


@attrs.define(frozen=False, init=False, kw_only=True)
class Trino(presto.Presto):
    DIALECT_CLASS: ClassVar[Type[BaseDialect]] = Dialect
    CONNECT_URI_HELP = "trino://<user>@<host>/<catalog>/<schema>"
    CONNECT_URI_PARAMS = ["catalog", "schema"]

    _conn: Any

    def __init__(self, **kw) -> None:
        super().__init__()
        trino = import_trino()

        if kw.get("schema"):
            self.default_schema = kw.get("schema")

        if kw.get("http_session"):
            session = Session()
            session.proxies = kw.get("http_session", {}).get("proxies")

            kw["http_session"] = session

        auth = kw.get("auth")

        if auth:
            if auth.get("authType") == "basic":
                kw["auth"] = trino.auth.BasicAuthentication(
                    auth.get("username"),
                    auth.get("password")
                )
                kw["http_scheme"] = "https"

            elif auth.get("authType") == "jwt":
                kw["auth"] = trino.auth.JWTAuthentication(
                    auth.get("jwt")
                )
                kw["http_scheme"] = "https"

            elif auth.get("authType") == "oauth2":
                kw["auth"] = trino.auth.OAuth2Authentication()
                kw["http_scheme"] = "https"
                
        self._conn = trino.dbapi.connect(**kw)
