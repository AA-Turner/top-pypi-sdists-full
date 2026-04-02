from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WaldurFieldSuggestion")


@_attrs_define
class WaldurFieldSuggestion:
    """
    Attributes:
        field (str): Waldur User model field name
        description (str): Human-readable field description
        suggested_claims (list[str]): OIDC claims that could map to this field, ordered by likelihood
        available_claims (list[str]): Claims from this IdP that match the suggestions
    """

    field: str
    description: str
    suggested_claims: list[str]
    available_claims: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        description = self.description

        suggested_claims = self.suggested_claims

        available_claims = self.available_claims

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field": field,
                "description": description,
                "suggested_claims": suggested_claims,
                "available_claims": available_claims,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field = d.pop("field")

        description = d.pop("description")

        suggested_claims = cast(list[str], d.pop("suggested_claims"))

        available_claims = cast(list[str], d.pop("available_claims"))

        waldur_field_suggestion = cls(
            field=field,
            description=description,
            suggested_claims=suggested_claims,
            available_claims=available_claims,
        )

        waldur_field_suggestion.additional_properties = d
        return waldur_field_suggestion

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
