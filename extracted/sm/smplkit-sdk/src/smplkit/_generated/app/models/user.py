from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime


T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """A person with access to one or more accounts in smplkit.

    Example:
        {'account': 'd290f1ee-6c54-4b01-90e6-d701748f0851', 'auth_provider': 'GOOGLE', 'created_at':
            '2026-03-20T11:02:16.616Z', 'display_name': 'Jane Smith', 'email': 'jane@example.com', 'email_verified': True,
            'profile_pic': 'https://lh3.googleusercontent.com/a/example', 'role': 'OWNER'}

    Attributes:
        display_name (str): Human-readable display name shown in the console and on shared resources.
        email (None | str | Unset): Email address used to sign in to the user account.
        profile_pic (None | str | Unset): URL of an external profile picture (e.g. the value supplied by the user's
            identity provider).
        avatar_url (None | str | Unset): Server-generated `data:` URL containing the user's avatar image bytes when one
            has been captured. `null` when no avatar is available — callers should fall back to Gravatar or initials.
        auth_provider (None | str | Unset): Identity provider that authenticates the user, e.g. `google`, `microsoft`,
            or `email`.
        email_verified (bool | Unset): Whether the user has completed email verification. Default: False.
        role (None | str | Unset): Role the user holds in the current account context. One of `OWNER`, `ADMIN`,
            `MEMBER`, or `VIEWER`.
        account (None | str | Unset): UUID of the account the user is acting within.
        created_at (datetime.datetime | None | Unset): When the user record was created.
    """

    display_name: str
    email: None | str | Unset = UNSET
    profile_pic: None | str | Unset = UNSET
    avatar_url: None | str | Unset = UNSET
    auth_provider: None | str | Unset = UNSET
    email_verified: bool | Unset = False
    role: None | str | Unset = UNSET
    account: None | str | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        email: None | str | Unset
        if isinstance(self.email, Unset):
            email = UNSET
        else:
            email = self.email

        profile_pic: None | str | Unset
        if isinstance(self.profile_pic, Unset):
            profile_pic = UNSET
        else:
            profile_pic = self.profile_pic

        avatar_url: None | str | Unset
        if isinstance(self.avatar_url, Unset):
            avatar_url = UNSET
        else:
            avatar_url = self.avatar_url

        auth_provider: None | str | Unset
        if isinstance(self.auth_provider, Unset):
            auth_provider = UNSET
        else:
            auth_provider = self.auth_provider

        email_verified = self.email_verified

        role: None | str | Unset
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

        account: None | str | Unset
        if isinstance(self.account, Unset):
            account = UNSET
        else:
            account = self.account

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "display_name": display_name,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if profile_pic is not UNSET:
            field_dict["profile_pic"] = profile_pic
        if avatar_url is not UNSET:
            field_dict["avatar_url"] = avatar_url
        if auth_provider is not UNSET:
            field_dict["auth_provider"] = auth_provider
        if email_verified is not UNSET:
            field_dict["email_verified"] = email_verified
        if role is not UNSET:
            field_dict["role"] = role
        if account is not UNSET:
            field_dict["account"] = account
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        display_name = d.pop("display_name")

        def _parse_email(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        email = _parse_email(d.pop("email", UNSET))

        def _parse_profile_pic(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        profile_pic = _parse_profile_pic(d.pop("profile_pic", UNSET))

        def _parse_avatar_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        avatar_url = _parse_avatar_url(d.pop("avatar_url", UNSET))

        def _parse_auth_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        auth_provider = _parse_auth_provider(d.pop("auth_provider", UNSET))

        email_verified = d.pop("email_verified", UNSET)

        def _parse_role(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        role = _parse_role(d.pop("role", UNSET))

        def _parse_account(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        account = _parse_account(d.pop("account", UNSET))

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

        user = cls(
            display_name=display_name,
            email=email,
            profile_pic=profile_pic,
            avatar_url=avatar_url,
            auth_provider=auth_provider,
            email_verified=email_verified,
            role=role,
            account=account,
            created_at=created_at,
        )

        user.additional_properties = d
        return user

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
