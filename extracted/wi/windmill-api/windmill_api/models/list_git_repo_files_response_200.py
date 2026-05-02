from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_git_repo_files_response_200_windmill_large_files_item import (
        ListGitRepoFilesResponse200WindmillLargeFilesItem,
    )


T = TypeVar("T", bound="ListGitRepoFilesResponse200")


@_attrs_define
class ListGitRepoFilesResponse200:
    """
    Attributes:
        windmill_large_files (List['ListGitRepoFilesResponse200WindmillLargeFilesItem']):
        next_marker (Union[Unset, str]):
        restricted_access (Union[Unset, bool]):
    """

    windmill_large_files: List["ListGitRepoFilesResponse200WindmillLargeFilesItem"]
    next_marker: Union[Unset, str] = UNSET
    restricted_access: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        windmill_large_files = []
        for windmill_large_files_item_data in self.windmill_large_files:
            windmill_large_files_item = windmill_large_files_item_data.to_dict()

            windmill_large_files.append(windmill_large_files_item)

        next_marker = self.next_marker
        restricted_access = self.restricted_access

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "windmill_large_files": windmill_large_files,
            }
        )
        if next_marker is not UNSET:
            field_dict["next_marker"] = next_marker
        if restricted_access is not UNSET:
            field_dict["restricted_access"] = restricted_access

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_git_repo_files_response_200_windmill_large_files_item import (
            ListGitRepoFilesResponse200WindmillLargeFilesItem,
        )

        d = src_dict.copy()
        windmill_large_files = []
        _windmill_large_files = d.pop("windmill_large_files")
        for windmill_large_files_item_data in _windmill_large_files:
            windmill_large_files_item = ListGitRepoFilesResponse200WindmillLargeFilesItem.from_dict(
                windmill_large_files_item_data
            )

            windmill_large_files.append(windmill_large_files_item)

        next_marker = d.pop("next_marker", UNSET)

        restricted_access = d.pop("restricted_access", UNSET)

        list_git_repo_files_response_200 = cls(
            windmill_large_files=windmill_large_files,
            next_marker=next_marker,
            restricted_access=restricted_access,
        )

        list_git_repo_files_response_200.additional_properties = d
        return list_git_repo_files_response_200

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
