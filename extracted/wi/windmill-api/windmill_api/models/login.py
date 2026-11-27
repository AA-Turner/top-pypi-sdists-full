from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Login")


@_attrs_define
class Login:
    """
    Attributes:
        email (str):
        password (str):
        totp_code (Union[Unset, str]): Current code of the account's authenticator app, or one of its recovery codes.
            Required once the account has two-factor authentication enabled; the login answers "Two-factor code required"
            when it is missing and the password is correct.
    """

    email: str
    password: str
    totp_code: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        password = self.password
        totp_code = self.totp_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "password": password,
            }
        )
        if totp_code is not UNSET:
            field_dict["totp_code"] = totp_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        password = d.pop("password")

        totp_code = d.pop("totp_code", UNSET)

        login = cls(
            email=email,
            password=password,
            totp_code=totp_code,
        )

        login.additional_properties = d
        return login

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
