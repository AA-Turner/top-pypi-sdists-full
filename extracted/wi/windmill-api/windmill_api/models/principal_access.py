from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.principal_access_folders_item import PrincipalAccessFoldersItem
    from ..models.principal_access_items_item import PrincipalAccessItemsItem


T = TypeVar("T", bound="PrincipalAccess")


@_attrs_define
class PrincipalAccess:
    """
    Attributes:
        principal (str):
        is_admin (bool):
        groups (List[str]):
        folders (List['PrincipalAccessFoldersItem']):
        items (List['PrincipalAccessItemsItem']):
    """

    principal: str
    is_admin: bool
    groups: List[str]
    folders: List["PrincipalAccessFoldersItem"]
    items: List["PrincipalAccessItemsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        principal = self.principal
        is_admin = self.is_admin
        groups = self.groups

        folders = []
        for folders_item_data in self.folders:
            folders_item = folders_item_data.to_dict()

            folders.append(folders_item)

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()

            items.append(items_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "principal": principal,
                "is_admin": is_admin,
                "groups": groups,
                "folders": folders,
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.principal_access_folders_item import PrincipalAccessFoldersItem
        from ..models.principal_access_items_item import PrincipalAccessItemsItem

        d = src_dict.copy()
        principal = d.pop("principal")

        is_admin = d.pop("is_admin")

        groups = cast(List[str], d.pop("groups"))

        folders = []
        _folders = d.pop("folders")
        for folders_item_data in _folders:
            folders_item = PrincipalAccessFoldersItem.from_dict(folders_item_data)

            folders.append(folders_item)

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = PrincipalAccessItemsItem.from_dict(items_item_data)

            items.append(items_item)

        principal_access = cls(
            principal=principal,
            is_admin=is_admin,
            groups=groups,
            folders=folders,
            items=items,
        )

        principal_access.additional_properties = d
        return principal_access

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
