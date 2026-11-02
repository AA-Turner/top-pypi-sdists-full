from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.discover_ghes_installations_response_200_item_assigned_workspaces_item import (
        DiscoverGhesInstallationsResponse200ItemAssignedWorkspacesItem,
    )


T = TypeVar("T", bound="DiscoverGhesInstallationsResponse200Item")


@_attrs_define
class DiscoverGhesInstallationsResponse200Item:
    """
    Attributes:
        installation_id (int):
        account_id (str): GitHub login of the installation's account (org or user)
        assigned_workspaces (List['DiscoverGhesInstallationsResponse200ItemAssignedWorkspacesItem']):
    """

    installation_id: int
    account_id: str
    assigned_workspaces: List["DiscoverGhesInstallationsResponse200ItemAssignedWorkspacesItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        installation_id = self.installation_id
        account_id = self.account_id
        assigned_workspaces = []
        for assigned_workspaces_item_data in self.assigned_workspaces:
            assigned_workspaces_item = assigned_workspaces_item_data.to_dict()

            assigned_workspaces.append(assigned_workspaces_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "installation_id": installation_id,
                "account_id": account_id,
                "assigned_workspaces": assigned_workspaces,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.discover_ghes_installations_response_200_item_assigned_workspaces_item import (
            DiscoverGhesInstallationsResponse200ItemAssignedWorkspacesItem,
        )

        d = src_dict.copy()
        installation_id = d.pop("installation_id")

        account_id = d.pop("account_id")

        assigned_workspaces = []
        _assigned_workspaces = d.pop("assigned_workspaces")
        for assigned_workspaces_item_data in _assigned_workspaces:
            assigned_workspaces_item = DiscoverGhesInstallationsResponse200ItemAssignedWorkspacesItem.from_dict(
                assigned_workspaces_item_data
            )

            assigned_workspaces.append(assigned_workspaces_item)

        discover_ghes_installations_response_200_item = cls(
            installation_id=installation_id,
            account_id=account_id,
            assigned_workspaces=assigned_workspaces,
        )

        discover_ghes_installations_response_200_item.additional_properties = d
        return discover_ghes_installations_response_200_item

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
