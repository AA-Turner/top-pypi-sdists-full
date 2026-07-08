from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateOrganizationInviteResponse409")


@_attrs_define
class CreateOrganizationInviteResponse409:
    """Org Region Required Exception

    Attributes:
        detail (str | Unset):
        extra (Any | Unset): Additional error details (free-form)
        status_code (int | Unset):
    """

    detail: str | Unset = UNSET
    extra: Any | Unset = UNSET
    status_code: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail = self.detail

        extra = self.extra

        status_code = self.status_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if detail is not UNSET:
            field_dict["detail"] = detail
        if extra is not UNSET:
            field_dict["extra"] = extra
        if status_code is not UNSET:
            field_dict["status_code"] = status_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        detail = d.pop("detail", UNSET)

        extra = d.pop("extra", UNSET)

        status_code = d.pop("status_code", UNSET)

        create_organization_invite_response_409 = cls(
            detail=detail,
            extra=extra,
            status_code=status_code,
        )

        create_organization_invite_response_409.additional_properties = d
        return create_organization_invite_response_409

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
