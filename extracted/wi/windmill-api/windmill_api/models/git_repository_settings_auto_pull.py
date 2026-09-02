from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.git_repository_settings_auto_pull_mode import GitRepositorySettingsAutoPullMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.git_repository_settings_auto_pull_last_pull_status import GitRepositorySettingsAutoPullLastPullStatus
    from ..models.git_repository_settings_auto_pull_last_synced_sha import GitRepositorySettingsAutoPullLastSyncedSha


T = TypeVar("T", bound="GitRepositorySettingsAutoPull")


@_attrs_define
class GitRepositorySettingsAutoPull:
    """
    Attributes:
        enabled (bool):
        mode (Union[Unset, GitRepositorySettingsAutoPullMode]):
        poll_interval_s (Union[Unset, int]):
        sync_forks (Union[Unset, bool]):
        webhook_id (Union[Unset, int]):
        webhook_secret (Union[Unset, str]):
        webhook_url (Union[Unset, str]):
        webhook_error (Union[Unset, str]):
        last_synced_sha (Union[Unset, GitRepositorySettingsAutoPullLastSyncedSha]):
        last_pull_status (Union[Unset, GitRepositorySettingsAutoPullLastPullStatus]):
    """

    enabled: bool
    mode: Union[Unset, GitRepositorySettingsAutoPullMode] = UNSET
    poll_interval_s: Union[Unset, int] = UNSET
    sync_forks: Union[Unset, bool] = UNSET
    webhook_id: Union[Unset, int] = UNSET
    webhook_secret: Union[Unset, str] = UNSET
    webhook_url: Union[Unset, str] = UNSET
    webhook_error: Union[Unset, str] = UNSET
    last_synced_sha: Union[Unset, "GitRepositorySettingsAutoPullLastSyncedSha"] = UNSET
    last_pull_status: Union[Unset, "GitRepositorySettingsAutoPullLastPullStatus"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        mode: Union[Unset, str] = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        poll_interval_s = self.poll_interval_s
        sync_forks = self.sync_forks
        webhook_id = self.webhook_id
        webhook_secret = self.webhook_secret
        webhook_url = self.webhook_url
        webhook_error = self.webhook_error
        last_synced_sha: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.last_synced_sha, Unset):
            last_synced_sha = self.last_synced_sha.to_dict()

        last_pull_status: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.last_pull_status, Unset):
            last_pull_status = self.last_pull_status.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
            }
        )
        if mode is not UNSET:
            field_dict["mode"] = mode
        if poll_interval_s is not UNSET:
            field_dict["poll_interval_s"] = poll_interval_s
        if sync_forks is not UNSET:
            field_dict["sync_forks"] = sync_forks
        if webhook_id is not UNSET:
            field_dict["webhook_id"] = webhook_id
        if webhook_secret is not UNSET:
            field_dict["webhook_secret"] = webhook_secret
        if webhook_url is not UNSET:
            field_dict["webhook_url"] = webhook_url
        if webhook_error is not UNSET:
            field_dict["webhook_error"] = webhook_error
        if last_synced_sha is not UNSET:
            field_dict["last_synced_sha"] = last_synced_sha
        if last_pull_status is not UNSET:
            field_dict["last_pull_status"] = last_pull_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.git_repository_settings_auto_pull_last_pull_status import (
            GitRepositorySettingsAutoPullLastPullStatus,
        )
        from ..models.git_repository_settings_auto_pull_last_synced_sha import (
            GitRepositorySettingsAutoPullLastSyncedSha,
        )

        d = src_dict.copy()
        enabled = d.pop("enabled")

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, GitRepositorySettingsAutoPullMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = GitRepositorySettingsAutoPullMode(_mode)

        poll_interval_s = d.pop("poll_interval_s", UNSET)

        sync_forks = d.pop("sync_forks", UNSET)

        webhook_id = d.pop("webhook_id", UNSET)

        webhook_secret = d.pop("webhook_secret", UNSET)

        webhook_url = d.pop("webhook_url", UNSET)

        webhook_error = d.pop("webhook_error", UNSET)

        _last_synced_sha = d.pop("last_synced_sha", UNSET)
        last_synced_sha: Union[Unset, GitRepositorySettingsAutoPullLastSyncedSha]
        if isinstance(_last_synced_sha, Unset):
            last_synced_sha = UNSET
        else:
            last_synced_sha = GitRepositorySettingsAutoPullLastSyncedSha.from_dict(_last_synced_sha)

        _last_pull_status = d.pop("last_pull_status", UNSET)
        last_pull_status: Union[Unset, GitRepositorySettingsAutoPullLastPullStatus]
        if isinstance(_last_pull_status, Unset):
            last_pull_status = UNSET
        else:
            last_pull_status = GitRepositorySettingsAutoPullLastPullStatus.from_dict(_last_pull_status)

        git_repository_settings_auto_pull = cls(
            enabled=enabled,
            mode=mode,
            poll_interval_s=poll_interval_s,
            sync_forks=sync_forks,
            webhook_id=webhook_id,
            webhook_secret=webhook_secret,
            webhook_url=webhook_url,
            webhook_error=webhook_error,
            last_synced_sha=last_synced_sha,
            last_pull_status=last_pull_status,
        )

        git_repository_settings_auto_pull.additional_properties = d
        return git_repository_settings_auto_pull

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
