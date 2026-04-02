from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CustomerOecdCodeStats")


@_attrs_define
class CustomerOecdCodeStats:
    """
    Attributes:
        name (str): Name from the record
        uuid (str): UUID from the record
        count (int): Count value from the record
        abbreviation (str): Customer abbreviation from the record
        oecd (str):
    """

    name: str
    uuid: str
    count: int
    abbreviation: str
    oecd: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        uuid = self.uuid

        count = self.count

        abbreviation = self.abbreviation

        oecd = self.oecd

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "uuid": uuid,
                "count": count,
                "abbreviation": abbreviation,
                "oecd": oecd,
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

        oecd = d.pop("oecd")

        customer_oecd_code_stats = cls(
            name=name,
            uuid=uuid,
            count=count,
            abbreviation=abbreviation,
            oecd=oecd,
        )

        customer_oecd_code_stats.additional_properties = d
        return customer_oecd_code_stats

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
