from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_target_skipped_reason_code import ManagedAgentsEvaluationTargetSkippedReasonCode
from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsEvaluationTargetSkipped")



@_attrs_define
class ManagedAgentsEvaluationTargetSkipped:
    """ Audit event payload for a target whose processing ended without a completed verdict audit.

        Example:
            {'child_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'reason': 'example', 'reason_code':
                'child_create_failed', 'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            reason (str): Sanitized operator-readable explanation of the skip.
            reason_code (ManagedAgentsEvaluationTargetSkippedReasonCode): Stable machine-readable classification of the
                skipped target.
            snapshot_event_id (UUID): Canonical transcript event boundary frozen for the skipped target.
            target_session_id (UUID): Root target whose processing ended without a completed verdict audit.
            child_session_id (UUID | Unset): Evaluation child identity when creation reached that stage.
     """

    reason: str
    reason_code: ManagedAgentsEvaluationTargetSkippedReasonCode
    snapshot_event_id: UUID
    target_session_id: UUID
    child_session_id: UUID | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        reason_code = self.reason_code.value

        snapshot_event_id = str(self.snapshot_event_id)

        target_session_id = str(self.target_session_id)

        child_session_id: str | Unset = UNSET
        if not isinstance(self.child_session_id, Unset):
            child_session_id = str(self.child_session_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "reason": reason,
            "reason_code": reason_code,
            "snapshot_event_id": snapshot_event_id,
            "target_session_id": target_session_id,
        })
        if child_session_id is not UNSET:
            field_dict["child_session_id"] = child_session_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = d.pop("reason")

        reason_code = ManagedAgentsEvaluationTargetSkippedReasonCode(d.pop("reason_code"))




        snapshot_event_id = UUID(d.pop("snapshot_event_id"))




        target_session_id = UUID(d.pop("target_session_id"))




        _child_session_id = d.pop("child_session_id", UNSET)
        child_session_id: UUID | Unset
        if isinstance(_child_session_id,  Unset):
            child_session_id = UNSET
        else:
            child_session_id = UUID(_child_session_id)




        managed_agents_evaluation_target_skipped = cls(
            reason=reason,
            reason_code=reason_code,
            snapshot_event_id=snapshot_event_id,
            target_session_id=target_session_id,
            child_session_id=child_session_id,
        )

        return managed_agents_evaluation_target_skipped

