from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blank_enum import BlankEnum
from ..models.feedback_category_enum import FeedbackCategoryEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnonymousChatFeedbackRequestRequest")


@_attrs_define
class AnonymousChatFeedbackRequestRequest:
    """
    Attributes:
        interaction_uuid (UUID): UUID of the interaction the feedback is about (from the streaming `m` frame).
        feedback_token (str): HMAC-bound bearer issued in the streaming `m` frame.
        score (int): +1 thumbs-up or -1 thumbs-down (0 not accepted).
        comment (Union[None, Unset, str]): Optional free-text comment. Default: ''.
        category (Union[BlankEnum, FeedbackCategoryEnum, None, Unset]): Required when score == -1; rejected when score
            == 1. Default: BlankEnum.VALUE_0.
    """

    interaction_uuid: UUID
    feedback_token: str
    score: int
    comment: Union[None, Unset, str] = ""
    category: Union[BlankEnum, FeedbackCategoryEnum, None, Unset] = BlankEnum.VALUE_0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        interaction_uuid = str(self.interaction_uuid)

        feedback_token = self.feedback_token

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
        elif isinstance(self.category, BlankEnum):
            category = self.category.value
        else:
            category = self.category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "interaction_uuid": interaction_uuid,
                "feedback_token": feedback_token,
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
        interaction_uuid = UUID(d.pop("interaction_uuid"))

        feedback_token = d.pop("feedback_token")

        score = d.pop("score")

        def _parse_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment = _parse_comment(d.pop("comment", UNSET))

        def _parse_category(data: object) -> Union[BlankEnum, FeedbackCategoryEnum, None, Unset]:
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
            try:
                if not isinstance(data, str):
                    raise TypeError()
                category_type_1 = BlankEnum(data)

                return category_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BlankEnum, FeedbackCategoryEnum, None, Unset], data)

        category = _parse_category(d.pop("category", UNSET))

        anonymous_chat_feedback_request_request = cls(
            interaction_uuid=interaction_uuid,
            feedback_token=feedback_token,
            score=score,
            comment=comment,
            category=category,
        )

        anonymous_chat_feedback_request_request.additional_properties = d
        return anonymous_chat_feedback_request_request

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
