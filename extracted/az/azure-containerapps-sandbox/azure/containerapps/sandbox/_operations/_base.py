"""Base protocol for operation mixins."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

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
    _generated: Any

    @property
    def _group_path(self) -> str: ...


class _SandboxClientProtocol(_GroupClientProtocol, Protocol):
    """Methods that sandbox-scoped operation mixins rely on.

    :class:`SandboxClient` satisfies this protocol.
    """

    _sandbox_id: str

    @property
    def _sbx_path(self) -> str: ...
