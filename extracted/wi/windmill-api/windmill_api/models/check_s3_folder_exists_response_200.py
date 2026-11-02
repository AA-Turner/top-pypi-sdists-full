from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CheckS3FolderExistsResponse200")


@_attrs_define
class CheckS3FolderExistsResponse200:
    """
    Attributes:
        exists (bool): Whether the path exists
        is_folder (bool): Whether the path is a folder (true) or file (false)
    """

    exists: bool
    is_folder: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        exists = self.exists
        is_folder = self.is_folder

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "exists": exists,
                "is_folder": is_folder,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        exists = d.pop("exists")

        is_folder = d.pop("is_folder")

        check_s3_folder_exists_response_200 = cls(
            exists=exists,
            is_folder=is_folder,
        )

        check_s3_folder_exists_response_200.additional_properties = d
        return check_s3_folder_exists_response_200

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
