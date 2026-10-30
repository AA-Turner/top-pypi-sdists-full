from importlib import import_module
from importlib.metadata import version
from typing import TYPE_CHECKING, Protocol

import httpx


class HttpBackend(Protocol):
    """The httpx-compatible module the installed mistralai client is built on.

    mistralai 2.x uses httpx and 3.x uses httpx2, a fork with the same public API. The httpx
    module satisfies this protocol, so call sites are type-checked against httpx's API whichever
    backend is selected at runtime.
    """

    Client: type[httpx.Client]
    AsyncClient: type[httpx.AsyncClient]
    Headers: type[httpx.Headers]
    Limits: type[httpx.Limits]
    HTTPTransport: type[httpx.HTTPTransport]
    AsyncHTTPTransport: type[httpx.AsyncHTTPTransport]
    MockTransport: type[httpx.MockTransport]
    Request: type[httpx.Request]
    Response: type[httpx.Response]
    HTTPStatusError: type[httpx.HTTPStatusError]
    ConnectError: type[httpx.ConnectError]
    TimeoutException: type[httpx.TimeoutException]
    ConnectTimeout: type[httpx.ConnectTimeout]
    ReadTimeout: type[httpx.ReadTimeout]
    WriteTimeout: type[httpx.WriteTimeout]
    RemoteProtocolError: type[httpx.RemoteProtocolError]


_BACKEND_BY_MISTRALAI_MAJOR = {2: "httpx", 3: "httpx2"}


def _select_backend() -> HttpBackend:
    mistralai_version = version("mistralai")
    module_name = _BACKEND_BY_MISTRALAI_MAJOR.get(int(mistralai_version.split(".")[0]))
    if module_name is None:
        raise ImportError(f"mistralai-workflows does not support mistralai {mistralai_version}")
    backend: HttpBackend = import_module(module_name)
    return backend


MISTRAL_HTTP: HttpBackend = httpx if TYPE_CHECKING else _select_backend()
