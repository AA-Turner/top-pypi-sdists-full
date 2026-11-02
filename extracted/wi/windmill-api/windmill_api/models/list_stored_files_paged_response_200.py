from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_stored_files_paged_response_200_files_item import ListStoredFilesPagedResponse200FilesItem
    from ..models.list_stored_files_paged_response_200_folders_item import ListStoredFilesPagedResponse200FoldersItem


T = TypeVar("T", bound="ListStoredFilesPagedResponse200")


@_attrs_define
class ListStoredFilesPagedResponse200:
    """
    Attributes:
        folders (List['ListStoredFilesPagedResponse200FoldersItem']):
        files (List['ListStoredFilesPagedResponse200FilesItem']):
        restricted_access (bool):
        next_page_token (Union[Unset, str]): When set, more entries remain at this level
    """

    folders: List["ListStoredFilesPagedResponse200FoldersItem"]
    files: List["ListStoredFilesPagedResponse200FilesItem"]
    restricted_access: bool
    next_page_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        folders = []
        for folders_item_data in self.folders:
            folders_item = folders_item_data.to_dict()

            folders.append(folders_item)

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()

            files.append(files_item)

        restricted_access = self.restricted_access
        next_page_token = self.next_page_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "folders": folders,
                "files": files,
                "restricted_access": restricted_access,
            }
        )
        if next_page_token is not UNSET:
            field_dict["next_page_token"] = next_page_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_stored_files_paged_response_200_files_item import ListStoredFilesPagedResponse200FilesItem
        from ..models.list_stored_files_paged_response_200_folders_item import (
            ListStoredFilesPagedResponse200FoldersItem,
        )

        d = src_dict.copy()
        folders = []
        _folders = d.pop("folders")
        for folders_item_data in _folders:
            folders_item = ListStoredFilesPagedResponse200FoldersItem.from_dict(folders_item_data)

            folders.append(folders_item)

        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = ListStoredFilesPagedResponse200FilesItem.from_dict(files_item_data)

            files.append(files_item)

        restricted_access = d.pop("restricted_access")

        next_page_token = d.pop("next_page_token", UNSET)

        list_stored_files_paged_response_200 = cls(
            folders=folders,
            files=files,
            restricted_access=restricted_access,
            next_page_token=next_page_token,
        )

        list_stored_files_paged_response_200.additional_properties = d
        return list_stored_files_paged_response_200

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
