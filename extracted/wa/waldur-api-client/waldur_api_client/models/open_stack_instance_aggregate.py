from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OpenStackInstanceAggregate")


@_attrs_define
class OpenStackInstanceAggregate:
    """
    Attributes:
        group_key (str): Group key value
        group_label (str): Human-readable group label
        instance_count (int): Number of instances
        total_cores (int): Total vCPUs
        total_ram_mb (int): Total RAM in MiB
        total_disk_mb (int): Total disk in MiB
        total_volume_size_mb (int): Total attached volume size in MiB
        total_floating_ips (int): Total number of floating IPs
    """

    group_key: str
    group_label: str
    instance_count: int
    total_cores: int
    total_ram_mb: int
    total_disk_mb: int
    total_volume_size_mb: int
    total_floating_ips: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        group_key = self.group_key

        group_label = self.group_label

        instance_count = self.instance_count

        total_cores = self.total_cores

        total_ram_mb = self.total_ram_mb

        total_disk_mb = self.total_disk_mb

        total_volume_size_mb = self.total_volume_size_mb

        total_floating_ips = self.total_floating_ips

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "group_key": group_key,
                "group_label": group_label,
                "instance_count": instance_count,
                "total_cores": total_cores,
                "total_ram_mb": total_ram_mb,
                "total_disk_mb": total_disk_mb,
                "total_volume_size_mb": total_volume_size_mb,
                "total_floating_ips": total_floating_ips,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        group_key = d.pop("group_key")

        group_label = d.pop("group_label")

        instance_count = d.pop("instance_count")

        total_cores = d.pop("total_cores")

        total_ram_mb = d.pop("total_ram_mb")

        total_disk_mb = d.pop("total_disk_mb")

        total_volume_size_mb = d.pop("total_volume_size_mb")

        total_floating_ips = d.pop("total_floating_ips")

        open_stack_instance_aggregate = cls(
            group_key=group_key,
            group_label=group_label,
            instance_count=instance_count,
            total_cores=total_cores,
            total_ram_mb=total_ram_mb,
            total_disk_mb=total_disk_mb,
            total_volume_size_mb=total_volume_size_mb,
            total_floating_ips=total_floating_ips,
        )

        open_stack_instance_aggregate.additional_properties = d
        return open_stack_instance_aggregate

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
