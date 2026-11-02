from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.update_request_phase import UpdateRequestPhase
from typing import cast
import datetime






T = TypeVar("T", bound="UpdateRequest")



@_attrs_define
class UpdateRequest:
    """ 
        Attributes:
            phase (UpdateRequestPhase): `queued`: accepted, and the pull request is still behind.
                `expired`: still behind after 5 minutes. An expired request stays
                until the pull request is gone, a new request replaces it, or an
                hour passes.
            requested_at (datetime.datetime):
            expires_at (datetime.datetime): When the server stops waiting in the current phase: 5 minutes
                after the request while `queued`.
     """

    phase: UpdateRequestPhase
    requested_at: datetime.datetime
    expires_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        phase = self.phase.value

        requested_at = self.requested_at.isoformat()

        expires_at = self.expires_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "phase": phase,
            "requestedAt": requested_at,
            "expiresAt": expires_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        phase = UpdateRequestPhase(d.pop("phase"))




        requested_at = datetime.datetime.fromisoformat(d.pop("requestedAt"))




        expires_at = datetime.datetime.fromisoformat(d.pop("expiresAt"))




        update_request = cls(
            phase=phase,
            requested_at=requested_at,
            expires_at=expires_at,
        )


        update_request.additional_properties = d
        return update_request

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
