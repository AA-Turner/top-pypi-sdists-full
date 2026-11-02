from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.vnc_credential_connection_security_type import (
    VncCredentialConnectionSecurityType,
)

if TYPE_CHECKING:
    from ..models.vnc_credential import VncCredential


T = TypeVar("T", bound="VncCredentialConnection")


@_attrs_define
class VncCredentialConnection:
    """
    Attributes:
        credential (VncCredential):
        username (str):
        password (str):
        hostname (str):
        port (int):
        security_type (VncCredentialConnectionSecurityType):
    """

    credential: VncCredential
    username: str
    password: str
    hostname: str
    port: int
    security_type: VncCredentialConnectionSecurityType

    def to_dict(self) -> dict[str, Any]:
        credential = self.credential.to_dict()

        username = self.username

        password = self.password

        hostname = self.hostname

        port = self.port

        security_type = self.security_type.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "credential": credential,
                "username": username,
                "password": password,
                "hostname": hostname,
                "port": port,
                "security_type": security_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vnc_credential import VncCredential

        d = dict(src_dict)
        credential = VncCredential.from_dict(d.pop("credential"))

        username = d.pop("username")

        password = d.pop("password")

        hostname = d.pop("hostname")

        port = d.pop("port")

        security_type = VncCredentialConnectionSecurityType(d.pop("security_type"))

        vnc_credential_connection = cls(
            credential=credential,
            username=username,
            password=password,
            hostname=hostname,
            port=port,
            security_type=security_type,
        )

        return vnc_credential_connection
