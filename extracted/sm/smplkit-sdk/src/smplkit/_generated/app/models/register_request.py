from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.register_request_entry_point import check_register_request_entry_point
from ..models.register_request_entry_point import RegisterRequestEntryPoint


T = TypeVar("T", bound="RegisterRequest")


@_attrs_define
class RegisterRequest:
    """Body for the email + password registration endpoint.

    Example:
        {'email': 'jane@example.com', 'entry_point': 'GET_STARTED', 'password': 'correct-horse-battery-staple'}

    Attributes:
        email (str): Email address that becomes the new user's login identifier.
        password (str): Password for the new account. Must be at least 8 characters.
        entry_point (RegisterRequestEntryPoint | Unset): How the customer arrived at the registration page. Allowed
            values: `LOGIN`, `GET_STARTED`, `LIVE_DEMO`, `UNKNOWN`. Defaults to `UNKNOWN` when omitted. Case-insensitive on
            input.
    """

    email: str
    password: str
    entry_point: RegisterRequestEntryPoint | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        password = self.password

        entry_point: str | Unset = UNSET
        if not isinstance(self.entry_point, Unset):
            entry_point = self.entry_point

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "password": password,
            }
        )
        if entry_point is not UNSET:
            field_dict["entry_point"] = entry_point

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        password = d.pop("password")

        _entry_point = d.pop("entry_point", UNSET)
        entry_point: RegisterRequestEntryPoint | Unset
        if isinstance(_entry_point, Unset):
            entry_point = UNSET
        else:
            entry_point = check_register_request_entry_point(_entry_point)

        register_request = cls(
            email=email,
            password=password,
            entry_point=entry_point,
        )

        register_request.additional_properties = d
        return register_request

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
