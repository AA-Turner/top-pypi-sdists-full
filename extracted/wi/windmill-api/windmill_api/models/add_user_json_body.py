from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddUserJsonBody")


@_attrs_define
class AddUserJsonBody:
    """
    Attributes:
        email (str):
        is_admin (bool):
        username (Union[Unset, str]):
        operator (Union[Unset, bool]): Legacy role selector, true for the `operator` role.
        role (Union[Unset, str]): The workspace role to give, one of the workspace's roles. Wins over `operator`.
    """

    email: str
    is_admin: bool
    username: Union[Unset, str] = UNSET
    operator: Union[Unset, bool] = UNSET
    role: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        is_admin = self.is_admin
        username = self.username
        operator = self.operator
        role = self.role

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "is_admin": is_admin,
            }
        )
        if username is not UNSET:
            field_dict["username"] = username
        if operator is not UNSET:
            field_dict["operator"] = operator
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        is_admin = d.pop("is_admin")

        username = d.pop("username", UNSET)

        operator = d.pop("operator", UNSET)

        role = d.pop("role", UNSET)

        add_user_json_body = cls(
            email=email,
            is_admin=is_admin,
            username=username,
            operator=operator,
            role=role,
        )

        add_user_json_body.additional_properties = d
        return add_user_json_body

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
