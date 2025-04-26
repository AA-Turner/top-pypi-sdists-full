from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GlobalUsersOverwriteJsonBodyItem")


@_attrs_define
class GlobalUsersOverwriteJsonBodyItem:
    """
    Attributes:
        email (str):
        super_admin (bool):
        verified (bool):
        first_time_user (bool):
        password_hash (Union[Unset, str]):
        name (Union[Unset, str]):
        company (Union[Unset, str]):
        username (Union[Unset, str]):
    """

    email: str
    super_admin: bool
    verified: bool
    first_time_user: bool
    password_hash: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    company: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        super_admin = self.super_admin
        verified = self.verified
        first_time_user = self.first_time_user
        password_hash = self.password_hash
        name = self.name
        company = self.company
        username = self.username

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "super_admin": super_admin,
                "verified": verified,
                "first_time_user": first_time_user,
            }
        )
        if password_hash is not UNSET:
            field_dict["password_hash"] = password_hash
        if name is not UNSET:
            field_dict["name"] = name
        if company is not UNSET:
            field_dict["company"] = company
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        super_admin = d.pop("super_admin")

        verified = d.pop("verified")

        first_time_user = d.pop("first_time_user")

        password_hash = d.pop("password_hash", UNSET)

        name = d.pop("name", UNSET)

        company = d.pop("company", UNSET)

        username = d.pop("username", UNSET)

        global_users_overwrite_json_body_item = cls(
            email=email,
            super_admin=super_admin,
            verified=verified,
            first_time_user=first_time_user,
            password_hash=password_hash,
            name=name,
            company=company,
            username=username,
        )

        global_users_overwrite_json_body_item.additional_properties = d
        return global_users_overwrite_json_body_item

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
