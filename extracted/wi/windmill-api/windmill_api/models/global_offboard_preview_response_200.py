from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.global_offboard_preview_response_200_workspaces_item import (
        GlobalOffboardPreviewResponse200WorkspacesItem,
    )


T = TypeVar("T", bound="GlobalOffboardPreviewResponse200")


@_attrs_define
class GlobalOffboardPreviewResponse200:
    """
    Attributes:
        workspaces (List['GlobalOffboardPreviewResponse200WorkspacesItem']):
    """

    workspaces: List["GlobalOffboardPreviewResponse200WorkspacesItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspaces = []
        for workspaces_item_data in self.workspaces:
            workspaces_item = workspaces_item_data.to_dict()

            workspaces.append(workspaces_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspaces": workspaces,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.global_offboard_preview_response_200_workspaces_item import (
            GlobalOffboardPreviewResponse200WorkspacesItem,
        )

        d = src_dict.copy()
        workspaces = []
        _workspaces = d.pop("workspaces")
        for workspaces_item_data in _workspaces:
            workspaces_item = GlobalOffboardPreviewResponse200WorkspacesItem.from_dict(workspaces_item_data)

            workspaces.append(workspaces_item)

        global_offboard_preview_response_200 = cls(
            workspaces=workspaces,
        )

        global_offboard_preview_response_200.additional_properties = d
        return global_offboard_preview_response_200

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
