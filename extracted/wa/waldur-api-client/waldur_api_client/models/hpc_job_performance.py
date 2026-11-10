from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chart_spec import ChartSpec
    from ..models.hpc_job_performance_summary import HpcJobPerformanceSummary
    from ..models.hpc_job_process import HpcJobProcess


T = TypeVar("T", bound="HpcJobPerformance")


@_attrs_define
class HpcJobPerformance:
    """
    Attributes:
        available (bool):
        message (str): Why there is nothing to show, when not available
        start_time (Union[Unset, int]): Epoch seconds
        end_time (Union[Unset, int]): Epoch seconds
        resolution (Union[Unset, int]): Seconds between points
        summary (Union[Unset, HpcJobPerformanceSummary]):
        charts (Union[Unset, list['ChartSpec']]):
        processes (Union[Unset, list['HpcJobProcess']]):
        warnings (Union[Unset, list[str]]):
    """

    available: bool
    message: str
    start_time: Union[Unset, int] = UNSET
    end_time: Union[Unset, int] = UNSET
    resolution: Union[Unset, int] = UNSET
    summary: Union[Unset, "HpcJobPerformanceSummary"] = UNSET
    charts: Union[Unset, list["ChartSpec"]] = UNSET
    processes: Union[Unset, list["HpcJobProcess"]] = UNSET
    warnings: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        available = self.available

        message = self.message

        start_time = self.start_time

        end_time = self.end_time

        resolution = self.resolution

        summary: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.summary, Unset):
            summary = self.summary.to_dict()

        charts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.charts, Unset):
            charts = []
            for charts_item_data in self.charts:
                charts_item = charts_item_data.to_dict()
                charts.append(charts_item)

        processes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.processes, Unset):
            processes = []
            for processes_item_data in self.processes:
                processes_item = processes_item_data.to_dict()
                processes.append(processes_item)

        warnings: Union[Unset, list[str]] = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "available": available,
                "message": message,
            }
        )
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if resolution is not UNSET:
            field_dict["resolution"] = resolution
        if summary is not UNSET:
            field_dict["summary"] = summary
        if charts is not UNSET:
            field_dict["charts"] = charts
        if processes is not UNSET:
            field_dict["processes"] = processes
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chart_spec import ChartSpec
        from ..models.hpc_job_performance_summary import HpcJobPerformanceSummary
        from ..models.hpc_job_process import HpcJobProcess

        d = dict(src_dict)
        available = d.pop("available")

        message = d.pop("message")

        start_time = d.pop("start_time", UNSET)

        end_time = d.pop("end_time", UNSET)

        resolution = d.pop("resolution", UNSET)

        _summary = d.pop("summary", UNSET)
        summary: Union[Unset, HpcJobPerformanceSummary]
        if isinstance(_summary, Unset):
            summary = UNSET
        else:
            summary = HpcJobPerformanceSummary.from_dict(_summary)

        charts = []
        _charts = d.pop("charts", UNSET)
        for charts_item_data in _charts or []:
            charts_item = ChartSpec.from_dict(charts_item_data)

            charts.append(charts_item)

        processes = []
        _processes = d.pop("processes", UNSET)
        for processes_item_data in _processes or []:
            processes_item = HpcJobProcess.from_dict(processes_item_data)

            processes.append(processes_item)

        warnings = cast(list[str], d.pop("warnings", UNSET))

        hpc_job_performance = cls(
            available=available,
            message=message,
            start_time=start_time,
            end_time=end_time,
            resolution=resolution,
            summary=summary,
            charts=charts,
            processes=processes,
            warnings=warnings,
        )

        hpc_job_performance.additional_properties = d
        return hpc_job_performance

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
