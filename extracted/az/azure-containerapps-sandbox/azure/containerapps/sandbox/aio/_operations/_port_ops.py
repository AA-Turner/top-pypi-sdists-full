"""Async port operations for sandbox-scoped client."""
from __future__ import annotations

from typing import Any

from azure.core.tracing.decorator_async import distributed_trace_async

from azure.containerapps.sandbox._helpers import _ERROR_MAP
from azure.containerapps.sandbox._models import (
    AddPortRequest,
    PortIpAccessControl,
    SandboxPort,
)
from azure.containerapps.sandbox._port_helpers import _extract_port_from_response, _prepare_port
from azure.containerapps.sandbox._response_helpers import _normalize_response
from azure.containerapps.sandbox.models import PortAuthConfig, PortAuthEntraId, UpdatePortsContent

class AsyncPortOperationsMixin:
    """Async port operations on a sandbox."""

    @distributed_trace_async
    async def add_port(self, port: int, *,
                       anonymous: bool = False, email: str | None = None,
                       ip_access_control: PortIpAccessControl | None = None,
                       **kwargs: Any) -> SandboxPort:
        """Add a port, defaulting to anonymous access when no email is provided.

        :keyword ip_access_control: Optional inbound source-IP allow/deny policy
            for the port. See :class:`~azure.containerapps.sandbox.PortIpAccessControl`.
        """
        auth = (
            PortAuthConfig(anonymous=True)
            if anonymous or not email
            else PortAuthConfig(entra_id=PortAuthEntraId(enabled=True, emails=[email]))
        )
        body = _prepare_port(AddPortRequest(port=port, auth=auth, ip_access_control=ip_access_control))
        response = await self._generated.sandboxes.add_port(
            self._sandbox_id,
            body,
            **{"error_map": _ERROR_MAP, "cls": _normalize_response, **kwargs},
        )
        return _extract_port_from_response(response, port)

    @distributed_trace_async
    async def remove_port(self, port: int, **kwargs: Any) -> None:
        """Remove a port."""
        await self._generated.sandboxes.remove_port(
            self._sandbox_id, {"port": port}, **{"error_map": _ERROR_MAP, **kwargs},
        )

    @distributed_trace_async
    async def update_ports(self, ports: list[AddPortRequest | int], **kwargs: Any) -> list[SandboxPort]:
        """Replace all port mappings on this sandbox."""
        body = UpdatePortsContent({"ports": [_prepare_port(port) for port in ports]})
        result = await self._generated.sandboxes.set_ports(
            self._sandbox_id,
            body,
            **{"error_map": _ERROR_MAP, "cls": _normalize_response, **kwargs},
        )
        return result.ports if result.ports is not None else []
