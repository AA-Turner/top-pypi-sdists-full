from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.billing_invoice import BillingInvoice


T = TypeVar("T", bound="BillingInvoiceList")


@_attrs_define
class BillingInvoiceList:
    """
    Attributes:
        invoices (list[BillingInvoice]):
    """

    invoices: list[BillingInvoice]

    def to_dict(self) -> dict[str, Any]:
        invoices = []
        for invoices_item_data in self.invoices:
            invoices_item = invoices_item_data.to_dict()
            invoices.append(invoices_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "invoices": invoices,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_invoice import BillingInvoice

        d = dict(src_dict)
        invoices = []
        _invoices = d.pop("invoices")
        for invoices_item_data in _invoices:
            invoices_item = BillingInvoice.from_dict(invoices_item_data)

            invoices.append(invoices_item)

        billing_invoice_list = cls(
            invoices=invoices,
        )

        return billing_invoice_list
