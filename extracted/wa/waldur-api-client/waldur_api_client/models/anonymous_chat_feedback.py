import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.feedback_category_enum import FeedbackCategoryEnum

T = TypeVar("T", bound="AnonymousChatFeedback")


@_attrs_define
class AnonymousChatFeedback:
    """
    Attributes:
        interaction_uuid (UUID):
        score (Union[None, int]):
        comment (str):
        category (FeedbackCategoryEnum):
        submitted_from_ip (Union[None, str]): An IPv4 or IPv6 address.
        submitted_at (Union[None, datetime.datetime]):
        llm_resolution_score (Union[None, int]):
        llm_intent_category (str):
        llm_hallucination_detected (bool):
        llm_hallucination_details (str):
        llm_summary (str):
        llm_reviewed_at (Union[None, datetime.datetime]):
        llm_judge_input_tokens (int):
        llm_judge_output_tokens (int):
        llm_judge_model (str):
        modified_at (datetime.datetime):
    """

    interaction_uuid: UUID
    score: Union[None, int]
    comment: str
    category: FeedbackCategoryEnum
    submitted_from_ip: Union[None, str]
    submitted_at: Union[None, datetime.datetime]
    llm_resolution_score: Union[None, int]
    llm_intent_category: str
    llm_hallucination_detected: bool
    llm_hallucination_details: str
    llm_summary: str
    llm_reviewed_at: Union[None, datetime.datetime]
    llm_judge_input_tokens: int
    llm_judge_output_tokens: int
    llm_judge_model: str
    modified_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        interaction_uuid = str(self.interaction_uuid)

        score: Union[None, int]
        score = self.score

        comment = self.comment

        category = self.category.value

        submitted_from_ip: Union[None, str]
        submitted_from_ip = self.submitted_from_ip

        submitted_at: Union[None, str]
        if isinstance(self.submitted_at, datetime.datetime):
            submitted_at = self.submitted_at.isoformat()
        else:
            submitted_at = self.submitted_at

        llm_resolution_score: Union[None, int]
        llm_resolution_score = self.llm_resolution_score

        llm_intent_category = self.llm_intent_category

        llm_hallucination_detected = self.llm_hallucination_detected

        llm_hallucination_details = self.llm_hallucination_details

        llm_summary = self.llm_summary

        llm_reviewed_at: Union[None, str]
        if isinstance(self.llm_reviewed_at, datetime.datetime):
            llm_reviewed_at = self.llm_reviewed_at.isoformat()
        else:
            llm_reviewed_at = self.llm_reviewed_at

        llm_judge_input_tokens = self.llm_judge_input_tokens

        llm_judge_output_tokens = self.llm_judge_output_tokens

        llm_judge_model = self.llm_judge_model

        modified_at = self.modified_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "interaction_uuid": interaction_uuid,
                "score": score,
                "comment": comment,
                "category": category,
                "submitted_from_ip": submitted_from_ip,
                "submitted_at": submitted_at,
                "llm_resolution_score": llm_resolution_score,
                "llm_intent_category": llm_intent_category,
                "llm_hallucination_detected": llm_hallucination_detected,
                "llm_hallucination_details": llm_hallucination_details,
                "llm_summary": llm_summary,
                "llm_reviewed_at": llm_reviewed_at,
                "llm_judge_input_tokens": llm_judge_input_tokens,
                "llm_judge_output_tokens": llm_judge_output_tokens,
                "llm_judge_model": llm_judge_model,
                "modified_at": modified_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        interaction_uuid = UUID(d.pop("interaction_uuid"))

        def _parse_score(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        score = _parse_score(d.pop("score"))

        comment = d.pop("comment")

        category = FeedbackCategoryEnum(d.pop("category"))

        def _parse_submitted_from_ip(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        submitted_from_ip = _parse_submitted_from_ip(d.pop("submitted_from_ip"))

        def _parse_submitted_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                submitted_at_type_0 = isoparse(data)

                return submitted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        submitted_at = _parse_submitted_at(d.pop("submitted_at"))

        def _parse_llm_resolution_score(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        llm_resolution_score = _parse_llm_resolution_score(d.pop("llm_resolution_score"))

        llm_intent_category = d.pop("llm_intent_category")

        llm_hallucination_detected = d.pop("llm_hallucination_detected")

        llm_hallucination_details = d.pop("llm_hallucination_details")

        llm_summary = d.pop("llm_summary")

        def _parse_llm_reviewed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                llm_reviewed_at_type_0 = isoparse(data)

                return llm_reviewed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        llm_reviewed_at = _parse_llm_reviewed_at(d.pop("llm_reviewed_at"))

        llm_judge_input_tokens = d.pop("llm_judge_input_tokens")

        llm_judge_output_tokens = d.pop("llm_judge_output_tokens")

        llm_judge_model = d.pop("llm_judge_model")

        modified_at = isoparse(d.pop("modified_at"))

        anonymous_chat_feedback = cls(
            interaction_uuid=interaction_uuid,
            score=score,
            comment=comment,
            category=category,
            submitted_from_ip=submitted_from_ip,
            submitted_at=submitted_at,
            llm_resolution_score=llm_resolution_score,
            llm_intent_category=llm_intent_category,
            llm_hallucination_detected=llm_hallucination_detected,
            llm_hallucination_details=llm_hallucination_details,
            llm_summary=llm_summary,
            llm_reviewed_at=llm_reviewed_at,
            llm_judge_input_tokens=llm_judge_input_tokens,
            llm_judge_output_tokens=llm_judge_output_tokens,
            llm_judge_model=llm_judge_model,
            modified_at=modified_at,
        )

        anonymous_chat_feedback.additional_properties = d
        return anonymous_chat_feedback

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
