"""Port operations for sandbox-scoped client."""
from __future__ import annotations

import logging
from typing import Any

from azure.core.tracing.decorator import distributed_trace

from azure.containerapps.sandbox._models import (
    AddPortRequest,
    PortIpAccessControl,
    SandboxPort,
)

logger = logging.getLogger("azure.containerapps.sandbox")


def _extract_port_from_response(response, requested_port: int) -> SandboxPort:
    """Extract the entry for ``requested_port`` from an add_port response."""
    if isinstance(response, dict) and isinstance(response.get("ports"), list):
        ports = response["ports"]
    elif isinstance(response, list):
        ports = response
    else:
        return SandboxPort._from_dict(response if isinstance(response, dict) else {})
    if not ports:
        return SandboxPort(port=requested_port)
    matches = [p for p in ports if isinstance(p, dict) and p.get("port") == requested_port]
    chosen = matches[-1] if matches else ports[-1]
    return SandboxPort._from_dict(chosen)


class PortOperationsMixin:
    """Port operations on a sandbox."""

    @distributed_trace
    def add_port(self, port: int, *,
                 anonymous: bool = False, email: str | None = None,
                 ip_access_control: PortIpAccessControl | None = None,
                 **kwargs: Any) -> SandboxPort:
        """Add a port to this sandbox.

        :keyword ip_access_control: Optional inbound source-IP allow/deny policy
            for the port. See :class:`~azure.containerapps.sandbox.PortIpAccessControl`.
        """
        body: dict = {"port": port}
        if anonymous:
            logger.warning("Port %d exposed with anonymous access — accessible without authentication.", port)
            body["auth"] = {"anonymous": True}
        elif email:
            body["auth"] = {"entraId": {"enabled": True, "emails": [email]}}
        if ip_access_control is not None:
            ip_access_control.validate()
            body["ipAccessControl"] = ip_access_control._to_dict()
        response = self._dp_post(f"{self._sbx_path}/ports/add", body)
        return _extract_port_from_response(response, port)

    @distributed_trace
    def remove_port(self, port: int, **kwargs: Any) -> None:
        """Remove a port."""
        self._dp_post(f"{self._sbx_path}/ports/remove", {"port": port})

    @distributed_trace
    def update_ports(self, ports: list[AddPortRequest | int], **kwargs: Any) -> list[SandboxPort]:
        """Replace all port mappings on this sandbox."""
        result = self._dp_put(f"{self._sbx_path}/ports", {"ports": [{"port": p} if isinstance(p, int) else p._to_dict() for p in ports]})
        if isinstance(result, list):
            raw_ports = result
        elif isinstance(result, dict):
            raw_ports = result.get("ports", [])
        else:
            raw_ports = []
        return [SandboxPort._from_dict(p) for p in raw_ports]
