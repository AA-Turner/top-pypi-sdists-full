from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.jira_issue_fields_request import JiraIssueFieldsRequest


T = TypeVar("T", bound="JiraIssueRequest")


@_attrs_define
class JiraIssueRequest:
    """
    Attributes:
        key (str): Jira issue key
        fields (JiraIssueFieldsRequest):
    """

    key: str
    fields: "JiraIssueFieldsRequest"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        fields = self.fields.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "fields": fields,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.jira_issue_fields_request import JiraIssueFieldsRequest

        d = dict(src_dict)
        key = d.pop("key")

        fields = JiraIssueFieldsRequest.from_dict(d.pop("fields"))

        jira_issue_request = cls(
            key=key,
            fields=fields,
        )

        jira_issue_request.additional_properties = d
        return jira_issue_request

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
