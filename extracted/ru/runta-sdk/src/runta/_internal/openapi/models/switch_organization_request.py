from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SwitchOrganizationRequest")


@_attrs_define
class SwitchOrganizationRequest:
    """
    Attributes:
        organization (str): Organization id or slug.
    """

    organization: str

    def to_dict(self) -> dict[str, Any]:
        organization = self.organization

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "organization": organization,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        organization = d.pop("organization")

        switch_organization_request = cls(
            organization=organization,
        )

        return switch_organization_request
