from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SoftwareModule")


@_attrs_define
class SoftwareModule:
    """
    Attributes:
        module_name (Union[Unset, str]):
        module_version (Union[Unset, str]):
    """

    module_name: Union[Unset, str] = UNSET
    module_version: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        module_name = self.module_name

        module_version = self.module_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if module_name is not UNSET:
            field_dict["module_name"] = module_name
        if module_version is not UNSET:
            field_dict["module_version"] = module_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        module_name = d.pop("module_name", UNSET)

        module_version = d.pop("module_version", UNSET)

        software_module = cls(
            module_name=module_name,
            module_version=module_version,
        )

        software_module.additional_properties = d
        return software_module

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
