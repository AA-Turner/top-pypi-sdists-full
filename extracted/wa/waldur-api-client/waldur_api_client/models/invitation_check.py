from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InvitationCheck")


@_attrs_define
class InvitationCheck:
    """
    Attributes:
        email (str): Email address to check for existing invitations
        civil_number_required (Union[Unset, bool]): Whether civil number verification is required
    """

    email: str
    civil_number_required: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        civil_number_required = self.civil_number_required

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
            }
        )
        if civil_number_required is not UNSET:
            field_dict["civil_number_required"] = civil_number_required

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        civil_number_required = d.pop("civil_number_required", UNSET)

        invitation_check = cls(
            email=email,
            civil_number_required=civil_number_required,
        )

        invitation_check.additional_properties = d
        return invitation_check

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
