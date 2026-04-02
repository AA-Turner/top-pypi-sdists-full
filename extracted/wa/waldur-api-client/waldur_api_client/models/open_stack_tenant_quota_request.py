from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackTenantQuotaRequest")


@_attrs_define
class OpenStackTenantQuotaRequest:
    """
    Attributes:
        instances (Union[Unset, int]):
        volumes (Union[Unset, int]):
        snapshots (Union[Unset, int]):
        ram (Union[Unset, int]):
        vcpu (Union[Unset, int]):
        storage (Union[Unset, int]):
        security_group_count (Union[Unset, int]):
        security_group_rule_count (Union[Unset, int]):
    """

    instances: Union[Unset, int] = UNSET
    volumes: Union[Unset, int] = UNSET
    snapshots: Union[Unset, int] = UNSET
    ram: Union[Unset, int] = UNSET
    vcpu: Union[Unset, int] = UNSET
    storage: Union[Unset, int] = UNSET
    security_group_count: Union[Unset, int] = UNSET
    security_group_rule_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        instances = self.instances

        volumes = self.volumes

        snapshots = self.snapshots

        ram = self.ram

        vcpu = self.vcpu

        storage = self.storage

        security_group_count = self.security_group_count

        security_group_rule_count = self.security_group_rule_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if instances is not UNSET:
            field_dict["instances"] = instances
        if volumes is not UNSET:
            field_dict["volumes"] = volumes
        if snapshots is not UNSET:
            field_dict["snapshots"] = snapshots
        if ram is not UNSET:
            field_dict["ram"] = ram
        if vcpu is not UNSET:
            field_dict["vcpu"] = vcpu
        if storage is not UNSET:
            field_dict["storage"] = storage
        if security_group_count is not UNSET:
            field_dict["security_group_count"] = security_group_count
        if security_group_rule_count is not UNSET:
            field_dict["security_group_rule_count"] = security_group_rule_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        instances = d.pop("instances", UNSET)

        volumes = d.pop("volumes", UNSET)

        snapshots = d.pop("snapshots", UNSET)

        ram = d.pop("ram", UNSET)

        vcpu = d.pop("vcpu", UNSET)

        storage = d.pop("storage", UNSET)

        security_group_count = d.pop("security_group_count", UNSET)

        security_group_rule_count = d.pop("security_group_rule_count", UNSET)

        open_stack_tenant_quota_request = cls(
            instances=instances,
            volumes=volumes,
            snapshots=snapshots,
            ram=ram,
            vcpu=vcpu,
            storage=storage,
            security_group_count=security_group_count,
            security_group_rule_count=security_group_rule_count,
        )

        open_stack_tenant_quota_request.additional_properties = d
        return open_stack_tenant_quota_request

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
