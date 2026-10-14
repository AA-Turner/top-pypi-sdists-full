from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MatrixPassword")


@_attrs_define
class MatrixPassword:
    """
    Attributes:
        homeserver_url (str):
        matrix_user_id (str):
        password (str):
    """

    homeserver_url: str
    matrix_user_id: str
    password: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        homeserver_url = self.homeserver_url

        matrix_user_id = self.matrix_user_id

        password = self.password

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "homeserver_url": homeserver_url,
                "matrix_user_id": matrix_user_id,
                "password": password,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        homeserver_url = d.pop("homeserver_url")

        matrix_user_id = d.pop("matrix_user_id")

        password = d.pop("password")

        matrix_password = cls(
            homeserver_url=homeserver_url,
            matrix_user_id=matrix_user_id,
            password=password,
        )

        matrix_password.additional_properties = d
        return matrix_password

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
