from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast

if TYPE_CHECKING:
    from ..models.manual_review_item import ManualReviewItem


T = TypeVar("T", bound="RemoveReferencesAttributes")


@_attrs_define
class RemoveReferencesAttributes:
    """Counts and follow-ups returned by the remove-references action.

    Attributes:
        flags_modified (list[str]): Keys of flags whose rules were modified.
        rules_removed (int): Total number of rules removed across all flags.
        rules_needing_manual_review (list[ManualReviewItem]): Rules that referenced the context but could not be removed
            automatically (typically because the reference is inside an `and` expression where removal would broaden the
            rule).
    """

    flags_modified: list[str]
    rules_removed: int
    rules_needing_manual_review: list[ManualReviewItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flags_modified = self.flags_modified

        rules_removed = self.rules_removed

        rules_needing_manual_review = []
        for rules_needing_manual_review_item_data in self.rules_needing_manual_review:
            rules_needing_manual_review_item = rules_needing_manual_review_item_data.to_dict()
            rules_needing_manual_review.append(rules_needing_manual_review_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "flags_modified": flags_modified,
                "rules_removed": rules_removed,
                "rules_needing_manual_review": rules_needing_manual_review,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.manual_review_item import ManualReviewItem

        d = dict(src_dict)
        flags_modified = cast(list[str], d.pop("flags_modified"))

        rules_removed = d.pop("rules_removed")

        rules_needing_manual_review = []
        _rules_needing_manual_review = d.pop("rules_needing_manual_review")
        for rules_needing_manual_review_item_data in _rules_needing_manual_review:
            rules_needing_manual_review_item = ManualReviewItem.from_dict(rules_needing_manual_review_item_data)

            rules_needing_manual_review.append(rules_needing_manual_review_item)

        remove_references_attributes = cls(
            flags_modified=flags_modified,
            rules_removed=rules_removed,
            rules_needing_manual_review=rules_needing_manual_review,
        )

        remove_references_attributes.additional_properties = d
        return remove_references_attributes

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
