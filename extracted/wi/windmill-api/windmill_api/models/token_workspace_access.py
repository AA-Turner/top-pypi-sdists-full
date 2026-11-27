from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.token_workspace_access_folders_item import TokenWorkspaceAccessFoldersItem


T = TypeVar("T", bound="TokenWorkspaceAccess")


@_attrs_define
class TokenWorkspaceAccess:
    """
    Attributes:
        workspace_id (str):
        usable (bool): whether the token is accepted in this workspace at all
        is_admin (Union[Unset, bool]):
        is_operator (Union[Unset, bool]):
        groups (Union[Unset, List[str]]):
        folders (Union[Unset, List['TokenWorkspaceAccessFoldersItem']]):
    """

    workspace_id: str
    usable: bool
    is_admin: Union[Unset, bool] = UNSET
    is_operator: Union[Unset, bool] = UNSET
    groups: Union[Unset, List[str]] = UNSET
    folders: Union[Unset, List["TokenWorkspaceAccessFoldersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        usable = self.usable
        is_admin = self.is_admin
        is_operator = self.is_operator
        groups: Union[Unset, List[str]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = self.groups

        folders: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.folders, Unset):
            folders = []
            for folders_item_data in self.folders:
                folders_item = folders_item_data.to_dict()

                folders.append(folders_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_id": workspace_id,
                "usable": usable,
            }
        )
        if is_admin is not UNSET:
            field_dict["is_admin"] = is_admin
        if is_operator is not UNSET:
            field_dict["is_operator"] = is_operator
        if groups is not UNSET:
            field_dict["groups"] = groups
        if folders is not UNSET:
            field_dict["folders"] = folders

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.token_workspace_access_folders_item import TokenWorkspaceAccessFoldersItem

        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        usable = d.pop("usable")

        is_admin = d.pop("is_admin", UNSET)

        is_operator = d.pop("is_operator", UNSET)

        groups = cast(List[str], d.pop("groups", UNSET))

        folders = []
        _folders = d.pop("folders", UNSET)
        for folders_item_data in _folders or []:
            folders_item = TokenWorkspaceAccessFoldersItem.from_dict(folders_item_data)

            folders.append(folders_item)

        token_workspace_access = cls(
            workspace_id=workspace_id,
            usable=usable,
            is_admin=is_admin,
            is_operator=is_operator,
            groups=groups,
            folders=folders,
        )

        token_workspace_access.additional_properties = d
        return token_workspace_access

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
