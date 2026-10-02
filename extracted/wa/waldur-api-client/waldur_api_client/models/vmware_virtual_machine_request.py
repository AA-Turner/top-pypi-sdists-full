from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.guest_os_enum import GuestOsEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vmware_nested_network_request import VmwareNestedNetworkRequest


T = TypeVar("T", bound="VmwareVirtualMachineRequest")


@_attrs_define
class VmwareVirtualMachineRequest:
    """
    Attributes:
        name (str):
        service_settings (str):
        project (str):
        description (Union[Unset, str]):
        guest_os (Union[GuestOsEnum, None, Unset]):
        cores (Union[Unset, int]): Number of cores in a VM
        cores_per_socket (Union[Unset, int]): Number of cores per socket in a VM
        ram (Union[Unset, int]): Memory size in MiB
        template (Union[None, Unset, str]):
        cluster (Union[None, Unset, str]):
        networks (Union[Unset, list['VmwareNestedNetworkRequest']]):
        datastore (Union[None, Unset, str]):
        folder (Union[None, Unset, str]):
    """

    name: str
    service_settings: str
    project: str
    description: Union[Unset, str] = UNSET
    guest_os: Union[GuestOsEnum, None, Unset] = UNSET
    cores: Union[Unset, int] = UNSET
    cores_per_socket: Union[Unset, int] = UNSET
    ram: Union[Unset, int] = UNSET
    template: Union[None, Unset, str] = UNSET
    cluster: Union[None, Unset, str] = UNSET
    networks: Union[Unset, list["VmwareNestedNetworkRequest"]] = UNSET
    datastore: Union[None, Unset, str] = UNSET
    folder: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        service_settings = self.service_settings

        project = self.project

        description = self.description

        guest_os: Union[None, Unset, str]
        if isinstance(self.guest_os, Unset):
            guest_os = UNSET
        elif isinstance(self.guest_os, GuestOsEnum):
            guest_os = self.guest_os.value
        else:
            guest_os = self.guest_os

        cores = self.cores

        cores_per_socket = self.cores_per_socket

        ram = self.ram

        template: Union[None, Unset, str]
        if isinstance(self.template, Unset):
            template = UNSET
        else:
            template = self.template

        cluster: Union[None, Unset, str]
        if isinstance(self.cluster, Unset):
            cluster = UNSET
        else:
            cluster = self.cluster

        networks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.networks, Unset):
            networks = []
            for networks_item_data in self.networks:
                networks_item = networks_item_data.to_dict()
                networks.append(networks_item)

        datastore: Union[None, Unset, str]
        if isinstance(self.datastore, Unset):
            datastore = UNSET
        else:
            datastore = self.datastore

        folder: Union[None, Unset, str]
        if isinstance(self.folder, Unset):
            folder = UNSET
        else:
            folder = self.folder

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "service_settings": service_settings,
                "project": project,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if guest_os is not UNSET:
            field_dict["guest_os"] = guest_os
        if cores is not UNSET:
            field_dict["cores"] = cores
        if cores_per_socket is not UNSET:
            field_dict["cores_per_socket"] = cores_per_socket
        if ram is not UNSET:
            field_dict["ram"] = ram
        if template is not UNSET:
            field_dict["template"] = template
        if cluster is not UNSET:
            field_dict["cluster"] = cluster
        if networks is not UNSET:
            field_dict["networks"] = networks
        if datastore is not UNSET:
            field_dict["datastore"] = datastore
        if folder is not UNSET:
            field_dict["folder"] = folder

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vmware_nested_network_request import VmwareNestedNetworkRequest

        d = dict(src_dict)
        name = d.pop("name")

        service_settings = d.pop("service_settings")

        project = d.pop("project")

        description = d.pop("description", UNSET)

        def _parse_guest_os(data: object) -> Union[GuestOsEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                guest_os_type_0 = GuestOsEnum(data)

                return guest_os_type_0
            except:  # noqa: E722
                pass
            return cast(Union[GuestOsEnum, None, Unset], data)

        guest_os = _parse_guest_os(d.pop("guest_os", UNSET))

        cores = d.pop("cores", UNSET)

        cores_per_socket = d.pop("cores_per_socket", UNSET)

        ram = d.pop("ram", UNSET)

        def _parse_template(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        template = _parse_template(d.pop("template", UNSET))

        def _parse_cluster(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cluster = _parse_cluster(d.pop("cluster", UNSET))

        networks = []
        _networks = d.pop("networks", UNSET)
        for networks_item_data in _networks or []:
            networks_item = VmwareNestedNetworkRequest.from_dict(networks_item_data)

            networks.append(networks_item)

        def _parse_datastore(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        datastore = _parse_datastore(d.pop("datastore", UNSET))

        def _parse_folder(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        folder = _parse_folder(d.pop("folder", UNSET))

        vmware_virtual_machine_request = cls(
            name=name,
            service_settings=service_settings,
            project=project,
            description=description,
            guest_os=guest_os,
            cores=cores,
            cores_per_socket=cores_per_socket,
            ram=ram,
            template=template,
            cluster=cluster,
            networks=networks,
            datastore=datastore,
            folder=folder,
        )

        vmware_virtual_machine_request.additional_properties = d
        return vmware_virtual_machine_request

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
