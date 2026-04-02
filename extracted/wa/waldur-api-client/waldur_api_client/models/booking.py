import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="Booking")


@_attrs_define
class Booking:
    """
    Attributes:
        created_by_full_name (Union[None, str]):
        start (datetime.datetime):
        end (datetime.datetime):
    """

    created_by_full_name: Union[None, str]
    start: datetime.datetime
    end: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_by_full_name: Union[None, str]
        created_by_full_name = self.created_by_full_name

        start = self.start.isoformat()

        end = self.end.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_by_full_name": created_by_full_name,
                "start": start,
                "end": end,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_created_by_full_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        created_by_full_name = _parse_created_by_full_name(d.pop("created_by_full_name"))

        start = isoparse(d.pop("start"))

        end = isoparse(d.pop("end"))

        booking = cls(
            created_by_full_name=created_by_full_name,
            start=start,
            end=end,
        )

        booking.additional_properties = d
        return booking

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
