import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="UserAuthToken")


@_attrs_define
class UserAuthToken:
    """
    Attributes:
        created (datetime.datetime):
        user_first_name (str):
        user_last_name (str):
        user_username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_ characters
        user_is_active (bool): Designates whether this user should be treated as active. Unselect this instead of
            deleting accounts.
        user_token_lifetime (Union[None, int]): Token lifetime in seconds.
        token (str):
    """

    created: datetime.datetime
    user_first_name: str
    user_last_name: str
    user_username: str
    user_is_active: bool
    user_token_lifetime: Union[None, int]
    token: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created = self.created.isoformat()

        user_first_name = self.user_first_name

        user_last_name = self.user_last_name

        user_username = self.user_username

        user_is_active = self.user_is_active

        user_token_lifetime: Union[None, int]
        user_token_lifetime = self.user_token_lifetime

        token = self.token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created": created,
                "user_first_name": user_first_name,
                "user_last_name": user_last_name,
                "user_username": user_username,
                "user_is_active": user_is_active,
                "user_token_lifetime": user_token_lifetime,
                "token": token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created = isoparse(d.pop("created"))

        user_first_name = d.pop("user_first_name")

        user_last_name = d.pop("user_last_name")

        user_username = d.pop("user_username")

        user_is_active = d.pop("user_is_active")

        def _parse_user_token_lifetime(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        user_token_lifetime = _parse_user_token_lifetime(d.pop("user_token_lifetime"))

        token = d.pop("token")

        user_auth_token = cls(
            created=created,
            user_first_name=user_first_name,
            user_last_name=user_last_name,
            user_username=user_username,
            user_is_active=user_is_active,
            user_token_lifetime=user_token_lifetime,
            token=token,
        )

        user_auth_token.additional_properties = d
        return user_auth_token

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
