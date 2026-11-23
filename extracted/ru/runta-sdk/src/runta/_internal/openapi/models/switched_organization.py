from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SwitchedOrganization")


@_attrs_define
class SwitchedOrganization:
    """
    Attributes:
        access_token (str):
        token_type (str):
        expires_in (int):
        organization_id (str):
        name (str):
        slug (str):
    """

    access_token: str
    token_type: str
    expires_in: int
    organization_id: str
    name: str
    slug: str

    def to_dict(self) -> dict[str, Any]:
        access_token = self.access_token

        token_type = self.token_type

        expires_in = self.expires_in

        organization_id = self.organization_id

        name = self.name

        slug = self.slug

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "access_token": access_token,
                "token_type": token_type,
                "expires_in": expires_in,
                "organization_id": organization_id,
                "name": name,
                "slug": slug,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        access_token = d.pop("access_token")

        token_type = d.pop("token_type")

        expires_in = d.pop("expires_in")

        organization_id = d.pop("organization_id")

        name = d.pop("name")

        slug = d.pop("slug")

        switched_organization = cls(
            access_token=access_token,
            token_type=token_type,
            expires_in=expires_in,
            organization_id=organization_id,
            name=name,
            slug=slug,
        )

        return switched_organization
