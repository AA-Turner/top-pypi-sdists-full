from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GenerateSuggestionsResponse")


@_attrs_define
class GenerateSuggestionsResponse:
    """
    Attributes:
        suggestions_created (int):
        reviewers_evaluated (int):
        source_used (str):
        suggestions (list[str]):
    """

    suggestions_created: int
    reviewers_evaluated: int
    source_used: str
    suggestions: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        suggestions_created = self.suggestions_created

        reviewers_evaluated = self.reviewers_evaluated

        source_used = self.source_used

        suggestions = self.suggestions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "suggestions_created": suggestions_created,
                "reviewers_evaluated": reviewers_evaluated,
                "source_used": source_used,
                "suggestions": suggestions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        suggestions_created = d.pop("suggestions_created")

        reviewers_evaluated = d.pop("reviewers_evaluated")

        source_used = d.pop("source_used")

        suggestions = cast(list[str], d.pop("suggestions"))

        generate_suggestions_response = cls(
            suggestions_created=suggestions_created,
            reviewers_evaluated=reviewers_evaluated,
            source_used=source_used,
            suggestions=suggestions,
        )

        generate_suggestions_response.additional_properties = d
        return generate_suggestions_response

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
