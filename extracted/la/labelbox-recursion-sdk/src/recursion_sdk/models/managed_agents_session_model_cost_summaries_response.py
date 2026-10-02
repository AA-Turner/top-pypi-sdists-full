from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_session_model_cost_summary_response import ManagedAgentsSessionModelCostSummaryResponse





T = TypeVar("T", bound="ManagedAgentsSessionModelCostSummariesResponse")



@_attrs_define
class ManagedAgentsSessionModelCostSummariesResponse:
    """ One session's three scope rollups, read from a single database snapshot so self, subtree, and tree cannot disagree
    with one another.

        Example:
            {'self': {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count': 'example', 'completeness':
                'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'},
                'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'subtree': {'adjustment_count': 'example',
                'attempt_count': 'example', 'charge_count': 'example', 'completeness': 'complete', 'model_cost_usd': 'example',
                'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'tree': {'adjustment_count': 'example',
                'attempt_count': 'example', 'charge_count': 'example', 'completeness': 'complete', 'model_cost_usd': 'example',
                'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}

        Attributes:
            self_ (ManagedAgentsSessionModelCostSummaryResponse): Model-cost rollup for one session scope: the exact ledger
                amount, how complete the accounting behind it is, and the counts it was derived from. attempt_count is every
                provider call the ledger is accountable for, charge_count only those that produced a receipt, and
                adjustment_count the signed corrections applied since. Model spend only: sandbox, tool, and storage cost are not
                included. Example: {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count': 'example',
                'completeness': 'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
            session_id (str): Session these three rollups were requested for (UUID).
            subtree (ManagedAgentsSessionModelCostSummaryResponse): Model-cost rollup for one session scope: the exact
                ledger amount, how complete the accounting behind it is, and the counts it was derived from. attempt_count is
                every provider call the ledger is accountable for, charge_count only those that produced a receipt, and
                adjustment_count the signed corrections applied since. Model spend only: sandbox, tool, and storage cost are not
                included. Example: {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count': 'example',
                'completeness': 'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
            tree (ManagedAgentsSessionModelCostSummaryResponse): Model-cost rollup for one session scope: the exact ledger
                amount, how complete the accounting behind it is, and the counts it was derived from. attempt_count is every
                provider call the ledger is accountable for, charge_count only those that produced a receipt, and
                adjustment_count the signed corrections applied since. Model spend only: sandbox, tool, and storage cost are not
                included. Example: {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count': 'example',
                'completeness': 'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
     """

    self_: ManagedAgentsSessionModelCostSummaryResponse
    session_id: str
    subtree: ManagedAgentsSessionModelCostSummaryResponse
    tree: ManagedAgentsSessionModelCostSummaryResponse
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_session_model_cost_summary_response import ManagedAgentsSessionModelCostSummaryResponse # noqa: PLC0415
        self_ = self.self_.to_dict()

        session_id = self.session_id

        subtree = self.subtree.to_dict()

        tree = self.tree.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "self": self_,
            "session_id": session_id,
            "subtree": subtree,
            "tree": tree,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_session_model_cost_summary_response import ManagedAgentsSessionModelCostSummaryResponse # noqa: PLC0415
        d = dict(src_dict)
        self_ = ManagedAgentsSessionModelCostSummaryResponse.from_dict(d.pop("self"))




        session_id = d.pop("session_id")

        subtree = ManagedAgentsSessionModelCostSummaryResponse.from_dict(d.pop("subtree"))




        tree = ManagedAgentsSessionModelCostSummaryResponse.from_dict(d.pop("tree"))




        managed_agents_session_model_cost_summaries_response = cls(
            self_=self_,
            session_id=session_id,
            subtree=subtree,
            tree=tree,
        )


        managed_agents_session_model_cost_summaries_response.additional_properties = d
        return managed_agents_session_model_cost_summaries_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
