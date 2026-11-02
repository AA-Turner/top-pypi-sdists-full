from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_workspace_roles_response_200_roles_item_source import ListWorkspaceRolesResponse200RolesItemSource

if TYPE_CHECKING:
    from ..models.list_workspace_roles_response_200_roles_item_capabilities import (
        ListWorkspaceRolesResponse200RolesItemCapabilities,
    )


T = TypeVar("T", bound="ListWorkspaceRolesResponse200RolesItem")


@_attrs_define
class ListWorkspaceRolesResponse200RolesItem:
    """
    Attributes:
        name (str):
        label (str):
        capabilities (ListWorkspaceRolesResponse200RolesItemCapabilities):
        source (ListWorkspaceRolesResponse200RolesItemSource):
        overridden (bool):
    """

    name: str
    label: str
    capabilities: "ListWorkspaceRolesResponse200RolesItemCapabilities"
    source: ListWorkspaceRolesResponse200RolesItemSource
    overridden: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        label = self.label
        capabilities = self.capabilities.to_dict()

        source = self.source.value

        overridden = self.overridden

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "label": label,
                "capabilities": capabilities,
                "source": source,
                "overridden": overridden,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_workspace_roles_response_200_roles_item_capabilities import (
            ListWorkspaceRolesResponse200RolesItemCapabilities,
        )

        d = src_dict.copy()
        name = d.pop("name")

        label = d.pop("label")

        capabilities = ListWorkspaceRolesResponse200RolesItemCapabilities.from_dict(d.pop("capabilities"))

        source = ListWorkspaceRolesResponse200RolesItemSource(d.pop("source"))

        overridden = d.pop("overridden")

        list_workspace_roles_response_200_roles_item = cls(
            name=name,
            label=label,
            capabilities=capabilities,
            source=source,
            overridden=overridden,
        )

        list_workspace_roles_response_200_roles_item.additional_properties = d
        return list_workspace_roles_response_200_roles_item

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
