from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.invitation_duplicate_check_item_request import InvitationDuplicateCheckItemRequest


T = TypeVar("T", bound="InvitationDuplicateCheckRequest")


@_attrs_define
class InvitationDuplicateCheckRequest:
    """
    Attributes:
        scope (str): URL of the scope (Customer or Project) for this invitation list
        invitations (list['InvitationDuplicateCheckItemRequest']):
    """

    scope: str
    invitations: list["InvitationDuplicateCheckItemRequest"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope = self.scope

        invitations = []
        for invitations_item_data in self.invitations:
            invitations_item = invitations_item_data.to_dict()
            invitations.append(invitations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scope": scope,
                "invitations": invitations,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.invitation_duplicate_check_item_request import InvitationDuplicateCheckItemRequest

        d = dict(src_dict)
        scope = d.pop("scope")

        invitations = []
        _invitations = d.pop("invitations")
        for invitations_item_data in _invitations:
            invitations_item = InvitationDuplicateCheckItemRequest.from_dict(invitations_item_data)

            invitations.append(invitations_item)

        invitation_duplicate_check_request = cls(
            scope=scope,
            invitations=invitations,
        )

        invitation_duplicate_check_request.additional_properties = d
        return invitation_duplicate_check_request

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
