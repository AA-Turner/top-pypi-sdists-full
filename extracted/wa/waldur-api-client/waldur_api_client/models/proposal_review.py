import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.proposal_review_state_enum import ProposalReviewStateEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProposalReview")


@_attrs_define
class ProposalReview:
    """
    Attributes:
        url (str):
        uuid (UUID):
        proposal (str):
        proposal_name (str):
        proposal_uuid (UUID):
        proposal_slug (str):
        state (ProposalReviewStateEnum):
        review_end_date (datetime.datetime):
        round_uuid (UUID):
        round_name (str):
        round_slug (str):
        round_cutoff_time (datetime.datetime):
        round_start_time (datetime.datetime):
        call_name (str):
        call_uuid (UUID):
        call_slug (str):
        call_managing_organisation_uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        reviewer (Union[Unset, str]):
        reviewer_full_name (Union[Unset, str]):
        reviewer_uuid (Union[Unset, UUID]):
        anonymous_reviewer_name (Union[None, Unset, str]): Generate an anonymous reviewer identifier like 'Reviewer 1',
            'Reviewer 2'.
            Returns None if the review is not associated with a proposal.
        summary_score (Union[Unset, int]):
        summary_public_comment (Union[Unset, str]):
        summary_private_comment (Union[Unset, str]):
        comment_project_title (Union[None, Unset, str]):
        comment_project_summary (Union[None, Unset, str]):
        comment_project_is_confidential (Union[None, Unset, str]):
        comment_project_has_civilian_purpose (Union[None, Unset, str]):
        comment_project_description (Union[None, Unset, str]):
        comment_project_duration (Union[None, Unset, str]):
        comment_project_supporting_documentation (Union[None, Unset, str]):
        comment_resource_requests (Union[None, Unset, str]):
        comment_team (Union[None, Unset, str]):
    """

    url: str
    uuid: UUID
    proposal: str
    proposal_name: str
    proposal_uuid: UUID
    proposal_slug: str
    state: ProposalReviewStateEnum
    review_end_date: datetime.datetime
    round_uuid: UUID
    round_name: str
    round_slug: str
    round_cutoff_time: datetime.datetime
    round_start_time: datetime.datetime
    call_name: str
    call_uuid: UUID
    call_slug: str
    call_managing_organisation_uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    reviewer: Union[Unset, str] = UNSET
    reviewer_full_name: Union[Unset, str] = UNSET
    reviewer_uuid: Union[Unset, UUID] = UNSET
    anonymous_reviewer_name: Union[None, Unset, str] = UNSET
    summary_score: Union[Unset, int] = UNSET
    summary_public_comment: Union[Unset, str] = UNSET
    summary_private_comment: Union[Unset, str] = UNSET
    comment_project_title: Union[None, Unset, str] = UNSET
    comment_project_summary: Union[None, Unset, str] = UNSET
    comment_project_is_confidential: Union[None, Unset, str] = UNSET
    comment_project_has_civilian_purpose: Union[None, Unset, str] = UNSET
    comment_project_description: Union[None, Unset, str] = UNSET
    comment_project_duration: Union[None, Unset, str] = UNSET
    comment_project_supporting_documentation: Union[None, Unset, str] = UNSET
    comment_resource_requests: Union[None, Unset, str] = UNSET
    comment_team: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        proposal = self.proposal

        proposal_name = self.proposal_name

        proposal_uuid = str(self.proposal_uuid)

        proposal_slug = self.proposal_slug

        state = self.state.value

        review_end_date = self.review_end_date.isoformat()

        round_uuid = str(self.round_uuid)

        round_name = self.round_name

        round_slug = self.round_slug

        round_cutoff_time = self.round_cutoff_time.isoformat()

        round_start_time = self.round_start_time.isoformat()

        call_name = self.call_name

        call_uuid = str(self.call_uuid)

        call_slug = self.call_slug

        call_managing_organisation_uuid = str(self.call_managing_organisation_uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        reviewer = self.reviewer

        reviewer_full_name = self.reviewer_full_name

        reviewer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.reviewer_uuid, Unset):
            reviewer_uuid = str(self.reviewer_uuid)

        anonymous_reviewer_name: Union[None, Unset, str]
        if isinstance(self.anonymous_reviewer_name, Unset):
            anonymous_reviewer_name = UNSET
        else:
            anonymous_reviewer_name = self.anonymous_reviewer_name

        summary_score = self.summary_score

        summary_public_comment = self.summary_public_comment

        summary_private_comment = self.summary_private_comment

        comment_project_title: Union[None, Unset, str]
        if isinstance(self.comment_project_title, Unset):
            comment_project_title = UNSET
        else:
            comment_project_title = self.comment_project_title

        comment_project_summary: Union[None, Unset, str]
        if isinstance(self.comment_project_summary, Unset):
            comment_project_summary = UNSET
        else:
            comment_project_summary = self.comment_project_summary

        comment_project_is_confidential: Union[None, Unset, str]
        if isinstance(self.comment_project_is_confidential, Unset):
            comment_project_is_confidential = UNSET
        else:
            comment_project_is_confidential = self.comment_project_is_confidential

        comment_project_has_civilian_purpose: Union[None, Unset, str]
        if isinstance(self.comment_project_has_civilian_purpose, Unset):
            comment_project_has_civilian_purpose = UNSET
        else:
            comment_project_has_civilian_purpose = self.comment_project_has_civilian_purpose

        comment_project_description: Union[None, Unset, str]
        if isinstance(self.comment_project_description, Unset):
            comment_project_description = UNSET
        else:
            comment_project_description = self.comment_project_description

        comment_project_duration: Union[None, Unset, str]
        if isinstance(self.comment_project_duration, Unset):
            comment_project_duration = UNSET
        else:
            comment_project_duration = self.comment_project_duration

        comment_project_supporting_documentation: Union[None, Unset, str]
        if isinstance(self.comment_project_supporting_documentation, Unset):
            comment_project_supporting_documentation = UNSET
        else:
            comment_project_supporting_documentation = self.comment_project_supporting_documentation

        comment_resource_requests: Union[None, Unset, str]
        if isinstance(self.comment_resource_requests, Unset):
            comment_resource_requests = UNSET
        else:
            comment_resource_requests = self.comment_resource_requests

        comment_team: Union[None, Unset, str]
        if isinstance(self.comment_team, Unset):
            comment_team = UNSET
        else:
            comment_team = self.comment_team

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "proposal": proposal,
                "proposal_name": proposal_name,
                "proposal_uuid": proposal_uuid,
                "proposal_slug": proposal_slug,
                "state": state,
                "review_end_date": review_end_date,
                "round_uuid": round_uuid,
                "round_name": round_name,
                "round_slug": round_slug,
                "round_cutoff_time": round_cutoff_time,
                "round_start_time": round_start_time,
                "call_name": call_name,
                "call_uuid": call_uuid,
                "call_slug": call_slug,
                "call_managing_organisation_uuid": call_managing_organisation_uuid,
                "created": created,
                "modified": modified,
            }
        )
        if reviewer is not UNSET:
            field_dict["reviewer"] = reviewer
        if reviewer_full_name is not UNSET:
            field_dict["reviewer_full_name"] = reviewer_full_name
        if reviewer_uuid is not UNSET:
            field_dict["reviewer_uuid"] = reviewer_uuid
        if anonymous_reviewer_name is not UNSET:
            field_dict["anonymous_reviewer_name"] = anonymous_reviewer_name
        if summary_score is not UNSET:
            field_dict["summary_score"] = summary_score
        if summary_public_comment is not UNSET:
            field_dict["summary_public_comment"] = summary_public_comment
        if summary_private_comment is not UNSET:
            field_dict["summary_private_comment"] = summary_private_comment
        if comment_project_title is not UNSET:
            field_dict["comment_project_title"] = comment_project_title
        if comment_project_summary is not UNSET:
            field_dict["comment_project_summary"] = comment_project_summary
        if comment_project_is_confidential is not UNSET:
            field_dict["comment_project_is_confidential"] = comment_project_is_confidential
        if comment_project_has_civilian_purpose is not UNSET:
            field_dict["comment_project_has_civilian_purpose"] = comment_project_has_civilian_purpose
        if comment_project_description is not UNSET:
            field_dict["comment_project_description"] = comment_project_description
        if comment_project_duration is not UNSET:
            field_dict["comment_project_duration"] = comment_project_duration
        if comment_project_supporting_documentation is not UNSET:
            field_dict["comment_project_supporting_documentation"] = comment_project_supporting_documentation
        if comment_resource_requests is not UNSET:
            field_dict["comment_resource_requests"] = comment_resource_requests
        if comment_team is not UNSET:
            field_dict["comment_team"] = comment_team

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        proposal = d.pop("proposal")

        proposal_name = d.pop("proposal_name")

        proposal_uuid = UUID(d.pop("proposal_uuid"))

        proposal_slug = d.pop("proposal_slug")

        state = ProposalReviewStateEnum(d.pop("state"))

        review_end_date = isoparse(d.pop("review_end_date"))

        round_uuid = UUID(d.pop("round_uuid"))

        round_name = d.pop("round_name")

        round_slug = d.pop("round_slug")

        round_cutoff_time = isoparse(d.pop("round_cutoff_time"))

        round_start_time = isoparse(d.pop("round_start_time"))

        call_name = d.pop("call_name")

        call_uuid = UUID(d.pop("call_uuid"))

        call_slug = d.pop("call_slug")

        call_managing_organisation_uuid = UUID(d.pop("call_managing_organisation_uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        reviewer = d.pop("reviewer", UNSET)

        reviewer_full_name = d.pop("reviewer_full_name", UNSET)

        _reviewer_uuid = d.pop("reviewer_uuid", UNSET)
        reviewer_uuid: Union[Unset, UUID]
        if isinstance(_reviewer_uuid, Unset):
            reviewer_uuid = UNSET
        else:
            reviewer_uuid = UUID(_reviewer_uuid)

        def _parse_anonymous_reviewer_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        anonymous_reviewer_name = _parse_anonymous_reviewer_name(d.pop("anonymous_reviewer_name", UNSET))

        summary_score = d.pop("summary_score", UNSET)

        summary_public_comment = d.pop("summary_public_comment", UNSET)

        summary_private_comment = d.pop("summary_private_comment", UNSET)

        def _parse_comment_project_title(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment_project_title = _parse_comment_project_title(d.pop("comment_project_title", UNSET))

        def _parse_comment_project_summary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment_project_summary = _parse_comment_project_summary(d.pop("comment_project_summary", UNSET))

        def _parse_comment_project_is_confidential(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment_project_is_confidential = _parse_comment_project_is_confidential(
            d.pop("comment_project_is_confidential", UNSET)
        )

        def _parse_comment_project_has_civilian_purpose(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment_project_has_civilian_purpose = _parse_comment_project_has_civilian_purpose(
            d.pop("comment_project_has_civilian_purpose", UNSET)
        )

        def _parse_comment_project_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment_project_description = _parse_comment_project_description(d.pop("comment_project_description", UNSET))

        def _parse_comment_project_duration(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment_project_duration = _parse_comment_project_duration(d.pop("comment_project_duration", UNSET))

        def _parse_comment_project_supporting_documentation(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment_project_supporting_documentation = _parse_comment_project_supporting_documentation(
            d.pop("comment_project_supporting_documentation", UNSET)
        )

        def _parse_comment_resource_requests(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment_resource_requests = _parse_comment_resource_requests(d.pop("comment_resource_requests", UNSET))

        def _parse_comment_team(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment_team = _parse_comment_team(d.pop("comment_team", UNSET))

        proposal_review = cls(
            url=url,
            uuid=uuid,
            proposal=proposal,
            proposal_name=proposal_name,
            proposal_uuid=proposal_uuid,
            proposal_slug=proposal_slug,
            state=state,
            review_end_date=review_end_date,
            round_uuid=round_uuid,
            round_name=round_name,
            round_slug=round_slug,
            round_cutoff_time=round_cutoff_time,
            round_start_time=round_start_time,
            call_name=call_name,
            call_uuid=call_uuid,
            call_slug=call_slug,
            call_managing_organisation_uuid=call_managing_organisation_uuid,
            created=created,
            modified=modified,
            reviewer=reviewer,
            reviewer_full_name=reviewer_full_name,
            reviewer_uuid=reviewer_uuid,
            anonymous_reviewer_name=anonymous_reviewer_name,
            summary_score=summary_score,
            summary_public_comment=summary_public_comment,
            summary_private_comment=summary_private_comment,
            comment_project_title=comment_project_title,
            comment_project_summary=comment_project_summary,
            comment_project_is_confidential=comment_project_is_confidential,
            comment_project_has_civilian_purpose=comment_project_has_civilian_purpose,
            comment_project_description=comment_project_description,
            comment_project_duration=comment_project_duration,
            comment_project_supporting_documentation=comment_project_supporting_documentation,
            comment_resource_requests=comment_resource_requests,
            comment_team=comment_team,
        )

        proposal_review.additional_properties = d
        return proposal_review

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
