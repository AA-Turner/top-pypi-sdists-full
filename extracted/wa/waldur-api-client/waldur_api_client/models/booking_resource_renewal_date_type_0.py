import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="BookingResourceRenewalDateType0")


@_attrs_define
class BookingResourceRenewalDateType0:
    """ """

    additional_properties: dict[str, datetime.date] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.isoformat()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        booking_resource_renewal_date_type_0 = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = isoparse(prop_dict).date()

            additional_properties[prop_name] = additional_property

        booking_resource_renewal_date_type_0.additional_properties = additional_properties
        return booking_resource_renewal_date_type_0

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> datetime.date:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: datetime.date) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
