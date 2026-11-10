from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.hpc_output_series_kind_enum import HpcOutputSeriesKindEnum

if TYPE_CHECKING:
    from ..models.chart_spec import ChartSpec
    from ..models.hpc_output_series_summary import HpcOutputSeriesSummary


T = TypeVar("T", bound="HpcOutputSeries")


@_attrs_define
class HpcOutputSeries:
    """
    Attributes:
        path (str):
        kind (HpcOutputSeriesKindEnum):
        title (str):
        summary (HpcOutputSeriesSummary):
        chart (ChartSpec):
    """

    path: str
    kind: HpcOutputSeriesKindEnum
    title: str
    summary: "HpcOutputSeriesSummary"
    chart: "ChartSpec"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        kind = self.kind.value

        title = self.title

        summary = self.summary.to_dict()

        chart = self.chart.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "kind": kind,
                "title": title,
                "summary": summary,
                "chart": chart,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chart_spec import ChartSpec
        from ..models.hpc_output_series_summary import HpcOutputSeriesSummary

        d = dict(src_dict)
        path = d.pop("path")

        kind = HpcOutputSeriesKindEnum(d.pop("kind"))

        title = d.pop("title")

        summary = HpcOutputSeriesSummary.from_dict(d.pop("summary"))

        chart = ChartSpec.from_dict(d.pop("chart"))

        hpc_output_series = cls(
            path=path,
            kind=kind,
            title=title,
            summary=summary,
            chart=chart,
        )

        hpc_output_series.additional_properties = d
        return hpc_output_series

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
