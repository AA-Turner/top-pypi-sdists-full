from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_evaluation import ManagedAgentsEvaluation





T = TypeVar("T", bound="ManagedAgentsEvaluationListResponse")



@_attrs_define
class ManagedAgentsEvaluationListResponse:
    """ One organization-scoped page of immutable evaluation verdicts and an optional continuation.

        Example:
            {'evaluations': [{'archetype': 'artifact', 'child_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'created_at': '2026-02-18T09:30:00Z', 'criteria': [{'criterion_key': 'example', 'evidence_event_ids':
                ['9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'], 'rationale': 'example', 'verdict': 'pass'}], 'evaluation_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'evaluator_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'evaluator_agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'failure_class': 'none', 'result': 'pass',
                'run_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'size_bucket': 'unknown', 'snapshot_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'summary': 'example', 'target_agent_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'next_page_token': 'example'}

        Attributes:
            evaluations (list[ManagedAgentsEvaluation]): Newest-first immutable evaluation verdicts for this page.
            next_page_token (str | Unset): Signed one-hour continuation bound to the organization, filters, and effective
                limit.
     """

    evaluations: list[ManagedAgentsEvaluation]
    next_page_token: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_evaluation import ManagedAgentsEvaluation # noqa: PLC0415
        evaluations = []
        for evaluations_item_data in self.evaluations:
            evaluations_item = evaluations_item_data.to_dict()
            evaluations.append(evaluations_item)



        next_page_token = self.next_page_token


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "evaluations": evaluations,
        })
        if next_page_token is not UNSET:
            field_dict["next_page_token"] = next_page_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_evaluation import ManagedAgentsEvaluation # noqa: PLC0415
        d = dict(src_dict)
        evaluations = []
        _evaluations = d.pop("evaluations")
        for evaluations_item_data in (_evaluations):
            evaluations_item = ManagedAgentsEvaluation.from_dict(evaluations_item_data)



            evaluations.append(evaluations_item)


        next_page_token = d.pop("next_page_token", UNSET)

        managed_agents_evaluation_list_response = cls(
            evaluations=evaluations,
            next_page_token=next_page_token,
        )

        return managed_agents_evaluation_list_response

