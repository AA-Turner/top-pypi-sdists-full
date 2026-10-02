import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.provider_support_user_role_enum import ProviderSupportUserRoleEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProviderSupportUser")


@_attrs_define
class ProviderSupportUser:
    """
    Attributes:
        url (str):
        uuid (UUID):
        user (str):
        user_full_name (str):
        user_email (str):
        provider_helpdesk (UUID):
        open_ticket_count (int):
        has_capacity (bool):
        created (datetime.datetime):
        modified (datetime.datetime):
        role (Union[Unset, ProviderSupportUserRoleEnum]):
        is_active (Union[Unset, bool]):
        skills (Union[Unset, list[str]]): List of skill tags for routing.
        max_open_tickets (Union[Unset, int]): Maximum number of open tickets this user can handle.
    """

    url: str
    uuid: UUID
    user: str
    user_full_name: str
    user_email: str
    provider_helpdesk: UUID
    open_ticket_count: int
    has_capacity: bool
    created: datetime.datetime
    modified: datetime.datetime
    role: Union[Unset, ProviderSupportUserRoleEnum] = UNSET
    is_active: Union[Unset, bool] = UNSET
    skills: Union[Unset, list[str]] = UNSET
    max_open_tickets: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        user = self.user

        user_full_name = self.user_full_name

        user_email = self.user_email

        provider_helpdesk = str(self.provider_helpdesk)

        open_ticket_count = self.open_ticket_count

        has_capacity = self.has_capacity

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        is_active = self.is_active

        skills: Union[Unset, list[str]] = UNSET
        if not isinstance(self.skills, Unset):
            skills = self.skills

        max_open_tickets = self.max_open_tickets

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "user": user,
                "user_full_name": user_full_name,
                "user_email": user_email,
                "provider_helpdesk": provider_helpdesk,
                "open_ticket_count": open_ticket_count,
                "has_capacity": has_capacity,
                "created": created,
                "modified": modified,
            }
        )
        if role is not UNSET:
            field_dict["role"] = role
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if skills is not UNSET:
            field_dict["skills"] = skills
        if max_open_tickets is not UNSET:
            field_dict["max_open_tickets"] = max_open_tickets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        user = d.pop("user")

        user_full_name = d.pop("user_full_name")

        user_email = d.pop("user_email")

        provider_helpdesk = UUID(d.pop("provider_helpdesk"))

        open_ticket_count = d.pop("open_ticket_count")

        has_capacity = d.pop("has_capacity")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        _role = d.pop("role", UNSET)
        role: Union[Unset, ProviderSupportUserRoleEnum]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = ProviderSupportUserRoleEnum(_role)

        is_active = d.pop("is_active", UNSET)

        skills = cast(list[str], d.pop("skills", UNSET))

        max_open_tickets = d.pop("max_open_tickets", UNSET)

        provider_support_user = cls(
            url=url,
            uuid=uuid,
            user=user,
            user_full_name=user_full_name,
            user_email=user_email,
            provider_helpdesk=provider_helpdesk,
            open_ticket_count=open_ticket_count,
            has_capacity=has_capacity,
            created=created,
            modified=modified,
            role=role,
            is_active=is_active,
            skills=skills,
            max_open_tickets=max_open_tickets,
        )

        provider_support_user.additional_properties = d
        return provider_support_user

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
