from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HpcReservation")


@_attrs_define
class HpcReservation:
    """
    Attributes:
        name (str):
        start (int):
        end (int):
        node_list (str):
        node_count (Union[None, int]):
        maintenance (bool):
        active (bool):
        partitions (list[str]):
        announced (Union[None, bool]): For maintenance reservations: whether Waldur announces it.
    """

    name: str
    start: int
    end: int
    node_list: str
    node_count: Union[None, int]
    maintenance: bool
    active: bool
    partitions: list[str]
    announced: Union[None, bool]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        start = self.start

        end = self.end

        node_list = self.node_list

        node_count: Union[None, int]
        node_count = self.node_count

        maintenance = self.maintenance

        active = self.active

        partitions = self.partitions

        announced: Union[None, bool]
        announced = self.announced

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "start": start,
                "end": end,
                "node_list": node_list,
                "node_count": node_count,
                "maintenance": maintenance,
                "active": active,
                "partitions": partitions,
                "announced": announced,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        start = d.pop("start")

        end = d.pop("end")

        node_list = d.pop("node_list")

        def _parse_node_count(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        node_count = _parse_node_count(d.pop("node_count"))

        maintenance = d.pop("maintenance")

        active = d.pop("active")

        partitions = cast(list[str], d.pop("partitions"))

        def _parse_announced(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        announced = _parse_announced(d.pop("announced"))

        hpc_reservation = cls(
            name=name,
            start=start,
            end=end,
            node_list=node_list,
            node_count=node_count,
            maintenance=maintenance,
            active=active,
            partitions=partitions,
            announced=announced,
        )

        hpc_reservation.additional_properties = d
        return hpc_reservation

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
