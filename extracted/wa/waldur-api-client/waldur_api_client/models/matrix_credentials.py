from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MatrixCredentials")


@_attrs_define
class MatrixCredentials:
    """
    Attributes:
        method (str):
        homeserver_url (str):
        matrix_user_id (str):
        password (Union[Unset, str]):
        login_token (Union[Unset, str]):
        oidc_provider_url (Union[Unset, str]):
        room_id (Union[Unset, str]):
        access_token (Union[Unset, str]):
    """

    method: str
    homeserver_url: str
    matrix_user_id: str
    password: Union[Unset, str] = UNSET
    login_token: Union[Unset, str] = UNSET
    oidc_provider_url: Union[Unset, str] = UNSET
    room_id: Union[Unset, str] = UNSET
    access_token: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        method = self.method

        homeserver_url = self.homeserver_url

        matrix_user_id = self.matrix_user_id

        password = self.password

        login_token = self.login_token

        oidc_provider_url = self.oidc_provider_url

        room_id = self.room_id

        access_token = self.access_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "method": method,
                "homeserver_url": homeserver_url,
                "matrix_user_id": matrix_user_id,
            }
        )
        if password is not UNSET:
            field_dict["password"] = password
        if login_token is not UNSET:
            field_dict["login_token"] = login_token
        if oidc_provider_url is not UNSET:
            field_dict["oidc_provider_url"] = oidc_provider_url
        if room_id is not UNSET:
            field_dict["room_id"] = room_id
        if access_token is not UNSET:
            field_dict["access_token"] = access_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        method = d.pop("method")

        homeserver_url = d.pop("homeserver_url")

        matrix_user_id = d.pop("matrix_user_id")

        password = d.pop("password", UNSET)

        login_token = d.pop("login_token", UNSET)

        oidc_provider_url = d.pop("oidc_provider_url", UNSET)

        room_id = d.pop("room_id", UNSET)

        access_token = d.pop("access_token", UNSET)

        matrix_credentials = cls(
            method=method,
            homeserver_url=homeserver_url,
            matrix_user_id=matrix_user_id,
            password=password,
            login_token=login_token,
            oidc_provider_url=oidc_provider_url,
            room_id=room_id,
            access_token=access_token,
        )

        matrix_credentials.additional_properties = d
        return matrix_credentials

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
