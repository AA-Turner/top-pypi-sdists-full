from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.agent_stats_backend_type import AgentStatsBackendType


T = TypeVar("T", bound="AgentStatsProcessors")


@_attrs_define
class AgentStatsProcessors:
    """
    Attributes:
        total (int):
        by_backend_type (list['AgentStatsBackendType']):
        stale_count (int):
    """

    total: int
    by_backend_type: list["AgentStatsBackendType"]
    stale_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total = self.total

        by_backend_type = []
        for by_backend_type_item_data in self.by_backend_type:
            by_backend_type_item = by_backend_type_item_data.to_dict()
            by_backend_type.append(by_backend_type_item)

        stale_count = self.stale_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "by_backend_type": by_backend_type,
                "stale_count": stale_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_stats_backend_type import AgentStatsBackendType

        d = dict(src_dict)
        total = d.pop("total")

        by_backend_type = []
        _by_backend_type = d.pop("by_backend_type")
        for by_backend_type_item_data in _by_backend_type:
            by_backend_type_item = AgentStatsBackendType.from_dict(by_backend_type_item_data)

            by_backend_type.append(by_backend_type_item)

        stale_count = d.pop("stale_count")

        agent_stats_processors = cls(
            total=total,
            by_backend_type=by_backend_type,
            stale_count=stale_count,
        )

        agent_stats_processors.additional_properties = d
        return agent_stats_processors

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
