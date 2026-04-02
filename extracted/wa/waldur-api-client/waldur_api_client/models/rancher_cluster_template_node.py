from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.rancher_node_role_enum import RancherNodeRoleEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="RancherClusterTemplateNode")


@_attrs_define
class RancherClusterTemplateNode:
    """
    Attributes:
        min_vcpu (int):
        min_ram (int):
        system_volume_size (int):
        role (RancherNodeRoleEnum):
        preferred_volume_type (Union[Unset, str]):
    """

    min_vcpu: int
    min_ram: int
    system_volume_size: int
    role: RancherNodeRoleEnum
    preferred_volume_type: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        min_vcpu = self.min_vcpu

        min_ram = self.min_ram

        system_volume_size = self.system_volume_size

        role = self.role.value

        preferred_volume_type = self.preferred_volume_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "min_vcpu": min_vcpu,
                "min_ram": min_ram,
                "system_volume_size": system_volume_size,
                "role": role,
            }
        )
        if preferred_volume_type is not UNSET:
            field_dict["preferred_volume_type"] = preferred_volume_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        min_vcpu = d.pop("min_vcpu")

        min_ram = d.pop("min_ram")

        system_volume_size = d.pop("system_volume_size")

        role = RancherNodeRoleEnum(d.pop("role"))

        preferred_volume_type = d.pop("preferred_volume_type", UNSET)

        rancher_cluster_template_node = cls(
            min_vcpu=min_vcpu,
            min_ram=min_ram,
            system_volume_size=system_volume_size,
            role=role,
            preferred_volume_type=preferred_volume_type,
        )

        rancher_cluster_template_node.additional_properties = d
        return rancher_cluster_template_node

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
