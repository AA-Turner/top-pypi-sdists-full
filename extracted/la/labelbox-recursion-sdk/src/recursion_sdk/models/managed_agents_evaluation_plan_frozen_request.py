from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_evaluation_plan_criterion_request import ManagedAgentsEvaluationPlanCriterionRequest
  from ..models.managed_agents_evaluation_plan_target_request import ManagedAgentsEvaluationPlanTargetRequest





T = TypeVar("T", bound="ManagedAgentsEvaluationPlanFrozenRequest")



@_attrs_define
class ManagedAgentsEvaluationPlanFrozenRequest:
    """ Audit event payload that freezes the complete target set, rubric, concurrency, and cost cap before child work
    starts.

        Example:
            {'criteria': [{'criterion_key': 'example', 'criterion_text': 'example'}], 'max_concurrent_threads': 1,
                'max_tree_cost_usd': 'example', 'targets': [{'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}]}

        Attributes:
            criteria (list[ManagedAgentsEvaluationPlanCriterionRequest] | Unset): Ordered rubric criteria frozen from the
                evaluator version.
            max_concurrent_threads (int | Unset): Maximum evaluation children admitted concurrently for this run.
            max_tree_cost_usd (str | Unset): Optional exact decimal USD cap on billed cost shared by the evaluation tree.
            targets (list[ManagedAgentsEvaluationPlanTargetRequest] | Unset): Ordered target sessions and their immutable
                transcript snapshots.
     """

    criteria: list[ManagedAgentsEvaluationPlanCriterionRequest] | Unset = UNSET
    max_concurrent_threads: int | Unset = UNSET
    max_tree_cost_usd: str | Unset = UNSET
    targets: list[ManagedAgentsEvaluationPlanTargetRequest] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_evaluation_plan_criterion_request import ManagedAgentsEvaluationPlanCriterionRequest # noqa: PLC0415
        from ..models.managed_agents_evaluation_plan_target_request import ManagedAgentsEvaluationPlanTargetRequest # noqa: PLC0415
        criteria: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.criteria, Unset):
            criteria = []
            for criteria_item_data in self.criteria:
                criteria_item = criteria_item_data.to_dict()
                criteria.append(criteria_item)



        max_concurrent_threads = self.max_concurrent_threads

        max_tree_cost_usd = self.max_tree_cost_usd

        targets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.targets, Unset):
            targets = []
            for targets_item_data in self.targets:
                targets_item = targets_item_data.to_dict()
                targets.append(targets_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if criteria is not UNSET:
            field_dict["criteria"] = criteria
        if max_concurrent_threads is not UNSET:
            field_dict["max_concurrent_threads"] = max_concurrent_threads
        if max_tree_cost_usd is not UNSET:
            field_dict["max_tree_cost_usd"] = max_tree_cost_usd
        if targets is not UNSET:
            field_dict["targets"] = targets

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_evaluation_plan_criterion_request import ManagedAgentsEvaluationPlanCriterionRequest # noqa: PLC0415
        from ..models.managed_agents_evaluation_plan_target_request import ManagedAgentsEvaluationPlanTargetRequest # noqa: PLC0415
        d = dict(src_dict)
        _criteria = d.pop("criteria", UNSET)
        criteria: list[ManagedAgentsEvaluationPlanCriterionRequest] | Unset = UNSET
        if _criteria is not UNSET:
            criteria = []
            for criteria_item_data in _criteria:
                criteria_item = ManagedAgentsEvaluationPlanCriterionRequest.from_dict(criteria_item_data)



                criteria.append(criteria_item)


        max_concurrent_threads = d.pop("max_concurrent_threads", UNSET)

        max_tree_cost_usd = d.pop("max_tree_cost_usd", UNSET)

        _targets = d.pop("targets", UNSET)
        targets: list[ManagedAgentsEvaluationPlanTargetRequest] | Unset = UNSET
        if _targets is not UNSET:
            targets = []
            for targets_item_data in _targets:
                targets_item = ManagedAgentsEvaluationPlanTargetRequest.from_dict(targets_item_data)



                targets.append(targets_item)


        managed_agents_evaluation_plan_frozen_request = cls(
            criteria=criteria,
            max_concurrent_threads=max_concurrent_threads,
            max_tree_cost_usd=max_tree_cost_usd,
            targets=targets,
        )

        return managed_agents_evaluation_plan_frozen_request

