from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GithubAppStaleWebhooksResponse200Item")


@_attrs_define
class GithubAppStaleWebhooksResponse200Item:
    """
    Attributes:
        workspace_id (str):
        git_repo_resource_path (str):
        registered_url (Union[Unset, None, str]):
    """

    workspace_id: str
    git_repo_resource_path: str
    registered_url: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        git_repo_resource_path = self.git_repo_resource_path
        registered_url = self.registered_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_id": workspace_id,
                "git_repo_resource_path": git_repo_resource_path,
            }
        )
        if registered_url is not UNSET:
            field_dict["registered_url"] = registered_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        git_repo_resource_path = d.pop("git_repo_resource_path")

        registered_url = d.pop("registered_url", UNSET)

        github_app_stale_webhooks_response_200_item = cls(
            workspace_id=workspace_id,
            git_repo_resource_path=git_repo_resource_path,
            registered_url=registered_url,
        )

        github_app_stale_webhooks_response_200_item.additional_properties = d
        return github_app_stale_webhooks_response_200_item

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
