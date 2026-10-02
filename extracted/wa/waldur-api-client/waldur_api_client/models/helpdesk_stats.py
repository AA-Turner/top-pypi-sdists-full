from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.helpdesk_stats_by_priority import HelpdeskStatsByPriority
    from ..models.helpdesk_stats_by_status import HelpdeskStatsByStatus


T = TypeVar("T", bound="HelpdeskStats")


@_attrs_define
class HelpdeskStats:
    """
    Attributes:
        total_open (int):
        total_closed_this_month (int):
        total_routed (int):
        total_escalated (int):
        sla_breach_count (int):
        avg_first_response_hours (Union[None, float]):
        avg_resolution_hours (Union[None, float]):
        by_status (HelpdeskStatsByStatus):
        by_priority (HelpdeskStatsByPriority):
    """

    total_open: int
    total_closed_this_month: int
    total_routed: int
    total_escalated: int
    sla_breach_count: int
    avg_first_response_hours: Union[None, float]
    avg_resolution_hours: Union[None, float]
    by_status: "HelpdeskStatsByStatus"
    by_priority: "HelpdeskStatsByPriority"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_open = self.total_open

        total_closed_this_month = self.total_closed_this_month

        total_routed = self.total_routed

        total_escalated = self.total_escalated

        sla_breach_count = self.sla_breach_count

        avg_first_response_hours: Union[None, float]
        avg_first_response_hours = self.avg_first_response_hours

        avg_resolution_hours: Union[None, float]
        avg_resolution_hours = self.avg_resolution_hours

        by_status = self.by_status.to_dict()

        by_priority = self.by_priority.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_open": total_open,
                "total_closed_this_month": total_closed_this_month,
                "total_routed": total_routed,
                "total_escalated": total_escalated,
                "sla_breach_count": sla_breach_count,
                "avg_first_response_hours": avg_first_response_hours,
                "avg_resolution_hours": avg_resolution_hours,
                "by_status": by_status,
                "by_priority": by_priority,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.helpdesk_stats_by_priority import HelpdeskStatsByPriority
        from ..models.helpdesk_stats_by_status import HelpdeskStatsByStatus

        d = dict(src_dict)
        total_open = d.pop("total_open")

        total_closed_this_month = d.pop("total_closed_this_month")

        total_routed = d.pop("total_routed")

        total_escalated = d.pop("total_escalated")

        sla_breach_count = d.pop("sla_breach_count")

        def _parse_avg_first_response_hours(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        avg_first_response_hours = _parse_avg_first_response_hours(d.pop("avg_first_response_hours"))

        def _parse_avg_resolution_hours(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        avg_resolution_hours = _parse_avg_resolution_hours(d.pop("avg_resolution_hours"))

        by_status = HelpdeskStatsByStatus.from_dict(d.pop("by_status"))

        by_priority = HelpdeskStatsByPriority.from_dict(d.pop("by_priority"))

        helpdesk_stats = cls(
            total_open=total_open,
            total_closed_this_month=total_closed_this_month,
            total_routed=total_routed,
            total_escalated=total_escalated,
            sla_breach_count=sla_breach_count,
            avg_first_response_hours=avg_first_response_hours,
            avg_resolution_hours=avg_resolution_hours,
            by_status=by_status,
            by_priority=by_priority,
        )

        helpdesk_stats.additional_properties = d
        return helpdesk_stats

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
