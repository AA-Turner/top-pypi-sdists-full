from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v_mware_virtual_machine_create_order_attributes_guest_os_type_1 import (
    VMwareVirtualMachineCreateOrderAttributesGuestOsType1,
)
from ..models.v_mware_virtual_machine_create_order_attributes_guest_os_type_2_type_1 import (
    VMwareVirtualMachineCreateOrderAttributesGuestOsType2Type1,
)
from ..models.v_mware_virtual_machine_create_order_attributes_guest_os_type_3_type_1 import (
    VMwareVirtualMachineCreateOrderAttributesGuestOsType3Type1,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="VMwareVirtualMachineCreateOrderAttributes")


@_attrs_define
class VMwareVirtualMachineCreateOrderAttributes:
    """
    Attributes:
        name (str):
        description (Union[Unset, str]):
        guest_os (Union[None, Unset, VMwareVirtualMachineCreateOrderAttributesGuestOsType1,
            VMwareVirtualMachineCreateOrderAttributesGuestOsType2Type1,
            VMwareVirtualMachineCreateOrderAttributesGuestOsType3Type1]):
        cores_per_socket (Union[Unset, int]): Number of cores per socket in a VM
        template (Union[None, Unset, str]):
        cluster (Union[None, Unset, str]):
        datastore (Union[None, Unset, str]):
    """

    name: str
    description: Union[Unset, str] = UNSET
    guest_os: Union[
        None,
        Unset,
        VMwareVirtualMachineCreateOrderAttributesGuestOsType1,
        VMwareVirtualMachineCreateOrderAttributesGuestOsType2Type1,
        VMwareVirtualMachineCreateOrderAttributesGuestOsType3Type1,
    ] = UNSET
    cores_per_socket: Union[Unset, int] = UNSET
    template: Union[None, Unset, str] = UNSET
    cluster: Union[None, Unset, str] = UNSET
    datastore: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        guest_os: Union[None, Unset, str]
        if isinstance(self.guest_os, Unset):
            guest_os = UNSET
        elif isinstance(self.guest_os, VMwareVirtualMachineCreateOrderAttributesGuestOsType1):
            guest_os = self.guest_os.value
        elif isinstance(self.guest_os, VMwareVirtualMachineCreateOrderAttributesGuestOsType2Type1):
            guest_os = self.guest_os.value
        elif isinstance(self.guest_os, VMwareVirtualMachineCreateOrderAttributesGuestOsType3Type1):
            guest_os = self.guest_os.value
        else:
            guest_os = self.guest_os

        cores_per_socket = self.cores_per_socket

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

        datastore: Union[None, Unset, str]
        if isinstance(self.datastore, Unset):
            datastore = UNSET
        else:
            datastore = self.datastore

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if guest_os is not UNSET:
            field_dict["guest_os"] = guest_os
        if cores_per_socket is not UNSET:
            field_dict["cores_per_socket"] = cores_per_socket
        if template is not UNSET:
            field_dict["template"] = template
        if cluster is not UNSET:
            field_dict["cluster"] = cluster
        if datastore is not UNSET:
            field_dict["datastore"] = datastore

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        def _parse_guest_os(
            data: object,
        ) -> Union[
            None,
            Unset,
            VMwareVirtualMachineCreateOrderAttributesGuestOsType1,
            VMwareVirtualMachineCreateOrderAttributesGuestOsType2Type1,
            VMwareVirtualMachineCreateOrderAttributesGuestOsType3Type1,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                guest_os_type_1 = VMwareVirtualMachineCreateOrderAttributesGuestOsType1(data)

                return guest_os_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                guest_os_type_2_type_1 = VMwareVirtualMachineCreateOrderAttributesGuestOsType2Type1(data)

                return guest_os_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                guest_os_type_3_type_1 = VMwareVirtualMachineCreateOrderAttributesGuestOsType3Type1(data)

                return guest_os_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    Unset,
                    VMwareVirtualMachineCreateOrderAttributesGuestOsType1,
                    VMwareVirtualMachineCreateOrderAttributesGuestOsType2Type1,
                    VMwareVirtualMachineCreateOrderAttributesGuestOsType3Type1,
                ],
                data,
            )

        guest_os = _parse_guest_os(d.pop("guest_os", UNSET))

        cores_per_socket = d.pop("cores_per_socket", UNSET)

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

        def _parse_datastore(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        datastore = _parse_datastore(d.pop("datastore", UNSET))

        v_mware_virtual_machine_create_order_attributes = cls(
            name=name,
            description=description,
            guest_os=guest_os,
            cores_per_socket=cores_per_socket,
            template=template,
            cluster=cluster,
            datastore=datastore,
        )

        v_mware_virtual_machine_create_order_attributes.additional_properties = d
        return v_mware_virtual_machine_create_order_attributes

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
