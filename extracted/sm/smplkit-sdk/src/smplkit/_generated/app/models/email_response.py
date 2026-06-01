from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.email_resource import EmailResource


T = TypeVar("T", bound="EmailResponse")


@_attrs_define
class EmailResponse:
    """JSON:API single-resource response envelope for a contact-us message.

    Attributes:
        data (EmailResource): JSON:API resource envelope for a contact-us submission.

            `id` must not be specified for create requests (the server assigns it). Example: {'attributes': {'body': 'Hi, I
            have a question about the pro plan pricing...', 'sent_at': '2026-04-22T14:32:01.234Z', 'topic': 'billing'},
            'id': 'd4e5f6a7-b8c9-0123-defa-234567890123', 'type': 'email'}.
    """

    data: EmailResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.email_resource import EmailResource

        d = dict(src_dict)
        data = EmailResource.from_dict(d.pop("data"))

        email_response = cls(
            data=data,
        )

        email_response.additional_properties = d
        return email_response

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
