from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LiveKitTotals")


@_attrs_define
class LiveKitTotals:
    """
    Attributes:
        room_count (int):
        participant_count (int):
        publisher_count (int):
    """

    room_count: int
    participant_count: int
    publisher_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        room_count = self.room_count

        participant_count = self.participant_count

        publisher_count = self.publisher_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "room_count": room_count,
                "participant_count": participant_count,
                "publisher_count": publisher_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        room_count = d.pop("room_count")

        participant_count = d.pop("participant_count")

        publisher_count = d.pop("publisher_count")

        live_kit_totals = cls(
            room_count=room_count,
            participant_count=participant_count,
            publisher_count=publisher_count,
        )

        live_kit_totals.additional_properties = d
        return live_kit_totals

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
