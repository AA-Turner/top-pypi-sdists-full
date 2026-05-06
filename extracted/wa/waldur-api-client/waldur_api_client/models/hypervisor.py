from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Hypervisor")


@_attrs_define
class Hypervisor:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        settings (str):
        backend_id (str):
        hypervisor_type (Union[Unset, str]): Hypervisor type, e.g. KVM, QEMU, VMware
        vcpus (Union[Unset, int]): Total vCPUs
        vcpus_used (Union[Unset, int]): Used vCPUs
        memory_mb (Union[Unset, int]): Total RAM in MiB
        memory_mb_used (Union[Unset, int]): Used RAM in MiB
        local_gb (Union[Unset, int]): Total disk in GiB
        local_gb_used (Union[Unset, int]): Used disk in GiB
        running_vms (Union[Unset, int]): Number of running VMs
        state (Union[Unset, str]): Hypervisor state, e.g. up or down
        status (Union[Unset, str]): Hypervisor status, e.g. enabled or disabled
    """

    url: str
    uuid: UUID
    name: str
    settings: str
    backend_id: str
    hypervisor_type: Union[Unset, str] = UNSET
    vcpus: Union[Unset, int] = UNSET
    vcpus_used: Union[Unset, int] = UNSET
    memory_mb: Union[Unset, int] = UNSET
    memory_mb_used: Union[Unset, int] = UNSET
    local_gb: Union[Unset, int] = UNSET
    local_gb_used: Union[Unset, int] = UNSET
    running_vms: Union[Unset, int] = UNSET
    state: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        settings = self.settings

        backend_id = self.backend_id

        hypervisor_type = self.hypervisor_type

        vcpus = self.vcpus

        vcpus_used = self.vcpus_used

        memory_mb = self.memory_mb

        memory_mb_used = self.memory_mb_used

        local_gb = self.local_gb

        local_gb_used = self.local_gb_used

        running_vms = self.running_vms

        state = self.state

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "settings": settings,
                "backend_id": backend_id,
            }
        )
        if hypervisor_type is not UNSET:
            field_dict["hypervisor_type"] = hypervisor_type
        if vcpus is not UNSET:
            field_dict["vcpus"] = vcpus
        if vcpus_used is not UNSET:
            field_dict["vcpus_used"] = vcpus_used
        if memory_mb is not UNSET:
            field_dict["memory_mb"] = memory_mb
        if memory_mb_used is not UNSET:
            field_dict["memory_mb_used"] = memory_mb_used
        if local_gb is not UNSET:
            field_dict["local_gb"] = local_gb
        if local_gb_used is not UNSET:
            field_dict["local_gb_used"] = local_gb_used
        if running_vms is not UNSET:
            field_dict["running_vms"] = running_vms
        if state is not UNSET:
            field_dict["state"] = state
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        settings = d.pop("settings")

        backend_id = d.pop("backend_id")

        hypervisor_type = d.pop("hypervisor_type", UNSET)

        vcpus = d.pop("vcpus", UNSET)

        vcpus_used = d.pop("vcpus_used", UNSET)

        memory_mb = d.pop("memory_mb", UNSET)

        memory_mb_used = d.pop("memory_mb_used", UNSET)

        local_gb = d.pop("local_gb", UNSET)

        local_gb_used = d.pop("local_gb_used", UNSET)

        running_vms = d.pop("running_vms", UNSET)

        state = d.pop("state", UNSET)

        status = d.pop("status", UNSET)

        hypervisor = cls(
            url=url,
            uuid=uuid,
            name=name,
            settings=settings,
            backend_id=backend_id,
            hypervisor_type=hypervisor_type,
            vcpus=vcpus,
            vcpus_used=vcpus_used,
            memory_mb=memory_mb,
            memory_mb_used=memory_mb_used,
            local_gb=local_gb,
            local_gb_used=local_gb_used,
            running_vms=running_vms,
            state=state,
            status=status,
        )

        hypervisor.additional_properties = d
        return hypervisor

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
