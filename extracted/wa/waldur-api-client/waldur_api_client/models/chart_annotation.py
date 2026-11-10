from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.chart_annotation_type_enum import ChartAnnotationTypeEnum
from ..models.tone_enum import ToneEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChartAnnotation")


@_attrs_define
class ChartAnnotation:
    """
    Attributes:
        type_ (ChartAnnotationTypeEnum):
        value (float):
        value_end (Union[None, Unset, float]):
        label (Union[Unset, str]):
        tone (Union[Unset, ToneEnum]):  Default: ToneEnum.NEUTRAL.
    """

    type_: ChartAnnotationTypeEnum
    value: float
    value_end: Union[None, Unset, float] = UNSET
    label: Union[Unset, str] = UNSET
    tone: Union[Unset, ToneEnum] = ToneEnum.NEUTRAL
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        value = self.value

        value_end: Union[None, Unset, float]
        if isinstance(self.value_end, Unset):
            value_end = UNSET
        else:
            value_end = self.value_end

        label = self.label

        tone: Union[Unset, str] = UNSET
        if not isinstance(self.tone, Unset):
            tone = self.tone.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "value": value,
            }
        )
        if value_end is not UNSET:
            field_dict["value_end"] = value_end
        if label is not UNSET:
            field_dict["label"] = label
        if tone is not UNSET:
            field_dict["tone"] = tone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = ChartAnnotationTypeEnum(d.pop("type"))

        value = d.pop("value")

        def _parse_value_end(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        value_end = _parse_value_end(d.pop("value_end", UNSET))

        label = d.pop("label", UNSET)

        _tone = d.pop("tone", UNSET)
        tone: Union[Unset, ToneEnum]
        if isinstance(_tone, Unset):
            tone = UNSET
        else:
            tone = ToneEnum(_tone)

        chart_annotation = cls(
            type_=type_,
            value=value,
            value_end=value_end,
            label=label,
            tone=tone,
        )

        chart_annotation.additional_properties = d
        return chart_annotation

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
