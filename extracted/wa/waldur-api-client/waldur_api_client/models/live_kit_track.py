from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LiveKitTrack")


@_attrs_define
class LiveKitTrack:
    """
    Attributes:
        sid (str):
        name (str):
        type_ (str):
        muted (bool):
        width (int):
        height (int):
    """

    sid: str
    name: str
    type_: str
    muted: bool
    width: int
    height: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sid = self.sid

        name = self.name

        type_ = self.type_

        muted = self.muted

        width = self.width

        height = self.height

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sid": sid,
                "name": name,
                "type": type_,
                "muted": muted,
                "width": width,
                "height": height,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sid = d.pop("sid")

        name = d.pop("name")

        type_ = d.pop("type")

        muted = d.pop("muted")

        width = d.pop("width")

        height = d.pop("height")

        live_kit_track = cls(
            sid=sid,
            name=name,
            type_=type_,
            muted=muted,
            width=width,
            height=height,
        )

        live_kit_track.additional_properties = d
        return live_kit_track

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
