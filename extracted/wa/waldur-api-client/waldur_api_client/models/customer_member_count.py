from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CustomerMemberCount")


@_attrs_define
class CustomerMemberCount:
    """
    Attributes:
        uuid (UUID): UUID of the customer
        name (str): Name of the customer
        abbreviation (str): Abbreviation of the customer
        count (int): Number of members
        has_resources (bool): Whether the customer has resources
    """

    uuid: UUID
    name: str
    abbreviation: str
    count: int
    has_resources: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        abbreviation = self.abbreviation

        count = self.count

        has_resources = self.has_resources

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "abbreviation": abbreviation,
                "count": count,
                "has_resources": has_resources,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        abbreviation = d.pop("abbreviation")

        count = d.pop("count")

        has_resources = d.pop("has_resources")

        customer_member_count = cls(
            uuid=uuid,
            name=name,
            abbreviation=abbreviation,
            count=count,
            has_resources=has_resources,
        )

        customer_member_count.additional_properties = d
        return customer_member_count

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
