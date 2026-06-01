from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.user_resource_type import check_user_resource_type
from ..models.user_resource_type import UserResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.user import User


T = TypeVar("T", bound="UserResource")


@_attrs_define
class UserResource:
    """JSON:API resource envelope for a user.

    `id` must not be specified for create requests (the server assigns it).

        Example:
            {'attributes': {'account': 'd290f1ee-6c54-4b01-90e6-d701748f0851', 'auth_provider': 'GOOGLE', 'created_at':
                '2026-03-20T11:02:16.616Z', 'display_name': 'Jane Smith', 'email': 'jane@example.com', 'email_verified': True,
                'profile_pic': 'https://lh3.googleusercontent.com/a/example', 'role': 'OWNER'}, 'id': 'a1b2c3d4-e5f6-7890-abcd-
                ef1234567890', 'type': 'user'}

        Attributes:
            type_ (UserResourceType):
            attributes (User): A person with access to one or more accounts in smplkit. Example: {'account':
                'd290f1ee-6c54-4b01-90e6-d701748f0851', 'auth_provider': 'GOOGLE', 'created_at': '2026-03-20T11:02:16.616Z',
                'display_name': 'Jane Smith', 'email': 'jane@example.com', 'email_verified': True, 'profile_pic':
                'https://lh3.googleusercontent.com/a/example', 'role': 'OWNER'}.
            id (None | str | Unset):
    """

    type_: UserResourceType
    attributes: User
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user import User

        d = dict(src_dict)
        type_ = check_user_resource_type(d.pop("type"))

        attributes = User.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        user_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        user_resource.additional_properties = d
        return user_resource

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
