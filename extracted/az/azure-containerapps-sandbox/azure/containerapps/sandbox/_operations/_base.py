"""Base protocol for operation mixins."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

from azure.core.rest import HttpRequest, HttpResponse

if TYPE_CHECKING:
    pass


class _GroupClientProtocol(Protocol):
    """Methods that group-level operation mixins rely on.

    :class:`SandboxGroupClient` satisfies this protocol.
    """

    _endpoint: str
    _api_version: str
    _pipeline: Any
    _credential: Any
    _scope: str
    _subscription_id: str
    _resource_group: str
    _sandbox_group: str

    @property
    def _group_path(self) -> str: ...

    def _send_request(self, request: HttpRequest, *, stream: bool = False) -> HttpResponse: ...
    def _dp_get(self, path: str, *, params: dict | None = None) -> dict | list: ...
    def _dp_put(self, path: str, body: dict | bytes | None = None, *, headers: dict | None = None, params: dict | None = None) -> dict: ...
    def _dp_post(self, path: str, body: dict | None = None) -> dict: ...
    def _dp_delete(self, path: str) -> None: ...


class _SandboxClientProtocol(_GroupClientProtocol, Protocol):
    """Methods that sandbox-scoped operation mixins rely on.

    :class:`SandboxClient` satisfies this protocol.
    """

    _sandbox_id: str

    @property
    def _sbx_path(self) -> str: ...
