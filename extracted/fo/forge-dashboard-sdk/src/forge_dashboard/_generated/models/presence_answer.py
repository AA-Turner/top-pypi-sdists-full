from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="PresenceAnswer")



@_attrs_define
class PresenceAnswer:
    """ 
        Attributes:
            heartbeat_seconds (int): How often a visible tab reports itself visible again.
            idle_after_seconds (int): How long a visible tab may go without input before it reports
                `visible: false`. 0 means the server's idle mode is off and the
                page never needs to.
     """

    heartbeat_seconds: int
    idle_after_seconds: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        heartbeat_seconds = self.heartbeat_seconds

        idle_after_seconds = self.idle_after_seconds


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "heartbeatSeconds": heartbeat_seconds,
            "idleAfterSeconds": idle_after_seconds,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        heartbeat_seconds = d.pop("heartbeatSeconds")

        idle_after_seconds = d.pop("idleAfterSeconds")

        presence_answer = cls(
            heartbeat_seconds=heartbeat_seconds,
            idle_after_seconds=idle_after_seconds,
        )


        presence_answer.additional_properties = d
        return presence_answer

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
