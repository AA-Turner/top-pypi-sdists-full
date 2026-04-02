from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.suggest_alternative_reviewers_suggestions_item import SuggestAlternativeReviewersSuggestionsItem


T = TypeVar("T", bound="SuggestAlternativeReviewers")


@_attrs_define
class SuggestAlternativeReviewers:
    """
    Attributes:
        suggestions (list['SuggestAlternativeReviewersSuggestionsItem']): List of alternative reviewers with affinity
            scores
    """

    suggestions: list["SuggestAlternativeReviewersSuggestionsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        suggestions = []
        for suggestions_item_data in self.suggestions:
            suggestions_item = suggestions_item_data.to_dict()
            suggestions.append(suggestions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "suggestions": suggestions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.suggest_alternative_reviewers_suggestions_item import SuggestAlternativeReviewersSuggestionsItem

        d = dict(src_dict)
        suggestions = []
        _suggestions = d.pop("suggestions")
        for suggestions_item_data in _suggestions:
            suggestions_item = SuggestAlternativeReviewersSuggestionsItem.from_dict(suggestions_item_data)

            suggestions.append(suggestions_item)

        suggest_alternative_reviewers = cls(
            suggestions=suggestions,
        )

        suggest_alternative_reviewers.additional_properties = d
        return suggest_alternative_reviewers

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
