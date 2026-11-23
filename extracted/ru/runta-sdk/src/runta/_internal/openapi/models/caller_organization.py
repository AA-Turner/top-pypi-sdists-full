from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.organization_role import OrganizationRole

T = TypeVar("T", bound="CallerOrganization")


@_attrs_define
class CallerOrganization:
    """An organization the device credential can select.

    Attributes:
        id (str):
        name (str):
        slug (str):
        role (OrganizationRole): Role granted to the caller in the current organization.
        current (bool): True when this is the organization the credential acts in.
    """

    id: str
    name: str
    slug: str
    role: OrganizationRole
    current: bool

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        slug = self.slug

        role = self.role.value

        current = self.current

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "name": name,
                "slug": slug,
                "role": role,
                "current": current,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        slug = d.pop("slug")

        role = OrganizationRole(d.pop("role"))

        current = d.pop("current")

        caller_organization = cls(
            id=id,
            name=name,
            slug=slug,
            role=role,
            current=current,
        )

        return caller_organization
