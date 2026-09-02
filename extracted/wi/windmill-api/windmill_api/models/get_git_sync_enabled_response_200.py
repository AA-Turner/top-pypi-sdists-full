from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetGitSyncEnabledResponse200")


@_attrs_define
class GetGitSyncEnabledResponse200:
    """
    Attributes:
        enabled (Union[Unset, bool]):
        reason (Union[Unset, None, str]):
        max_repos (Union[Unset, None, int]):
        user_count (Union[Unset, None, int]):
        max_users (Union[Unset, None, int]):
    """

    enabled: Union[Unset, bool] = UNSET
    reason: Union[Unset, None, str] = UNSET
    max_repos: Union[Unset, None, int] = UNSET
    user_count: Union[Unset, None, int] = UNSET
    max_users: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        reason = self.reason
        max_repos = self.max_repos
        user_count = self.user_count
        max_users = self.max_users

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if reason is not UNSET:
            field_dict["reason"] = reason
        if max_repos is not UNSET:
            field_dict["max_repos"] = max_repos
        if user_count is not UNSET:
            field_dict["user_count"] = user_count
        if max_users is not UNSET:
            field_dict["max_users"] = max_users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        reason = d.pop("reason", UNSET)

        max_repos = d.pop("max_repos", UNSET)

        user_count = d.pop("user_count", UNSET)

        max_users = d.pop("max_users", UNSET)

        get_git_sync_enabled_response_200 = cls(
            enabled=enabled,
            reason=reason,
            max_repos=max_repos,
            user_count=user_count,
            max_users=max_users,
        )

        get_git_sync_enabled_response_200.additional_properties = d
        return get_git_sync_enabled_response_200

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
