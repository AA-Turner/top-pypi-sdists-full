from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.guest_list_guests_item import GuestListGuestsItem
    from ..models.guest_list_usage import GuestListUsage


T = TypeVar("T", bound="GuestList")


@_attrs_define
class GuestList:
    """
    Attributes:
        usage (GuestListUsage): Guests are free up to `free_allowance` distinct emails over the trailing `window_days`.
            Past that an Enterprise plan meters them (`metered`, four guests to one seat: `billable_guests`, `guest_seats`);
            every other plan and build admits no new email until the count drops. `instance_enabled` is the superadmin
            switch (`guest_access_disabled` global setting) every workspace switch sits under.
        guests (List['GuestListGuestsItem']):
    """

    usage: "GuestListUsage"
    guests: List["GuestListGuestsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        usage = self.usage.to_dict()

        guests = []
        for guests_item_data in self.guests:
            guests_item = guests_item_data.to_dict()

            guests.append(guests_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "usage": usage,
                "guests": guests,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.guest_list_guests_item import GuestListGuestsItem
        from ..models.guest_list_usage import GuestListUsage

        d = src_dict.copy()
        usage = GuestListUsage.from_dict(d.pop("usage"))

        guests = []
        _guests = d.pop("guests")
        for guests_item_data in _guests:
            guests_item = GuestListGuestsItem.from_dict(guests_item_data)

            guests.append(guests_item)

        guest_list = cls(
            usage=usage,
            guests=guests,
        )

        guest_list.additional_properties = d
        return guest_list

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
