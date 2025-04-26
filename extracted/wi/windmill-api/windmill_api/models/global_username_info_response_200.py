from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.global_username_info_response_200_workspace_usernames_item import (
        GlobalUsernameInfoResponse200WorkspaceUsernamesItem,
    )


T = TypeVar("T", bound="GlobalUsernameInfoResponse200")


@_attrs_define
class GlobalUsernameInfoResponse200:
    """
    Attributes:
        username (str):
        workspace_usernames (List['GlobalUsernameInfoResponse200WorkspaceUsernamesItem']):
    """

    username: str
    workspace_usernames: List["GlobalUsernameInfoResponse200WorkspaceUsernamesItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username
        workspace_usernames = []
        for workspace_usernames_item_data in self.workspace_usernames:
            workspace_usernames_item = workspace_usernames_item_data.to_dict()

            workspace_usernames.append(workspace_usernames_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "workspace_usernames": workspace_usernames,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.global_username_info_response_200_workspace_usernames_item import (
            GlobalUsernameInfoResponse200WorkspaceUsernamesItem,
        )

        d = src_dict.copy()
        username = d.pop("username")

        workspace_usernames = []
        _workspace_usernames = d.pop("workspace_usernames")
        for workspace_usernames_item_data in _workspace_usernames:
            workspace_usernames_item = GlobalUsernameInfoResponse200WorkspaceUsernamesItem.from_dict(
                workspace_usernames_item_data
            )

            workspace_usernames.append(workspace_usernames_item)

        global_username_info_response_200 = cls(
            username=username,
            workspace_usernames=workspace_usernames,
        )

        global_username_info_response_200.additional_properties = d
        return global_username_info_response_200

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
