from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmailInvitationRequest")


@_attrs_define
class EmailInvitationRequest:
    """
    Attributes:
        email (str): Email address to send the invitation to
        invitation_message (Union[Unset, str]): Custom message to include in invitation email
        max_assignments (Union[Unset, int]):  Default: 5.
    """

    email: str
    invitation_message: Union[Unset, str] = UNSET
    max_assignments: Union[Unset, int] = 5
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        invitation_message = self.invitation_message

        max_assignments = self.max_assignments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
            }
        )
        if invitation_message is not UNSET:
            field_dict["invitation_message"] = invitation_message
        if max_assignments is not UNSET:
            field_dict["max_assignments"] = max_assignments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        invitation_message = d.pop("invitation_message", UNSET)

        max_assignments = d.pop("max_assignments", UNSET)

        email_invitation_request = cls(
            email=email,
            invitation_message=invitation_message,
            max_assignments=max_assignments,
        )

        email_invitation_request.additional_properties = d
        return email_invitation_request

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
