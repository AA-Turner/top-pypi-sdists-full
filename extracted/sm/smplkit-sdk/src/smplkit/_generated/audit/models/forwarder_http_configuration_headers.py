from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="ForwarderHttpConfigurationHeaders")


@_attrs_define
class ForwarderHttpConfigurationHeaders:
    """HTTP headers attached to each request, as a name→value object (e.g. `{"Authorization": "Bearer s3cr3t"}`). Override
    an individual header in a specific environment by its name via a `headers.<name>` entry in that environment's
    overrides; header names match case-insensitively.

    """

    additional_properties: dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        forwarder_http_configuration_headers = cls()

        forwarder_http_configuration_headers.additional_properties = d
        return forwarder_http_configuration_headers

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
