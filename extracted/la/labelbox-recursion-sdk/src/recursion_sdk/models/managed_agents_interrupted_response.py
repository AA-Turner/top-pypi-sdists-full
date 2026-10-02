from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsInterruptedResponse")



@_attrs_define
class ManagedAgentsInterruptedResponse:
    """ Response body of POST /v1/sessions/{session_id}/interrupt. An interrupt is a cooperative control, not a session
    cancellation: the session stays alive and keeps accepting events. Use POST /v1/sessions/{session_id}/cancel to stop
    it.

        Example:
            {'interrupted': True, 'temporal_signaled': True}

        Attributes:
            interrupted (bool): True when the interrupt reached a live workflow and a running operation was told to stop.
                False means the request was accepted and the stop recorded, but nothing running was confirmed interrupted --
                typically a session whose workflow had already finished.
            temporal_signaled (bool): Compatibility alias of interrupted, carrying the same value on every response. It
                predates interrupted reporting whether anything was actually reached, and is kept so existing callers keep
                working; read interrupted instead.
     """

    interrupted: bool
    temporal_signaled: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        interrupted = self.interrupted

        temporal_signaled = self.temporal_signaled


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "interrupted": interrupted,
            "temporal_signaled": temporal_signaled,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        interrupted = d.pop("interrupted")

        temporal_signaled = d.pop("temporal_signaled")

        managed_agents_interrupted_response = cls(
            interrupted=interrupted,
            temporal_signaled=temporal_signaled,
        )


        managed_agents_interrupted_response.additional_properties = d
        return managed_agents_interrupted_response

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
