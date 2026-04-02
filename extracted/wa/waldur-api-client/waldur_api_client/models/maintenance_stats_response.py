from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.daily_maintenance_stats import DailyMaintenanceStats
    from ..models.maintenance_provider_stats import MaintenanceProviderStats
    from ..models.maintenance_stats_response_by_impact_level import MaintenanceStatsResponseByImpactLevel
    from ..models.maintenance_stats_response_by_state import MaintenanceStatsResponseByState
    from ..models.maintenance_stats_response_by_type import MaintenanceStatsResponseByType
    from ..models.maintenance_stats_summary import MaintenanceStatsSummary


T = TypeVar("T", bound="MaintenanceStatsResponse")


@_attrs_define
class MaintenanceStatsResponse:
    """
    Attributes:
        summary (MaintenanceStatsSummary):
        by_state (MaintenanceStatsResponseByState): Total counts grouped by state
        by_type (MaintenanceStatsResponseByType): Total counts grouped by maintenance type
        by_impact_level (MaintenanceStatsResponseByImpactLevel): Total counts grouped by max impact level
        daily (list['DailyMaintenanceStats']): Daily breakdown
        providers (list['MaintenanceProviderStats']): Statistics per provider
    """

    summary: "MaintenanceStatsSummary"
    by_state: "MaintenanceStatsResponseByState"
    by_type: "MaintenanceStatsResponseByType"
    by_impact_level: "MaintenanceStatsResponseByImpactLevel"
    daily: list["DailyMaintenanceStats"]
    providers: list["MaintenanceProviderStats"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        summary = self.summary.to_dict()

        by_state = self.by_state.to_dict()

        by_type = self.by_type.to_dict()

        by_impact_level = self.by_impact_level.to_dict()

        daily = []
        for daily_item_data in self.daily:
            daily_item = daily_item_data.to_dict()
            daily.append(daily_item)

        providers = []
        for providers_item_data in self.providers:
            providers_item = providers_item_data.to_dict()
            providers.append(providers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "summary": summary,
                "by_state": by_state,
                "by_type": by_type,
                "by_impact_level": by_impact_level,
                "daily": daily,
                "providers": providers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daily_maintenance_stats import DailyMaintenanceStats
        from ..models.maintenance_provider_stats import MaintenanceProviderStats
        from ..models.maintenance_stats_response_by_impact_level import MaintenanceStatsResponseByImpactLevel
        from ..models.maintenance_stats_response_by_state import MaintenanceStatsResponseByState
        from ..models.maintenance_stats_response_by_type import MaintenanceStatsResponseByType
        from ..models.maintenance_stats_summary import MaintenanceStatsSummary

        d = dict(src_dict)
        summary = MaintenanceStatsSummary.from_dict(d.pop("summary"))

        by_state = MaintenanceStatsResponseByState.from_dict(d.pop("by_state"))

        by_type = MaintenanceStatsResponseByType.from_dict(d.pop("by_type"))

        by_impact_level = MaintenanceStatsResponseByImpactLevel.from_dict(d.pop("by_impact_level"))

        daily = []
        _daily = d.pop("daily")
        for daily_item_data in _daily:
            daily_item = DailyMaintenanceStats.from_dict(daily_item_data)

            daily.append(daily_item)

        providers = []
        _providers = d.pop("providers")
        for providers_item_data in _providers:
            providers_item = MaintenanceProviderStats.from_dict(providers_item_data)

            providers.append(providers_item)

        maintenance_stats_response = cls(
            summary=summary,
            by_state=by_state,
            by_type=by_type,
            by_impact_level=by_impact_level,
            daily=daily,
            providers=providers,
        )

        maintenance_stats_response.additional_properties = d
        return maintenance_stats_response

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
