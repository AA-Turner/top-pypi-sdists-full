from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_git_sync_settings_repositories_item_exclude_types_override_item import (
    WorkspaceGitSyncSettingsRepositoriesItemExcludeTypesOverrideItem,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceGitSyncSettingsRepositoriesItem")


@_attrs_define
class WorkspaceGitSyncSettingsRepositoriesItem:
    """
    Attributes:
        script_path (str):
        git_repo_resource_path (str):
        use_individual_branch (Union[Unset, bool]):
        group_by_folder (Union[Unset, bool]):
        exclude_types_override (Union[Unset, List[WorkspaceGitSyncSettingsRepositoriesItemExcludeTypesOverrideItem]]):
    """

    script_path: str
    git_repo_resource_path: str
    use_individual_branch: Union[Unset, bool] = UNSET
    group_by_folder: Union[Unset, bool] = UNSET
    exclude_types_override: Union[Unset, List[WorkspaceGitSyncSettingsRepositoriesItemExcludeTypesOverrideItem]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        script_path = self.script_path
        git_repo_resource_path = self.git_repo_resource_path
        use_individual_branch = self.use_individual_branch
        group_by_folder = self.group_by_folder
        exclude_types_override: Union[Unset, List[str]] = UNSET
        if not isinstance(self.exclude_types_override, Unset):
            exclude_types_override = []
            for exclude_types_override_item_data in self.exclude_types_override:
                exclude_types_override_item = exclude_types_override_item_data.value

                exclude_types_override.append(exclude_types_override_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "script_path": script_path,
                "git_repo_resource_path": git_repo_resource_path,
            }
        )
        if use_individual_branch is not UNSET:
            field_dict["use_individual_branch"] = use_individual_branch
        if group_by_folder is not UNSET:
            field_dict["group_by_folder"] = group_by_folder
        if exclude_types_override is not UNSET:
            field_dict["exclude_types_override"] = exclude_types_override

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        script_path = d.pop("script_path")

        git_repo_resource_path = d.pop("git_repo_resource_path")

        use_individual_branch = d.pop("use_individual_branch", UNSET)

        group_by_folder = d.pop("group_by_folder", UNSET)

        exclude_types_override = []
        _exclude_types_override = d.pop("exclude_types_override", UNSET)
        for exclude_types_override_item_data in _exclude_types_override or []:
            exclude_types_override_item = WorkspaceGitSyncSettingsRepositoriesItemExcludeTypesOverrideItem(
                exclude_types_override_item_data
            )

            exclude_types_override.append(exclude_types_override_item)

        workspace_git_sync_settings_repositories_item = cls(
            script_path=script_path,
            git_repo_resource_path=git_repo_resource_path,
            use_individual_branch=use_individual_branch,
            group_by_folder=group_by_folder,
            exclude_types_override=exclude_types_override,
        )

        workspace_git_sync_settings_repositories_item.additional_properties = d
        return workspace_git_sync_settings_repositories_item

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
