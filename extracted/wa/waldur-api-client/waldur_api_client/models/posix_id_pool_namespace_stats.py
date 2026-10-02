from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PosixIdPoolNamespaceStats")


@_attrs_define
class PosixIdPoolNamespaceStats:
    """
    Attributes:
        min_ (int):
        max_ (int):
        next_ (int):
        capacity (int):
        used (int):
        utilization (float):
    """

    min_: int
    max_: int
    next_: int
    capacity: int
    used: int
    utilization: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        min_ = self.min_

        max_ = self.max_

        next_ = self.next_

        capacity = self.capacity

        used = self.used

        utilization = self.utilization

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "min": min_,
                "max": max_,
                "next": next_,
                "capacity": capacity,
                "used": used,
                "utilization": utilization,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        min_ = d.pop("min")

        max_ = d.pop("max")

        next_ = d.pop("next")

        capacity = d.pop("capacity")

        used = d.pop("used")

        utilization = d.pop("utilization")

        posix_id_pool_namespace_stats = cls(
            min_=min_,
            max_=max_,
            next_=next_,
            capacity=capacity,
            used=used,
            utilization=utilization,
        )

        posix_id_pool_namespace_stats.additional_properties = d
        return posix_id_pool_namespace_stats

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
