from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MatrixTicketDraftIssue")


@_attrs_define
class MatrixTicketDraftIssue:
    """
    Attributes:
        issue_uuid (str):
        issue_key (str):
        issue_url (str):
    """

    issue_uuid: str
    issue_key: str
    issue_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        issue_uuid = self.issue_uuid

        issue_key = self.issue_key

        issue_url = self.issue_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "issue_uuid": issue_uuid,
                "issue_key": issue_key,
                "issue_url": issue_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        issue_uuid = d.pop("issue_uuid")

        issue_key = d.pop("issue_key")

        issue_url = d.pop("issue_url")

        matrix_ticket_draft_issue = cls(
            issue_uuid=issue_uuid,
            issue_key=issue_key,
            issue_url=issue_url,
        )

        matrix_ticket_draft_issue.additional_properties = d
        return matrix_ticket_draft_issue

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
