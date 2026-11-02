from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.vnc_gateway_connection_security_type import (
    VncGatewayConnectionSecurityType,
)
from ..models.vnc_gateway_connection_username import VncGatewayConnectionUsername

T = TypeVar("T", bound="VncGatewayConnection")


@_attrs_define
class VncGatewayConnection:
    """Fixed native VNC gateway connection parameters for runtimes in this zone.

    Attributes:
        hostname (str): Public VNC gateway DNS hostname.
        port (int): Public native VNC TCP port.
        username (VncGatewayConnectionUsername): Username required by the X509Plain handshake.
        security_type (VncGatewayConnectionSecurityType): VeNCrypt authentication subtype required by the gateway.
    """

    hostname: str
    port: int
    username: VncGatewayConnectionUsername
    security_type: VncGatewayConnectionSecurityType

    def to_dict(self) -> dict[str, Any]:
        hostname = self.hostname

        port = self.port

        username = self.username.value

        security_type = self.security_type.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "hostname": hostname,
                "port": port,
                "username": username,
                "security_type": security_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        hostname = d.pop("hostname")

        port = d.pop("port")

        username = VncGatewayConnectionUsername(d.pop("username"))

        security_type = VncGatewayConnectionSecurityType(d.pop("security_type"))

        vnc_gateway_connection = cls(
            hostname=hostname,
            port=port,
            username=username,
            security_type=security_type,
        )

        return vnc_gateway_connection
