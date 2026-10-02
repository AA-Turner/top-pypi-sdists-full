from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.live_kit_track import LiveKitTrack


T = TypeVar("T", bound="LiveKitParticipant")


@_attrs_define
class LiveKitParticipant:
    """
    Attributes:
        sid (str):
        identity (str):
        state (str):
        is_publisher (bool):
        joined_at (int):
        tracks (list['LiveKitTrack']):
    """

    sid: str
    identity: str
    state: str
    is_publisher: bool
    joined_at: int
    tracks: list["LiveKitTrack"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sid = self.sid

        identity = self.identity

        state = self.state

        is_publisher = self.is_publisher

        joined_at = self.joined_at

        tracks = []
        for tracks_item_data in self.tracks:
            tracks_item = tracks_item_data.to_dict()
            tracks.append(tracks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sid": sid,
                "identity": identity,
                "state": state,
                "is_publisher": is_publisher,
                "joined_at": joined_at,
                "tracks": tracks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.live_kit_track import LiveKitTrack

        d = dict(src_dict)
        sid = d.pop("sid")

        identity = d.pop("identity")

        state = d.pop("state")

        is_publisher = d.pop("is_publisher")

        joined_at = d.pop("joined_at")

        tracks = []
        _tracks = d.pop("tracks")
        for tracks_item_data in _tracks:
            tracks_item = LiveKitTrack.from_dict(tracks_item_data)

            tracks.append(tracks_item)

        live_kit_participant = cls(
            sid=sid,
            identity=identity,
            state=state,
            is_publisher=is_publisher,
            joined_at=joined_at,
            tracks=tracks,
        )

        live_kit_participant.additional_properties = d
        return live_kit_participant

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
