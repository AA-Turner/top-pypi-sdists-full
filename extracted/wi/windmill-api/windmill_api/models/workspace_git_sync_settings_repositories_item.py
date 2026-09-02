from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_git_sync_settings_repositories_item_exclude_types_override_item import (
    WorkspaceGitSyncSettingsRepositoriesItemExcludeTypesOverrideItem,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace_git_sync_settings_repositories_item_auto_pull import (
        WorkspaceGitSyncSettingsRepositoriesItemAutoPull,
    )
    from ..models.workspace_git_sync_settings_repositories_item_settings import (
        WorkspaceGitSyncSettingsRepositoriesItemSettings,
    )


T = TypeVar("T", bound="WorkspaceGitSyncSettingsRepositoriesItem")


@_attrs_define
class WorkspaceGitSyncSettingsRepositoriesItem:
    """
    Attributes:
        git_repo_resource_path (str):
        script_path (Union[Unset, str]):
        use_individual_branch (Union[Unset, bool]):
        group_by_folder (Union[Unset, bool]):
        collapsed (Union[Unset, bool]):
        settings (Union[Unset, WorkspaceGitSyncSettingsRepositoriesItemSettings]):
        exclude_types_override (Union[Unset, List[WorkspaceGitSyncSettingsRepositoriesItemExcludeTypesOverrideItem]]):
        auto_pull (Union[Unset, WorkspaceGitSyncSettingsRepositoriesItemAutoPull]):
        promotion_open_prs (Union[Unset, bool]):
        fork_open_prs (Union[Unset, bool]):
        open_pr_error (Union[Unset, str]): server-owned, last failure opening a PR for a deploy branch of this repo
    """

    git_repo_resource_path: str
    script_path: Union[Unset, str] = UNSET
    use_individual_branch: Union[Unset, bool] = UNSET
    group_by_folder: Union[Unset, bool] = UNSET
    collapsed: Union[Unset, bool] = UNSET
    settings: Union[Unset, "WorkspaceGitSyncSettingsRepositoriesItemSettings"] = UNSET
    exclude_types_override: Union[Unset, List[WorkspaceGitSyncSettingsRepositoriesItemExcludeTypesOverrideItem]] = UNSET
    auto_pull: Union[Unset, "WorkspaceGitSyncSettingsRepositoriesItemAutoPull"] = UNSET
    promotion_open_prs: Union[Unset, bool] = UNSET
    fork_open_prs: Union[Unset, bool] = UNSET
    open_pr_error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        git_repo_resource_path = self.git_repo_resource_path
        script_path = self.script_path
        use_individual_branch = self.use_individual_branch
        group_by_folder = self.group_by_folder
        collapsed = self.collapsed
        settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        exclude_types_override: Union[Unset, List[str]] = UNSET
        if not isinstance(self.exclude_types_override, Unset):
            exclude_types_override = []
            for exclude_types_override_item_data in self.exclude_types_override:
                exclude_types_override_item = exclude_types_override_item_data.value

                exclude_types_override.append(exclude_types_override_item)

        auto_pull: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.auto_pull, Unset):
            auto_pull = self.auto_pull.to_dict()

        promotion_open_prs = self.promotion_open_prs
        fork_open_prs = self.fork_open_prs
        open_pr_error = self.open_pr_error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "git_repo_resource_path": git_repo_resource_path,
            }
        )
        if script_path is not UNSET:
            field_dict["script_path"] = script_path
        if use_individual_branch is not UNSET:
            field_dict["use_individual_branch"] = use_individual_branch
        if group_by_folder is not UNSET:
            field_dict["group_by_folder"] = group_by_folder
        if collapsed is not UNSET:
            field_dict["collapsed"] = collapsed
        if settings is not UNSET:
            field_dict["settings"] = settings
        if exclude_types_override is not UNSET:
            field_dict["exclude_types_override"] = exclude_types_override
        if auto_pull is not UNSET:
            field_dict["auto_pull"] = auto_pull
        if promotion_open_prs is not UNSET:
            field_dict["promotion_open_prs"] = promotion_open_prs
        if fork_open_prs is not UNSET:
            field_dict["fork_open_prs"] = fork_open_prs
        if open_pr_error is not UNSET:
            field_dict["open_pr_error"] = open_pr_error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workspace_git_sync_settings_repositories_item_auto_pull import (
            WorkspaceGitSyncSettingsRepositoriesItemAutoPull,
        )
        from ..models.workspace_git_sync_settings_repositories_item_settings import (
            WorkspaceGitSyncSettingsRepositoriesItemSettings,
        )

        d = src_dict.copy()
        git_repo_resource_path = d.pop("git_repo_resource_path")

        script_path = d.pop("script_path", UNSET)

        use_individual_branch = d.pop("use_individual_branch", UNSET)

        group_by_folder = d.pop("group_by_folder", UNSET)

        collapsed = d.pop("collapsed", UNSET)

        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, WorkspaceGitSyncSettingsRepositoriesItemSettings]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = WorkspaceGitSyncSettingsRepositoriesItemSettings.from_dict(_settings)

        exclude_types_override = []
        _exclude_types_override = d.pop("exclude_types_override", UNSET)
        for exclude_types_override_item_data in _exclude_types_override or []:
            exclude_types_override_item = WorkspaceGitSyncSettingsRepositoriesItemExcludeTypesOverrideItem(
                exclude_types_override_item_data
            )

            exclude_types_override.append(exclude_types_override_item)

        _auto_pull = d.pop("auto_pull", UNSET)
        auto_pull: Union[Unset, WorkspaceGitSyncSettingsRepositoriesItemAutoPull]
        if isinstance(_auto_pull, Unset):
            auto_pull = UNSET
        else:
            auto_pull = WorkspaceGitSyncSettingsRepositoriesItemAutoPull.from_dict(_auto_pull)

        promotion_open_prs = d.pop("promotion_open_prs", UNSET)

        fork_open_prs = d.pop("fork_open_prs", UNSET)

        open_pr_error = d.pop("open_pr_error", UNSET)

        workspace_git_sync_settings_repositories_item = cls(
            git_repo_resource_path=git_repo_resource_path,
            script_path=script_path,
            use_individual_branch=use_individual_branch,
            group_by_folder=group_by_folder,
            collapsed=collapsed,
            settings=settings,
            exclude_types_override=exclude_types_override,
            auto_pull=auto_pull,
            promotion_open_prs=promotion_open_prs,
            fork_open_prs=fork_open_prs,
            open_pr_error=open_pr_error,
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
