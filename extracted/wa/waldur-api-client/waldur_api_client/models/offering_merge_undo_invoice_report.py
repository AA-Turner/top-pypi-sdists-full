from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.offering_merge_skipped_invoice_item import OfferingMergeSkippedInvoiceItem


T = TypeVar("T", bound="OfferingMergeUndoInvoiceReport")


@_attrs_define
class OfferingMergeUndoInvoiceReport:
    """
    Attributes:
        policy (str): The merge's invoice_policy.
        restored (int):
        moved_back (int):
        skipped (list['OfferingMergeSkippedInvoiceItem']):
    """

    policy: str
    restored: int
    moved_back: int
    skipped: list["OfferingMergeSkippedInvoiceItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        policy = self.policy

        restored = self.restored

        moved_back = self.moved_back

        skipped = []
        for skipped_item_data in self.skipped:
            skipped_item = skipped_item_data.to_dict()
            skipped.append(skipped_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "policy": policy,
                "restored": restored,
                "moved_back": moved_back,
                "skipped": skipped,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_merge_skipped_invoice_item import OfferingMergeSkippedInvoiceItem

        d = dict(src_dict)
        policy = d.pop("policy")

        restored = d.pop("restored")

        moved_back = d.pop("moved_back")

        skipped = []
        _skipped = d.pop("skipped")
        for skipped_item_data in _skipped:
            skipped_item = OfferingMergeSkippedInvoiceItem.from_dict(skipped_item_data)

            skipped.append(skipped_item)

        offering_merge_undo_invoice_report = cls(
            policy=policy,
            restored=restored,
            moved_back=moved_back,
            skipped=skipped,
        )

        offering_merge_undo_invoice_report.additional_properties = d
        return offering_merge_undo_invoice_report

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
