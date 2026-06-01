from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="InvitationCreateItem")


@_attrs_define
class InvitationCreateItem:
    """One invitation in a bulk-create request.

    Example:
        {'email': 'alice@example.com', 'groups': ['production_stewards'], 'role': 'MEMBER'}

    Attributes:
        email (str): Email address to send the invitation to.
        role (str | Unset): Role to assign on acceptance. One of `ADMIN`, `MEMBER`, or `VIEWER`. `OWNER` cannot be
            assigned via invitation. Case-insensitive on input. Default: 'MEMBER'.
        groups (list[str] | None | Unset): Optional list of Environment Access Group ids to add the invitee to on
            acceptance. Every accepted invitation also yields the reserved `default` membership, regardless of this field.
            Unknown group ids are rejected at create time with `422`.
    """

    email: str
    role: str | Unset = "MEMBER"
    groups: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        role = self.role

        groups: list[str] | None | Unset
        if isinstance(self.groups, Unset):
            groups = UNSET
        elif isinstance(self.groups, list):
            groups = self.groups

        else:
            groups = self.groups

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
            }
        )
        if role is not UNSET:
            field_dict["role"] = role
        if groups is not UNSET:
            field_dict["groups"] = groups

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        role = d.pop("role", UNSET)

        def _parse_groups(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                groups_type_0 = cast(list[str], data)

                return groups_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        groups = _parse_groups(d.pop("groups", UNSET))

        invitation_create_item = cls(
            email=email,
            role=role,
            groups=groups,
        )

        invitation_create_item.additional_properties = d
        return invitation_create_item

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
