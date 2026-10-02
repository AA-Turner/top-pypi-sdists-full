from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LiveKitRoomSummary")


@_attrs_define
class LiveKitRoomSummary:
    """
    Attributes:
        sid (str):
        name (str):
        num_participants (int):
        num_publishers (int):
        creation_time (int):
        max_participants (int):
        metadata (str):
    """

    sid: str
    name: str
    num_participants: int
    num_publishers: int
    creation_time: int
    max_participants: int
    metadata: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sid = self.sid

        name = self.name

        num_participants = self.num_participants

        num_publishers = self.num_publishers

        creation_time = self.creation_time

        max_participants = self.max_participants

        metadata = self.metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sid": sid,
                "name": name,
                "num_participants": num_participants,
                "num_publishers": num_publishers,
                "creation_time": creation_time,
                "max_participants": max_participants,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sid = d.pop("sid")

        name = d.pop("name")

        num_participants = d.pop("num_participants")

        num_publishers = d.pop("num_publishers")

        creation_time = d.pop("creation_time")

        max_participants = d.pop("max_participants")

        metadata = d.pop("metadata")

        live_kit_room_summary = cls(
            sid=sid,
            name=name,
            num_participants=num_participants,
            num_publishers=num_publishers,
            creation_time=creation_time,
            max_participants=max_participants,
            metadata=metadata,
        )

        live_kit_room_summary.additional_properties = d
        return live_kit_room_summary

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
