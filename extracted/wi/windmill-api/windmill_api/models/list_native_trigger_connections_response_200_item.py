from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListNativeTriggerConnectionsResponse200Item")


@_attrs_define
class ListNativeTriggerConnectionsResponse200Item:
    """An account connected for native triggers, stored as an OAuth resource

    Attributes:
        path (str): Path of the resource and variable holding the connection
        workspace (bool): Whether this is the workspace connection, which every member may use
        owner (Union[Unset, None, str]): Username of whoever connected the account, when the caller can read its
            resource
    """

    path: str
    workspace: bool
    owner: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        workspace = self.workspace
        owner = self.owner

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "workspace": workspace,
            }
        )
        if owner is not UNSET:
            field_dict["owner"] = owner

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        workspace = d.pop("workspace")

        owner = d.pop("owner", UNSET)

        list_native_trigger_connections_response_200_item = cls(
            path=path,
            workspace=workspace,
            owner=owner,
        )

        list_native_trigger_connections_response_200_item.additional_properties = d
        return list_native_trigger_connections_response_200_item

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
