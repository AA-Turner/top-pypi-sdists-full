from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="K8SDefaultConfiguration")


@_attrs_define
class K8SDefaultConfiguration:
    """
    Attributes:
        default_controller_vcpus (Union[Unset, int]):
        default_controller_ram_gb (Union[Unset, int]):
        default_controller_system_disk_gb (Union[Unset, int]):
        default_controller_etcd_disk_gb (Union[Unset, int]):
        default_lb_vcpus (Union[Unset, int]):
        default_lb_ram_gb (Union[Unset, int]):
        default_lb_system_disk_gb (Union[Unset, int]):
        default_lb_logs_disk_gb (Union[Unset, int]):
        minimal_worker_vcpus (Union[Unset, int]):
        minimal_worker_ram_gb (Union[Unset, int]):
        default_worker_data_disk_gb (Union[Unset, int]):
        default_storage_data_disk_gb (Union[Unset, int]):
        default_storage_san_disk_gb (Union[Unset, int]):
        available_kubernetes_versions (Union[Unset, str]): Comma-separated list of Kubernetes versions (e.g.,
            1.32.0,1.33.0,1.34.0)
    """

    default_controller_vcpus: Union[Unset, int] = UNSET
    default_controller_ram_gb: Union[Unset, int] = UNSET
    default_controller_system_disk_gb: Union[Unset, int] = UNSET
    default_controller_etcd_disk_gb: Union[Unset, int] = UNSET
    default_lb_vcpus: Union[Unset, int] = UNSET
    default_lb_ram_gb: Union[Unset, int] = UNSET
    default_lb_system_disk_gb: Union[Unset, int] = UNSET
    default_lb_logs_disk_gb: Union[Unset, int] = UNSET
    minimal_worker_vcpus: Union[Unset, int] = UNSET
    minimal_worker_ram_gb: Union[Unset, int] = UNSET
    default_worker_data_disk_gb: Union[Unset, int] = UNSET
    default_storage_data_disk_gb: Union[Unset, int] = UNSET
    default_storage_san_disk_gb: Union[Unset, int] = UNSET
    available_kubernetes_versions: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default_controller_vcpus = self.default_controller_vcpus

        default_controller_ram_gb = self.default_controller_ram_gb

        default_controller_system_disk_gb = self.default_controller_system_disk_gb

        default_controller_etcd_disk_gb = self.default_controller_etcd_disk_gb

        default_lb_vcpus = self.default_lb_vcpus

        default_lb_ram_gb = self.default_lb_ram_gb

        default_lb_system_disk_gb = self.default_lb_system_disk_gb

        default_lb_logs_disk_gb = self.default_lb_logs_disk_gb

        minimal_worker_vcpus = self.minimal_worker_vcpus

        minimal_worker_ram_gb = self.minimal_worker_ram_gb

        default_worker_data_disk_gb = self.default_worker_data_disk_gb

        default_storage_data_disk_gb = self.default_storage_data_disk_gb

        default_storage_san_disk_gb = self.default_storage_san_disk_gb

        available_kubernetes_versions = self.available_kubernetes_versions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if default_controller_vcpus is not UNSET:
            field_dict["default_controller_vcpus"] = default_controller_vcpus
        if default_controller_ram_gb is not UNSET:
            field_dict["default_controller_ram_gb"] = default_controller_ram_gb
        if default_controller_system_disk_gb is not UNSET:
            field_dict["default_controller_system_disk_gb"] = default_controller_system_disk_gb
        if default_controller_etcd_disk_gb is not UNSET:
            field_dict["default_controller_etcd_disk_gb"] = default_controller_etcd_disk_gb
        if default_lb_vcpus is not UNSET:
            field_dict["default_lb_vcpus"] = default_lb_vcpus
        if default_lb_ram_gb is not UNSET:
            field_dict["default_lb_ram_gb"] = default_lb_ram_gb
        if default_lb_system_disk_gb is not UNSET:
            field_dict["default_lb_system_disk_gb"] = default_lb_system_disk_gb
        if default_lb_logs_disk_gb is not UNSET:
            field_dict["default_lb_logs_disk_gb"] = default_lb_logs_disk_gb
        if minimal_worker_vcpus is not UNSET:
            field_dict["minimal_worker_vcpus"] = minimal_worker_vcpus
        if minimal_worker_ram_gb is not UNSET:
            field_dict["minimal_worker_ram_gb"] = minimal_worker_ram_gb
        if default_worker_data_disk_gb is not UNSET:
            field_dict["default_worker_data_disk_gb"] = default_worker_data_disk_gb
        if default_storage_data_disk_gb is not UNSET:
            field_dict["default_storage_data_disk_gb"] = default_storage_data_disk_gb
        if default_storage_san_disk_gb is not UNSET:
            field_dict["default_storage_san_disk_gb"] = default_storage_san_disk_gb
        if available_kubernetes_versions is not UNSET:
            field_dict["available_kubernetes_versions"] = available_kubernetes_versions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        default_controller_vcpus = d.pop("default_controller_vcpus", UNSET)

        default_controller_ram_gb = d.pop("default_controller_ram_gb", UNSET)

        default_controller_system_disk_gb = d.pop("default_controller_system_disk_gb", UNSET)

        default_controller_etcd_disk_gb = d.pop("default_controller_etcd_disk_gb", UNSET)

        default_lb_vcpus = d.pop("default_lb_vcpus", UNSET)

        default_lb_ram_gb = d.pop("default_lb_ram_gb", UNSET)

        default_lb_system_disk_gb = d.pop("default_lb_system_disk_gb", UNSET)

        default_lb_logs_disk_gb = d.pop("default_lb_logs_disk_gb", UNSET)

        minimal_worker_vcpus = d.pop("minimal_worker_vcpus", UNSET)

        minimal_worker_ram_gb = d.pop("minimal_worker_ram_gb", UNSET)

        default_worker_data_disk_gb = d.pop("default_worker_data_disk_gb", UNSET)

        default_storage_data_disk_gb = d.pop("default_storage_data_disk_gb", UNSET)

        default_storage_san_disk_gb = d.pop("default_storage_san_disk_gb", UNSET)

        available_kubernetes_versions = d.pop("available_kubernetes_versions", UNSET)

        k8s_default_configuration = cls(
            default_controller_vcpus=default_controller_vcpus,
            default_controller_ram_gb=default_controller_ram_gb,
            default_controller_system_disk_gb=default_controller_system_disk_gb,
            default_controller_etcd_disk_gb=default_controller_etcd_disk_gb,
            default_lb_vcpus=default_lb_vcpus,
            default_lb_ram_gb=default_lb_ram_gb,
            default_lb_system_disk_gb=default_lb_system_disk_gb,
            default_lb_logs_disk_gb=default_lb_logs_disk_gb,
            minimal_worker_vcpus=minimal_worker_vcpus,
            minimal_worker_ram_gb=minimal_worker_ram_gb,
            default_worker_data_disk_gb=default_worker_data_disk_gb,
            default_storage_data_disk_gb=default_storage_data_disk_gb,
            default_storage_san_disk_gb=default_storage_san_disk_gb,
            available_kubernetes_versions=available_kubernetes_versions,
        )

        k8s_default_configuration.additional_properties = d
        return k8s_default_configuration

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
