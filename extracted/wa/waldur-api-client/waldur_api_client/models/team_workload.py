from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TeamWorkload")


@_attrs_define
class TeamWorkload:
    """
    Attributes:
        uuid (UUID):
        user_full_name (str):
        open_ticket_count (int):
        max_open_tickets (int):
        has_capacity (bool):
    """

    uuid: UUID
    user_full_name: str
    open_ticket_count: int
    max_open_tickets: int
    has_capacity: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        user_full_name = self.user_full_name

        open_ticket_count = self.open_ticket_count

        max_open_tickets = self.max_open_tickets

        has_capacity = self.has_capacity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "user_full_name": user_full_name,
                "open_ticket_count": open_ticket_count,
                "max_open_tickets": max_open_tickets,
                "has_capacity": has_capacity,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        user_full_name = d.pop("user_full_name")

        open_ticket_count = d.pop("open_ticket_count")

        max_open_tickets = d.pop("max_open_tickets")

        has_capacity = d.pop("has_capacity")

        team_workload = cls(
            uuid=uuid,
            user_full_name=user_full_name,
            open_ticket_count=open_ticket_count,
            max_open_tickets=max_open_tickets,
            has_capacity=has_capacity,
        )

        team_workload.additional_properties = d
        return team_workload

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
