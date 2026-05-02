from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_global_connected_repositories_response_200_item_repositories_item import (
        GetGlobalConnectedRepositoriesResponse200ItemRepositoriesItem,
    )


T = TypeVar("T", bound="GetGlobalConnectedRepositoriesResponse200Item")


@_attrs_define
class GetGlobalConnectedRepositoriesResponse200Item:
    """
    Attributes:
        installation_id (float):
        account_id (str):
        repositories (List['GetGlobalConnectedRepositoriesResponse200ItemRepositoriesItem']):
        total_count (float): Total number of repositories available for this installation
        per_page (float): Number of repositories loaded per page
        workspace_id (Union[Unset, str]):
        error (Union[Unset, str]): Error message if token retrieval failed
    """

    installation_id: float
    account_id: str
    repositories: List["GetGlobalConnectedRepositoriesResponse200ItemRepositoriesItem"]
    total_count: float
    per_page: float
    workspace_id: Union[Unset, str] = UNSET
    error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        installation_id = self.installation_id
        account_id = self.account_id
        repositories = []
        for repositories_item_data in self.repositories:
            repositories_item = repositories_item_data.to_dict()

            repositories.append(repositories_item)

        total_count = self.total_count
        per_page = self.per_page
        workspace_id = self.workspace_id
        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "installation_id": installation_id,
                "account_id": account_id,
                "repositories": repositories,
                "total_count": total_count,
                "per_page": per_page,
            }
        )
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_global_connected_repositories_response_200_item_repositories_item import (
            GetGlobalConnectedRepositoriesResponse200ItemRepositoriesItem,
        )

        d = src_dict.copy()
        installation_id = d.pop("installation_id")

        account_id = d.pop("account_id")

        repositories = []
        _repositories = d.pop("repositories")
        for repositories_item_data in _repositories:
            repositories_item = GetGlobalConnectedRepositoriesResponse200ItemRepositoriesItem.from_dict(
                repositories_item_data
            )

            repositories.append(repositories_item)

        total_count = d.pop("total_count")

        per_page = d.pop("per_page")

        workspace_id = d.pop("workspace_id", UNSET)

        error = d.pop("error", UNSET)

        get_global_connected_repositories_response_200_item = cls(
            installation_id=installation_id,
            account_id=account_id,
            repositories=repositories,
            total_count=total_count,
            per_page=per_page,
            workspace_id=workspace_id,
            error=error,
        )

        get_global_connected_repositories_response_200_item.additional_properties = d
        return get_global_connected_repositories_response_200_item

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
