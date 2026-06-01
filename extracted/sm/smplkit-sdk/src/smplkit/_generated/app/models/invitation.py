from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime


T = TypeVar("T", bound="Invitation")


@_attrs_define
class Invitation:
    """An invitation for a person to join an account.

    Invitations carry a time-limited token; the recipient redeems the
    token to become a member of the inviting account at the assigned role.

        Example:
            {'created_at': '2026-03-20T11:02:16.616Z', 'email': 'mike@example.com', 'expires_at':
                '2026-04-20T11:02:16.616Z', 'invited_by': 'd290f1ee-6c54-4b01-90e6-d701748f0851', 'role': 'MEMBER', 'status':
                'PENDING', 'updated_at': '2026-03-20T11:02:16.616Z'}

        Attributes:
            email (None | str | Unset): Email address the invitation was sent to.
            role (None | str | Unset): Role to assign on acceptance. One of `ADMIN`, `MEMBER`, or `VIEWER`.
            status (None | str | Unset): Lifecycle state of the invitation. One of `PENDING`, `ACCEPTED`, `REVOKED`, or
                `EXPIRED`.
            invited_by (None | str | Unset): UUID of the user who sent the invitation.
            groups (list[str] | None | Unset): Environment Access Group ids the invitee will be added to on acceptance, in
                addition to the always-applied `default` group. Empty array or `null` means default-only.
            account_name (None | str | Unset): Name of the account the recipient is being invited to join.
            inviter_display_name (None | str | Unset): Display name of the user who sent the invitation.
            token (None | str | Unset): Single-use token that the recipient redeems to accept the invitation. Echoed on
                responses so the inviting client can construct the acceptance link.
            expires_at (datetime.datetime | None | Unset): When the invitation token stops being redeemable.
            created_at (datetime.datetime | None | Unset): When the invitation was issued.
            updated_at (datetime.datetime | None | Unset): When the invitation record was last modified.
    """

    email: None | str | Unset = UNSET
    role: None | str | Unset = UNSET
    status: None | str | Unset = UNSET
    invited_by: None | str | Unset = UNSET
    groups: list[str] | None | Unset = UNSET
    account_name: None | str | Unset = UNSET
    inviter_display_name: None | str | Unset = UNSET
    token: None | str | Unset = UNSET
    expires_at: datetime.datetime | None | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email: None | str | Unset
        if isinstance(self.email, Unset):
            email = UNSET
        else:
            email = self.email

        role: None | str | Unset
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        invited_by: None | str | Unset
        if isinstance(self.invited_by, Unset):
            invited_by = UNSET
        else:
            invited_by = self.invited_by

        groups: list[str] | None | Unset
        if isinstance(self.groups, Unset):
            groups = UNSET
        elif isinstance(self.groups, list):
            groups = self.groups

        else:
            groups = self.groups

        account_name: None | str | Unset
        if isinstance(self.account_name, Unset):
            account_name = UNSET
        else:
            account_name = self.account_name

        inviter_display_name: None | str | Unset
        if isinstance(self.inviter_display_name, Unset):
            inviter_display_name = UNSET
        else:
            inviter_display_name = self.inviter_display_name

        token: None | str | Unset
        if isinstance(self.token, Unset):
            token = UNSET
        else:
            token = self.token

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if role is not UNSET:
            field_dict["role"] = role
        if status is not UNSET:
            field_dict["status"] = status
        if invited_by is not UNSET:
            field_dict["invited_by"] = invited_by
        if groups is not UNSET:
            field_dict["groups"] = groups
        if account_name is not UNSET:
            field_dict["account_name"] = account_name
        if inviter_display_name is not UNSET:
            field_dict["inviter_display_name"] = inviter_display_name
        if token is not UNSET:
            field_dict["token"] = token
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_email(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        email = _parse_email(d.pop("email", UNSET))

        def _parse_role(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        role = _parse_role(d.pop("role", UNSET))

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_invited_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        invited_by = _parse_invited_by(d.pop("invited_by", UNSET))

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

        def _parse_account_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        account_name = _parse_account_name(d.pop("account_name", UNSET))

        def _parse_inviter_display_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        inviter_display_name = _parse_inviter_display_name(d.pop("inviter_display_name", UNSET))

        def _parse_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        token = _parse_token(d.pop("token", UNSET))

        def _parse_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        invitation = cls(
            email=email,
            role=role,
            status=status,
            invited_by=invited_by,
            groups=groups,
            account_name=account_name,
            inviter_display_name=inviter_display_name,
            token=token,
            expires_at=expires_at,
            created_at=created_at,
            updated_at=updated_at,
        )

        invitation.additional_properties = d
        return invitation

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
