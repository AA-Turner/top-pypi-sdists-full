from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.flag_environment import FlagEnvironment


T = TypeVar("T", bound="FlagEnvironments")


@_attrs_define
class FlagEnvironments:
    """Per-environment configuration keyed by environment name (`production`, `staging`, etc.). Environments not listed
    fall back to the flag's global `default`.

    """

    additional_properties: dict[str, FlagEnvironment] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.flag_environment import FlagEnvironment

        d = dict(src_dict)
        flag_environments = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = FlagEnvironment.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        flag_environments.additional_properties = additional_properties
        return flag_environments

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> FlagEnvironment:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: FlagEnvironment) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
