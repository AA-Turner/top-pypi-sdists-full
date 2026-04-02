from pydantic import AmqpDsn, TypeAdapter

from ._base import Check, CheckResult

try:
    import aio_pika
except ImportError as exc:
    raise ImportError("Using this module requires aio_pika library.") from exc


class RabbitMqCheck(Check):
    _host: str
    _port: int
    _secure: bool
    _user: str
    _password: str
    _timeout: float
    _name: str

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        port: int = 5672,
        secure: bool = True,
        timeout: float = 60.0,
        name: str = "RabbitMQ",
    ):
        self._host = host
        self._port = port
        self._secure = secure
        self._user = user
        self._password = password
        self._timeout = timeout
        self._name = name

    @classmethod
    def from_url(cls, url: str, timeout: float = 60.0, name: str = "RabbitMQ") -> "RabbitMqCheck":
        ampq_url = TypeAdapter(AmqpDsn).validate_python(url)
        return cls(
            host=ampq_url.host,  # type: ignore[arg-type]
            user=ampq_url.username,  # type: ignore[arg-type]
            password=ampq_url.password,  # type: ignore[arg-type]
            port=ampq_url.port if ampq_url.port else 5672,
            secure=ampq_url.scheme == "amqps",
            timeout=timeout,
            name=name,
        )

    async def __call__(self) -> CheckResult:
        try:
            async with await aio_pika.connect_robust(
                host=self._host,
                port=self._port,
                login=self._user,
                password=self._password,
                ssl=self._secure,
            ):
                return CheckResult(name=self._name, passed=True)
        except Exception as exception:
            return CheckResult(name=self._name, passed=False, details=str(exception))
