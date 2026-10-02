from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.access_subnet_impact_address_source_enum import AccessSubnetImpactAddressSourceEnum

T = TypeVar("T", bound="AccessSubnetImpactAddress")


@_attrs_define
class AccessSubnetImpactAddress:
    """
    Attributes:
        inet (str):
        description (str):
        source (AccessSubnetImpactAddressSourceEnum):
        is_staff_managed (bool):
    """

    inet: str
    description: str
    source: AccessSubnetImpactAddressSourceEnum
    is_staff_managed: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        inet = self.inet

        description = self.description

        source = self.source.value

        is_staff_managed = self.is_staff_managed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inet": inet,
                "description": description,
                "source": source,
                "is_staff_managed": is_staff_managed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        inet = d.pop("inet")

        description = d.pop("description")

        source = AccessSubnetImpactAddressSourceEnum(d.pop("source"))

        is_staff_managed = d.pop("is_staff_managed")

        access_subnet_impact_address = cls(
            inet=inet,
            description=description,
            source=source,
            is_staff_managed=is_staff_managed,
        )

        access_subnet_impact_address.additional_properties = d
        return access_subnet_impact_address

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
