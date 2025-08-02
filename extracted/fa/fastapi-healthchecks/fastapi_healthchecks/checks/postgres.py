from traceback import format_exc
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from ._base import Check, CheckResult

try:
    import asyncpg
except ImportError as exc:
    raise ImportError("Using this module requires the asyncpg library.") from exc

if TYPE_CHECKING:
    from urllib.parse import ParseResult

    from asyncpg.connection import Connection


class PostgreSqlCheck(Check):
    _host: str
    _port: int
    _username: str | None
    _password: str | None
    _database: str | None
    _timeout: float | None
    _name: str

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        username: str | None = None,
        password: str | None = None,
        database: str | None = None,
        timeout: float | None = 60.0,
        name: str = "PostgreSQL",
    ) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._database = database
        self._timeout = timeout
        self._name = name

    @classmethod
    def from_url(cls, url: str, timeout: float | None = 60.0, name: str = "PostgreSQL") -> "PostgreSqlCheck":
        parse_result: "ParseResult" = urlparse(url)
        return PostgreSqlCheck(
            host=parse_result.hostname or "localhost",
            port=parse_result.port or 5432,
            username=parse_result.username,
            password=parse_result.password,
            database=parse_result.path.lstrip("/"),
            timeout=timeout,
            name=name,
        )

    async def __call__(self) -> CheckResult:
        connection: "Connection | None" = None
        try:
            connection = await asyncpg.connect(
                host=self._host,
                port=self._port,
                user=self._username,
                password=self._password,
                database=self._database,
                timeout=self._timeout,
            )
            async with connection.transaction(readonly=True):
                passed: bool = bool(await connection.fetchval("SELECT 1"))
                return CheckResult(name=self._name, passed=passed)
        except Exception:
            details: str = format_exc()
            return CheckResult(name=self._name, passed=False, details=details)
        finally:
            if connection is not None and not connection.is_closed():
                await connection.close(timeout=self._timeout)
