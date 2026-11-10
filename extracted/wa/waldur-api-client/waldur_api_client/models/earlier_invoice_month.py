import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="EarlierInvoiceMonth")


@_attrs_define
class EarlierInvoiceMonth:
    """
    Attributes:
        period (datetime.date): The month, as its first day.
        cost (str): Cost the credit could pay: the project's items on offerings the credit covers, net of volume
            discounts, before tax.
        covered (str): What paid for it: the credit compensation on the month's invoice, later payments of the month,
            and staff refunds of its items.
        uncovered (str): Cost that nothing paid for yet.
        in_period (bool): Whether the month is within the months the credit pays.
    """

    period: datetime.date
    cost: str
    covered: str
    uncovered: str
    in_period: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period = self.period.isoformat()

        cost = self.cost

        covered = self.covered

        uncovered = self.uncovered

        in_period = self.in_period

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period": period,
                "cost": cost,
                "covered": covered,
                "uncovered": uncovered,
                "in_period": in_period,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period = isoparse(d.pop("period")).date()

        cost = d.pop("cost")

        covered = d.pop("covered")

        uncovered = d.pop("uncovered")

        in_period = d.pop("in_period")

        earlier_invoice_month = cls(
            period=period,
            cost=cost,
            covered=covered,
            uncovered=uncovered,
            in_period=in_period,
        )

        earlier_invoice_month.additional_properties = d
        return earlier_invoice_month

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
