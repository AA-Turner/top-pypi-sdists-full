from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_archetype import ManagedAgentsEvaluationArchetype
from ..models.managed_agents_evaluation_failure_class import ManagedAgentsEvaluationFailureClass
from ..models.managed_agents_evaluation_result import ManagedAgentsEvaluationResult
from ..models.managed_agents_evaluation_size_bucket import ManagedAgentsEvaluationSizeBucket
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_evaluation_criterion import ManagedAgentsEvaluationCriterion





T = TypeVar("T", bound="ManagedAgentsEvaluation")



@_attrs_define
class ManagedAgentsEvaluation:
    """ One immutable evaluator verdict over a frozen target-session transcript snapshot.

        Example:
            {'archetype': 'artifact', 'child_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at':
                '2026-02-18T09:30:00Z', 'criteria': [{'criterion_key': 'example', 'evidence_event_ids':
                ['9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'], 'rationale': 'example', 'verdict': 'pass'}], 'evaluation_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'evaluator_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'evaluator_agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'failure_class': 'none', 'result': 'pass',
                'run_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'size_bucket': 'unknown', 'snapshot_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'summary': 'example', 'target_agent_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            archetype (ManagedAgentsEvaluationArchetype): Evaluator-classified shape of the target work.
            child_session_id (UUID): Evaluation child session that inspected this target snapshot.
            created_at (datetime.datetime): UTC timestamp when the immutable evaluation row was recorded.
            criteria (list[ManagedAgentsEvaluationCriterion]): Key-sorted immutable criterion verdicts and their evidence.
            evaluation_id (UUID): Stable identity of this immutable evaluation snapshot.
            evaluator_agent_id (UUID): Evaluation agent that produced this verdict.
            evaluator_agent_version_id (UUID): Immutable evaluator version containing the frozen rubric.
            failure_class (ManagedAgentsEvaluationFailureClass): Stable reason class when the overall result is not a pass.
            result (ManagedAgentsEvaluationResult): Overall verdict across the frozen rubric criteria.
            run_session_id (UUID): Platform-internal root session coordinating the evaluation run.
            size_bucket (ManagedAgentsEvaluationSizeBucket): Evaluator-classified relative size of the target work.
            snapshot_event_id (UUID): Canonical UUID transcript boundary; may be a current UUIDv7 or a retained legacy
                UUIDv4 event id.
            summary (str): Evaluator-authored concise explanation of the overall verdict.
            target_agent_id (UUID): Agent attributed to the target at its first durable event.
            target_agent_version_id (UUID): Immutable target-agent version captured for the evaluation.
            target_session_id (UUID): Root session whose frozen transcript was evaluated.
     """

    archetype: ManagedAgentsEvaluationArchetype
    child_session_id: UUID
    created_at: datetime.datetime
    criteria: list[ManagedAgentsEvaluationCriterion]
    evaluation_id: UUID
    evaluator_agent_id: UUID
    evaluator_agent_version_id: UUID
    failure_class: ManagedAgentsEvaluationFailureClass
    result: ManagedAgentsEvaluationResult
    run_session_id: UUID
    size_bucket: ManagedAgentsEvaluationSizeBucket
    snapshot_event_id: UUID
    summary: str
    target_agent_id: UUID
    target_agent_version_id: UUID
    target_session_id: UUID





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_evaluation_criterion import ManagedAgentsEvaluationCriterion # noqa: PLC0415
        archetype = self.archetype.value

        child_session_id = str(self.child_session_id)

        created_at = self.created_at.isoformat()

        criteria = []
        for criteria_item_data in self.criteria:
            criteria_item = criteria_item_data.to_dict()
            criteria.append(criteria_item)



        evaluation_id = str(self.evaluation_id)

        evaluator_agent_id = str(self.evaluator_agent_id)

        evaluator_agent_version_id = str(self.evaluator_agent_version_id)

        failure_class = self.failure_class.value

        result = self.result.value

        run_session_id = str(self.run_session_id)

        size_bucket = self.size_bucket.value

        snapshot_event_id = str(self.snapshot_event_id)

        summary = self.summary

        target_agent_id = str(self.target_agent_id)

        target_agent_version_id = str(self.target_agent_version_id)

        target_session_id = str(self.target_session_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "archetype": archetype,
            "child_session_id": child_session_id,
            "created_at": created_at,
            "criteria": criteria,
            "evaluation_id": evaluation_id,
            "evaluator_agent_id": evaluator_agent_id,
            "evaluator_agent_version_id": evaluator_agent_version_id,
            "failure_class": failure_class,
            "result": result,
            "run_session_id": run_session_id,
            "size_bucket": size_bucket,
            "snapshot_event_id": snapshot_event_id,
            "summary": summary,
            "target_agent_id": target_agent_id,
            "target_agent_version_id": target_agent_version_id,
            "target_session_id": target_session_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_evaluation_criterion import ManagedAgentsEvaluationCriterion # noqa: PLC0415
        d = dict(src_dict)
        archetype = ManagedAgentsEvaluationArchetype(d.pop("archetype"))




        child_session_id = UUID(d.pop("child_session_id"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        criteria = []
        _criteria = d.pop("criteria")
        for criteria_item_data in (_criteria):
            criteria_item = ManagedAgentsEvaluationCriterion.from_dict(criteria_item_data)



            criteria.append(criteria_item)


        evaluation_id = UUID(d.pop("evaluation_id"))




        evaluator_agent_id = UUID(d.pop("evaluator_agent_id"))




        evaluator_agent_version_id = UUID(d.pop("evaluator_agent_version_id"))




        failure_class = ManagedAgentsEvaluationFailureClass(d.pop("failure_class"))




        result = ManagedAgentsEvaluationResult(d.pop("result"))




        run_session_id = UUID(d.pop("run_session_id"))




        size_bucket = ManagedAgentsEvaluationSizeBucket(d.pop("size_bucket"))




        snapshot_event_id = UUID(d.pop("snapshot_event_id"))




        summary = d.pop("summary")

        target_agent_id = UUID(d.pop("target_agent_id"))




        target_agent_version_id = UUID(d.pop("target_agent_version_id"))




        target_session_id = UUID(d.pop("target_session_id"))




        managed_agents_evaluation = cls(
            archetype=archetype,
            child_session_id=child_session_id,
            created_at=created_at,
            criteria=criteria,
            evaluation_id=evaluation_id,
            evaluator_agent_id=evaluator_agent_id,
            evaluator_agent_version_id=evaluator_agent_version_id,
            failure_class=failure_class,
            result=result,
            run_session_id=run_session_id,
            size_bucket=size_bucket,
            snapshot_event_id=snapshot_event_id,
            summary=summary,
            target_agent_id=target_agent_id,
            target_agent_version_id=target_agent_version_id,
            target_session_id=target_session_id,
        )

        return managed_agents_evaluation

