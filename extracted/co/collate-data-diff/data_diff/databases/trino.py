from typing import Any, ClassVar, Type

import attrs
from requests import Session

from data_diff.abcs.database_types import TemporalType, TimestampTZ, ColType_UUID
from data_diff.databases import presto
from data_diff.databases.base import import_helper
from data_diff.databases.base import TIMESTAMP_PRECISION_POS, BaseDialect


@import_helper("trino")
def import_trino():
    import trino

    return trino


class Dialect(presto.Dialect):
    name = "Trino"

    def set_timezone_to_utc(self) -> str:
        # Trino has its own statement form that PrestoDB does not accept.
        return "SET TIME ZONE 'UTC'"

    def type_repr(self, t) -> str:
        # The base dialect emits TIMESTAMP(p) for TimestampTZ, which Trino
        # interprets as TIMESTAMP WITHOUT TIME ZONE. That silently drops the
        # offset on insert, so be explicit and emit TIMESTAMP(p) WITH TIME ZONE.
        if isinstance(t, TimestampTZ):
            return f"TIMESTAMP({t.precision}) WITH TIME ZONE"
        return super().type_repr(t)

    def normalize_timestamp(self, value: str, coltype: TemporalType) -> str:
        # Trino's date_format truncates fractional seconds to millisecond
        # precision and loses any trailing microseconds. Casting the value to
        # TIMESTAMP(p) and then to VARCHAR keeps the full precision. For
        # TIMESTAMP WITH TIME ZONE columns the cast would preserve the source
        # offset instead of using the session timezone, so apply
        # AT TIME ZONE 'UTC' first to normalize.
        inner_prec = coltype.precision if coltype.rounds else 6
        if isinstance(coltype, TimestampTZ):
            value = f"({value}) AT TIME ZONE 'UTC'"
        s = f"CAST(CAST({value} AS TIMESTAMP({inner_prec})) AS VARCHAR)"
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
                kw["auth"] = trino.auth.BasicAuthentication(auth.get("username"), auth.get("password"))
                kw["http_scheme"] = "https"

            elif auth.get("authType") == "jwt":
                kw["auth"] = trino.auth.JWTAuthentication(auth.get("jwt"))
                kw["http_scheme"] = "https"

            elif auth.get("authType") == "oauth2":
                kw["auth"] = trino.auth.OAuth2Authentication()
                kw["http_scheme"] = "https"

        self._conn = trino.dbapi.connect(**kw)
