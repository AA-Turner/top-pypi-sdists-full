from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_instance_datatable_roles_response_200_item_cluster import (
    ListInstanceDatatableRolesResponse200ItemCluster,
)

T = TypeVar("T", bound="ListInstanceDatatableRolesResponse200Item")


@_attrs_define
class ListInstanceDatatableRolesResponse200Item:
    """
    Attributes:
        id (str):
        name (str):
        enabled (bool):
        cluster (ListInstanceDatatableRolesResponse200ItemCluster): The Windmill-managed Postgres cluster a data table
            role is a login on: Windmill's own (behind `instance` data tables) or the external instance cluster (behind
            `external_instance` ones). Defaults to `instance`.
    """

    id: str
    name: str
    enabled: bool
    cluster: ListInstanceDatatableRolesResponse200ItemCluster
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        enabled = self.enabled
        cluster = self.cluster.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "enabled": enabled,
                "cluster": cluster,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        enabled = d.pop("enabled")

        cluster = ListInstanceDatatableRolesResponse200ItemCluster(d.pop("cluster"))

        list_instance_datatable_roles_response_200_item = cls(
            id=id,
            name=name,
            enabled=enabled,
            cluster=cluster,
        )

        list_instance_datatable_roles_response_200_item.additional_properties = d
        return list_instance_datatable_roles_response_200_item

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
