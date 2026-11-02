from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_npm_package_filetree_response_200_files_item import GetNpmPackageFiletreeResponse200FilesItem


T = TypeVar("T", bound="GetNpmPackageFiletreeResponse200")


@_attrs_define
class GetNpmPackageFiletreeResponse200:
    """
    Attributes:
        default (Union[Unset, str]):
        files (Union[Unset, List['GetNpmPackageFiletreeResponse200FilesItem']]):
    """

    default: Union[Unset, str] = UNSET
    files: Union[Unset, List["GetNpmPackageFiletreeResponse200FilesItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        default = self.default
        files: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()

                files.append(files_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if default is not UNSET:
            field_dict["default"] = default
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_npm_package_filetree_response_200_files_item import GetNpmPackageFiletreeResponse200FilesItem

        d = src_dict.copy()
        default = d.pop("default", UNSET)

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = GetNpmPackageFiletreeResponse200FilesItem.from_dict(files_item_data)

            files.append(files_item)

        get_npm_package_filetree_response_200 = cls(
            default=default,
            files=files,
        )

        get_npm_package_filetree_response_200.additional_properties = d
        return get_npm_package_filetree_response_200

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
