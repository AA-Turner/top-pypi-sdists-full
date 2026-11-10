from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.chart_axis_type_enum import ChartAxisTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChartAxis")


@_attrs_define
class ChartAxis:
    """
    Attributes:
        type_ (Union[Unset, ChartAxisTypeEnum]):  Default: ChartAxisTypeEnum.VALUE.
        label (Union[Unset, str]):
        unit (Union[Unset, str]):
        min_ (Union[None, Unset, float]):
        max_ (Union[None, Unset, float]):
        categories (Union[Unset, list[str]]): Category labels, in order, for a category axis.
    """

    type_: Union[Unset, ChartAxisTypeEnum] = ChartAxisTypeEnum.VALUE
    label: Union[Unset, str] = UNSET
    unit: Union[Unset, str] = UNSET
    min_: Union[None, Unset, float] = UNSET
    max_: Union[None, Unset, float] = UNSET
    categories: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        label = self.label

        unit = self.unit

        min_: Union[None, Unset, float]
        if isinstance(self.min_, Unset):
            min_ = UNSET
        else:
            min_ = self.min_

        max_: Union[None, Unset, float]
        if isinstance(self.max_, Unset):
            max_ = UNSET
        else:
            max_ = self.max_

        categories: Union[Unset, list[str]] = UNSET
        if not isinstance(self.categories, Unset):
            categories = self.categories

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if label is not UNSET:
            field_dict["label"] = label
        if unit is not UNSET:
            field_dict["unit"] = unit
        if min_ is not UNSET:
            field_dict["min"] = min_
        if max_ is not UNSET:
            field_dict["max"] = max_
        if categories is not UNSET:
            field_dict["categories"] = categories

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, ChartAxisTypeEnum]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = ChartAxisTypeEnum(_type_)

        label = d.pop("label", UNSET)

        unit = d.pop("unit", UNSET)

        def _parse_min_(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        min_ = _parse_min_(d.pop("min", UNSET))

        def _parse_max_(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        max_ = _parse_max_(d.pop("max", UNSET))

        categories = cast(list[str], d.pop("categories", UNSET))

        chart_axis = cls(
            type_=type_,
            label=label,
            unit=unit,
            min_=min_,
            max_=max_,
            categories=categories,
        )

        chart_axis.additional_properties = d
        return chart_axis

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
