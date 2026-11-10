from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PolicyCostBreakdown")


@_attrs_define
class PolicyCostBreakdown:
    """
    Attributes:
        cost_before_credit (Union[Unset, str]): The invoiced cost within the policy's period before any credit, tax
            included.
        credit_drawn (Union[Unset, str]): Credit compensation already written on the period's invoices. 0 for a policy
            that does not take credit into account, which counts the cost credit paid as well.
        credit_pending (Union[Unset, str]): Credit the current month will still draw that is not written yet. 0 for a
            policy that does not take credit into account.
        earlier_months (Union[Unset, str]): The part of current_cost from months before the current one. 0 for a one-
            month period. For a policy that takes credit into account, credit added now pays only the current month, so this
            part stays until those months are paid; see ProjectCredit.pay_earlier_invoices. A policy that does not take
            credit into account counts this part in full, whatever credit paid.
    """

    cost_before_credit: Union[Unset, str] = UNSET
    credit_drawn: Union[Unset, str] = UNSET
    credit_pending: Union[Unset, str] = UNSET
    earlier_months: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cost_before_credit = self.cost_before_credit

        credit_drawn = self.credit_drawn

        credit_pending = self.credit_pending

        earlier_months = self.earlier_months

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cost_before_credit is not UNSET:
            field_dict["cost_before_credit"] = cost_before_credit
        if credit_drawn is not UNSET:
            field_dict["credit_drawn"] = credit_drawn
        if credit_pending is not UNSET:
            field_dict["credit_pending"] = credit_pending
        if earlier_months is not UNSET:
            field_dict["earlier_months"] = earlier_months

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cost_before_credit = d.pop("cost_before_credit", UNSET)

        credit_drawn = d.pop("credit_drawn", UNSET)

        credit_pending = d.pop("credit_pending", UNSET)

        earlier_months = d.pop("earlier_months", UNSET)

        policy_cost_breakdown = cls(
            cost_before_credit=cost_before_credit,
            credit_drawn=credit_drawn,
            credit_pending=credit_pending,
            earlier_months=earlier_months,
        )

        policy_cost_breakdown.additional_properties = d
        return policy_cost_breakdown

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
