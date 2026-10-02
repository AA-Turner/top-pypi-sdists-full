from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.reviewer_suggestion_status_enum import ReviewerSuggestionStatusEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewerSuggestionRequest")


@_attrs_define
class ReviewerSuggestionRequest:
    """
    Attributes:
        status (Union[Unset, ReviewerSuggestionStatusEnum]):
        rejection_reason (Union[Unset, str]):
    """

    status: Union[Unset, ReviewerSuggestionStatusEnum] = UNSET
    rejection_reason: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        rejection_reason = self.rejection_reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if rejection_reason is not UNSET:
            field_dict["rejection_reason"] = rejection_reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _status = d.pop("status", UNSET)
        status: Union[Unset, ReviewerSuggestionStatusEnum]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ReviewerSuggestionStatusEnum(_status)

        rejection_reason = d.pop("rejection_reason", UNSET)

        reviewer_suggestion_request = cls(
            status=status,
            rejection_reason=rejection_reason,
        )

        reviewer_suggestion_request.additional_properties = d
        return reviewer_suggestion_request

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
