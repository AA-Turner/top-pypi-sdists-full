from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.rancher_node_role_enum import RancherNodeRoleEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_volume_request import DataVolumeRequest


T = TypeVar("T", bound="RancherCreateNodeRequest")


@_attrs_define
class RancherCreateNodeRequest:
    """
    Attributes:
        cluster (str):
        role (RancherNodeRoleEnum):
        subnet (Union[None, str]):
        system_volume_size (Union[Unset, int]):
        system_volume_type (Union[None, Unset, str]):
        memory (Union[Unset, int]):
        cpu (Union[Unset, int]):
        flavor (Union[None, Unset, str]):
        data_volumes (Union[Unset, list['DataVolumeRequest']]):
        ssh_public_key (Union[Unset, str]):
        tenant (Union[Unset, str]):
    """

    cluster: str
    role: RancherNodeRoleEnum
    subnet: Union[None, str]
    system_volume_size: Union[Unset, int] = UNSET
    system_volume_type: Union[None, Unset, str] = UNSET
    memory: Union[Unset, int] = UNSET
    cpu: Union[Unset, int] = UNSET
    flavor: Union[None, Unset, str] = UNSET
    data_volumes: Union[Unset, list["DataVolumeRequest"]] = UNSET
    ssh_public_key: Union[Unset, str] = UNSET
    tenant: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cluster = self.cluster

        role = self.role.value

        subnet: Union[None, str]
        subnet = self.subnet

        system_volume_size = self.system_volume_size

        system_volume_type: Union[None, Unset, str]
        if isinstance(self.system_volume_type, Unset):
            system_volume_type = UNSET
        else:
            system_volume_type = self.system_volume_type

        memory = self.memory

        cpu = self.cpu

        flavor: Union[None, Unset, str]
        if isinstance(self.flavor, Unset):
            flavor = UNSET
        else:
            flavor = self.flavor

        data_volumes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.data_volumes, Unset):
            data_volumes = []
            for data_volumes_item_data in self.data_volumes:
                data_volumes_item = data_volumes_item_data.to_dict()
                data_volumes.append(data_volumes_item)

        ssh_public_key = self.ssh_public_key

        tenant = self.tenant

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cluster": cluster,
                "role": role,
                "subnet": subnet,
            }
        )
        if system_volume_size is not UNSET:
            field_dict["system_volume_size"] = system_volume_size
        if system_volume_type is not UNSET:
            field_dict["system_volume_type"] = system_volume_type
        if memory is not UNSET:
            field_dict["memory"] = memory
        if cpu is not UNSET:
            field_dict["cpu"] = cpu
        if flavor is not UNSET:
            field_dict["flavor"] = flavor
        if data_volumes is not UNSET:
            field_dict["data_volumes"] = data_volumes
        if ssh_public_key is not UNSET:
            field_dict["ssh_public_key"] = ssh_public_key
        if tenant is not UNSET:
            field_dict["tenant"] = tenant

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_volume_request import DataVolumeRequest

        d = dict(src_dict)
        cluster = d.pop("cluster")

        role = RancherNodeRoleEnum(d.pop("role"))

        def _parse_subnet(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        subnet = _parse_subnet(d.pop("subnet"))

        system_volume_size = d.pop("system_volume_size", UNSET)

        def _parse_system_volume_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        system_volume_type = _parse_system_volume_type(d.pop("system_volume_type", UNSET))

        memory = d.pop("memory", UNSET)

        cpu = d.pop("cpu", UNSET)

        def _parse_flavor(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        flavor = _parse_flavor(d.pop("flavor", UNSET))

        data_volumes = []
        _data_volumes = d.pop("data_volumes", UNSET)
        for data_volumes_item_data in _data_volumes or []:
            data_volumes_item = DataVolumeRequest.from_dict(data_volumes_item_data)

            data_volumes.append(data_volumes_item)

        ssh_public_key = d.pop("ssh_public_key", UNSET)

        tenant = d.pop("tenant", UNSET)

        rancher_create_node_request = cls(
            cluster=cluster,
            role=role,
            subnet=subnet,
            system_volume_size=system_volume_size,
            system_volume_type=system_volume_type,
            memory=memory,
            cpu=cpu,
            flavor=flavor,
            data_volumes=data_volumes,
            ssh_public_key=ssh_public_key,
            tenant=tenant,
        )

        rancher_create_node_request.additional_properties = d
        return rancher_create_node_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
