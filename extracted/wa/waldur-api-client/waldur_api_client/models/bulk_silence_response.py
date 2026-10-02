from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkSilenceResponse")


@_attrs_define
class BulkSilenceResponse:
    """
    Attributes:
        status (str):
        count (int):
        duration_days (Union[None, Unset, int]):
    """

    status: str
    count: int
    duration_days: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        count = self.count

        duration_days: Union[None, Unset, int]
        if isinstance(self.duration_days, Unset):
            duration_days = UNSET
        else:
            duration_days = self.duration_days

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "count": count,
            }
        )
        if duration_days is not UNSET:
            field_dict["duration_days"] = duration_days

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = d.pop("status")

        count = d.pop("count")

        def _parse_duration_days(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        duration_days = _parse_duration_days(d.pop("duration_days", UNSET))

        bulk_silence_response = cls(
            status=status,
            count=count,
            duration_days=duration_days,
        )

        bulk_silence_response.additional_properties = d
        return bulk_silence_response

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
