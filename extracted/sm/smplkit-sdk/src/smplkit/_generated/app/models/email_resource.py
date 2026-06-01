from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.email_resource_type import check_email_resource_type
from ..models.email_resource_type import EmailResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.email import Email


T = TypeVar("T", bound="EmailResource")


@_attrs_define
class EmailResource:
    """JSON:API resource envelope for a contact-us submission.

    `id` must not be specified for create requests (the server assigns it).

        Example:
            {'attributes': {'body': 'Hi, I have a question about the pro plan pricing...', 'sent_at':
                '2026-04-22T14:32:01.234Z', 'topic': 'billing'}, 'id': 'd4e5f6a7-b8c9-0123-defa-234567890123', 'type': 'email'}

        Attributes:
            type_ (EmailResourceType):
            attributes (Email): A contact-us submission. Sending the resource delivers a support
                ticket and an auto-response email; nothing is persisted. The `id`
                returned on the response is a per-request correlation identifier. Example: {'body': 'Hi, I have a question about
                the pro plan pricing...', 'topic': 'billing'}.
            id (None | str | Unset):
    """

    type_: EmailResourceType
    attributes: Email
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.email import Email

        d = dict(src_dict)
        type_ = check_email_resource_type(d.pop("type"))

        attributes = Email.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        email_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        email_resource.additional_properties = d
        return email_resource

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
