import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="EmailLog")


@_attrs_define
class EmailLog:
    """
    Attributes:
        uuid (UUID):
        url (str):
        sent_at (datetime.datetime):
        subject (str):
        body (str):
        emails (list[str]):
    """

    uuid: UUID
    url: str
    sent_at: datetime.datetime
    subject: str
    body: str
    emails: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        sent_at = self.sent_at.isoformat()

        subject = self.subject

        body = self.body

        emails = self.emails

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "sent_at": sent_at,
                "subject": subject,
                "body": body,
                "emails": emails,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        sent_at = isoparse(d.pop("sent_at"))

        subject = d.pop("subject")

        body = d.pop("body")

        emails = cast(list[str], d.pop("emails"))

        email_log = cls(
            uuid=uuid,
            url=url,
            sent_at=sent_at,
            subject=subject,
            body=body,
            emails=emails,
        )

        email_log.additional_properties = d
        return email_log

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
