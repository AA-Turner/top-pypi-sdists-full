from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.provider_stats_by_status import ProviderStatsByStatus


T = TypeVar("T", bound="ProviderStats")


@_attrs_define
class ProviderStats:
    """
    Attributes:
        total_open (int):
        total_resolved (int):
        total_escalated (int):
        sla_breach_count (int):
        avg_resolution_hours (Union[None, float]):
        by_status (ProviderStatsByStatus):
    """

    total_open: int
    total_resolved: int
    total_escalated: int
    sla_breach_count: int
    avg_resolution_hours: Union[None, float]
    by_status: "ProviderStatsByStatus"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_open = self.total_open

        total_resolved = self.total_resolved

        total_escalated = self.total_escalated

        sla_breach_count = self.sla_breach_count

        avg_resolution_hours: Union[None, float]
        avg_resolution_hours = self.avg_resolution_hours

        by_status = self.by_status.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_open": total_open,
                "total_resolved": total_resolved,
                "total_escalated": total_escalated,
                "sla_breach_count": sla_breach_count,
                "avg_resolution_hours": avg_resolution_hours,
                "by_status": by_status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provider_stats_by_status import ProviderStatsByStatus

        d = dict(src_dict)
        total_open = d.pop("total_open")

        total_resolved = d.pop("total_resolved")

        total_escalated = d.pop("total_escalated")

        sla_breach_count = d.pop("sla_breach_count")

        def _parse_avg_resolution_hours(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        avg_resolution_hours = _parse_avg_resolution_hours(d.pop("avg_resolution_hours"))

        by_status = ProviderStatsByStatus.from_dict(d.pop("by_status"))

        provider_stats = cls(
            total_open=total_open,
            total_resolved=total_resolved,
            total_escalated=total_escalated,
            sla_breach_count=sla_breach_count,
            avg_resolution_hours=avg_resolution_hours,
            by_status=by_status,
        )

        provider_stats.additional_properties = d
        return provider_stats

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
