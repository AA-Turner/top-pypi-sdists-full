from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.live_kit_room_summary import LiveKitRoomSummary
    from ..models.live_kit_totals import LiveKitTotals


T = TypeVar("T", bound="LiveKitOverviewResponse")


@_attrs_define
class LiveKitOverviewResponse:
    """
    Attributes:
        rooms (list['LiveKitRoomSummary']):
        totals (LiveKitTotals):
        livekit_url (str):
    """

    rooms: list["LiveKitRoomSummary"]
    totals: "LiveKitTotals"
    livekit_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rooms = []
        for rooms_item_data in self.rooms:
            rooms_item = rooms_item_data.to_dict()
            rooms.append(rooms_item)

        totals = self.totals.to_dict()

        livekit_url = self.livekit_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rooms": rooms,
                "totals": totals,
                "livekit_url": livekit_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.live_kit_room_summary import LiveKitRoomSummary
        from ..models.live_kit_totals import LiveKitTotals

        d = dict(src_dict)
        rooms = []
        _rooms = d.pop("rooms")
        for rooms_item_data in _rooms:
            rooms_item = LiveKitRoomSummary.from_dict(rooms_item_data)

            rooms.append(rooms_item)

        totals = LiveKitTotals.from_dict(d.pop("totals"))

        livekit_url = d.pop("livekit_url")

        live_kit_overview_response = cls(
            rooms=rooms,
            totals=totals,
            livekit_url=livekit_url,
        )

        live_kit_overview_response.additional_properties = d
        return live_kit_overview_response

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
