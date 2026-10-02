from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_evaluation_plan_criterion import ManagedAgentsEvaluationPlanCriterion
  from ..models.managed_agents_evaluation_plan_target import ManagedAgentsEvaluationPlanTarget





T = TypeVar("T", bound="ManagedAgentsEvaluationPlanFrozen")



@_attrs_define
class ManagedAgentsEvaluationPlanFrozen:
    """ Audit event payload that freezes the complete target set, rubric, concurrency, and cost cap before child work
    starts.

        Example:
            {'criteria': [{'criterion_key': 'example', 'criterion_text': 'example'}], 'max_concurrent_threads': 1,
                'max_tree_cost_usd': 'example', 'targets': [{'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}]}

        Attributes:
            criteria (list[ManagedAgentsEvaluationPlanCriterion]): Ordered rubric criteria frozen from the evaluator
                version.
            max_concurrent_threads (int): Maximum evaluation children admitted concurrently for this run.
            targets (list[ManagedAgentsEvaluationPlanTarget]): Ordered target sessions and their immutable transcript
                snapshots.
            max_tree_cost_usd (str | Unset): Optional exact decimal USD cap on billed cost shared by the evaluation tree.
     """

    criteria: list[ManagedAgentsEvaluationPlanCriterion]
    max_concurrent_threads: int
    targets: list[ManagedAgentsEvaluationPlanTarget]
    max_tree_cost_usd: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_evaluation_plan_criterion import ManagedAgentsEvaluationPlanCriterion # noqa: PLC0415
        from ..models.managed_agents_evaluation_plan_target import ManagedAgentsEvaluationPlanTarget # noqa: PLC0415
        criteria = []
        for criteria_item_data in self.criteria:
            criteria_item = criteria_item_data.to_dict()
            criteria.append(criteria_item)



        max_concurrent_threads = self.max_concurrent_threads

        targets = []
        for targets_item_data in self.targets:
            targets_item = targets_item_data.to_dict()
            targets.append(targets_item)



        max_tree_cost_usd = self.max_tree_cost_usd


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "criteria": criteria,
            "max_concurrent_threads": max_concurrent_threads,
            "targets": targets,
        })
        if max_tree_cost_usd is not UNSET:
            field_dict["max_tree_cost_usd"] = max_tree_cost_usd

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_evaluation_plan_criterion import ManagedAgentsEvaluationPlanCriterion # noqa: PLC0415
        from ..models.managed_agents_evaluation_plan_target import ManagedAgentsEvaluationPlanTarget # noqa: PLC0415
        d = dict(src_dict)
        criteria = []
        _criteria = d.pop("criteria")
        for criteria_item_data in (_criteria):
            criteria_item = ManagedAgentsEvaluationPlanCriterion.from_dict(criteria_item_data)



            criteria.append(criteria_item)


        max_concurrent_threads = d.pop("max_concurrent_threads")

        targets = []
        _targets = d.pop("targets")
        for targets_item_data in (_targets):
            targets_item = ManagedAgentsEvaluationPlanTarget.from_dict(targets_item_data)



            targets.append(targets_item)


        max_tree_cost_usd = d.pop("max_tree_cost_usd", UNSET)

        managed_agents_evaluation_plan_frozen = cls(
            criteria=criteria,
            max_concurrent_threads=max_concurrent_threads,
            targets=targets,
            max_tree_cost_usd=max_tree_cost_usd,
        )

        return managed_agents_evaluation_plan_frozen

