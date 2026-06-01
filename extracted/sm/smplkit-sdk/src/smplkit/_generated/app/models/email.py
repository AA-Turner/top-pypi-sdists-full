from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.contact_topic import check_contact_topic
from ..models.contact_topic import ContactTopic
from dateutil.parser import isoparse
from typing import cast
import datetime


T = TypeVar("T", bound="Email")


@_attrs_define
class Email:
    """A contact-us submission. Sending the resource delivers a support
    ticket and an auto-response email; nothing is persisted. The `id`
    returned on the response is a per-request correlation identifier.

        Example:
            {'body': 'Hi, I have a question about the pro plan pricing...', 'topic': 'billing'}

        Attributes:
            topic (ContactTopic): Topic options accepted on contact-us submissions.
            body (str): Free-form text of the message. Trimmed before validation.
            sent_at (datetime.datetime | None | Unset): When the message was accepted by the server.
    """

    topic: ContactTopic
    body: str
    sent_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        topic: str = self.topic

        body = self.body

        sent_at: None | str | Unset
        if isinstance(self.sent_at, Unset):
            sent_at = UNSET
        elif isinstance(self.sent_at, datetime.datetime):
            sent_at = self.sent_at.isoformat()
        else:
            sent_at = self.sent_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topic": topic,
                "body": body,
            }
        )
        if sent_at is not UNSET:
            field_dict["sent_at"] = sent_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        topic = check_contact_topic(d.pop("topic"))

        body = d.pop("body")

        def _parse_sent_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                sent_at_type_0 = isoparse(data)

                return sent_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        sent_at = _parse_sent_at(d.pop("sent_at", UNSET))

        email = cls(
            topic=topic,
            body=body,
            sent_at=sent_at,
        )

        email.additional_properties = d
        return email

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
