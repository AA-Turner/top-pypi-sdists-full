from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.chart_spec import ChartSpec
    from ..models.hpc_job_failure import HpcJobFailure
    from ..models.hpc_job_totals import HpcJobTotals
    from ..models.hpc_partition_wait import HpcPartitionWait
    from ..models.hpc_suggestion import HpcSuggestion


T = TypeVar("T", bound="HpcJobStats")


@_attrs_define
class HpcJobStats:
    """
    Attributes:
        days (int):
        since (int):
        until (int):
        totals (HpcJobTotals):
        cpu_hours (float):
        failures (list['HpcJobFailure']):
        wait_by_partition (list['HpcPartitionWait']):
        suggestions (list['HpcSuggestion']):
        charts (list['ChartSpec']):
    """

    days: int
    since: int
    until: int
    totals: "HpcJobTotals"
    cpu_hours: float
    failures: list["HpcJobFailure"]
    wait_by_partition: list["HpcPartitionWait"]
    suggestions: list["HpcSuggestion"]
    charts: list["ChartSpec"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        days = self.days

        since = self.since

        until = self.until

        totals = self.totals.to_dict()

        cpu_hours = self.cpu_hours

        failures = []
        for failures_item_data in self.failures:
            failures_item = failures_item_data.to_dict()
            failures.append(failures_item)

        wait_by_partition = []
        for wait_by_partition_item_data in self.wait_by_partition:
            wait_by_partition_item = wait_by_partition_item_data.to_dict()
            wait_by_partition.append(wait_by_partition_item)

        suggestions = []
        for suggestions_item_data in self.suggestions:
            suggestions_item = suggestions_item_data.to_dict()
            suggestions.append(suggestions_item)

        charts = []
        for charts_item_data in self.charts:
            charts_item = charts_item_data.to_dict()
            charts.append(charts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "days": days,
                "since": since,
                "until": until,
                "totals": totals,
                "cpu_hours": cpu_hours,
                "failures": failures,
                "wait_by_partition": wait_by_partition,
                "suggestions": suggestions,
                "charts": charts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chart_spec import ChartSpec
        from ..models.hpc_job_failure import HpcJobFailure
        from ..models.hpc_job_totals import HpcJobTotals
        from ..models.hpc_partition_wait import HpcPartitionWait
        from ..models.hpc_suggestion import HpcSuggestion

        d = dict(src_dict)
        days = d.pop("days")

        since = d.pop("since")

        until = d.pop("until")

        totals = HpcJobTotals.from_dict(d.pop("totals"))

        cpu_hours = d.pop("cpu_hours")

        failures = []
        _failures = d.pop("failures")
        for failures_item_data in _failures:
            failures_item = HpcJobFailure.from_dict(failures_item_data)

            failures.append(failures_item)

        wait_by_partition = []
        _wait_by_partition = d.pop("wait_by_partition")
        for wait_by_partition_item_data in _wait_by_partition:
            wait_by_partition_item = HpcPartitionWait.from_dict(wait_by_partition_item_data)

            wait_by_partition.append(wait_by_partition_item)

        suggestions = []
        _suggestions = d.pop("suggestions")
        for suggestions_item_data in _suggestions:
            suggestions_item = HpcSuggestion.from_dict(suggestions_item_data)

            suggestions.append(suggestions_item)

        charts = []
        _charts = d.pop("charts")
        for charts_item_data in _charts:
            charts_item = ChartSpec.from_dict(charts_item_data)

            charts.append(charts_item)

        hpc_job_stats = cls(
            days=days,
            since=since,
            until=until,
            totals=totals,
            cpu_hours=cpu_hours,
            failures=failures,
            wait_by_partition=wait_by_partition,
            suggestions=suggestions,
            charts=charts,
        )

        hpc_job_stats.additional_properties = d
        return hpc_job_stats

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
