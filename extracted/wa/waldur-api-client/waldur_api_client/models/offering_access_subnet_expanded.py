from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingAccessSubnetExpanded")


@_attrs_define
class OfferingAccessSubnetExpanded:
    """
    Attributes:
        inet (str):
        description (str):
        is_staff_managed (bool):
        customer_uuid (str):
        customer_name (str):
        offering_uuid (str):
        offering_name (str):
    """

    inet: str
    description: str
    is_staff_managed: bool
    customer_uuid: str
    customer_name: str
    offering_uuid: str
    offering_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        inet = self.inet

        description = self.description

        is_staff_managed = self.is_staff_managed

        customer_uuid = self.customer_uuid

        customer_name = self.customer_name

        offering_uuid = self.offering_uuid

        offering_name = self.offering_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inet": inet,
                "description": description,
                "is_staff_managed": is_staff_managed,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        inet = d.pop("inet")

        description = d.pop("description")

        is_staff_managed = d.pop("is_staff_managed")

        customer_uuid = d.pop("customer_uuid")

        customer_name = d.pop("customer_name")

        offering_uuid = d.pop("offering_uuid")

        offering_name = d.pop("offering_name")

        offering_access_subnet_expanded = cls(
            inet=inet,
            description=description,
            is_staff_managed=is_staff_managed,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
        )

        offering_access_subnet_expanded.additional_properties = d
        return offering_access_subnet_expanded

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
