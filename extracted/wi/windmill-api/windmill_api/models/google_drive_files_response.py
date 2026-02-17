from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.google_drive_files_response_files_item import GoogleDriveFilesResponseFilesItem


T = TypeVar("T", bound="GoogleDriveFilesResponse")


@_attrs_define
class GoogleDriveFilesResponse:
    """
    Attributes:
        files (List['GoogleDriveFilesResponseFilesItem']):
        next_page_token (Union[Unset, str]):
    """

    files: List["GoogleDriveFilesResponseFilesItem"]
    next_page_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()

            files.append(files_item)

        next_page_token = self.next_page_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "files": files,
            }
        )
        if next_page_token is not UNSET:
            field_dict["next_page_token"] = next_page_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.google_drive_files_response_files_item import GoogleDriveFilesResponseFilesItem

        d = src_dict.copy()
        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = GoogleDriveFilesResponseFilesItem.from_dict(files_item_data)

            files.append(files_item)

        next_page_token = d.pop("next_page_token", UNSET)

        google_drive_files_response = cls(
            files=files,
            next_page_token=next_page_token,
        )

        google_drive_files_response.additional_properties = d
        return google_drive_files_response

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
