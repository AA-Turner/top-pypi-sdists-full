from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_target_started_clone_state import ManagedAgentsEvaluationTargetStartedCloneState
from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsEvaluationTargetStarted")



@_attrs_define
class ManagedAgentsEvaluationTargetStarted:
    """ Audit event payload linking one frozen target to its isolated evaluation child and reserved verdict identity.

        Example:
            {'child_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'clone_state': 'ready', 'evaluation_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandbox_provider': 'example', 'snapshot_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            child_session_id (UUID): Evaluation child session created for this target.
            clone_state (ManagedAgentsEvaluationTargetStartedCloneState): Whether the child received a ready clone or needed
                no sandbox.
            evaluation_id (UUID): Immutable verdict identity reserved for this target.
            snapshot_event_id (UUID): Canonical event id bounding the immutable target transcript snapshot.
            target_session_id (UUID): Root session whose frozen snapshot is being evaluated.
            sandbox_provider (str | Unset): Provider of the isolated clone when the target has a sandbox.
     """

    child_session_id: UUID
    clone_state: ManagedAgentsEvaluationTargetStartedCloneState
    evaluation_id: UUID
    snapshot_event_id: UUID
    target_session_id: UUID
    sandbox_provider: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        child_session_id = str(self.child_session_id)

        clone_state = self.clone_state.value

        evaluation_id = str(self.evaluation_id)

        snapshot_event_id = str(self.snapshot_event_id)

        target_session_id = str(self.target_session_id)

        sandbox_provider = self.sandbox_provider


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "child_session_id": child_session_id,
            "clone_state": clone_state,
            "evaluation_id": evaluation_id,
            "snapshot_event_id": snapshot_event_id,
            "target_session_id": target_session_id,
        })
        if sandbox_provider is not UNSET:
            field_dict["sandbox_provider"] = sandbox_provider

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        child_session_id = UUID(d.pop("child_session_id"))




        clone_state = ManagedAgentsEvaluationTargetStartedCloneState(d.pop("clone_state"))




        evaluation_id = UUID(d.pop("evaluation_id"))




        snapshot_event_id = UUID(d.pop("snapshot_event_id"))




        target_session_id = UUID(d.pop("target_session_id"))




        sandbox_provider = d.pop("sandbox_provider", UNSET)

        managed_agents_evaluation_target_started = cls(
            child_session_id=child_session_id,
            clone_state=clone_state,
            evaluation_id=evaluation_id,
            snapshot_event_id=snapshot_event_id,
            target_session_id=target_session_id,
            sandbox_provider=sandbox_provider,
        )

        return managed_agents_evaluation_target_started

