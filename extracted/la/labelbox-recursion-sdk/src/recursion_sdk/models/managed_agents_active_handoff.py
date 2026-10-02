from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_active_handoff_state import ManagedAgentsActiveHandoffState
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsActiveHandoff")



@_attrs_define
class ManagedAgentsActiveHandoff:
    """ Public, credential-free state of a browser handoff that is awaiting a person, currently driven by one, or being
    resolved back to the agent.

        Example:
            {'access_expires_at': '2026-02-18T09:30:00Z', 'deadline_at': '2026-02-18T09:30:00Z', 'handoff_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'reason': 'example', 'requested_at': '2026-02-18T09:30:00Z', 'state':
                'awaiting_user', 'wake_cause': 'example'}

        Attributes:
            deadline_at (datetime.datetime): When the handoff automatically expires and the agent resumes.
            handoff_id (str): Stable identifier for this browser handoff.
            reason (str): Why the agent asked a person to take over the shared browser.
            requested_at (datetime.datetime): When the agent requested the handoff.
            state (ManagedAgentsActiveHandoffState): Whether nobody has opened access yet, one person currently owns the
                display, or hand-back/deadline resolution is being delivered.
            access_expires_at (datetime.datetime | Unset): Latest time the current display access remains usable; never
                later than deadline_at.
            wake_cause (str | Unset): Resolution cause once resolved: user_handed_back, deadline_elapsed, cancelled, or
                interrupted.
     """

    deadline_at: datetime.datetime
    handoff_id: str
    reason: str
    requested_at: datetime.datetime
    state: ManagedAgentsActiveHandoffState
    access_expires_at: datetime.datetime | Unset = UNSET
    wake_cause: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        deadline_at = self.deadline_at.isoformat()

        handoff_id = self.handoff_id

        reason = self.reason

        requested_at = self.requested_at.isoformat()

        state = self.state.value

        access_expires_at: str | Unset = UNSET
        if not isinstance(self.access_expires_at, Unset):
            access_expires_at = self.access_expires_at.isoformat()

        wake_cause = self.wake_cause


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "deadline_at": deadline_at,
            "handoff_id": handoff_id,
            "reason": reason,
            "requested_at": requested_at,
            "state": state,
        })
        if access_expires_at is not UNSET:
            field_dict["access_expires_at"] = access_expires_at
        if wake_cause is not UNSET:
            field_dict["wake_cause"] = wake_cause

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        deadline_at = datetime.datetime.fromisoformat(d.pop("deadline_at"))




        handoff_id = d.pop("handoff_id")

        reason = d.pop("reason")

        requested_at = datetime.datetime.fromisoformat(d.pop("requested_at"))




        state = ManagedAgentsActiveHandoffState(d.pop("state"))




        _access_expires_at = d.pop("access_expires_at", UNSET)
        access_expires_at: datetime.datetime | Unset
        if isinstance(_access_expires_at,  Unset):
            access_expires_at = UNSET
        else:
            access_expires_at = datetime.datetime.fromisoformat(_access_expires_at)




        wake_cause = d.pop("wake_cause", UNSET)

        managed_agents_active_handoff = cls(
            deadline_at=deadline_at,
            handoff_id=handoff_id,
            reason=reason,
            requested_at=requested_at,
            state=state,
            access_expires_at=access_expires_at,
            wake_cause=wake_cause,
        )


        managed_agents_active_handoff.additional_properties = d
        return managed_agents_active_handoff

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
