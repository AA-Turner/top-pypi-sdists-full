from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CustomerIndustryFlagStats")


@_attrs_define
class CustomerIndustryFlagStats:
    """
    Attributes:
        name (str): Name from the record
        uuid (str): UUID from the record
        count (int): Count value from the record
        abbreviation (str): Customer abbreviation from the record
        is_industry (str): Industry classification flag
    """

    name: str
    uuid: str
    count: int
    abbreviation: str
    is_industry: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        uuid = self.uuid

        count = self.count

        abbreviation = self.abbreviation

        is_industry = self.is_industry

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "uuid": uuid,
                "count": count,
                "abbreviation": abbreviation,
                "is_industry": is_industry,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        uuid = d.pop("uuid")

        count = d.pop("count")

        abbreviation = d.pop("abbreviation")

        is_industry = d.pop("is_industry")

        customer_industry_flag_stats = cls(
            name=name,
            uuid=uuid,
            count=count,
            abbreviation=abbreviation,
            is_industry=is_industry,
        )

        customer_industry_flag_stats.additional_properties = d
        return customer_industry_flag_stats

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
