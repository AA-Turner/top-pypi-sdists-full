from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_instance_datatable_role_json_body_cluster import CreateInstanceDatatableRoleJsonBodyCluster
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateInstanceDatatableRoleJsonBody")


@_attrs_define
class CreateInstanceDatatableRoleJsonBody:
    """
    Attributes:
        name (str):
        cluster (Union[Unset, CreateInstanceDatatableRoleJsonBodyCluster]): The Windmill-managed Postgres cluster a data
            table role is a login on: Windmill's own (behind `instance` data tables) or the external instance cluster
            (behind `external_instance` ones). Defaults to `instance`.
    """

    name: str
    cluster: Union[Unset, CreateInstanceDatatableRoleJsonBodyCluster] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        cluster: Union[Unset, str] = UNSET
        if not isinstance(self.cluster, Unset):
            cluster = self.cluster.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if cluster is not UNSET:
            field_dict["cluster"] = cluster

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        _cluster = d.pop("cluster", UNSET)
        cluster: Union[Unset, CreateInstanceDatatableRoleJsonBodyCluster]
        if isinstance(_cluster, Unset):
            cluster = UNSET
        else:
            cluster = CreateInstanceDatatableRoleJsonBodyCluster(_cluster)

        create_instance_datatable_role_json_body = cls(
            name=name,
            cluster=cluster,
        )

        create_instance_datatable_role_json_body.additional_properties = d
        return create_instance_datatable_role_json_body

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
