from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.agent_stats_services_state import AgentStatsServicesState


T = TypeVar("T", bound="AgentStatsServices")


@_attrs_define
class AgentStatsServices:
    """
    Attributes:
        total (int):
        by_state (AgentStatsServicesState):
        stale_count (int):
    """

    total: int
    by_state: "AgentStatsServicesState"
    stale_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total = self.total

        by_state = self.by_state.to_dict()

        stale_count = self.stale_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "by_state": by_state,
                "stale_count": stale_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_stats_services_state import AgentStatsServicesState

        d = dict(src_dict)
        total = d.pop("total")

        by_state = AgentStatsServicesState.from_dict(d.pop("by_state"))

        stale_count = d.pop("stale_count")

        agent_stats_services = cls(
            total=total,
            by_state=by_state,
            stale_count=stale_count,
        )

        agent_stats_services.additional_properties = d
        return agent_stats_services

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
