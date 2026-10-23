import httpx2 as httpx
from httpx2 import (
    URL as URL,
    Proxy as Proxy,
    Timeout as Timeout,
    Response as Response,
    BaseTransport as BaseTransport,
    AsyncBaseTransport as AsyncBaseTransport,
)
from httpx2._config import DEFAULT_TIMEOUT_CONFIG  # pyright: ignore[reportPrivateImportUsage]

HTTPX_DEFAULT_TIMEOUT = DEFAULT_TIMEOUT_CONFIG

__all__ = [
    "httpx",
    "HTTPX_DEFAULT_TIMEOUT",
    "URL",
    "Proxy",
    "Timeout",
    "Response",
    "BaseTransport",
    "AsyncBaseTransport",
]
