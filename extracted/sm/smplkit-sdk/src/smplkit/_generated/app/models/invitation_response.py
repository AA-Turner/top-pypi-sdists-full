from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.invitation_resource import InvitationResource


T = TypeVar("T", bound="InvitationResponse")


@_attrs_define
class InvitationResponse:
    """JSON:API single-resource response envelope for an invitation.

    Attributes:
        data (InvitationResource): JSON:API resource envelope for an invitation.

            `id` must not be specified for create requests (the server assigns it). Example: {'attributes': {'created_at':
            '2026-03-20T11:02:16.616Z', 'email': 'mike@example.com', 'expires_at': '2026-04-20T11:02:16.616Z', 'invited_by':
            'd290f1ee-6c54-4b01-90e6-d701748f0851', 'role': 'MEMBER', 'status': 'PENDING', 'updated_at':
            '2026-03-20T11:02:16.616Z'}, 'id': 'd4e5f6a7-b8c9-0123-defa-234567890123', 'type': 'invitation'}.
    """

    data: InvitationResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.invitation_resource import InvitationResource

        d = dict(src_dict)
        data = InvitationResource.from_dict(d.pop("data"))

        invitation_response = cls(
            data=data,
        )

        invitation_response.additional_properties = d
        return invitation_response

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
