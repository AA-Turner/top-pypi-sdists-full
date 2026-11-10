from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.chart_type_enum import ChartTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chart_annotation import ChartAnnotation
    from ..models.chart_axis import ChartAxis
    from ..models.chart_link import ChartLink
    from ..models.chart_series import ChartSeries


T = TypeVar("T", bound="ChartSpec")


@_attrs_define
class ChartSpec:
    """
    Attributes:
        chart_type (ChartTypeEnum):
        title (str):
        x (ChartAxis):
        y (ChartAxis):
        series (list['ChartSeries']):
        subtitle (Union[Unset, str]):
        y2 (Union[Unset, ChartAxis]):
        annotations (Union[Unset, list['ChartAnnotation']]):
        link (Union[Unset, ChartLink]):
        empty_message (Union[Unset, str]): Shown instead of the chart when no series has points.
    """

    chart_type: ChartTypeEnum
    title: str
    x: "ChartAxis"
    y: "ChartAxis"
    series: list["ChartSeries"]
    subtitle: Union[Unset, str] = UNSET
    y2: Union[Unset, "ChartAxis"] = UNSET
    annotations: Union[Unset, list["ChartAnnotation"]] = UNSET
    link: Union[Unset, "ChartLink"] = UNSET
    empty_message: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        chart_type = self.chart_type.value

        title = self.title

        x = self.x.to_dict()

        y = self.y.to_dict()

        series = []
        for series_item_data in self.series:
            series_item = series_item_data.to_dict()
            series.append(series_item)

        subtitle = self.subtitle

        y2: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.y2, Unset):
            y2 = self.y2.to_dict()

        annotations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.annotations, Unset):
            annotations = []
            for annotations_item_data in self.annotations:
                annotations_item = annotations_item_data.to_dict()
                annotations.append(annotations_item)

        link: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.link, Unset):
            link = self.link.to_dict()

        empty_message = self.empty_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chart_type": chart_type,
                "title": title,
                "x": x,
                "y": y,
                "series": series,
            }
        )
        if subtitle is not UNSET:
            field_dict["subtitle"] = subtitle
        if y2 is not UNSET:
            field_dict["y2"] = y2
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if link is not UNSET:
            field_dict["link"] = link
        if empty_message is not UNSET:
            field_dict["empty_message"] = empty_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chart_annotation import ChartAnnotation
        from ..models.chart_axis import ChartAxis
        from ..models.chart_link import ChartLink
        from ..models.chart_series import ChartSeries

        d = dict(src_dict)
        chart_type = ChartTypeEnum(d.pop("chart_type"))

        title = d.pop("title")

        x = ChartAxis.from_dict(d.pop("x"))

        y = ChartAxis.from_dict(d.pop("y"))

        series = []
        _series = d.pop("series")
        for series_item_data in _series:
            series_item = ChartSeries.from_dict(series_item_data)

            series.append(series_item)

        subtitle = d.pop("subtitle", UNSET)

        _y2 = d.pop("y2", UNSET)
        y2: Union[Unset, ChartAxis]
        if isinstance(_y2, Unset):
            y2 = UNSET
        else:
            y2 = ChartAxis.from_dict(_y2)

        annotations = []
        _annotations = d.pop("annotations", UNSET)
        for annotations_item_data in _annotations or []:
            annotations_item = ChartAnnotation.from_dict(annotations_item_data)

            annotations.append(annotations_item)

        _link = d.pop("link", UNSET)
        link: Union[Unset, ChartLink]
        if isinstance(_link, Unset):
            link = UNSET
        else:
            link = ChartLink.from_dict(_link)

        empty_message = d.pop("empty_message", UNSET)

        chart_spec = cls(
            chart_type=chart_type,
            title=title,
            x=x,
            y=y,
            series=series,
            subtitle=subtitle,
            y2=y2,
            annotations=annotations,
            link=link,
            empty_message=empty_message,
        )

        chart_spec.additional_properties = d
        return chart_spec

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
