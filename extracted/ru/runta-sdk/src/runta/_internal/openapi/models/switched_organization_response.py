from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.switched_organization import SwitchedOrganization


T = TypeVar("T", bound="SwitchedOrganizationResponse")


@_attrs_define
class SwitchedOrganizationResponse:
    """
    Attributes:
        data (SwitchedOrganization):
    """

    data: SwitchedOrganization

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.switched_organization import SwitchedOrganization

        d = dict(src_dict)
        data = SwitchedOrganization.from_dict(d.pop("data"))

        switched_organization_response = cls(
            data=data,
        )

        return switched_organization_response
