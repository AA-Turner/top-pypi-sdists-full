from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.style_enum import StyleEnum
from ..models.tone_enum import ToneEnum
from ..models.y_axis_enum import YAxisEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChartSeries")


@_attrs_define
class ChartSeries:
    """
    Attributes:
        name (str):
        points (list[list[Union[None, float, str]]]): [x, y] pairs; heatmap [x, y, value]; timeline [row, start, end,
            limit_end].
        style (Union[Unset, StyleEnum]):  Default: StyleEnum.SOLID.
        tone (Union[Unset, ToneEnum]):
        y_axis (Union[Unset, YAxisEnum]):  Default: YAxisEnum.PRIMARY.
        labels (Union[Unset, list[str]]): Tooltip text per point.
        ids (Union[Unset, list[str]]): Identifier per point (e.g. a job ID) the page may link to.
    """

    name: str
    points: list[list[Union[None, float, str]]]
    style: Union[Unset, StyleEnum] = StyleEnum.SOLID
    tone: Union[Unset, ToneEnum] = UNSET
    y_axis: Union[Unset, YAxisEnum] = YAxisEnum.PRIMARY
    labels: Union[Unset, list[str]] = UNSET
    ids: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        points = []
        for points_item_data in self.points:
            points_item = []
            for points_item_item_data in points_item_data:
                points_item_item: Union[None, float, str]
                points_item_item = points_item_item_data
                points_item.append(points_item_item)

            points.append(points_item)

        style: Union[Unset, str] = UNSET
        if not isinstance(self.style, Unset):
            style = self.style.value

        tone: Union[Unset, str] = UNSET
        if not isinstance(self.tone, Unset):
            tone = self.tone.value

        y_axis: Union[Unset, str] = UNSET
        if not isinstance(self.y_axis, Unset):
            y_axis = self.y_axis.value

        labels: Union[Unset, list[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.ids, Unset):
            ids = self.ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "points": points,
            }
        )
        if style is not UNSET:
            field_dict["style"] = style
        if tone is not UNSET:
            field_dict["tone"] = tone
        if y_axis is not UNSET:
            field_dict["y_axis"] = y_axis
        if labels is not UNSET:
            field_dict["labels"] = labels
        if ids is not UNSET:
            field_dict["ids"] = ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        points = []
        _points = d.pop("points")
        for points_item_data in _points:
            points_item = []
            _points_item = points_item_data
            for points_item_item_data in _points_item:

                def _parse_points_item_item(data: object) -> Union[None, float, str]:
                    if data is None:
                        return data
                    return cast(Union[None, float, str], data)

                points_item_item = _parse_points_item_item(points_item_item_data)

                points_item.append(points_item_item)

            points.append(points_item)

        _style = d.pop("style", UNSET)
        style: Union[Unset, StyleEnum]
        if isinstance(_style, Unset):
            style = UNSET
        else:
            style = StyleEnum(_style)

        _tone = d.pop("tone", UNSET)
        tone: Union[Unset, ToneEnum]
        if isinstance(_tone, Unset):
            tone = UNSET
        else:
            tone = ToneEnum(_tone)

        _y_axis = d.pop("y_axis", UNSET)
        y_axis: Union[Unset, YAxisEnum]
        if isinstance(_y_axis, Unset):
            y_axis = UNSET
        else:
            y_axis = YAxisEnum(_y_axis)

        labels = cast(list[str], d.pop("labels", UNSET))

        ids = cast(list[str], d.pop("ids", UNSET))

        chart_series = cls(
            name=name,
            points=points,
            style=style,
            tone=tone,
            y_axis=y_axis,
            labels=labels,
            ids=ids,
        )

        chart_series.additional_properties = d
        return chart_series

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
