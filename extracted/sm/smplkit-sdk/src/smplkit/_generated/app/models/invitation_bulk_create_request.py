from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.invitation_create_item import InvitationCreateItem


T = TypeVar("T", bound="InvitationBulkCreateRequest")


@_attrs_define
class InvitationBulkCreateRequest:
    """Bulk-create request body for the invitations endpoint.

    Example:
        {'invitations': [{'email': 'alice@example.com', 'role': 'MEMBER'}, {'email': 'bob@example.com', 'role':
            'MEMBER'}]}

    Attributes:
        invitations (list[InvitationCreateItem]): One to fifty invitations to send in a single request.
    """

    invitations: list[InvitationCreateItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        invitations = []
        for invitations_item_data in self.invitations:
            invitations_item = invitations_item_data.to_dict()
            invitations.append(invitations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "invitations": invitations,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.invitation_create_item import InvitationCreateItem

        d = dict(src_dict)
        invitations = []
        _invitations = d.pop("invitations")
        for invitations_item_data in _invitations:
            invitations_item = InvitationCreateItem.from_dict(invitations_item_data)

            invitations.append(invitations_item)

        invitation_bulk_create_request = cls(
            invitations=invitations,
        )

        invitation_bulk_create_request.additional_properties = d
        return invitation_bulk_create_request

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
