from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateLoginLinkJsonBody")


@_attrs_define
class CreateLoginLinkJsonBody:
    """
    Attributes:
        email (str):
        expires_in_s (Union[Unset, int]): link lifetime in seconds, at most 900 (default 600)
        rd (Union[Unset, str]): same-origin path the browser lands on after login (default /user/workspaces)
        require_login_type (Union[Unset, str]): mint only while the account still has this login type (for example
            pending_oauth), so a link stops working once the owner has set a password or signed in with a provider
    """

    email: str
    expires_in_s: Union[Unset, int] = UNSET
    rd: Union[Unset, str] = UNSET
    require_login_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        expires_in_s = self.expires_in_s
        rd = self.rd
        require_login_type = self.require_login_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
            }
        )
        if expires_in_s is not UNSET:
            field_dict["expires_in_s"] = expires_in_s
        if rd is not UNSET:
            field_dict["rd"] = rd
        if require_login_type is not UNSET:
            field_dict["require_login_type"] = require_login_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        expires_in_s = d.pop("expires_in_s", UNSET)

        rd = d.pop("rd", UNSET)

        require_login_type = d.pop("require_login_type", UNSET)

        create_login_link_json_body = cls(
            email=email,
            expires_in_s=expires_in_s,
            rd=rd,
            require_login_type=require_login_type,
        )

        create_login_link_json_body.additional_properties = d
        return create_login_link_json_body

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
