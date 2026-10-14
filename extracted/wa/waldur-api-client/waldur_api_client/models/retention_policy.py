from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RetentionPolicy")


@_attrs_define
class RetentionPolicy:
    """
    Attributes:
        uuid (UUID):
        name (str):
        raw_days (Union[Unset, int]):
        hourly_days (Union[Unset, int]):
        daily_days (Union[None, Unset, int]): Empty keeps daily roll-ups forever.
    """

    uuid: UUID
    name: str
    raw_days: Union[Unset, int] = UNSET
    hourly_days: Union[Unset, int] = UNSET
    daily_days: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        raw_days = self.raw_days

        hourly_days = self.hourly_days

        daily_days: Union[None, Unset, int]
        if isinstance(self.daily_days, Unset):
            daily_days = UNSET
        else:
            daily_days = self.daily_days

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
            }
        )
        if raw_days is not UNSET:
            field_dict["raw_days"] = raw_days
        if hourly_days is not UNSET:
            field_dict["hourly_days"] = hourly_days
        if daily_days is not UNSET:
            field_dict["daily_days"] = daily_days

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        raw_days = d.pop("raw_days", UNSET)

        hourly_days = d.pop("hourly_days", UNSET)

        def _parse_daily_days(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        daily_days = _parse_daily_days(d.pop("daily_days", UNSET))

        retention_policy = cls(
            uuid=uuid,
            name=name,
            raw_days=raw_days,
            hourly_days=hourly_days,
            daily_days=daily_days,
        )

        retention_policy.additional_properties = d
        return retention_policy

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
