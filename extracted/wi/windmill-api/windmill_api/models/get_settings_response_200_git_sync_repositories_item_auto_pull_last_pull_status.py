from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetSettingsResponse200GitSyncRepositoriesItemAutoPullLastPullStatus")


@_attrs_define
class GetSettingsResponse200GitSyncRepositoriesItemAutoPullLastPullStatus:
    """
    Attributes:
        at (int):
        success (bool):
        synced_sha (Union[Unset, str]):
        job_id (Union[Unset, str]):
        error (Union[Unset, str]):
    """

    at: int
    success: bool
    synced_sha: Union[Unset, str] = UNSET
    job_id: Union[Unset, str] = UNSET
    error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        at = self.at
        success = self.success
        synced_sha = self.synced_sha
        job_id = self.job_id
        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "at": at,
                "success": success,
            }
        )
        if synced_sha is not UNSET:
            field_dict["synced_sha"] = synced_sha
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        at = d.pop("at")

        success = d.pop("success")

        synced_sha = d.pop("synced_sha", UNSET)

        job_id = d.pop("job_id", UNSET)

        error = d.pop("error", UNSET)

        get_settings_response_200_git_sync_repositories_item_auto_pull_last_pull_status = cls(
            at=at,
            success=success,
            synced_sha=synced_sha,
            job_id=job_id,
            error=error,
        )

        get_settings_response_200_git_sync_repositories_item_auto_pull_last_pull_status.additional_properties = d
        return get_settings_response_200_git_sync_repositories_item_auto_pull_last_pull_status

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
