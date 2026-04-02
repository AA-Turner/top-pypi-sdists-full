from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedInvitationUpdateRequest")


@_attrs_define
class PatchedInvitationUpdateRequest:
    """
    Attributes:
        email (Union[Unset, str]): Invitation link will be sent to this email. Note that user can accept invitation with
            different email.
        role (Union[Unset, UUID]): UUID of the new role to assign. Must be compatible with the invitation scope.
    """

    email: Union[Unset, str] = UNSET
    role: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = str(self.role)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email", UNSET)

        _role = d.pop("role", UNSET)
        role: Union[Unset, UUID]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = UUID(_role)

        patched_invitation_update_request = cls(
            email=email,
            role=role,
        )

        patched_invitation_update_request.additional_properties = d
        return patched_invitation_update_request

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
