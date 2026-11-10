from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.earlier_invoice_month import EarlierInvoiceMonth


T = TypeVar("T", bound="ProjectCreditEarlierInvoices")


@_attrs_define
class ProjectCreditEarlierInvoices:
    """
    Attributes:
        months (list['EarlierInvoiceMonth']):
        uncovered (str): Uncovered cost of every month listed: what a period-Total cost policy that takes credit into
            account counts of them.
        uncovered_in_period (str): Uncovered cost of the months the credit pays.
        payable_now (str): What the allocation would pay now: the uncovered cost of the months it pays, capped by what
            is left of the allocation and of the organization credit after this month's usage so far.
    """

    months: list["EarlierInvoiceMonth"]
    uncovered: str
    uncovered_in_period: str
    payable_now: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        months = []
        for months_item_data in self.months:
            months_item = months_item_data.to_dict()
            months.append(months_item)

        uncovered = self.uncovered

        uncovered_in_period = self.uncovered_in_period

        payable_now = self.payable_now

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "months": months,
                "uncovered": uncovered,
                "uncovered_in_period": uncovered_in_period,
                "payable_now": payable_now,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.earlier_invoice_month import EarlierInvoiceMonth

        d = dict(src_dict)
        months = []
        _months = d.pop("months")
        for months_item_data in _months:
            months_item = EarlierInvoiceMonth.from_dict(months_item_data)

            months.append(months_item)

        uncovered = d.pop("uncovered")

        uncovered_in_period = d.pop("uncovered_in_period")

        payable_now = d.pop("payable_now")

        project_credit_earlier_invoices = cls(
            months=months,
            uncovered=uncovered,
            uncovered_in_period=uncovered_in_period,
            payable_now=payable_now,
        )

        project_credit_earlier_invoices.additional_properties = d
        return project_credit_earlier_invoices

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
