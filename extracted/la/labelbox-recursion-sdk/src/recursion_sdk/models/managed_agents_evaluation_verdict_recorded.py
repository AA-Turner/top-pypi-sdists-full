from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_verdict_recorded_cost_completeness import ManagedAgentsEvaluationVerdictRecordedCostCompleteness
from ..models.managed_agents_evaluation_verdict_recorded_result import ManagedAgentsEvaluationVerdictRecordedResult
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsEvaluationVerdictRecorded")



@_attrs_define
class ManagedAgentsEvaluationVerdictRecorded:
    """ Audit event payload emitted after the authoritative immutable verdict and clone cost are recorded.

        Example:
            {'child_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'cost_completeness': 'complete', 'cost_usd':
                'example', 'evaluation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'failed_criterion_keys': ['example'],
                'result': 'pass', 'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            child_session_id (UUID): Evaluation child session that produced the verdict.
            cost_completeness (ManagedAgentsEvaluationVerdictRecordedCostCompleteness): Whether every cost component is
                final and priced.
            cost_usd (str): Exact canonical decimal USD attributed to this evaluation.
            evaluation_id (UUID): Immutable evaluation row that remains authoritative.
            failed_criterion_keys (list[str]): Sorted unique rubric keys whose verdict is fail.
            result (ManagedAgentsEvaluationVerdictRecordedResult): Overall verdict derived from the frozen criterion
                results.
            snapshot_event_id (UUID): Canonical event id bounding the transcript evidence considered.
            target_session_id (UUID): Root session evaluated by this immutable verdict.
     """

    child_session_id: UUID
    cost_completeness: ManagedAgentsEvaluationVerdictRecordedCostCompleteness
    cost_usd: str
    evaluation_id: UUID
    failed_criterion_keys: list[str]
    result: ManagedAgentsEvaluationVerdictRecordedResult
    snapshot_event_id: UUID
    target_session_id: UUID





    def to_dict(self) -> dict[str, Any]:
        child_session_id = str(self.child_session_id)

        cost_completeness = self.cost_completeness.value

        cost_usd = self.cost_usd

        evaluation_id = str(self.evaluation_id)

        failed_criterion_keys = self.failed_criterion_keys



        result = self.result.value

        snapshot_event_id = str(self.snapshot_event_id)

        target_session_id = str(self.target_session_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "child_session_id": child_session_id,
            "cost_completeness": cost_completeness,
            "cost_usd": cost_usd,
            "evaluation_id": evaluation_id,
            "failed_criterion_keys": failed_criterion_keys,
            "result": result,
            "snapshot_event_id": snapshot_event_id,
            "target_session_id": target_session_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        child_session_id = UUID(d.pop("child_session_id"))




        cost_completeness = ManagedAgentsEvaluationVerdictRecordedCostCompleteness(d.pop("cost_completeness"))




        cost_usd = d.pop("cost_usd")

        evaluation_id = UUID(d.pop("evaluation_id"))




        failed_criterion_keys = cast(list[str], d.pop("failed_criterion_keys"))


        result = ManagedAgentsEvaluationVerdictRecordedResult(d.pop("result"))




        snapshot_event_id = UUID(d.pop("snapshot_event_id"))




        target_session_id = UUID(d.pop("target_session_id"))




        managed_agents_evaluation_verdict_recorded = cls(
            child_session_id=child_session_id,
            cost_completeness=cost_completeness,
            cost_usd=cost_usd,
            evaluation_id=evaluation_id,
            failed_criterion_keys=failed_criterion_keys,
            result=result,
            snapshot_event_id=snapshot_event_id,
            target_session_id=target_session_id,
        )

        return managed_agents_evaluation_verdict_recorded

