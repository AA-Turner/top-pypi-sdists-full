from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProjectDigestPreviewResponse")


@_attrs_define
class ProjectDigestPreviewResponse:
    """
    Attributes:
        subject (str):
        html_body (str):
        text_body (str):
    """

    subject: str
    html_body: str
    text_body: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        subject = self.subject

        html_body = self.html_body

        text_body = self.text_body

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "subject": subject,
                "html_body": html_body,
                "text_body": text_body,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        subject = d.pop("subject")

        html_body = d.pop("html_body")

        text_body = d.pop("text_body")

        project_digest_preview_response = cls(
            subject=subject,
            html_body=html_body,
            text_body=text_body,
        )

        project_digest_preview_response.additional_properties = d
        return project_digest_preview_response

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
