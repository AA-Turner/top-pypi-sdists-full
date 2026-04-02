from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.jira_issue_fields_request_comment import JiraIssueFieldsRequestComment
    from ..models.jira_issue_project_request import JiraIssueProjectRequest


T = TypeVar("T", bound="JiraIssueFieldsRequest")


@_attrs_define
class JiraIssueFieldsRequest:
    """
    Attributes:
        project (JiraIssueProjectRequest):
        comment (Union[Unset, JiraIssueFieldsRequestComment]):
    """

    project: "JiraIssueProjectRequest"
    comment: Union[Unset, "JiraIssueFieldsRequestComment"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = self.project.to_dict()

        comment: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.comment, Unset):
            comment = self.comment.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project": project,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.jira_issue_fields_request_comment import JiraIssueFieldsRequestComment
        from ..models.jira_issue_project_request import JiraIssueProjectRequest

        d = dict(src_dict)
        project = JiraIssueProjectRequest.from_dict(d.pop("project"))

        _comment = d.pop("comment", UNSET)
        comment: Union[Unset, JiraIssueFieldsRequestComment]
        if isinstance(_comment, Unset):
            comment = UNSET
        else:
            comment = JiraIssueFieldsRequestComment.from_dict(_comment)

        jira_issue_fields_request = cls(
            project=project,
            comment=comment,
        )

        jira_issue_fields_request.additional_properties = d
        return jira_issue_fields_request

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
