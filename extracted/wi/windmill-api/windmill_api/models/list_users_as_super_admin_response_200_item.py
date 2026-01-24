from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_users_as_super_admin_response_200_item_login_type import (
    ListUsersAsSuperAdminResponse200ItemLoginType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListUsersAsSuperAdminResponse200Item")


@_attrs_define
class ListUsersAsSuperAdminResponse200Item:
    """
    Attributes:
        email (str):
        login_type (ListUsersAsSuperAdminResponse200ItemLoginType):
        super_admin (bool):
        verified (bool):
        first_time_user (bool):
        devops (Union[Unset, bool]):
        name (Union[Unset, str]):
        company (Union[Unset, str]):
        username (Union[Unset, str]):
        operator_only (Union[Unset, bool]):
    """

    email: str
    login_type: ListUsersAsSuperAdminResponse200ItemLoginType
    super_admin: bool
    verified: bool
    first_time_user: bool
    devops: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    company: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    operator_only: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        login_type = self.login_type.value

        super_admin = self.super_admin
        verified = self.verified
        first_time_user = self.first_time_user
        devops = self.devops
        name = self.name
        company = self.company
        username = self.username
        operator_only = self.operator_only

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "login_type": login_type,
                "super_admin": super_admin,
                "verified": verified,
                "first_time_user": first_time_user,
            }
        )
        if devops is not UNSET:
            field_dict["devops"] = devops
        if name is not UNSET:
            field_dict["name"] = name
        if company is not UNSET:
            field_dict["company"] = company
        if username is not UNSET:
            field_dict["username"] = username
        if operator_only is not UNSET:
            field_dict["operator_only"] = operator_only

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        login_type = ListUsersAsSuperAdminResponse200ItemLoginType(d.pop("login_type"))

        super_admin = d.pop("super_admin")

        verified = d.pop("verified")

        first_time_user = d.pop("first_time_user")

        devops = d.pop("devops", UNSET)

        name = d.pop("name", UNSET)

        company = d.pop("company", UNSET)

        username = d.pop("username", UNSET)

        operator_only = d.pop("operator_only", UNSET)

        list_users_as_super_admin_response_200_item = cls(
            email=email,
            login_type=login_type,
            super_admin=super_admin,
            verified=verified,
            first_time_user=first_time_user,
            devops=devops,
            name=name,
            company=company,
            username=username,
            operator_only=operator_only,
        )

        list_users_as_super_admin_response_200_item.additional_properties = d
        return list_users_as_super_admin_response_200_item

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
