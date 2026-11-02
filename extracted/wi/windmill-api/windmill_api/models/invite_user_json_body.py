from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InviteUserJsonBody")


@_attrs_define
class InviteUserJsonBody:
    """
    Attributes:
        email (str):
        is_admin (bool):
        operator (Union[Unset, bool]): Legacy role selector, true for the `operator` role.
        role (Union[Unset, str]): The workspace role to give, one of the workspace's roles. Wins over `operator`.
        parent_workspace_id (Union[Unset, None, str]):
    """

    email: str
    is_admin: bool
    operator: Union[Unset, bool] = UNSET
    role: Union[Unset, str] = UNSET
    parent_workspace_id: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        is_admin = self.is_admin
        operator = self.operator
        role = self.role
        parent_workspace_id = self.parent_workspace_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "is_admin": is_admin,
            }
        )
        if operator is not UNSET:
            field_dict["operator"] = operator
        if role is not UNSET:
            field_dict["role"] = role
        if parent_workspace_id is not UNSET:
            field_dict["parent_workspace_id"] = parent_workspace_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        is_admin = d.pop("is_admin")

        operator = d.pop("operator", UNSET)

        role = d.pop("role", UNSET)

        parent_workspace_id = d.pop("parent_workspace_id", UNSET)

        invite_user_json_body = cls(
            email=email,
            is_admin=is_admin,
            operator=operator,
            role=role,
            parent_workspace_id=parent_workspace_id,
        )

        invite_user_json_body.additional_properties = d
        return invite_user_json_body

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
