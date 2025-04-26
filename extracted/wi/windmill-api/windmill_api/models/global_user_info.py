from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.global_user_info_login_type import GlobalUserInfoLoginType
from ..types import UNSET, Unset

T = TypeVar("T", bound="GlobalUserInfo")


@_attrs_define
class GlobalUserInfo:
    """
    Attributes:
        email (str):
        login_type (GlobalUserInfoLoginType):
        super_admin (bool):
        verified (bool):
        devops (Union[Unset, bool]):
        name (Union[Unset, str]):
        company (Union[Unset, str]):
        username (Union[Unset, str]):
        operator_only (Union[Unset, bool]):
    """

    email: str
    login_type: GlobalUserInfoLoginType
    super_admin: bool
    verified: bool
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

        login_type = GlobalUserInfoLoginType(d.pop("login_type"))

        super_admin = d.pop("super_admin")

        verified = d.pop("verified")

        devops = d.pop("devops", UNSET)

        name = d.pop("name", UNSET)

        company = d.pop("company", UNSET)

        username = d.pop("username", UNSET)

        operator_only = d.pop("operator_only", UNSET)

        global_user_info = cls(
            email=email,
            login_type=login_type,
            super_admin=super_admin,
            verified=verified,
            devops=devops,
            name=name,
            company=company,
            username=username,
            operator_only=operator_only,
        )

        global_user_info.additional_properties = d
        return global_user_info

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
