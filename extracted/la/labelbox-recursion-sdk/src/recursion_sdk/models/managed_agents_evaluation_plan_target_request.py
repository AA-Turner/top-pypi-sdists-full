from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsEvaluationPlanTargetRequest")



@_attrs_define
class ManagedAgentsEvaluationPlanTargetRequest:
    """ One root target and the immutable transcript boundary frozen into an evaluation plan.

        Example:
            {'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            snapshot_event_id (UUID | Unset): Canonical event id at or before which the target transcript is frozen.
            target_session_id (UUID | Unset): Root session selected as an immutable evaluation target.
     """

    snapshot_event_id: UUID | Unset = UNSET
    target_session_id: UUID | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        snapshot_event_id: str | Unset = UNSET
        if not isinstance(self.snapshot_event_id, Unset):
            snapshot_event_id = str(self.snapshot_event_id)

        target_session_id: str | Unset = UNSET
        if not isinstance(self.target_session_id, Unset):
            target_session_id = str(self.target_session_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if snapshot_event_id is not UNSET:
            field_dict["snapshot_event_id"] = snapshot_event_id
        if target_session_id is not UNSET:
            field_dict["target_session_id"] = target_session_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _snapshot_event_id = d.pop("snapshot_event_id", UNSET)
        snapshot_event_id: UUID | Unset
        if isinstance(_snapshot_event_id,  Unset):
            snapshot_event_id = UNSET
        else:
            snapshot_event_id = UUID(_snapshot_event_id)




        _target_session_id = d.pop("target_session_id", UNSET)
        target_session_id: UUID | Unset
        if isinstance(_target_session_id,  Unset):
            target_session_id = UNSET
        else:
            target_session_id = UUID(_target_session_id)




        managed_agents_evaluation_plan_target_request = cls(
            snapshot_event_id=snapshot_event_id,
            target_session_id=target_session_id,
        )

        return managed_agents_evaluation_plan_target_request

