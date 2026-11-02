from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="RuntimeImageProtocolBinding")


@_attrs_define
class RuntimeImageProtocolBinding:
    """
    Attributes:
        protocol (str):
        environment_variable (str): Guest variable this image's onboarding writes the credential to.
        base_url (str): Endpoint the onboarding configures when the caller names none.
    """

    protocol: str
    environment_variable: str
    base_url: str

    def to_dict(self) -> dict[str, Any]:
        protocol = self.protocol

        environment_variable = self.environment_variable

        base_url = self.base_url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "protocol": protocol,
                "environment_variable": environment_variable,
                "base_url": base_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        protocol = d.pop("protocol")

        environment_variable = d.pop("environment_variable")

        base_url = d.pop("base_url")

        runtime_image_protocol_binding = cls(
            protocol=protocol,
            environment_variable=environment_variable,
            base_url=base_url,
        )

        return runtime_image_protocol_binding
