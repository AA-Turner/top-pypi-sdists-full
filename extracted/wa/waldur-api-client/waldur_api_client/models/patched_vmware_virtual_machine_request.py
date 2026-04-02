from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedVmwareVirtualMachineRequest")


@_attrs_define
class PatchedVmwareVirtualMachineRequest:
    """
    Attributes:
        description (Union[Unset, str]):
        cores (Union[Unset, int]): Number of cores in a VM
        cores_per_socket (Union[Unset, int]): Number of cores per socket in a VM
        ram (Union[Unset, int]): Memory size in MiB
    """

    description: Union[Unset, str] = UNSET
    cores: Union[Unset, int] = UNSET
    cores_per_socket: Union[Unset, int] = UNSET
    ram: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        cores = self.cores

        cores_per_socket = self.cores_per_socket

        ram = self.ram

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if cores is not UNSET:
            field_dict["cores"] = cores
        if cores_per_socket is not UNSET:
            field_dict["cores_per_socket"] = cores_per_socket
        if ram is not UNSET:
            field_dict["ram"] = ram

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        cores = d.pop("cores", UNSET)

        cores_per_socket = d.pop("cores_per_socket", UNSET)

        ram = d.pop("ram", UNSET)

        patched_vmware_virtual_machine_request = cls(
            description=description,
            cores=cores,
            cores_per_socket=cores_per_socket,
            ram=ram,
        )

        patched_vmware_virtual_machine_request.additional_properties = d
        return patched_vmware_virtual_machine_request

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
