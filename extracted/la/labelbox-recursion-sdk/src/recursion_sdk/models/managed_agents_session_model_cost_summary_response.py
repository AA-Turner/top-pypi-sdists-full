from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_session_model_cost_summary_response_completeness import ManagedAgentsSessionModelCostSummaryResponseCompleteness
from ..models.managed_agents_session_model_cost_summary_response_scope import ManagedAgentsSessionModelCostSummaryResponseScope






T = TypeVar("T", bound="ManagedAgentsSessionModelCostSummaryResponse")



@_attrs_define
class ManagedAgentsSessionModelCostSummaryResponse:
    """ Model-cost rollup for one session scope: the exact ledger amount, how complete the accounting behind it is, and the
    counts it was derived from. attempt_count is every provider call the ledger is accountable for, charge_count only
    those that produced a receipt, and adjustment_count the signed corrections applied since. Model spend only: sandbox,
    tool, and storage cost are not included.

        Example:
            {'adjustment_count': 'example', 'attempt_count': 'example', 'charge_count': 'example', 'completeness':
                'complete', 'model_cost_usd': 'example', 'scope': 'self', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            adjustment_count (str): Exact base-10 integer string.
            attempt_count (str): Exact base-10 integer string.
            charge_count (str): Exact base-10 integer string.
            completeness (ManagedAgentsSessionModelCostSummaryResponseCompleteness): Weakest accounting state present in
                scope, so a rollup never overstates confidence: complete when every attempt is fully priced, pending when no
                attempt has been recorded yet or an outcome is still unknown, unpriced when no catalog rule matched the
                provider's quantities, partial when only part of the cost is known or several states are mixed, legacy_partial
                for charges recorded before the current reconciliation rules, and indeterminate when an attempt may have been
                billed without a usable receipt.
            model_cost_usd (str): Exact canonical decimal USD string. It is model cost only, not total session spend.
                Customers receive the amount their organization is billed; only trusted internal callers receive raw ledger cost
                here.
            scope (ManagedAgentsSessionModelCostSummaryResponseScope): Which sessions contributed: self counts this
                session's own attempts, subtree adds every session beneath it, and tree covers every session sharing the same
                root session.
            session_id (str): Session this rollup was requested for (UUID). Scope decides which sessions in its tree
                contributed to the figures.
     """

    adjustment_count: str
    attempt_count: str
    charge_count: str
    completeness: ManagedAgentsSessionModelCostSummaryResponseCompleteness
    model_cost_usd: str
    scope: ManagedAgentsSessionModelCostSummaryResponseScope
    session_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        adjustment_count = self.adjustment_count

        attempt_count = self.attempt_count

        charge_count = self.charge_count

        completeness = self.completeness.value

        model_cost_usd = self.model_cost_usd

        scope = self.scope.value

        session_id = self.session_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "adjustment_count": adjustment_count,
            "attempt_count": attempt_count,
            "charge_count": charge_count,
            "completeness": completeness,
            "model_cost_usd": model_cost_usd,
            "scope": scope,
            "session_id": session_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        adjustment_count = d.pop("adjustment_count")

        attempt_count = d.pop("attempt_count")

        charge_count = d.pop("charge_count")

        completeness = ManagedAgentsSessionModelCostSummaryResponseCompleteness(d.pop("completeness"))




        model_cost_usd = d.pop("model_cost_usd")

        scope = ManagedAgentsSessionModelCostSummaryResponseScope(d.pop("scope"))




        session_id = d.pop("session_id")

        managed_agents_session_model_cost_summary_response = cls(
            adjustment_count=adjustment_count,
            attempt_count=attempt_count,
            charge_count=charge_count,
            completeness=completeness,
            model_cost_usd=model_cost_usd,
            scope=scope,
            session_id=session_id,
        )


        managed_agents_session_model_cost_summary_response.additional_properties = d
        return managed_agents_session_model_cost_summary_response

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
