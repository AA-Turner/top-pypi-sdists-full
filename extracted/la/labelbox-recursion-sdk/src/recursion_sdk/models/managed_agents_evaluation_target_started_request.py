from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_target_started_request_clone_state import ManagedAgentsEvaluationTargetStartedRequestCloneState
from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsEvaluationTargetStartedRequest")



@_attrs_define
class ManagedAgentsEvaluationTargetStartedRequest:
    """ Audit event payload linking one frozen target to its isolated evaluation child and reserved verdict identity.

        Example:
            {'child_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'clone_state': 'ready', 'evaluation_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandbox_provider': 'example', 'snapshot_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            child_session_id (UUID | Unset): Evaluation child session created for this target.
            clone_state (ManagedAgentsEvaluationTargetStartedRequestCloneState | Unset): Whether the child received a ready
                clone or needed no sandbox.
            evaluation_id (UUID | Unset): Immutable verdict identity reserved for this target.
            sandbox_provider (str | Unset): Provider of the isolated clone when the target has a sandbox.
            snapshot_event_id (UUID | Unset): Canonical event id bounding the immutable target transcript snapshot.
            target_session_id (UUID | Unset): Root session whose frozen snapshot is being evaluated.
     """

    child_session_id: UUID | Unset = UNSET
    clone_state: ManagedAgentsEvaluationTargetStartedRequestCloneState | Unset = UNSET
    evaluation_id: UUID | Unset = UNSET
    sandbox_provider: str | Unset = UNSET
    snapshot_event_id: UUID | Unset = UNSET
    target_session_id: UUID | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        child_session_id: str | Unset = UNSET
        if not isinstance(self.child_session_id, Unset):
            child_session_id = str(self.child_session_id)

        clone_state: str | Unset = UNSET
        if not isinstance(self.clone_state, Unset):
            clone_state = self.clone_state.value


        evaluation_id: str | Unset = UNSET
        if not isinstance(self.evaluation_id, Unset):
            evaluation_id = str(self.evaluation_id)

        sandbox_provider = self.sandbox_provider

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
        if clone_state is not UNSET:
            field_dict["clone_state"] = clone_state
        if evaluation_id is not UNSET:
            field_dict["evaluation_id"] = evaluation_id
        if sandbox_provider is not UNSET:
            field_dict["sandbox_provider"] = sandbox_provider
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




        _clone_state = d.pop("clone_state", UNSET)
        clone_state: ManagedAgentsEvaluationTargetStartedRequestCloneState | Unset
        if isinstance(_clone_state,  Unset):
            clone_state = UNSET
        else:
            clone_state = ManagedAgentsEvaluationTargetStartedRequestCloneState(_clone_state)




        _evaluation_id = d.pop("evaluation_id", UNSET)
        evaluation_id: UUID | Unset
        if isinstance(_evaluation_id,  Unset):
            evaluation_id = UNSET
        else:
            evaluation_id = UUID(_evaluation_id)




        sandbox_provider = d.pop("sandbox_provider", UNSET)

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




        managed_agents_evaluation_target_started_request = cls(
            child_session_id=child_session_id,
            clone_state=clone_state,
            evaluation_id=evaluation_id,
            sandbox_provider=sandbox_provider,
            snapshot_event_id=snapshot_event_id,
            target_session_id=target_session_id,
        )

        return managed_agents_evaluation_target_started_request

