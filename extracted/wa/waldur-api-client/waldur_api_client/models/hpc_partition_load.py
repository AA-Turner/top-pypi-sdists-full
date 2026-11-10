from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HpcPartitionLoad")


@_attrs_define
class HpcPartitionLoad:
    """
    Attributes:
        name (str):
        total (int):
        idle (int):
        mixed (int):
        allocated (int):
        unavailable (int):
        reserved (int):
        average_load_percent (Union[None, float]):
    """

    name: str
    total: int
    idle: int
    mixed: int
    allocated: int
    unavailable: int
    reserved: int
    average_load_percent: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        total = self.total

        idle = self.idle

        mixed = self.mixed

        allocated = self.allocated

        unavailable = self.unavailable

        reserved = self.reserved

        average_load_percent: Union[None, float]
        average_load_percent = self.average_load_percent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "total": total,
                "idle": idle,
                "mixed": mixed,
                "allocated": allocated,
                "unavailable": unavailable,
                "reserved": reserved,
                "average_load_percent": average_load_percent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        total = d.pop("total")

        idle = d.pop("idle")

        mixed = d.pop("mixed")

        allocated = d.pop("allocated")

        unavailable = d.pop("unavailable")

        reserved = d.pop("reserved")

        def _parse_average_load_percent(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        average_load_percent = _parse_average_load_percent(d.pop("average_load_percent"))

        hpc_partition_load = cls(
            name=name,
            total=total,
            idle=idle,
            mixed=mixed,
            allocated=allocated,
            unavailable=unavailable,
            reserved=reserved,
            average_load_percent=average_load_percent,
        )

        hpc_partition_load.additional_properties = d
        return hpc_partition_load

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
