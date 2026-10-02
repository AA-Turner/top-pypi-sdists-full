import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="RecentTicket")


@_attrs_define
class RecentTicket:
    """
    Attributes:
        uuid (UUID):
        key (str):
        summary (str):
        status (str):
        created (datetime.datetime):
    """

    uuid: UUID
    key: str
    summary: str
    status: str
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        key = self.key

        summary = self.summary

        status = self.status

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "key": key,
                "summary": summary,
                "status": status,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        key = d.pop("key")

        summary = d.pop("summary")

        status = d.pop("status")

        created = isoparse(d.pop("created"))

        recent_ticket = cls(
            uuid=uuid,
            key=key,
            summary=summary,
            status=status,
            created=created,
        )

        recent_ticket.additional_properties = d
        return recent_ticket

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
