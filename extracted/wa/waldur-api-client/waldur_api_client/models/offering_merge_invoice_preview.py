from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.offering_merge_invoice_preview_to_rewrite_by_policy import (
        OfferingMergeInvoicePreviewToRewriteByPolicy,
    )


T = TypeVar("T", bound="OfferingMergeInvoicePreview")


@_attrs_define
class OfferingMergeInvoicePreview:
    """
    Attributes:
        policy (str): The merge's invoice_policy.
        to_rewrite (int): Invoice items whose snapshot the chosen policy rewrites.
        to_rewrite_by_policy (OfferingMergeInvoicePreviewToRewriteByPolicy): Invoice items each policy would rewrite.
        on_closed_invoices (int):
        kept_on_closed_invoices (int):
    """

    policy: str
    to_rewrite: int
    to_rewrite_by_policy: "OfferingMergeInvoicePreviewToRewriteByPolicy"
    on_closed_invoices: int
    kept_on_closed_invoices: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        policy = self.policy

        to_rewrite = self.to_rewrite

        to_rewrite_by_policy = self.to_rewrite_by_policy.to_dict()

        on_closed_invoices = self.on_closed_invoices

        kept_on_closed_invoices = self.kept_on_closed_invoices

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "policy": policy,
                "to_rewrite": to_rewrite,
                "to_rewrite_by_policy": to_rewrite_by_policy,
                "on_closed_invoices": on_closed_invoices,
                "kept_on_closed_invoices": kept_on_closed_invoices,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_merge_invoice_preview_to_rewrite_by_policy import (
            OfferingMergeInvoicePreviewToRewriteByPolicy,
        )

        d = dict(src_dict)
        policy = d.pop("policy")

        to_rewrite = d.pop("to_rewrite")

        to_rewrite_by_policy = OfferingMergeInvoicePreviewToRewriteByPolicy.from_dict(d.pop("to_rewrite_by_policy"))

        on_closed_invoices = d.pop("on_closed_invoices")

        kept_on_closed_invoices = d.pop("kept_on_closed_invoices")

        offering_merge_invoice_preview = cls(
            policy=policy,
            to_rewrite=to_rewrite,
            to_rewrite_by_policy=to_rewrite_by_policy,
            on_closed_invoices=on_closed_invoices,
            kept_on_closed_invoices=kept_on_closed_invoices,
        )

        offering_merge_invoice_preview.additional_properties = d
        return offering_merge_invoice_preview

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
