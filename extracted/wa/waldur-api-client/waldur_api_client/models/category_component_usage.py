import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CategoryComponentUsage")


@_attrs_define
class CategoryComponentUsage:
    """
    Attributes:
        name (Union[Unset, str]): Display name for the measured unit, for example, Floating IP.
        type_ (Union[Unset, str]): Unique internal name of the measured unit, for example floating_ip.
        measured_unit (Union[Unset, str]): Unit of measurement, for example, GB.
        category_title (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        date (Union[Unset, datetime.date]):
        reported_usage (Union[None, Unset, int]):
        fixed_usage (Union[None, Unset, int]):
        scope (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    measured_unit: Union[Unset, str] = UNSET
    category_title: Union[Unset, str] = UNSET
    category_uuid: Union[Unset, UUID] = UNSET
    date: Union[Unset, datetime.date] = UNSET
    reported_usage: Union[None, Unset, int] = UNSET
    fixed_usage: Union[None, Unset, int] = UNSET
    scope: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_

        measured_unit = self.measured_unit

        category_title = self.category_title

        category_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.category_uuid, Unset):
            category_uuid = str(self.category_uuid)

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        reported_usage: Union[None, Unset, int]
        if isinstance(self.reported_usage, Unset):
            reported_usage = UNSET
        else:
            reported_usage = self.reported_usage

        fixed_usage: Union[None, Unset, int]
        if isinstance(self.fixed_usage, Unset):
            fixed_usage = UNSET
        else:
            fixed_usage = self.fixed_usage

        scope = self.scope

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_
        if measured_unit is not UNSET:
            field_dict["measured_unit"] = measured_unit
        if category_title is not UNSET:
            field_dict["category_title"] = category_title
        if category_uuid is not UNSET:
            field_dict["category_uuid"] = category_uuid
        if date is not UNSET:
            field_dict["date"] = date
        if reported_usage is not UNSET:
            field_dict["reported_usage"] = reported_usage
        if fixed_usage is not UNSET:
            field_dict["fixed_usage"] = fixed_usage
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        type_ = d.pop("type", UNSET)

        measured_unit = d.pop("measured_unit", UNSET)

        category_title = d.pop("category_title", UNSET)

        _category_uuid = d.pop("category_uuid", UNSET)
        category_uuid: Union[Unset, UUID]
        if isinstance(_category_uuid, Unset):
            category_uuid = UNSET
        else:
            category_uuid = UUID(_category_uuid)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        def _parse_reported_usage(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        reported_usage = _parse_reported_usage(d.pop("reported_usage", UNSET))

        def _parse_fixed_usage(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        fixed_usage = _parse_fixed_usage(d.pop("fixed_usage", UNSET))

        scope = d.pop("scope", UNSET)

        category_component_usage = cls(
            name=name,
            type_=type_,
            measured_unit=measured_unit,
            category_title=category_title,
            category_uuid=category_uuid,
            date=date,
            reported_usage=reported_usage,
            fixed_usage=fixed_usage,
            scope=scope,
        )

        category_component_usage.additional_properties = d
        return category_component_usage

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
