from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.compensate_in_enum import CompensateInEnum

if TYPE_CHECKING:
    from ..models.earlier_invoice_payment import EarlierInvoicePayment


T = TypeVar("T", bound="PayEarlierInvoices")


@_attrs_define
class PayEarlierInvoices:
    """
    Attributes:
        dry_run (bool):
        compensate_in (CompensateInEnum):
        payments (list['EarlierInvoicePayment']):
        total (str):
        project_credit_before (str):
        project_credit_after (str):
        customer_credit_before (str):
        customer_credit_after (str):
    """

    dry_run: bool
    compensate_in: CompensateInEnum
    payments: list["EarlierInvoicePayment"]
    total: str
    project_credit_before: str
    project_credit_after: str
    customer_credit_before: str
    customer_credit_after: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dry_run = self.dry_run

        compensate_in = self.compensate_in.value

        payments = []
        for payments_item_data in self.payments:
            payments_item = payments_item_data.to_dict()
            payments.append(payments_item)

        total = self.total

        project_credit_before = self.project_credit_before

        project_credit_after = self.project_credit_after

        customer_credit_before = self.customer_credit_before

        customer_credit_after = self.customer_credit_after

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dry_run": dry_run,
                "compensate_in": compensate_in,
                "payments": payments,
                "total": total,
                "project_credit_before": project_credit_before,
                "project_credit_after": project_credit_after,
                "customer_credit_before": customer_credit_before,
                "customer_credit_after": customer_credit_after,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.earlier_invoice_payment import EarlierInvoicePayment

        d = dict(src_dict)
        dry_run = d.pop("dry_run")

        compensate_in = CompensateInEnum(d.pop("compensate_in"))

        payments = []
        _payments = d.pop("payments")
        for payments_item_data in _payments:
            payments_item = EarlierInvoicePayment.from_dict(payments_item_data)

            payments.append(payments_item)

        total = d.pop("total")

        project_credit_before = d.pop("project_credit_before")

        project_credit_after = d.pop("project_credit_after")

        customer_credit_before = d.pop("customer_credit_before")

        customer_credit_after = d.pop("customer_credit_after")

        pay_earlier_invoices = cls(
            dry_run=dry_run,
            compensate_in=compensate_in,
            payments=payments,
            total=total,
            project_credit_before=project_credit_before,
            project_credit_after=project_credit_after,
            customer_credit_before=customer_credit_before,
            customer_credit_after=customer_credit_after,
        )

        pay_earlier_invoices.additional_properties = d
        return pay_earlier_invoices

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
