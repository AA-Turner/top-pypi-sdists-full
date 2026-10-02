from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.provider_support_user_role_enum import ProviderSupportUserRoleEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProviderSupportUserRequest")


@_attrs_define
class ProviderSupportUserRequest:
    """
    Attributes:
        user (str):
        provider_helpdesk (UUID):
        role (Union[Unset, ProviderSupportUserRoleEnum]):
        is_active (Union[Unset, bool]):
        skills (Union[Unset, list[str]]): List of skill tags for routing.
        max_open_tickets (Union[Unset, int]): Maximum number of open tickets this user can handle.
    """

    user: str
    provider_helpdesk: UUID
    role: Union[Unset, ProviderSupportUserRoleEnum] = UNSET
    is_active: Union[Unset, bool] = UNSET
    skills: Union[Unset, list[str]] = UNSET
    max_open_tickets: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user = self.user

        provider_helpdesk = str(self.provider_helpdesk)

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
                "user": user,
                "provider_helpdesk": provider_helpdesk,
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
        user = d.pop("user")

        provider_helpdesk = UUID(d.pop("provider_helpdesk"))

        _role = d.pop("role", UNSET)
        role: Union[Unset, ProviderSupportUserRoleEnum]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = ProviderSupportUserRoleEnum(_role)

        is_active = d.pop("is_active", UNSET)

        skills = cast(list[str], d.pop("skills", UNSET))

        max_open_tickets = d.pop("max_open_tickets", UNSET)

        provider_support_user_request = cls(
            user=user,
            provider_helpdesk=provider_helpdesk,
            role=role,
            is_active=is_active,
            skills=skills,
            max_open_tickets=max_open_tickets,
        )

        provider_support_user_request.additional_properties = d
        return provider_support_user_request

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
