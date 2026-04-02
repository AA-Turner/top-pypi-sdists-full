import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.reviewer_suggestion_status_enum import ReviewerSuggestionStatusEnum
from ..models.source_type_enum import SourceTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewerSuggestion")


@_attrs_define
class ReviewerSuggestion:
    """
    Attributes:
        url (str):
        uuid (UUID):
        call (str):
        call_uuid (UUID):
        call_name (str):
        reviewer (str):
        reviewer_uuid (UUID):
        reviewer_name (str):
        reviewer_email (str):
        reviewer_biography (str): Professional biography / summary
        affinity_score (float): Combined affinity score (0-1)
        keyword_score (Union[None, float]): Keyword matching score
        text_score (Union[None, float]): TF-IDF text similarity score
        status_display (str):
        reviewed_by (Union[None, str]):
        reviewed_by_name (str):
        reviewed_at (Union[None, datetime.datetime]):
        matched_keywords (Any): Keywords from reviewer's expertise that matched the source text
        top_matching_proposals (Any): Top proposals with highest affinity: [{uuid, name, slug, affinity}, ...]
        source_type (SourceTypeEnum):
        source_type_display (str):
        created (datetime.datetime):
        status (Union[Unset, ReviewerSuggestionStatusEnum]):
        rejection_reason (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    call: str
    call_uuid: UUID
    call_name: str
    reviewer: str
    reviewer_uuid: UUID
    reviewer_name: str
    reviewer_email: str
    reviewer_biography: str
    affinity_score: float
    keyword_score: Union[None, float]
    text_score: Union[None, float]
    status_display: str
    reviewed_by: Union[None, str]
    reviewed_by_name: str
    reviewed_at: Union[None, datetime.datetime]
    matched_keywords: Any
    top_matching_proposals: Any
    source_type: SourceTypeEnum
    source_type_display: str
    created: datetime.datetime
    status: Union[Unset, ReviewerSuggestionStatusEnum] = UNSET
    rejection_reason: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        call = self.call

        call_uuid = str(self.call_uuid)

        call_name = self.call_name

        reviewer = self.reviewer

        reviewer_uuid = str(self.reviewer_uuid)

        reviewer_name = self.reviewer_name

        reviewer_email = self.reviewer_email

        reviewer_biography = self.reviewer_biography

        affinity_score = self.affinity_score

        keyword_score: Union[None, float]
        keyword_score = self.keyword_score

        text_score: Union[None, float]
        text_score = self.text_score

        status_display = self.status_display

        reviewed_by: Union[None, str]
        reviewed_by = self.reviewed_by

        reviewed_by_name = self.reviewed_by_name

        reviewed_at: Union[None, str]
        if isinstance(self.reviewed_at, datetime.datetime):
            reviewed_at = self.reviewed_at.isoformat()
        else:
            reviewed_at = self.reviewed_at

        matched_keywords = self.matched_keywords

        top_matching_proposals = self.top_matching_proposals

        source_type = self.source_type.value

        source_type_display = self.source_type_display

        created = self.created.isoformat()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        rejection_reason = self.rejection_reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "call": call,
                "call_uuid": call_uuid,
                "call_name": call_name,
                "reviewer": reviewer,
                "reviewer_uuid": reviewer_uuid,
                "reviewer_name": reviewer_name,
                "reviewer_email": reviewer_email,
                "reviewer_biography": reviewer_biography,
                "affinity_score": affinity_score,
                "keyword_score": keyword_score,
                "text_score": text_score,
                "status_display": status_display,
                "reviewed_by": reviewed_by,
                "reviewed_by_name": reviewed_by_name,
                "reviewed_at": reviewed_at,
                "matched_keywords": matched_keywords,
                "top_matching_proposals": top_matching_proposals,
                "source_type": source_type,
                "source_type_display": source_type_display,
                "created": created,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if rejection_reason is not UNSET:
            field_dict["rejection_reason"] = rejection_reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        call = d.pop("call")

        call_uuid = UUID(d.pop("call_uuid"))

        call_name = d.pop("call_name")

        reviewer = d.pop("reviewer")

        reviewer_uuid = UUID(d.pop("reviewer_uuid"))

        reviewer_name = d.pop("reviewer_name")

        reviewer_email = d.pop("reviewer_email")

        reviewer_biography = d.pop("reviewer_biography")

        affinity_score = d.pop("affinity_score")

        def _parse_keyword_score(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        keyword_score = _parse_keyword_score(d.pop("keyword_score"))

        def _parse_text_score(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        text_score = _parse_text_score(d.pop("text_score"))

        status_display = d.pop("status_display")

        def _parse_reviewed_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reviewed_by = _parse_reviewed_by(d.pop("reviewed_by"))

        reviewed_by_name = d.pop("reviewed_by_name")

        def _parse_reviewed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reviewed_at_type_0 = isoparse(data)

                return reviewed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        reviewed_at = _parse_reviewed_at(d.pop("reviewed_at"))

        matched_keywords = d.pop("matched_keywords")

        top_matching_proposals = d.pop("top_matching_proposals")

        source_type = SourceTypeEnum(d.pop("source_type"))

        source_type_display = d.pop("source_type_display")

        created = isoparse(d.pop("created"))

        _status = d.pop("status", UNSET)
        status: Union[Unset, ReviewerSuggestionStatusEnum]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ReviewerSuggestionStatusEnum(_status)

        rejection_reason = d.pop("rejection_reason", UNSET)

        reviewer_suggestion = cls(
            url=url,
            uuid=uuid,
            call=call,
            call_uuid=call_uuid,
            call_name=call_name,
            reviewer=reviewer,
            reviewer_uuid=reviewer_uuid,
            reviewer_name=reviewer_name,
            reviewer_email=reviewer_email,
            reviewer_biography=reviewer_biography,
            affinity_score=affinity_score,
            keyword_score=keyword_score,
            text_score=text_score,
            status_display=status_display,
            reviewed_by=reviewed_by,
            reviewed_by_name=reviewed_by_name,
            reviewed_at=reviewed_at,
            matched_keywords=matched_keywords,
            top_matching_proposals=top_matching_proposals,
            source_type=source_type,
            source_type_display=source_type_display,
            created=created,
            status=status,
            rejection_reason=rejection_reason,
        )

        reviewer_suggestion.additional_properties = d
        return reviewer_suggestion

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
