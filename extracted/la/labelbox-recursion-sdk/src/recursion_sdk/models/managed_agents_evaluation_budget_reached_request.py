from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsEvaluationBudgetReachedRequest")



@_attrs_define
class ManagedAgentsEvaluationBudgetReachedRequest:
    """ Audit event payload listing targets stopped or left unadmitted when the evaluation tree reached its exact USD cap.

        Example:
            {'affected_target_session_ids': ['9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'], 'max_tree_cost_usd': 'example'}

        Attributes:
            affected_target_session_ids (list[UUID] | Unset): Target sessions stopped or not admitted because the cap was
                reached.
            max_tree_cost_usd (str | Unset): Exact decimal USD tree cap that stopped further admission.
     """

    affected_target_session_ids: list[UUID] | Unset = UNSET
    max_tree_cost_usd: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        affected_target_session_ids: list[str] | Unset = UNSET
        if not isinstance(self.affected_target_session_ids, Unset):
            affected_target_session_ids = []
            for affected_target_session_ids_item_data in self.affected_target_session_ids:
                affected_target_session_ids_item = str(affected_target_session_ids_item_data)
                affected_target_session_ids.append(affected_target_session_ids_item)



        max_tree_cost_usd = self.max_tree_cost_usd


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if affected_target_session_ids is not UNSET:
            field_dict["affected_target_session_ids"] = affected_target_session_ids
        if max_tree_cost_usd is not UNSET:
            field_dict["max_tree_cost_usd"] = max_tree_cost_usd

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _affected_target_session_ids = d.pop("affected_target_session_ids", UNSET)
        affected_target_session_ids: list[UUID] | Unset = UNSET
        if _affected_target_session_ids is not UNSET:
            affected_target_session_ids = []
            for affected_target_session_ids_item_data in _affected_target_session_ids:
                affected_target_session_ids_item = UUID(affected_target_session_ids_item_data)



                affected_target_session_ids.append(affected_target_session_ids_item)


        max_tree_cost_usd = d.pop("max_tree_cost_usd", UNSET)

        managed_agents_evaluation_budget_reached_request = cls(
            affected_target_session_ids=affected_target_session_ids,
            max_tree_cost_usd=max_tree_cost_usd,
        )

        return managed_agents_evaluation_budget_reached_request

