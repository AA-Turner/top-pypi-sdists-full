import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExternalJwtToken")


@_attrs_define
class ExternalJwtToken:
    """
    Attributes:
        jwt_hash (int):
        email (str):
        username (str):
        is_admin (bool):
        is_operator (bool):
        last_used_at (datetime.datetime):
        workspace_id (Union[Unset, str]):
        label (Union[Unset, str]):
        scopes (Union[Unset, List[str]]):
    """

    jwt_hash: int
    email: str
    username: str
    is_admin: bool
    is_operator: bool
    last_used_at: datetime.datetime
    workspace_id: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    scopes: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        jwt_hash = self.jwt_hash
        email = self.email
        username = self.username
        is_admin = self.is_admin
        is_operator = self.is_operator
        last_used_at = self.last_used_at.isoformat()

        workspace_id = self.workspace_id
        label = self.label
        scopes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "jwt_hash": jwt_hash,
                "email": email,
                "username": username,
                "is_admin": is_admin,
                "is_operator": is_operator,
                "last_used_at": last_used_at,
            }
        )
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if label is not UNSET:
            field_dict["label"] = label
        if scopes is not UNSET:
            field_dict["scopes"] = scopes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        jwt_hash = d.pop("jwt_hash")

        email = d.pop("email")

        username = d.pop("username")

        is_admin = d.pop("is_admin")

        is_operator = d.pop("is_operator")

        last_used_at = isoparse(d.pop("last_used_at"))

        workspace_id = d.pop("workspace_id", UNSET)

        label = d.pop("label", UNSET)

        scopes = cast(List[str], d.pop("scopes", UNSET))

        external_jwt_token = cls(
            jwt_hash=jwt_hash,
            email=email,
            username=username,
            is_admin=is_admin,
            is_operator=is_operator,
            last_used_at=last_used_at,
            workspace_id=workspace_id,
            label=label,
            scopes=scopes,
        )

        external_jwt_token.additional_properties = d
        return external_jwt_token

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
