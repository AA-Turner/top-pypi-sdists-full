from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="ApiKeyScopes")


@_attrs_define
class ApiKeyScopes:
    """Scope restrictions applied to the key, as a JSON object mapping dimension names to arrays of allowed values. An
    empty object (the default) grants unrestricted access. The `environments` dimension lists the environment keys the
    key may operate in (for example `{"environments": ["production"]}`); a request's environment must be one of them. A
    dimension that is absent or set to an empty array is unrestricted in that dimension.

        Example:
            {'environments': ['production']}

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        api_key_scopes = cls()

        api_key_scopes.additional_properties = d
        return api_key_scopes

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
