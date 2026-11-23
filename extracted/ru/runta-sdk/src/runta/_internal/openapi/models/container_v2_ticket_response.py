from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ContainerV2TicketResponse")


@_attrs_define
class ContainerV2TicketResponse:
    """
    Attributes:
        ticket (str):
        expires_at_unix_seconds (int):
    """

    ticket: str
    expires_at_unix_seconds: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ticket = self.ticket

        expires_at_unix_seconds = self.expires_at_unix_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ticket": ticket,
                "expires_at_unix_seconds": expires_at_unix_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ticket = d.pop("ticket")

        expires_at_unix_seconds = d.pop("expires_at_unix_seconds")

        container_v2_ticket_response = cls(
            ticket=ticket,
            expires_at_unix_seconds=expires_at_unix_seconds,
        )

        container_v2_ticket_response.additional_properties = d
        return container_v2_ticket_response

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
