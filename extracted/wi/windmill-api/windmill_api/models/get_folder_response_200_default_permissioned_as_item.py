from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetFolderResponse200DefaultPermissionedAsItem")


@_attrs_define
class GetFolderResponse200DefaultPermissionedAsItem:
    """
    Attributes:
        path_glob (str): Glob pattern evaluated against the item path *relative* to the folder root (e.g. "jobs/**"
            matches every item whose full path is `f/<folder>/jobs/...`). Supports `*`, `**`, `?`, `[abc]`, `{a,b}`.
        permissioned_as (str): Target identity the matched item should be permissioned as. Must be `u/<username>`,
            `g/<groupname>`, or an email that exists in this workspace.
    """

    path_glob: str
    permissioned_as: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path_glob = self.path_glob
        permissioned_as = self.permissioned_as

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path_glob": path_glob,
                "permissioned_as": permissioned_as,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path_glob = d.pop("path_glob")

        permissioned_as = d.pop("permissioned_as")

        get_folder_response_200_default_permissioned_as_item = cls(
            path_glob=path_glob,
            permissioned_as=permissioned_as,
        )

        get_folder_response_200_default_permissioned_as_item.additional_properties = d
        return get_folder_response_200_default_permissioned_as_item

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
