from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ducklake_settings_ducklakes_additional_property_catalog_resource_type import (
    DucklakeSettingsDucklakesAdditionalPropertyCatalogResourceType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="DucklakeSettingsDucklakesAdditionalPropertyCatalog")


@_attrs_define
class DucklakeSettingsDucklakesAdditionalPropertyCatalog:
    """
    Attributes:
        resource_type (DucklakeSettingsDucklakesAdditionalPropertyCatalogResourceType):
        resource_path (Union[Unset, str]):
    """

    resource_type: DucklakeSettingsDucklakesAdditionalPropertyCatalogResourceType
    resource_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        resource_type = self.resource_type.value

        resource_path = self.resource_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_type": resource_type,
            }
        )
        if resource_path is not UNSET:
            field_dict["resource_path"] = resource_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        resource_type = DucklakeSettingsDucklakesAdditionalPropertyCatalogResourceType(d.pop("resource_type"))

        resource_path = d.pop("resource_path", UNSET)

        ducklake_settings_ducklakes_additional_property_catalog = cls(
            resource_type=resource_type,
            resource_path=resource_path,
        )

        ducklake_settings_ducklakes_additional_property_catalog.additional_properties = d
        return ducklake_settings_ducklakes_additional_property_catalog

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
