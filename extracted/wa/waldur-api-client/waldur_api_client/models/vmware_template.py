import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="VmwareTemplate")


@_attrs_define
class VmwareTemplate:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        guest_os (str): Defines the valid guest operating system types used for configuring a virtual machine
        guest_os_name (str):
        description (Union[Unset, str]):
        cores (Union[Unset, int]): Number of cores in a VM
        cores_per_socket (Union[Unset, int]): Number of cores per socket in a VM
        ram (Union[Unset, int]): Memory size in MiB
        disk (Union[Unset, int]): Disk size in MiB
    """

    url: str
    uuid: UUID
    name: str
    created: datetime.datetime
    modified: datetime.datetime
    guest_os: str
    guest_os_name: str
    description: Union[Unset, str] = UNSET
    cores: Union[Unset, int] = UNSET
    cores_per_socket: Union[Unset, int] = UNSET
    ram: Union[Unset, int] = UNSET
    disk: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        guest_os = self.guest_os

        guest_os_name = self.guest_os_name

        description = self.description

        cores = self.cores

        cores_per_socket = self.cores_per_socket

        ram = self.ram

        disk = self.disk

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "created": created,
                "modified": modified,
                "guest_os": guest_os,
                "guest_os_name": guest_os_name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if cores is not UNSET:
            field_dict["cores"] = cores
        if cores_per_socket is not UNSET:
            field_dict["cores_per_socket"] = cores_per_socket
        if ram is not UNSET:
            field_dict["ram"] = ram
        if disk is not UNSET:
            field_dict["disk"] = disk

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        guest_os = d.pop("guest_os")

        guest_os_name = d.pop("guest_os_name")

        description = d.pop("description", UNSET)

        cores = d.pop("cores", UNSET)

        cores_per_socket = d.pop("cores_per_socket", UNSET)

        ram = d.pop("ram", UNSET)

        disk = d.pop("disk", UNSET)

        vmware_template = cls(
            url=url,
            uuid=uuid,
            name=name,
            created=created,
            modified=modified,
            guest_os=guest_os,
            guest_os_name=guest_os_name,
            description=description,
            cores=cores,
            cores_per_socket=cores_per_socket,
            ram=ram,
            disk=disk,
        )

        vmware_template.additional_properties = d
        return vmware_template

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
