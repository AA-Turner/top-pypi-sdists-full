from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GoogleDriveFilesResponseFilesItem")


@_attrs_define
class GoogleDriveFilesResponseFilesItem:
    """
    Attributes:
        id (str):
        name (str):
        mime_type (str):
        is_folder (Union[Unset, bool]):
    """

    id: str
    name: str
    mime_type: str
    is_folder: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        mime_type = self.mime_type
        is_folder = self.is_folder

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "mime_type": mime_type,
            }
        )
        if is_folder is not UNSET:
            field_dict["is_folder"] = is_folder

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        mime_type = d.pop("mime_type")

        is_folder = d.pop("is_folder", UNSET)

        google_drive_files_response_files_item = cls(
            id=id,
            name=name,
            mime_type=mime_type,
            is_folder=is_folder,
        )

        google_drive_files_response_files_item.additional_properties = d
        return google_drive_files_response_files_item

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
