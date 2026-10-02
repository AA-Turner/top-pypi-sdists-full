from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auth_method_enum import AuthMethodEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="DiscoverPrioritiesRequestRequest")


@_attrs_define
class DiscoverPrioritiesRequestRequest:
    """
    Attributes:
        api_url (str): Atlassian API URL (e.g., https://your-domain.atlassian.net)
        auth_method (AuthMethodEnum):
        email (Union[Unset, str]):
        token (Union[Unset, str]):
        personal_access_token (Union[Unset, str]):
        username (Union[Unset, str]):
        password (Union[Unset, str]):
        verify_ssl (Union[Unset, bool]):  Default: True.
    """

    api_url: str
    auth_method: AuthMethodEnum
    email: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET
    personal_access_token: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    verify_ssl: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_url = self.api_url

        auth_method = self.auth_method.value

        email = self.email

        token = self.token

        personal_access_token = self.personal_access_token

        username = self.username

        password = self.password

        verify_ssl = self.verify_ssl

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "api_url": api_url,
                "auth_method": auth_method,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if token is not UNSET:
            field_dict["token"] = token
        if personal_access_token is not UNSET:
            field_dict["personal_access_token"] = personal_access_token
        if username is not UNSET:
            field_dict["username"] = username
        if password is not UNSET:
            field_dict["password"] = password
        if verify_ssl is not UNSET:
            field_dict["verify_ssl"] = verify_ssl

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        api_url = d.pop("api_url")

        auth_method = AuthMethodEnum(d.pop("auth_method"))

        email = d.pop("email", UNSET)

        token = d.pop("token", UNSET)

        personal_access_token = d.pop("personal_access_token", UNSET)

        username = d.pop("username", UNSET)

        password = d.pop("password", UNSET)

        verify_ssl = d.pop("verify_ssl", UNSET)

        discover_priorities_request_request = cls(
            api_url=api_url,
            auth_method=auth_method,
            email=email,
            token=token,
            personal_access_token=personal_access_token,
            username=username,
            password=password,
            verify_ssl=verify_ssl,
        )

        discover_priorities_request_request.additional_properties = d
        return discover_priorities_request_request

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
