from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_membership_role import WorkspaceMembershipRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmailActionConfig")


@_attrs_define
class EmailActionConfig:
    """Configuration for email action

    Attributes:
        include_all_members (bool | Unset): Whether to deliver alert notifications to all members of the workspace
            Default: False.
        recipient_payload_fields (list[str] | Unset): Payload fields containing recipient email addresses
        recipients (list[str] | Unset): Explicit email addresses to receive alert notifications
        roles (list[WorkspaceMembershipRole] | Unset): Deliver alert notifications to workspace members holding any of
            these roles
    """

    include_all_members: bool | Unset = False
    recipient_payload_fields: list[str] | Unset = UNSET
    recipients: list[str] | Unset = UNSET
    roles: list[WorkspaceMembershipRole] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        include_all_members = self.include_all_members

        recipient_payload_fields: list[str] | Unset = UNSET
        if not isinstance(self.recipient_payload_fields, Unset):
            recipient_payload_fields = self.recipient_payload_fields

        recipients: list[str] | Unset = UNSET
        if not isinstance(self.recipients, Unset):
            recipients = self.recipients

        roles: list[str] | Unset = UNSET
        if not isinstance(self.roles, Unset):
            roles = []
            for roles_item_data in self.roles:
                roles_item = roles_item_data.value
                roles.append(roles_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if include_all_members is not UNSET:
            field_dict["include_all_members"] = include_all_members
        if recipient_payload_fields is not UNSET:
            field_dict["recipient_payload_fields"] = recipient_payload_fields
        if recipients is not UNSET:
            field_dict["recipients"] = recipients
        if roles is not UNSET:
            field_dict["roles"] = roles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        include_all_members = d.pop("include_all_members", UNSET)

        recipient_payload_fields = cast(
            list[str], d.pop("recipient_payload_fields", UNSET)
        )

        recipients = cast(list[str], d.pop("recipients", UNSET))

        _roles = d.pop("roles", UNSET)
        roles: list[WorkspaceMembershipRole] | Unset = UNSET
        if _roles is not UNSET:
            roles = []
            for roles_item_data in _roles:
                roles_item = WorkspaceMembershipRole(roles_item_data)

                roles.append(roles_item)

        email_action_config = cls(
            include_all_members=include_all_members,
            recipient_payload_fields=recipient_payload_fields,
            recipients=recipients,
            roles=roles,
        )

        email_action_config.additional_properties = d
        return email_action_config

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
