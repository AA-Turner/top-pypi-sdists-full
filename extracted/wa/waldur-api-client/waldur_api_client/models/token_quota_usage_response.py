import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TokenQuotaUsageResponse")


@_attrs_define
class TokenQuotaUsageResponse:
    """
    Attributes:
        daily_remaining (Union[None, int]): Get remaining daily tokens.
        daily_reset_at (datetime.datetime): Calculate next midnight (00:00:00).
        daily_system_default (int): Get system default daily token limit from constance config.
        weekly_remaining (Union[None, int]): Get remaining weekly tokens.
        weekly_reset_at (datetime.datetime): Calculate next Monday at midnight.
        weekly_system_default (int): Get system default weekly token limit from constance config.
        monthly_remaining (Union[None, int]): Get remaining monthly tokens.
        monthly_reset_at (datetime.datetime): Calculate first day of next month at midnight.
        monthly_system_default (int): Get system default monthly token limit from constance config.
        daily_limit (Union[None, Unset, int]): Daily token limit (non-negative integer). Null uses system default. -1
            means unlimited.
        daily_usage (Union[Unset, int]):
        weekly_limit (Union[None, Unset, int]): Weekly token limit (non-negative integer). Null uses system default. -1
            means unlimited.
        weekly_usage (Union[Unset, int]):
        monthly_limit (Union[None, Unset, int]): Monthly token limit (non-negative integer). Null uses system default.
            -1 means unlimited.
        monthly_usage (Union[Unset, int]):
    """

    daily_remaining: Union[None, int]
    daily_reset_at: datetime.datetime
    daily_system_default: int
    weekly_remaining: Union[None, int]
    weekly_reset_at: datetime.datetime
    weekly_system_default: int
    monthly_remaining: Union[None, int]
    monthly_reset_at: datetime.datetime
    monthly_system_default: int
    daily_limit: Union[None, Unset, int] = UNSET
    daily_usage: Union[Unset, int] = UNSET
    weekly_limit: Union[None, Unset, int] = UNSET
    weekly_usage: Union[Unset, int] = UNSET
    monthly_limit: Union[None, Unset, int] = UNSET
    monthly_usage: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        daily_remaining: Union[None, int]
        daily_remaining = self.daily_remaining

        daily_reset_at = self.daily_reset_at.isoformat()

        daily_system_default = self.daily_system_default

        weekly_remaining: Union[None, int]
        weekly_remaining = self.weekly_remaining

        weekly_reset_at = self.weekly_reset_at.isoformat()

        weekly_system_default = self.weekly_system_default

        monthly_remaining: Union[None, int]
        monthly_remaining = self.monthly_remaining

        monthly_reset_at = self.monthly_reset_at.isoformat()

        monthly_system_default = self.monthly_system_default

        daily_limit: Union[None, Unset, int]
        if isinstance(self.daily_limit, Unset):
            daily_limit = UNSET
        else:
            daily_limit = self.daily_limit

        daily_usage = self.daily_usage

        weekly_limit: Union[None, Unset, int]
        if isinstance(self.weekly_limit, Unset):
            weekly_limit = UNSET
        else:
            weekly_limit = self.weekly_limit

        weekly_usage = self.weekly_usage

        monthly_limit: Union[None, Unset, int]
        if isinstance(self.monthly_limit, Unset):
            monthly_limit = UNSET
        else:
            monthly_limit = self.monthly_limit

        monthly_usage = self.monthly_usage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "daily_remaining": daily_remaining,
                "daily_reset_at": daily_reset_at,
                "daily_system_default": daily_system_default,
                "weekly_remaining": weekly_remaining,
                "weekly_reset_at": weekly_reset_at,
                "weekly_system_default": weekly_system_default,
                "monthly_remaining": monthly_remaining,
                "monthly_reset_at": monthly_reset_at,
                "monthly_system_default": monthly_system_default,
            }
        )
        if daily_limit is not UNSET:
            field_dict["daily_limit"] = daily_limit
        if daily_usage is not UNSET:
            field_dict["daily_usage"] = daily_usage
        if weekly_limit is not UNSET:
            field_dict["weekly_limit"] = weekly_limit
        if weekly_usage is not UNSET:
            field_dict["weekly_usage"] = weekly_usage
        if monthly_limit is not UNSET:
            field_dict["monthly_limit"] = monthly_limit
        if monthly_usage is not UNSET:
            field_dict["monthly_usage"] = monthly_usage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_daily_remaining(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        daily_remaining = _parse_daily_remaining(d.pop("daily_remaining"))

        daily_reset_at = isoparse(d.pop("daily_reset_at"))

        daily_system_default = d.pop("daily_system_default")

        def _parse_weekly_remaining(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        weekly_remaining = _parse_weekly_remaining(d.pop("weekly_remaining"))

        weekly_reset_at = isoparse(d.pop("weekly_reset_at"))

        weekly_system_default = d.pop("weekly_system_default")

        def _parse_monthly_remaining(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        monthly_remaining = _parse_monthly_remaining(d.pop("monthly_remaining"))

        monthly_reset_at = isoparse(d.pop("monthly_reset_at"))

        monthly_system_default = d.pop("monthly_system_default")

        def _parse_daily_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        daily_limit = _parse_daily_limit(d.pop("daily_limit", UNSET))

        daily_usage = d.pop("daily_usage", UNSET)

        def _parse_weekly_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        weekly_limit = _parse_weekly_limit(d.pop("weekly_limit", UNSET))

        weekly_usage = d.pop("weekly_usage", UNSET)

        def _parse_monthly_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        monthly_limit = _parse_monthly_limit(d.pop("monthly_limit", UNSET))

        monthly_usage = d.pop("monthly_usage", UNSET)

        token_quota_usage_response = cls(
            daily_remaining=daily_remaining,
            daily_reset_at=daily_reset_at,
            daily_system_default=daily_system_default,
            weekly_remaining=weekly_remaining,
            weekly_reset_at=weekly_reset_at,
            weekly_system_default=weekly_system_default,
            monthly_remaining=monthly_remaining,
            monthly_reset_at=monthly_reset_at,
            monthly_system_default=monthly_system_default,
            daily_limit=daily_limit,
            daily_usage=daily_usage,
            weekly_limit=weekly_limit,
            weekly_usage=weekly_usage,
            monthly_limit=monthly_limit,
            monthly_usage=monthly_usage,
        )

        token_quota_usage_response.additional_properties = d
        return token_quota_usage_response

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
