from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.system_log_stats_instance import SystemLogStatsInstance


T = TypeVar("T", bound="SystemLogStatsResponse")


@_attrs_define
class SystemLogStatsResponse:
    """
    Attributes:
        instances (list['SystemLogStatsInstance']):
        total_size_bytes (int):
        total_size_mb (float):
    """

    instances: list["SystemLogStatsInstance"]
    total_size_bytes: int
    total_size_mb: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        instances = []
        for instances_item_data in self.instances:
            instances_item = instances_item_data.to_dict()
            instances.append(instances_item)

        total_size_bytes = self.total_size_bytes

        total_size_mb = self.total_size_mb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "instances": instances,
                "total_size_bytes": total_size_bytes,
                "total_size_mb": total_size_mb,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.system_log_stats_instance import SystemLogStatsInstance

        d = dict(src_dict)
        instances = []
        _instances = d.pop("instances")
        for instances_item_data in _instances:
            instances_item = SystemLogStatsInstance.from_dict(instances_item_data)

            instances.append(instances_item)

        total_size_bytes = d.pop("total_size_bytes")

        total_size_mb = d.pop("total_size_mb")

        system_log_stats_response = cls(
            instances=instances,
            total_size_bytes=total_size_bytes,
            total_size_mb=total_size_mb,
        )

        system_log_stats_response.additional_properties = d
        return system_log_stats_response

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
