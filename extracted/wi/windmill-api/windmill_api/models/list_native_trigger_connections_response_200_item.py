from typing import Any, Dict, List, Type, TypeVar, Union, cast

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
        managed (bool): Whether the integration trigger connect flow made it. Any other connection is a resource
            connected from Resources, which triggers can use but only Resources can replace or delete.
        owner (Union[Unset, None, str]): Username of whoever connected the account, when the caller can read its
            resource
        scopes (Union[Unset, None, List[str]]): Scopes the account was connected with; absent when unknown
        missing_scopes (Union[Unset, None, List[str]]): Scopes the service's triggers need that the account lacks;
            absent when unknown
    """

    path: str
    workspace: bool
    managed: bool
    owner: Union[Unset, None, str] = UNSET
    scopes: Union[Unset, None, List[str]] = UNSET
    missing_scopes: Union[Unset, None, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        workspace = self.workspace
        managed = self.managed
        owner = self.owner
        scopes: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            if self.scopes is None:
                scopes = None
            else:
                scopes = self.scopes

        missing_scopes: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.missing_scopes, Unset):
            if self.missing_scopes is None:
                missing_scopes = None
            else:
                missing_scopes = self.missing_scopes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "workspace": workspace,
                "managed": managed,
            }
        )
        if owner is not UNSET:
            field_dict["owner"] = owner
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if missing_scopes is not UNSET:
            field_dict["missing_scopes"] = missing_scopes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        workspace = d.pop("workspace")

        managed = d.pop("managed")

        owner = d.pop("owner", UNSET)

        scopes = cast(List[str], d.pop("scopes", UNSET))

        missing_scopes = cast(List[str], d.pop("missing_scopes", UNSET))

        list_native_trigger_connections_response_200_item = cls(
            path=path,
            workspace=workspace,
            managed=managed,
            owner=owner,
            scopes=scopes,
            missing_scopes=missing_scopes,
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
