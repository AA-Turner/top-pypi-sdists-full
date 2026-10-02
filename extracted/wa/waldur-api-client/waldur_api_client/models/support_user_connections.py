from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.support_user_attachment_brief import SupportUserAttachmentBrief
    from ..models.support_user_comment_brief import SupportUserCommentBrief
    from ..models.support_user_issue_brief import SupportUserIssueBrief


T = TypeVar("T", bound="SupportUserConnections")


@_attrs_define
class SupportUserConnections:
    """
    Attributes:
        reported_issues (list['SupportUserIssueBrief']):
        assigned_issues (list['SupportUserIssueBrief']):
        comments (list['SupportUserCommentBrief']):
        attachments (list['SupportUserAttachmentBrief']):
    """

    reported_issues: list["SupportUserIssueBrief"]
    assigned_issues: list["SupportUserIssueBrief"]
    comments: list["SupportUserCommentBrief"]
    attachments: list["SupportUserAttachmentBrief"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reported_issues = []
        for reported_issues_item_data in self.reported_issues:
            reported_issues_item = reported_issues_item_data.to_dict()
            reported_issues.append(reported_issues_item)

        assigned_issues = []
        for assigned_issues_item_data in self.assigned_issues:
            assigned_issues_item = assigned_issues_item_data.to_dict()
            assigned_issues.append(assigned_issues_item)

        comments = []
        for comments_item_data in self.comments:
            comments_item = comments_item_data.to_dict()
            comments.append(comments_item)

        attachments = []
        for attachments_item_data in self.attachments:
            attachments_item = attachments_item_data.to_dict()
            attachments.append(attachments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reported_issues": reported_issues,
                "assigned_issues": assigned_issues,
                "comments": comments,
                "attachments": attachments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.support_user_attachment_brief import SupportUserAttachmentBrief
        from ..models.support_user_comment_brief import SupportUserCommentBrief
        from ..models.support_user_issue_brief import SupportUserIssueBrief

        d = dict(src_dict)
        reported_issues = []
        _reported_issues = d.pop("reported_issues")
        for reported_issues_item_data in _reported_issues:
            reported_issues_item = SupportUserIssueBrief.from_dict(reported_issues_item_data)

            reported_issues.append(reported_issues_item)

        assigned_issues = []
        _assigned_issues = d.pop("assigned_issues")
        for assigned_issues_item_data in _assigned_issues:
            assigned_issues_item = SupportUserIssueBrief.from_dict(assigned_issues_item_data)

            assigned_issues.append(assigned_issues_item)

        comments = []
        _comments = d.pop("comments")
        for comments_item_data in _comments:
            comments_item = SupportUserCommentBrief.from_dict(comments_item_data)

            comments.append(comments_item)

        attachments = []
        _attachments = d.pop("attachments")
        for attachments_item_data in _attachments:
            attachments_item = SupportUserAttachmentBrief.from_dict(attachments_item_data)

            attachments.append(attachments_item)

        support_user_connections = cls(
            reported_issues=reported_issues,
            assigned_issues=assigned_issues,
            comments=comments,
            attachments=attachments,
        )

        support_user_connections.additional_properties = d
        return support_user_connections

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
