from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_target_skipped_request_reason_code import ManagedAgentsEvaluationTargetSkippedRequestReasonCode
from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsEvaluationTargetSkippedRequest")



@_attrs_define
class ManagedAgentsEvaluationTargetSkippedRequest:
    """ Audit event payload for a target whose processing ended without a completed verdict audit.

        Example:
            {'child_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'reason': 'example', 'reason_code':
                'child_create_failed', 'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            child_session_id (UUID | Unset): Evaluation child identity when creation reached that stage.
            reason (str | Unset): Sanitized operator-readable explanation of the skip.
            reason_code (ManagedAgentsEvaluationTargetSkippedRequestReasonCode | Unset): Stable machine-readable
                classification of the skipped target.
            snapshot_event_id (UUID | Unset): Canonical transcript event boundary frozen for the skipped target.
            target_session_id (UUID | Unset): Root target whose processing ended without a completed verdict audit.
     """

    child_session_id: UUID | Unset = UNSET
    reason: str | Unset = UNSET
    reason_code: ManagedAgentsEvaluationTargetSkippedRequestReasonCode | Unset = UNSET
    snapshot_event_id: UUID | Unset = UNSET
    target_session_id: UUID | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        child_session_id: str | Unset = UNSET
        if not isinstance(self.child_session_id, Unset):
            child_session_id = str(self.child_session_id)

        reason = self.reason

        reason_code: str | Unset = UNSET
        if not isinstance(self.reason_code, Unset):
            reason_code = self.reason_code.value


        snapshot_event_id: str | Unset = UNSET
        if not isinstance(self.snapshot_event_id, Unset):
            snapshot_event_id = str(self.snapshot_event_id)

        target_session_id: str | Unset = UNSET
        if not isinstance(self.target_session_id, Unset):
            target_session_id = str(self.target_session_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if child_session_id is not UNSET:
            field_dict["child_session_id"] = child_session_id
        if reason is not UNSET:
            field_dict["reason"] = reason
        if reason_code is not UNSET:
            field_dict["reason_code"] = reason_code
        if snapshot_event_id is not UNSET:
            field_dict["snapshot_event_id"] = snapshot_event_id
        if target_session_id is not UNSET:
            field_dict["target_session_id"] = target_session_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _child_session_id = d.pop("child_session_id", UNSET)
        child_session_id: UUID | Unset
        if isinstance(_child_session_id,  Unset):
            child_session_id = UNSET
        else:
            child_session_id = UUID(_child_session_id)




        reason = d.pop("reason", UNSET)

        _reason_code = d.pop("reason_code", UNSET)
        reason_code: ManagedAgentsEvaluationTargetSkippedRequestReasonCode | Unset
        if isinstance(_reason_code,  Unset):
            reason_code = UNSET
        else:
            reason_code = ManagedAgentsEvaluationTargetSkippedRequestReasonCode(_reason_code)




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




        managed_agents_evaluation_target_skipped_request = cls(
            child_session_id=child_session_id,
            reason=reason,
            reason_code=reason_code,
            snapshot_event_id=snapshot_event_id,
            target_session_id=target_session_id,
        )

        return managed_agents_evaluation_target_skipped_request

