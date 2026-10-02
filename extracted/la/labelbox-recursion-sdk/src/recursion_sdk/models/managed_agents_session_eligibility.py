from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_session_eligibility_reason import ManagedAgentsSessionEligibilityReason
from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsSessionEligibility")



@_attrs_define
class ManagedAgentsSessionEligibility:
    """ Current domain-owned Evaluate-now decision and immutable transcript snapshot boundary for one session.

        Example:
            {'eligible': True, 'reason': 'not_root', 'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            eligible (bool): Whether this session may be selected for Evaluate now.
            reason (ManagedAgentsSessionEligibilityReason | Unset): Stable reason the session is currently ineligible;
                omitted when eligible.
            snapshot_event_id (UUID | Unset): Newest durable canonical UUID event boundary frozen if evaluation starts now.
     """

    eligible: bool
    reason: ManagedAgentsSessionEligibilityReason | Unset = UNSET
    snapshot_event_id: UUID | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        eligible = self.eligible

        reason: str | Unset = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.value


        snapshot_event_id: str | Unset = UNSET
        if not isinstance(self.snapshot_event_id, Unset):
            snapshot_event_id = str(self.snapshot_event_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "eligible": eligible,
        })
        if reason is not UNSET:
            field_dict["reason"] = reason
        if snapshot_event_id is not UNSET:
            field_dict["snapshot_event_id"] = snapshot_event_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        eligible = d.pop("eligible")

        _reason = d.pop("reason", UNSET)
        reason: ManagedAgentsSessionEligibilityReason | Unset
        if isinstance(_reason,  Unset):
            reason = UNSET
        else:
            reason = ManagedAgentsSessionEligibilityReason(_reason)




        _snapshot_event_id = d.pop("snapshot_event_id", UNSET)
        snapshot_event_id: UUID | Unset
        if isinstance(_snapshot_event_id,  Unset):
            snapshot_event_id = UNSET
        else:
            snapshot_event_id = UUID(_snapshot_event_id)




        managed_agents_session_eligibility = cls(
            eligible=eligible,
            reason=reason,
            snapshot_event_id=snapshot_event_id,
        )

        return managed_agents_session_eligibility

