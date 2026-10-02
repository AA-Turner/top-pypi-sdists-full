from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetTokenQuotaRequest")


@_attrs_define
class SetTokenQuotaRequest:
    """
    Attributes:
        user_uuid (UUID): UUID of the user to set quota for.
        daily_limit (Union[None, Unset, int]): Daily token limit. Omit or null = system default, -1 = unlimited.
        weekly_limit (Union[None, Unset, int]): Weekly token limit. Omit or null = system default, -1 = unlimited.
        monthly_limit (Union[None, Unset, int]): Monthly token limit. Omit or null = system default, -1 = unlimited.
    """

    user_uuid: UUID
    daily_limit: Union[None, Unset, int] = UNSET
    weekly_limit: Union[None, Unset, int] = UNSET
    monthly_limit: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_uuid = str(self.user_uuid)

        daily_limit: Union[None, Unset, int]
        if isinstance(self.daily_limit, Unset):
            daily_limit = UNSET
        else:
            daily_limit = self.daily_limit

        weekly_limit: Union[None, Unset, int]
        if isinstance(self.weekly_limit, Unset):
            weekly_limit = UNSET
        else:
            weekly_limit = self.weekly_limit

        monthly_limit: Union[None, Unset, int]
        if isinstance(self.monthly_limit, Unset):
            monthly_limit = UNSET
        else:
            monthly_limit = self.monthly_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_uuid": user_uuid,
            }
        )
        if daily_limit is not UNSET:
            field_dict["daily_limit"] = daily_limit
        if weekly_limit is not UNSET:
            field_dict["weekly_limit"] = weekly_limit
        if monthly_limit is not UNSET:
            field_dict["monthly_limit"] = monthly_limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_uuid = UUID(d.pop("user_uuid"))

        def _parse_daily_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        daily_limit = _parse_daily_limit(d.pop("daily_limit", UNSET))

        def _parse_weekly_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        weekly_limit = _parse_weekly_limit(d.pop("weekly_limit", UNSET))

        def _parse_monthly_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        monthly_limit = _parse_monthly_limit(d.pop("monthly_limit", UNSET))

        set_token_quota_request = cls(
            user_uuid=user_uuid,
            daily_limit=daily_limit,
            weekly_limit=weekly_limit,
            monthly_limit=monthly_limit,
        )

        set_token_quota_request.additional_properties = d
        return set_token_quota_request

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
