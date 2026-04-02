from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DemoPresetUser")


@_attrs_define
class DemoPresetUser:
    """
    Attributes:
        username (str):
        password (str):
        email (Union[Unset, str]):
        is_staff (Union[Unset, bool]):  Default: False.
        is_support (Union[Unset, bool]):  Default: False.
    """

    username: str
    password: str
    email: Union[Unset, str] = UNSET
    is_staff: Union[Unset, bool] = False
    is_support: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        password = self.password

        email = self.email

        is_staff = self.is_staff

        is_support = self.is_support

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "password": password,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if is_staff is not UNSET:
            field_dict["is_staff"] = is_staff
        if is_support is not UNSET:
            field_dict["is_support"] = is_support

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username")

        password = d.pop("password")

        email = d.pop("email", UNSET)

        is_staff = d.pop("is_staff", UNSET)

        is_support = d.pop("is_support", UNSET)

        demo_preset_user = cls(
            username=username,
            password=password,
            email=email,
            is_staff=is_staff,
            is_support=is_support,
        )

        demo_preset_user.additional_properties = d
        return demo_preset_user

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
