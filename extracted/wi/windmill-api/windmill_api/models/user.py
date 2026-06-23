import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_added_via import UserAddedVia


T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """
    Attributes:
        email (str):
        username (str):
        is_admin (bool):
        is_super_admin (bool):
        created_at (datetime.datetime):
        operator (bool):
        disabled (bool):
        folders (List[str]):
        folders_read (List[str]):
        folders_owners (List[str]):
        name (Union[Unset, str]):
        groups (Union[Unset, List[str]]):
        added_via (Union[Unset, None, UserAddedVia]):
        is_service_account (Union[Unset, bool]):
    """

    email: str
    username: str
    is_admin: bool
    is_super_admin: bool
    created_at: datetime.datetime
    operator: bool
    disabled: bool
    folders: List[str]
    folders_read: List[str]
    folders_owners: List[str]
    name: Union[Unset, str] = UNSET
    groups: Union[Unset, List[str]] = UNSET
    added_via: Union[Unset, None, "UserAddedVia"] = UNSET
    is_service_account: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        username = self.username
        is_admin = self.is_admin
        is_super_admin = self.is_super_admin
        created_at = self.created_at.isoformat()

        operator = self.operator
        disabled = self.disabled
        folders = self.folders

        folders_read = self.folders_read

        folders_owners = self.folders_owners

        name = self.name
        groups: Union[Unset, List[str]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = self.groups

        added_via: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.added_via, Unset):
            added_via = self.added_via.to_dict() if self.added_via else None

        is_service_account = self.is_service_account

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "username": username,
                "is_admin": is_admin,
                "is_super_admin": is_super_admin,
                "created_at": created_at,
                "operator": operator,
                "disabled": disabled,
                "folders": folders,
                "folders_read": folders_read,
                "folders_owners": folders_owners,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if groups is not UNSET:
            field_dict["groups"] = groups
        if added_via is not UNSET:
            field_dict["added_via"] = added_via
        if is_service_account is not UNSET:
            field_dict["is_service_account"] = is_service_account

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_added_via import UserAddedVia

        d = src_dict.copy()
        email = d.pop("email")

        username = d.pop("username")

        is_admin = d.pop("is_admin")

        is_super_admin = d.pop("is_super_admin")

        created_at = isoparse(d.pop("created_at"))

        operator = d.pop("operator")

        disabled = d.pop("disabled")

        folders = cast(List[str], d.pop("folders"))

        folders_read = cast(List[str], d.pop("folders_read"))

        folders_owners = cast(List[str], d.pop("folders_owners"))

        name = d.pop("name", UNSET)

        groups = cast(List[str], d.pop("groups", UNSET))

        _added_via = d.pop("added_via", UNSET)
        added_via: Union[Unset, None, UserAddedVia]
        if _added_via is None:
            added_via = None
        elif isinstance(_added_via, Unset):
            added_via = UNSET
        else:
            added_via = UserAddedVia.from_dict(_added_via)

        is_service_account = d.pop("is_service_account", UNSET)

        user = cls(
            email=email,
            username=username,
            is_admin=is_admin,
            is_super_admin=is_super_admin,
            created_at=created_at,
            operator=operator,
            disabled=disabled,
            folders=folders,
            folders_read=folders_read,
            folders_owners=folders_owners,
            name=name,
            groups=groups,
            added_via=added_via,
            is_service_account=is_service_account,
        )

        user.additional_properties = d
        return user

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
