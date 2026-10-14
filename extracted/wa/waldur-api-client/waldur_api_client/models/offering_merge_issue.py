from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.offering_merge_issue_details import OfferingMergeIssueDetails


T = TypeVar("T", bound="OfferingMergeIssue")


@_attrs_define
class OfferingMergeIssue:
    """
    Attributes:
        code (str): Machine-readable reason.
        message (str):
        details (OfferingMergeIssueDetails): Issue-specific details: offerings, plans, keys or counts.
    """

    code: str
    message: str
    details: "OfferingMergeIssueDetails"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        details = self.details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
                "details": details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_merge_issue_details import OfferingMergeIssueDetails

        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        details = OfferingMergeIssueDetails.from_dict(d.pop("details"))

        offering_merge_issue = cls(
            code=code,
            message=message,
            details=details,
        )

        offering_merge_issue.additional_properties = d
        return offering_merge_issue

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
