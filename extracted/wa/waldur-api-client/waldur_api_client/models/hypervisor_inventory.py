from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HypervisorInventory")


@_attrs_define
class HypervisorInventory:
    """
    Attributes:
        url (str):
        uuid (UUID):
        hypervisor (str):
        hypervisor_uuid (UUID):
        hypervisor_name (str):
        settings (str):
        settings_uuid (UUID):
        resource_class (str): Placement resource class, e.g. VCPU, MEMORY_MB, DISK_GB, VGPU, PCI_DEVICE, NUMA_CORE,
            CUSTOM_*.
        effective_total (int): Capacity the Nova scheduler treats as available.
        total (Union[Unset, int]):
        reserved (Union[Unset, int]):
        allocation_ratio (Union[Unset, float]):
        used (Union[Unset, int]):
    """

    url: str
    uuid: UUID
    hypervisor: str
    hypervisor_uuid: UUID
    hypervisor_name: str
    settings: str
    settings_uuid: UUID
    resource_class: str
    effective_total: int
    total: Union[Unset, int] = UNSET
    reserved: Union[Unset, int] = UNSET
    allocation_ratio: Union[Unset, float] = UNSET
    used: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        hypervisor = self.hypervisor

        hypervisor_uuid = str(self.hypervisor_uuid)

        hypervisor_name = self.hypervisor_name

        settings = self.settings

        settings_uuid = str(self.settings_uuid)

        resource_class = self.resource_class

        effective_total = self.effective_total

        total = self.total

        reserved = self.reserved

        allocation_ratio = self.allocation_ratio

        used = self.used

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "hypervisor": hypervisor,
                "hypervisor_uuid": hypervisor_uuid,
                "hypervisor_name": hypervisor_name,
                "settings": settings,
                "settings_uuid": settings_uuid,
                "resource_class": resource_class,
                "effective_total": effective_total,
            }
        )
        if total is not UNSET:
            field_dict["total"] = total
        if reserved is not UNSET:
            field_dict["reserved"] = reserved
        if allocation_ratio is not UNSET:
            field_dict["allocation_ratio"] = allocation_ratio
        if used is not UNSET:
            field_dict["used"] = used

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        hypervisor = d.pop("hypervisor")

        hypervisor_uuid = UUID(d.pop("hypervisor_uuid"))

        hypervisor_name = d.pop("hypervisor_name")

        settings = d.pop("settings")

        settings_uuid = UUID(d.pop("settings_uuid"))

        resource_class = d.pop("resource_class")

        effective_total = d.pop("effective_total")

        total = d.pop("total", UNSET)

        reserved = d.pop("reserved", UNSET)

        allocation_ratio = d.pop("allocation_ratio", UNSET)

        used = d.pop("used", UNSET)

        hypervisor_inventory = cls(
            url=url,
            uuid=uuid,
            hypervisor=hypervisor,
            hypervisor_uuid=hypervisor_uuid,
            hypervisor_name=hypervisor_name,
            settings=settings,
            settings_uuid=settings_uuid,
            resource_class=resource_class,
            effective_total=effective_total,
            total=total,
            reserved=reserved,
            allocation_ratio=allocation_ratio,
            used=used,
        )

        hypervisor_inventory.additional_properties = d
        return hypervisor_inventory

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
