from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateUserGloballyJsonBody")


@_attrs_define
class CreateUserGloballyJsonBody:
    """
    Attributes:
        email (str):
        super_admin (bool):
        password (Union[Unset, str]):
        name (Union[Unset, str]):
        company (Union[Unset, str]):
        skip_email (Union[Unset, bool]): Skip sending email notifications to the user
        login_type (Union[Unset, str]): password (default, requires `password`), pending_oauth (no credential until the
            first OAuth login proving the address adopts the account), or a configured OAuth login client key
    """

    email: str
    super_admin: bool
    password: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    company: Union[Unset, str] = UNSET
    skip_email: Union[Unset, bool] = UNSET
    login_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        super_admin = self.super_admin
        password = self.password
        name = self.name
        company = self.company
        skip_email = self.skip_email
        login_type = self.login_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "super_admin": super_admin,
            }
        )
        if password is not UNSET:
            field_dict["password"] = password
        if name is not UNSET:
            field_dict["name"] = name
        if company is not UNSET:
            field_dict["company"] = company
        if skip_email is not UNSET:
            field_dict["skip_email"] = skip_email
        if login_type is not UNSET:
            field_dict["login_type"] = login_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        super_admin = d.pop("super_admin")

        password = d.pop("password", UNSET)

        name = d.pop("name", UNSET)

        company = d.pop("company", UNSET)

        skip_email = d.pop("skip_email", UNSET)

        login_type = d.pop("login_type", UNSET)

        create_user_globally_json_body = cls(
            email=email,
            super_admin=super_admin,
            password=password,
            name=name,
            company=company,
            skip_email=skip_email,
            login_type=login_type,
        )

        create_user_globally_json_body.additional_properties = d
        return create_user_globally_json_body

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
