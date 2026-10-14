from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MatrixSession")


@_attrs_define
class MatrixSession:
    """
    Attributes:
        homeserver_url (str):
        matrix_user_id (str):
        device_id (str):
        access_token (str):
        refresh_token (Union[None, str]):
        expires_in_ms (Union[None, int]):
        recovery_key (Union[None, str]): The user's secret-storage recovery key, or null before encryption is set up.
            Only ever returned to its owner.
    """

    homeserver_url: str
    matrix_user_id: str
    device_id: str
    access_token: str
    refresh_token: Union[None, str]
    expires_in_ms: Union[None, int]
    recovery_key: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        homeserver_url = self.homeserver_url

        matrix_user_id = self.matrix_user_id

        device_id = self.device_id

        access_token = self.access_token

        refresh_token: Union[None, str]
        refresh_token = self.refresh_token

        expires_in_ms: Union[None, int]
        expires_in_ms = self.expires_in_ms

        recovery_key: Union[None, str]
        recovery_key = self.recovery_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "homeserver_url": homeserver_url,
                "matrix_user_id": matrix_user_id,
                "device_id": device_id,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in_ms": expires_in_ms,
                "recovery_key": recovery_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        homeserver_url = d.pop("homeserver_url")

        matrix_user_id = d.pop("matrix_user_id")

        device_id = d.pop("device_id")

        access_token = d.pop("access_token")

        def _parse_refresh_token(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        refresh_token = _parse_refresh_token(d.pop("refresh_token"))

        def _parse_expires_in_ms(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        expires_in_ms = _parse_expires_in_ms(d.pop("expires_in_ms"))

        def _parse_recovery_key(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        recovery_key = _parse_recovery_key(d.pop("recovery_key"))

        matrix_session = cls(
            homeserver_url=homeserver_url,
            matrix_user_id=matrix_user_id,
            device_id=device_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in_ms=expires_in_ms,
            recovery_key=recovery_key,
        )

        matrix_session.additional_properties = d
        return matrix_session

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
