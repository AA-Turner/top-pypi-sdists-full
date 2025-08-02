from traceback import format_exc
from typing import TYPE_CHECKING

from ._base import Check, CheckResult

try:
    from redis.asyncio import Redis
    from redis.asyncio.connection import parse_url
except ImportError as exc:
    raise ImportError("Using this module requires the redis library.") from exc

if TYPE_CHECKING:
    from redis.asyncio.connection import ConnectKwargs


class RedisCheck(Check):
    _host: str
    _port: int
    _db: str | int
    _username: str | None
    _password: str | None
    _timeout: float | None
    _name: str

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: str | int = 0,
        username: str | None = None,
        password: str | None = None,
        timeout: float | None = 60.0,
        name: str = "Redis",
    ) -> None:
        self._host = host
        self._port = port
        self._db = db
        self._username = username
        self._password = password
        self._timeout = timeout
        self._name = name

    @classmethod
    def from_url(cls, *, url: str, timeout: float | None = 60.0, name: str = "Redis") -> "RedisCheck":
        kwargs: "ConnectKwargs" = parse_url(url)
        return RedisCheck(
            host=kwargs.get("host", "localhost"),
            port=kwargs.get("port", 6379),
            db=kwargs.get("db", 0),
            username=kwargs.get("username"),
            password=kwargs.get("password"),
            timeout=timeout,
            name=name,
        )

    async def __call__(self) -> CheckResult:
        try:
            async with Redis(
                host=self._host,
                port=self._port,
                db=self._db,
                username=self._username,
                password=self._password,
                socket_timeout=self._timeout,
                single_connection_client=True,
            ) as redis:  # type: Redis
                passed: bool = await redis.ping()
                return CheckResult(name=self._name, passed=passed)
        except Exception:
            details: str = format_exc()
            return CheckResult(name=self._name, passed=False, details=details)
