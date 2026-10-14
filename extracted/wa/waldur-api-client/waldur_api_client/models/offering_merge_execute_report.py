import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.offering_merge_check import OfferingMergeCheck
    from ..models.offering_merge_execute_invoice_report import OfferingMergeExecuteInvoiceReport


T = TypeVar("T", bound="OfferingMergeExecuteReport")


@_attrs_define
class OfferingMergeExecuteReport:
    """
    Attributes:
        passed (bool):
        checked_at (datetime.datetime):
        checks (list['OfferingMergeCheck']):
        invoice_items (OfferingMergeExecuteInvoiceReport):
    """

    passed: bool
    checked_at: datetime.datetime
    checks: list["OfferingMergeCheck"]
    invoice_items: "OfferingMergeExecuteInvoiceReport"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        passed = self.passed

        checked_at = self.checked_at.isoformat()

        checks = []
        for checks_item_data in self.checks:
            checks_item = checks_item_data.to_dict()
            checks.append(checks_item)

        invoice_items = self.invoice_items.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "passed": passed,
                "checked_at": checked_at,
                "checks": checks,
                "invoice_items": invoice_items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_merge_check import OfferingMergeCheck
        from ..models.offering_merge_execute_invoice_report import OfferingMergeExecuteInvoiceReport

        d = dict(src_dict)
        passed = d.pop("passed")

        checked_at = isoparse(d.pop("checked_at"))

        checks = []
        _checks = d.pop("checks")
        for checks_item_data in _checks:
            checks_item = OfferingMergeCheck.from_dict(checks_item_data)

            checks.append(checks_item)

        invoice_items = OfferingMergeExecuteInvoiceReport.from_dict(d.pop("invoice_items"))

        offering_merge_execute_report = cls(
            passed=passed,
            checked_at=checked_at,
            checks=checks,
            invoice_items=invoice_items,
        )

        offering_merge_execute_report.additional_properties = d
        return offering_merge_execute_report

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
