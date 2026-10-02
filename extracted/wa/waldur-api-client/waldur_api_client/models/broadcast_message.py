import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.broadcast_message_state_enum import BroadcastMessageStateEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.broadcast_message_emails import BroadcastMessageEmails
    from ..models.query_output import QueryOutput


T = TypeVar("T", bound="BroadcastMessage")


@_attrs_define
class BroadcastMessage:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        subject (Union[Unset, str]):
        body (Union[Unset, str]):
        query (Union[Unset, QueryOutput]):
        author_full_name (Union[Unset, str]):
        emails (Union[Unset, BroadcastMessageEmails]):
        state (Union[Unset, BroadcastMessageStateEnum]):
        send_at (Union[None, Unset, datetime.date]):
    """

    uuid: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    subject: Union[Unset, str] = UNSET
    body: Union[Unset, str] = UNSET
    query: Union[Unset, "QueryOutput"] = UNSET
    author_full_name: Union[Unset, str] = UNSET
    emails: Union[Unset, "BroadcastMessageEmails"] = UNSET
    state: Union[Unset, BroadcastMessageStateEnum] = UNSET
    send_at: Union[None, Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        subject = self.subject

        body = self.body

        query: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.query, Unset):
            query = self.query.to_dict()

        author_full_name = self.author_full_name

        emails: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.emails, Unset):
            emails = self.emails.to_dict()

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        send_at: Union[None, Unset, str]
        if isinstance(self.send_at, Unset):
            send_at = UNSET
        elif isinstance(self.send_at, datetime.date):
            send_at = self.send_at.isoformat()
        else:
            send_at = self.send_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if created is not UNSET:
            field_dict["created"] = created
        if subject is not UNSET:
            field_dict["subject"] = subject
        if body is not UNSET:
            field_dict["body"] = body
        if query is not UNSET:
            field_dict["query"] = query
        if author_full_name is not UNSET:
            field_dict["author_full_name"] = author_full_name
        if emails is not UNSET:
            field_dict["emails"] = emails
        if state is not UNSET:
            field_dict["state"] = state
        if send_at is not UNSET:
            field_dict["send_at"] = send_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.broadcast_message_emails import BroadcastMessageEmails
        from ..models.query_output import QueryOutput

        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        subject = d.pop("subject", UNSET)

        body = d.pop("body", UNSET)

        _query = d.pop("query", UNSET)
        query: Union[Unset, QueryOutput]
        if isinstance(_query, Unset):
            query = UNSET
        else:
            query = QueryOutput.from_dict(_query)

        author_full_name = d.pop("author_full_name", UNSET)

        _emails = d.pop("emails", UNSET)
        emails: Union[Unset, BroadcastMessageEmails]
        if isinstance(_emails, Unset):
            emails = UNSET
        else:
            emails = BroadcastMessageEmails.from_dict(_emails)

        _state = d.pop("state", UNSET)
        state: Union[Unset, BroadcastMessageStateEnum]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = BroadcastMessageStateEnum(_state)

        def _parse_send_at(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                send_at_type_0 = isoparse(data).date()

                return send_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        send_at = _parse_send_at(d.pop("send_at", UNSET))

        broadcast_message = cls(
            uuid=uuid,
            created=created,
            subject=subject,
            body=body,
            query=query,
            author_full_name=author_full_name,
            emails=emails,
            state=state,
            send_at=send_at,
        )

        broadcast_message.additional_properties = d
        return broadcast_message

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
