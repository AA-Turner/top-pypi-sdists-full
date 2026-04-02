from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewSubmitRequest")


@_attrs_define
class ReviewSubmitRequest:
    """
    Attributes:
        summary_score (Union[Unset, int]):
        summary_public_comment (Union[Unset, str]):
        summary_private_comment (Union[Unset, str]):
    """

    summary_score: Union[Unset, int] = UNSET
    summary_public_comment: Union[Unset, str] = UNSET
    summary_private_comment: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        summary_score = self.summary_score

        summary_public_comment = self.summary_public_comment

        summary_private_comment = self.summary_private_comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if summary_score is not UNSET:
            field_dict["summary_score"] = summary_score
        if summary_public_comment is not UNSET:
            field_dict["summary_public_comment"] = summary_public_comment
        if summary_private_comment is not UNSET:
            field_dict["summary_private_comment"] = summary_private_comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        summary_score = d.pop("summary_score", UNSET)

        summary_public_comment = d.pop("summary_public_comment", UNSET)

        summary_private_comment = d.pop("summary_private_comment", UNSET)

        review_submit_request = cls(
            summary_score=summary_score,
            summary_public_comment=summary_public_comment,
            summary_private_comment=summary_private_comment,
        )

        review_submit_request.additional_properties = d
        return review_submit_request

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
