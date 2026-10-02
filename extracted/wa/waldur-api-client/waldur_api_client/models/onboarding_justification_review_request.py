from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OnboardingJustificationReviewRequest")


@_attrs_define
class OnboardingJustificationReviewRequest:
    """
    Attributes:
        staff_notes (Union[Unset, str]): Administrator notes about the review decision
    """

    staff_notes: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        staff_notes = self.staff_notes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if staff_notes is not UNSET:
            field_dict["staff_notes"] = staff_notes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        staff_notes = d.pop("staff_notes", UNSET)

        onboarding_justification_review_request = cls(
            staff_notes=staff_notes,
        )

        onboarding_justification_review_request.additional_properties = d
        return onboarding_justification_review_request

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
