from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeleteGitSyncRepositoryJsonBody")


@_attrs_define
class DeleteGitSyncRepositoryJsonBody:
    """
    Attributes:
        git_repo_resource_path (str): The resource path of the git repository to delete
    """

    git_repo_resource_path: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        git_repo_resource_path = self.git_repo_resource_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "git_repo_resource_path": git_repo_resource_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        git_repo_resource_path = d.pop("git_repo_resource_path")

        delete_git_sync_repository_json_body = cls(
            git_repo_resource_path=git_repo_resource_path,
        )

        delete_git_sync_repository_json_body.additional_properties = d
        return delete_git_sync_repository_json_body

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
