from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_membership_role import WorkspaceMembershipRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmailSubscriptionUpsert")


@_attrs_define
class EmailSubscriptionUpsert:
    """
    Attributes:
        is_enabled (bool): Whether the email channel should deliver
        extra_emails (list[str] | Unset): Deliver to these literal addresses; at most 10
        include_all_members (bool | Unset): Deliver to every member of the workspace Default: False.
        roles (list[WorkspaceMembershipRole] | Unset): Deliver to members holding any of these roles
    """

    is_enabled: bool
    extra_emails: list[str] | Unset = UNSET
    include_all_members: bool | Unset = False
    roles: list[WorkspaceMembershipRole] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_enabled = self.is_enabled

        extra_emails: list[str] | Unset = UNSET
        if not isinstance(self.extra_emails, Unset):
            extra_emails = self.extra_emails

        include_all_members = self.include_all_members

        roles: list[str] | Unset = UNSET
        if not isinstance(self.roles, Unset):
            roles = []
            for roles_item_data in self.roles:
                roles_item = roles_item_data.value
                roles.append(roles_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_enabled": is_enabled,
            }
        )
        if extra_emails is not UNSET:
            field_dict["extra_emails"] = extra_emails
        if include_all_members is not UNSET:
            field_dict["include_all_members"] = include_all_members
        if roles is not UNSET:
            field_dict["roles"] = roles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_enabled = d.pop("is_enabled")

        extra_emails = cast(list[str], d.pop("extra_emails", UNSET))

        include_all_members = d.pop("include_all_members", UNSET)

        _roles = d.pop("roles", UNSET)
        roles: list[WorkspaceMembershipRole] | Unset = UNSET
        if _roles is not UNSET:
            roles = []
            for roles_item_data in _roles:
                roles_item = WorkspaceMembershipRole(roles_item_data)

                roles.append(roles_item)

        email_subscription_upsert = cls(
            is_enabled=is_enabled,
            extra_emails=extra_emails,
            include_all_members=include_all_members,
            roles=roles,
        )

        email_subscription_upsert.additional_properties = d
        return email_subscription_upsert

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
