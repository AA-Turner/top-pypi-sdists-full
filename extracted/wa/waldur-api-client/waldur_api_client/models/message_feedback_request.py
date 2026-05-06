from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.feedback_category_enum import FeedbackCategoryEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="MessageFeedbackRequest")


@_attrs_define
class MessageFeedbackRequest:
    """
    Attributes:
        score (bool): Feedback score: true=thumbs up, false=thumbs down.
        comment (Union[None, Unset, str]): Optional comment.
        category (Union[FeedbackCategoryEnum, None, Unset]): Optional category tag (only accepted when score=false).
    """

    score: bool
    comment: Union[None, Unset, str] = UNSET
    category: Union[FeedbackCategoryEnum, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        score = self.score

        comment: Union[None, Unset, str]
        if isinstance(self.comment, Unset):
            comment = UNSET
        else:
            comment = self.comment

        category: Union[None, Unset, str]
        if isinstance(self.category, Unset):
            category = UNSET
        elif isinstance(self.category, FeedbackCategoryEnum):
            category = self.category.value
        else:
            category = self.category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "score": score,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        score = d.pop("score")

        def _parse_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment = _parse_comment(d.pop("comment", UNSET))

        def _parse_category(data: object) -> Union[FeedbackCategoryEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                category_type_0 = FeedbackCategoryEnum(data)

                return category_type_0
            except:  # noqa: E722
                pass
            return cast(Union[FeedbackCategoryEnum, None, Unset], data)

        category = _parse_category(d.pop("category", UNSET))

        message_feedback_request = cls(
            score=score,
            comment=comment,
            category=category,
        )

        message_feedback_request.additional_properties = d
        return message_feedback_request

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
