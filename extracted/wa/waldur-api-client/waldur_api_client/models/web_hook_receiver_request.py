from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.jira_changelog_request import JiraChangelogRequest
    from ..models.jira_comment_request import JiraCommentRequest
    from ..models.jira_issue_request import JiraIssueRequest


T = TypeVar("T", bound="WebHookReceiverRequest")


@_attrs_define
class WebHookReceiverRequest:
    """
    Attributes:
        webhook_event (str):
        issue (JiraIssueRequest):
        comment (Union[Unset, JiraCommentRequest]):
        changelog (Union[Unset, JiraChangelogRequest]):
        issue_event_type_name (Union[Unset, str]):
    """

    webhook_event: str
    issue: "JiraIssueRequest"
    comment: Union[Unset, "JiraCommentRequest"] = UNSET
    changelog: Union[Unset, "JiraChangelogRequest"] = UNSET
    issue_event_type_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        webhook_event = self.webhook_event

        issue = self.issue.to_dict()

        comment: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.comment, Unset):
            comment = self.comment.to_dict()

        changelog: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.changelog, Unset):
            changelog = self.changelog.to_dict()

        issue_event_type_name = self.issue_event_type_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "webhookEvent": webhook_event,
                "issue": issue,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment
        if changelog is not UNSET:
            field_dict["changelog"] = changelog
        if issue_event_type_name is not UNSET:
            field_dict["issue_event_type_name"] = issue_event_type_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.jira_changelog_request import JiraChangelogRequest
        from ..models.jira_comment_request import JiraCommentRequest
        from ..models.jira_issue_request import JiraIssueRequest

        d = dict(src_dict)
        webhook_event = d.pop("webhookEvent")

        issue = JiraIssueRequest.from_dict(d.pop("issue"))

        _comment = d.pop("comment", UNSET)
        comment: Union[Unset, JiraCommentRequest]
        if isinstance(_comment, Unset):
            comment = UNSET
        else:
            comment = JiraCommentRequest.from_dict(_comment)

        _changelog = d.pop("changelog", UNSET)
        changelog: Union[Unset, JiraChangelogRequest]
        if isinstance(_changelog, Unset):
            changelog = UNSET
        else:
            changelog = JiraChangelogRequest.from_dict(_changelog)

        issue_event_type_name = d.pop("issue_event_type_name", UNSET)

        web_hook_receiver_request = cls(
            webhook_event=webhook_event,
            issue=issue,
            comment=comment,
            changelog=changelog,
            issue_event_type_name=issue_event_type_name,
        )

        web_hook_receiver_request.additional_properties = d
        return web_hook_receiver_request

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
