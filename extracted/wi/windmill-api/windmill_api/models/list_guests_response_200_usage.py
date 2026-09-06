from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListGuestsResponse200Usage")


@_attrs_define
class ListGuestsResponse200Usage:
    """Guests are free up to `free_allowance` distinct emails over the trailing `window_days`. Past that an Enterprise plan
    meters them (`metered`, four guests to one seat: `billable_guests`, `guest_seats`); every other plan and build
    admits no new email until the count drops. `instance_enabled` is the superadmin switch (`guest_access_disabled`
    global setting) every workspace switch sits under.

        Attributes:
            instance_enabled (bool):
            guest_count (int):
            window_days (int):
            free_allowance (int):
            metered (bool):
            billable_guests (int):
            guest_seats (int):
    """

    instance_enabled: bool
    guest_count: int
    window_days: int
    free_allowance: int
    metered: bool
    billable_guests: int
    guest_seats: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        instance_enabled = self.instance_enabled
        guest_count = self.guest_count
        window_days = self.window_days
        free_allowance = self.free_allowance
        metered = self.metered
        billable_guests = self.billable_guests
        guest_seats = self.guest_seats

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "instance_enabled": instance_enabled,
                "guest_count": guest_count,
                "window_days": window_days,
                "free_allowance": free_allowance,
                "metered": metered,
                "billable_guests": billable_guests,
                "guest_seats": guest_seats,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        instance_enabled = d.pop("instance_enabled")

        guest_count = d.pop("guest_count")

        window_days = d.pop("window_days")

        free_allowance = d.pop("free_allowance")

        metered = d.pop("metered")

        billable_guests = d.pop("billable_guests")

        guest_seats = d.pop("guest_seats")

        list_guests_response_200_usage = cls(
            instance_enabled=instance_enabled,
            guest_count=guest_count,
            window_days=window_days,
            free_allowance=free_allowance,
            metered=metered,
            billable_guests=billable_guests,
            guest_seats=guest_seats,
        )

        list_guests_response_200_usage.additional_properties = d
        return list_guests_response_200_usage

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
