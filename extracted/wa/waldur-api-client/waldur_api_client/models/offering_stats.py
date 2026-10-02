from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingStats")


@_attrs_define
class OfferingStats:
    """
    Attributes:
        count (int): Number of resources for the offering
        name (str): Name of the offering
        uuid (str): UUID of the offering
        country (str): Country of the offering
    """

    count: int
    name: str
    uuid: str
    country: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        name = self.name

        uuid = self.uuid

        country = self.country

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "name": name,
                "uuid": uuid,
                "country": country,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        name = d.pop("name")

        uuid = d.pop("uuid")

        country = d.pop("country")

        offering_stats = cls(
            count=count,
            name=name,
            uuid=uuid,
            country=country,
        )

        offering_stats.additional_properties = d
        return offering_stats

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
