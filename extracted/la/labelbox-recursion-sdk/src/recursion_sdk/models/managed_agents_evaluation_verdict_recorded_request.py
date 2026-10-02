from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_verdict_recorded_request_cost_completeness import ManagedAgentsEvaluationVerdictRecordedRequestCostCompleteness
from ..models.managed_agents_evaluation_verdict_recorded_request_result import ManagedAgentsEvaluationVerdictRecordedRequestResult
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsEvaluationVerdictRecordedRequest")



@_attrs_define
class ManagedAgentsEvaluationVerdictRecordedRequest:
    """ Audit event payload emitted after the authoritative immutable verdict and clone cost are recorded.

        Example:
            {'child_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'cost_completeness': 'complete', 'cost_usd':
                'example', 'evaluation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'failed_criterion_keys': ['example'],
                'result': 'pass', 'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            child_session_id (UUID | Unset): Evaluation child session that produced the verdict.
            cost_completeness (ManagedAgentsEvaluationVerdictRecordedRequestCostCompleteness | Unset): Whether every cost
                component is final and priced.
            cost_usd (str | Unset): Exact canonical decimal USD attributed to this evaluation.
            evaluation_id (UUID | Unset): Immutable evaluation row that remains authoritative.
            failed_criterion_keys (list[str] | Unset): Sorted unique rubric keys whose verdict is fail.
            result (ManagedAgentsEvaluationVerdictRecordedRequestResult | Unset): Overall verdict derived from the frozen
                criterion results.
            snapshot_event_id (UUID | Unset): Canonical event id bounding the transcript evidence considered.
            target_session_id (UUID | Unset): Root session evaluated by this immutable verdict.
     """

    child_session_id: UUID | Unset = UNSET
    cost_completeness: ManagedAgentsEvaluationVerdictRecordedRequestCostCompleteness | Unset = UNSET
    cost_usd: str | Unset = UNSET
    evaluation_id: UUID | Unset = UNSET
    failed_criterion_keys: list[str] | Unset = UNSET
    result: ManagedAgentsEvaluationVerdictRecordedRequestResult | Unset = UNSET
    snapshot_event_id: UUID | Unset = UNSET
    target_session_id: UUID | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        child_session_id: str | Unset = UNSET
        if not isinstance(self.child_session_id, Unset):
            child_session_id = str(self.child_session_id)

        cost_completeness: str | Unset = UNSET
        if not isinstance(self.cost_completeness, Unset):
            cost_completeness = self.cost_completeness.value


        cost_usd = self.cost_usd

        evaluation_id: str | Unset = UNSET
        if not isinstance(self.evaluation_id, Unset):
            evaluation_id = str(self.evaluation_id)

        failed_criterion_keys: list[str] | Unset = UNSET
        if not isinstance(self.failed_criterion_keys, Unset):
            failed_criterion_keys = self.failed_criterion_keys



        result: str | Unset = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.value


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
        if cost_completeness is not UNSET:
            field_dict["cost_completeness"] = cost_completeness
        if cost_usd is not UNSET:
            field_dict["cost_usd"] = cost_usd
        if evaluation_id is not UNSET:
            field_dict["evaluation_id"] = evaluation_id
        if failed_criterion_keys is not UNSET:
            field_dict["failed_criterion_keys"] = failed_criterion_keys
        if result is not UNSET:
            field_dict["result"] = result
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




        _cost_completeness = d.pop("cost_completeness", UNSET)
        cost_completeness: ManagedAgentsEvaluationVerdictRecordedRequestCostCompleteness | Unset
        if isinstance(_cost_completeness,  Unset):
            cost_completeness = UNSET
        else:
            cost_completeness = ManagedAgentsEvaluationVerdictRecordedRequestCostCompleteness(_cost_completeness)




        cost_usd = d.pop("cost_usd", UNSET)

        _evaluation_id = d.pop("evaluation_id", UNSET)
        evaluation_id: UUID | Unset
        if isinstance(_evaluation_id,  Unset):
            evaluation_id = UNSET
        else:
            evaluation_id = UUID(_evaluation_id)




        failed_criterion_keys = cast(list[str], d.pop("failed_criterion_keys", UNSET))


        _result = d.pop("result", UNSET)
        result: ManagedAgentsEvaluationVerdictRecordedRequestResult | Unset
        if isinstance(_result,  Unset):
            result = UNSET
        else:
            result = ManagedAgentsEvaluationVerdictRecordedRequestResult(_result)




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




        managed_agents_evaluation_verdict_recorded_request = cls(
            child_session_id=child_session_id,
            cost_completeness=cost_completeness,
            cost_usd=cost_usd,
            evaluation_id=evaluation_id,
            failed_criterion_keys=failed_criterion_keys,
            result=result,
            snapshot_event_id=snapshot_event_id,
            target_session_id=target_session_id,
        )

        return managed_agents_evaluation_verdict_recorded_request

