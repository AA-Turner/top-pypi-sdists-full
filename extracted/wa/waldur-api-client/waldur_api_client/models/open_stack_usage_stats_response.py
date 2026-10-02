from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OpenStackUsageStatsResponse")


@_attrs_define
class OpenStackUsageStatsResponse:
    """
    Attributes:
        name (str):
        running_instances_count (int):
        created_instances_count (int):
    """

    name: str
    running_instances_count: int
    created_instances_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        running_instances_count = self.running_instances_count

        created_instances_count = self.created_instances_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "running_instances_count": running_instances_count,
                "created_instances_count": created_instances_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        running_instances_count = d.pop("running_instances_count")

        created_instances_count = d.pop("created_instances_count")

        open_stack_usage_stats_response = cls(
            name=name,
            running_instances_count=running_instances_count,
            created_instances_count=created_instances_count,
        )

        open_stack_usage_stats_response.additional_properties = d
        return open_stack_usage_stats_response

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
