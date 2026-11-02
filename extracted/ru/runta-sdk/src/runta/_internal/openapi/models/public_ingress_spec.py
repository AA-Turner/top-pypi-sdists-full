from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.public_ingress_protocol import PublicIngressProtocol

T = TypeVar("T", bound="PublicIngressSpec")


@_attrs_define
class PublicIngressSpec:
    """Public ingress forwarding rule. Application URLs use the gateway lifecycle
    response contract described in the RuntimeIngress tag, including the
    `x-runta-runtime-state` header on gateway-generated HTTP 503/410 responses.

        Attributes:
            protocol (PublicIngressProtocol): HTTP/HTTPS application-layer ingress protocol.
            runtime_port (int): Port inside the runtime VM.
    """

    protocol: PublicIngressProtocol
    runtime_port: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        protocol = self.protocol.value

        runtime_port = self.runtime_port

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "protocol": protocol,
                "runtime_port": runtime_port,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        protocol = PublicIngressProtocol(d.pop("protocol"))

        runtime_port = d.pop("runtime_port")

        public_ingress_spec = cls(
            protocol=protocol,
            runtime_port=runtime_port,
        )

        public_ingress_spec.additional_properties = d
        return public_ingress_spec

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
