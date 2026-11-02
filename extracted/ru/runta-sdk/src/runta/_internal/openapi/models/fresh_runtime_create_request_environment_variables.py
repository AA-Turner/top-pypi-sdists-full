from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FreshRuntimeCreateRequestEnvironmentVariables")


@_attrs_define
class FreshRuntimeCreateRequestEnvironmentVariables:
    """Non-secret environment variables the runtime carries. Names must match [A-Za-z_][A-Za-z0-9_]* and be at most 128
    UTF-8 bytes. Names Runta sets itself are reserved: the RUNTA_ prefix, the runtime CA variables, the managed
    repository credentials, and the canonical names of the provider secret presets. Values must be at most 8192 UTF-8
    bytes each and 65536 in total, and must not contain NUL, CR, or LF.

    """

    additional_properties: dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        fresh_runtime_create_request_environment_variables = cls()

        fresh_runtime_create_request_environment_variables.additional_properties = d
        return fresh_runtime_create_request_environment_variables

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
