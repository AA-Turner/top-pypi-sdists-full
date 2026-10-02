from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_evaluation_run import ManagedAgentsEvaluationRun





T = TypeVar("T", bound="ManagedAgentsEvaluationRunListResponse")



@_attrs_define
class ManagedAgentsEvaluationRunListResponse:
    """ One page of organization-scoped evaluation-run summaries and an optional continuation.

        Example:
            {'evaluation_runs': [{'created_at': '2026-02-18T09:30:00Z', 'evaluator_agent_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'evaluator_agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'execution_state': 'provisioning', 'fail_count': 1, 'not_applicable_count': 1, 'pass_count': 1,
                'run_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'active', 'targets_total': 1, 'updated_at':
                '2026-02-18T09:30:00Z', 'verdicts_total': 1}], 'next_page_token': 'example'}

        Attributes:
            evaluation_runs (list[ManagedAgentsEvaluationRun]): Newest-first platform-internal evaluation-run summaries for
                this page.
            next_page_token (str | Unset): Signed one-hour continuation bound to the organization and effective limit.
     """

    evaluation_runs: list[ManagedAgentsEvaluationRun]
    next_page_token: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_evaluation_run import ManagedAgentsEvaluationRun # noqa: PLC0415
        evaluation_runs = []
        for evaluation_runs_item_data in self.evaluation_runs:
            evaluation_runs_item = evaluation_runs_item_data.to_dict()
            evaluation_runs.append(evaluation_runs_item)



        next_page_token = self.next_page_token


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "evaluation_runs": evaluation_runs,
        })
        if next_page_token is not UNSET:
            field_dict["next_page_token"] = next_page_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_evaluation_run import ManagedAgentsEvaluationRun # noqa: PLC0415
        d = dict(src_dict)
        evaluation_runs = []
        _evaluation_runs = d.pop("evaluation_runs")
        for evaluation_runs_item_data in (_evaluation_runs):
            evaluation_runs_item = ManagedAgentsEvaluationRun.from_dict(evaluation_runs_item_data)



            evaluation_runs.append(evaluation_runs_item)


        next_page_token = d.pop("next_page_token", UNSET)

        managed_agents_evaluation_run_list_response = cls(
            evaluation_runs=evaluation_runs,
            next_page_token=next_page_token,
        )

        return managed_agents_evaluation_run_list_response

