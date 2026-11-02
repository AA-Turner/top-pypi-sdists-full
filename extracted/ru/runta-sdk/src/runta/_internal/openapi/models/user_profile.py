from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.organization_role import OrganizationRole

T = TypeVar("T", bound="UserProfile")


@_attrs_define
class UserProfile:
    """Minimal current-user identity available to user-authorized device clients.

    Attributes:
        user_id (str):
        email (str):
        display_name (None | str):
        organization_id (str): Organization the API key is acting in.
        role (OrganizationRole): Role granted to the caller in the current organization.
        scopes (list[str]): Scopes on the calling API key.
    """

    user_id: str
    email: str
    display_name: None | str
    organization_id: str
    role: OrganizationRole
    scopes: list[str]

    def to_dict(self) -> dict[str, Any]:
        user_id = self.user_id

        email = self.email

        display_name: None | str
        display_name = self.display_name

        organization_id = self.organization_id

        role = self.role.value

        scopes = self.scopes

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "user_id": user_id,
                "email": email,
                "display_name": display_name,
                "organization_id": organization_id,
                "role": role,
                "scopes": scopes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_id = d.pop("user_id")

        email = d.pop("email")

        def _parse_display_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        display_name = _parse_display_name(d.pop("display_name"))

        organization_id = d.pop("organization_id")

        role = OrganizationRole(d.pop("role"))

        scopes = cast(list[str], d.pop("scopes"))

        user_profile = cls(
            user_id=user_id,
            email=email,
            display_name=display_name,
            organization_id=organization_id,
            role=role,
            scopes=scopes,
        )

        return user_profile
