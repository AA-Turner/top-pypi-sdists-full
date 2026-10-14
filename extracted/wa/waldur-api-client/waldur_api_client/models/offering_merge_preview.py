from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.offering_merge_entry import OfferingMergeEntry
    from ..models.offering_merge_invoice_preview import OfferingMergeInvoicePreview
    from ..models.offering_merge_issue import OfferingMergeIssue
    from ..models.offering_merge_preview_counts import OfferingMergePreviewCounts
    from ..models.offering_merge_preview_left_on_source import OfferingMergePreviewLeftOnSource
    from ..models.offering_merge_summaries import OfferingMergeSummaries


T = TypeVar("T", bound="OfferingMergePreview")


@_attrs_define
class OfferingMergePreview:
    """
    Attributes:
        target (str): Target offering UUID.
        sources (list[str]): Source offering UUIDs.
        counts (OfferingMergePreviewCounts): Rows per coverage registry entry (model.Field label).
        entries (list['OfferingMergeEntry']): The same counts, grouped by area and classified by effect.
        left_on_source (OfferingMergePreviewLeftOnSource): Rows that stay on a source because the target has them
            already.
        summaries_to_recompute (OfferingMergeSummaries):
        invoice_items (OfferingMergeInvoicePreview):
        blockers (list['OfferingMergeIssue']):
        warnings (list['OfferingMergeIssue']):
    """

    target: str
    sources: list[str]
    counts: "OfferingMergePreviewCounts"
    entries: list["OfferingMergeEntry"]
    left_on_source: "OfferingMergePreviewLeftOnSource"
    summaries_to_recompute: "OfferingMergeSummaries"
    invoice_items: "OfferingMergeInvoicePreview"
    blockers: list["OfferingMergeIssue"]
    warnings: list["OfferingMergeIssue"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target = self.target

        sources = self.sources

        counts = self.counts.to_dict()

        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()
            entries.append(entries_item)

        left_on_source = self.left_on_source.to_dict()

        summaries_to_recompute = self.summaries_to_recompute.to_dict()

        invoice_items = self.invoice_items.to_dict()

        blockers = []
        for blockers_item_data in self.blockers:
            blockers_item = blockers_item_data.to_dict()
            blockers.append(blockers_item)

        warnings = []
        for warnings_item_data in self.warnings:
            warnings_item = warnings_item_data.to_dict()
            warnings.append(warnings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target": target,
                "sources": sources,
                "counts": counts,
                "entries": entries,
                "left_on_source": left_on_source,
                "summaries_to_recompute": summaries_to_recompute,
                "invoice_items": invoice_items,
                "blockers": blockers,
                "warnings": warnings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_merge_entry import OfferingMergeEntry
        from ..models.offering_merge_invoice_preview import OfferingMergeInvoicePreview
        from ..models.offering_merge_issue import OfferingMergeIssue
        from ..models.offering_merge_preview_counts import OfferingMergePreviewCounts
        from ..models.offering_merge_preview_left_on_source import OfferingMergePreviewLeftOnSource
        from ..models.offering_merge_summaries import OfferingMergeSummaries

        d = dict(src_dict)
        target = d.pop("target")

        sources = cast(list[str], d.pop("sources"))

        counts = OfferingMergePreviewCounts.from_dict(d.pop("counts"))

        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = OfferingMergeEntry.from_dict(entries_item_data)

            entries.append(entries_item)

        left_on_source = OfferingMergePreviewLeftOnSource.from_dict(d.pop("left_on_source"))

        summaries_to_recompute = OfferingMergeSummaries.from_dict(d.pop("summaries_to_recompute"))

        invoice_items = OfferingMergeInvoicePreview.from_dict(d.pop("invoice_items"))

        blockers = []
        _blockers = d.pop("blockers")
        for blockers_item_data in _blockers:
            blockers_item = OfferingMergeIssue.from_dict(blockers_item_data)

            blockers.append(blockers_item)

        warnings = []
        _warnings = d.pop("warnings")
        for warnings_item_data in _warnings:
            warnings_item = OfferingMergeIssue.from_dict(warnings_item_data)

            warnings.append(warnings_item)

        offering_merge_preview = cls(
            target=target,
            sources=sources,
            counts=counts,
            entries=entries,
            left_on_source=left_on_source,
            summaries_to_recompute=summaries_to_recompute,
            invoice_items=invoice_items,
            blockers=blockers,
            warnings=warnings,
        )

        offering_merge_preview.additional_properties = d
        return offering_merge_preview

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
