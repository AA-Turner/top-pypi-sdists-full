from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_user_workspaces_response_200_workspaces_item_operator_settings import (
        ListUserWorkspacesResponse200WorkspacesItemOperatorSettings,
    )


T = TypeVar("T", bound="ListUserWorkspacesResponse200WorkspacesItem")


@_attrs_define
class ListUserWorkspacesResponse200WorkspacesItem:
    """
    Attributes:
        id (str):
        name (str):
        username (str):
        color (str):
        operator_settings (Union[Unset, None, ListUserWorkspacesResponse200WorkspacesItemOperatorSettings]):
    """

    id: str
    name: str
    username: str
    color: str
    operator_settings: Union[Unset, None, "ListUserWorkspacesResponse200WorkspacesItemOperatorSettings"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        username = self.username
        color = self.color
        operator_settings: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.operator_settings, Unset):
            operator_settings = self.operator_settings.to_dict() if self.operator_settings else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "username": username,
                "color": color,
            }
        )
        if operator_settings is not UNSET:
            field_dict["operator_settings"] = operator_settings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_user_workspaces_response_200_workspaces_item_operator_settings import (
            ListUserWorkspacesResponse200WorkspacesItemOperatorSettings,
        )

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        username = d.pop("username")

        color = d.pop("color")

        _operator_settings = d.pop("operator_settings", UNSET)
        operator_settings: Union[Unset, None, ListUserWorkspacesResponse200WorkspacesItemOperatorSettings]
        if _operator_settings is None:
            operator_settings = None
        elif isinstance(_operator_settings, Unset):
            operator_settings = UNSET
        else:
            operator_settings = ListUserWorkspacesResponse200WorkspacesItemOperatorSettings.from_dict(
                _operator_settings
            )

        list_user_workspaces_response_200_workspaces_item = cls(
            id=id,
            name=name,
            username=username,
            color=color,
            operator_settings=operator_settings,
        )

        list_user_workspaces_response_200_workspaces_item.additional_properties = d
        return list_user_workspaces_response_200_workspaces_item

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
