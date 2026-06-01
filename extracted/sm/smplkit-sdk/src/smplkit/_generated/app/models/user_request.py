from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.user_resource import UserResource


T = TypeVar("T", bound="UserRequest")


@_attrs_define
class UserRequest:
    """JSON:API request envelope for creating or updating a user.

    Attributes:
        data (UserResource): JSON:API resource envelope for a user.

            `id` must not be specified for create requests (the server assigns it). Example: {'attributes': {'account':
            'd290f1ee-6c54-4b01-90e6-d701748f0851', 'auth_provider': 'GOOGLE', 'created_at': '2026-03-20T11:02:16.616Z',
            'display_name': 'Jane Smith', 'email': 'jane@example.com', 'email_verified': True, 'profile_pic':
            'https://lh3.googleusercontent.com/a/example', 'role': 'OWNER'}, 'id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
            'type': 'user'}.
    """

    data: UserResource
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
        from ..models.user_resource import UserResource

        d = dict(src_dict)
        data = UserResource.from_dict(d.pop("data"))

        user_request = cls(
            data=data,
        )

        user_request.additional_properties = d
        return user_request

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
