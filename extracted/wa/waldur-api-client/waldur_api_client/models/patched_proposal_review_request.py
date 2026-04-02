from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedProposalReviewRequest")


@_attrs_define
class PatchedProposalReviewRequest:
    """
    Attributes:
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
        field_dict.update({})
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

        patched_proposal_review_request = cls(
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

        patched_proposal_review_request.additional_properties = d
        return patched_proposal_review_request

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
