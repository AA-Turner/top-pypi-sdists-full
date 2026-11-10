import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.spending_limit_period_enum import SpendingLimitPeriodEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="SpendingLimitStatus")


@_attrs_define
class SpendingLimitStatus:
    """
    Attributes:
        component_type (Union[Unset, str]):
        period (Union[Unset, SpendingLimitPeriodEnum]):
        limit (Union[Unset, float]):
        used (Union[Unset, float]): Usage reported in the current period.
        resets_at (Union[None, Unset, datetime.datetime]): When the current period ends and its usage starts from zero.
            Null for total, which never resets.
        reached (Union[Unset, bool]):
        last_reported_at (Union[None, Unset, datetime.datetime]): When usage of the component was last reported.
    """

    component_type: Union[Unset, str] = UNSET
    period: Union[Unset, SpendingLimitPeriodEnum] = UNSET
    limit: Union[Unset, float] = UNSET
    used: Union[Unset, float] = UNSET
    resets_at: Union[None, Unset, datetime.datetime] = UNSET
    reached: Union[Unset, bool] = UNSET
    last_reported_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        component_type = self.component_type

        period: Union[Unset, str] = UNSET
        if not isinstance(self.period, Unset):
            period = self.period.value

        limit = self.limit

        used = self.used

        resets_at: Union[None, Unset, str]
        if isinstance(self.resets_at, Unset):
            resets_at = UNSET
        elif isinstance(self.resets_at, datetime.datetime):
            resets_at = self.resets_at.isoformat()
        else:
            resets_at = self.resets_at

        reached = self.reached

        last_reported_at: Union[None, Unset, str]
        if isinstance(self.last_reported_at, Unset):
            last_reported_at = UNSET
        elif isinstance(self.last_reported_at, datetime.datetime):
            last_reported_at = self.last_reported_at.isoformat()
        else:
            last_reported_at = self.last_reported_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if component_type is not UNSET:
            field_dict["component_type"] = component_type
        if period is not UNSET:
            field_dict["period"] = period
        if limit is not UNSET:
            field_dict["limit"] = limit
        if used is not UNSET:
            field_dict["used"] = used
        if resets_at is not UNSET:
            field_dict["resets_at"] = resets_at
        if reached is not UNSET:
            field_dict["reached"] = reached
        if last_reported_at is not UNSET:
            field_dict["last_reported_at"] = last_reported_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        component_type = d.pop("component_type", UNSET)

        _period = d.pop("period", UNSET)
        period: Union[Unset, SpendingLimitPeriodEnum]
        if isinstance(_period, Unset):
            period = UNSET
        else:
            period = SpendingLimitPeriodEnum(_period)

        limit = d.pop("limit", UNSET)

        used = d.pop("used", UNSET)

        def _parse_resets_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resets_at_type_0 = isoparse(data)

                return resets_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        resets_at = _parse_resets_at(d.pop("resets_at", UNSET))

        reached = d.pop("reached", UNSET)

        def _parse_last_reported_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_reported_at_type_0 = isoparse(data)

                return last_reported_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_reported_at = _parse_last_reported_at(d.pop("last_reported_at", UNSET))

        spending_limit_status = cls(
            component_type=component_type,
            period=period,
            limit=limit,
            used=used,
            resets_at=resets_at,
            reached=reached,
            last_reported_at=last_reported_at,
        )

        spending_limit_status.additional_properties = d
        return spending_limit_status

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
