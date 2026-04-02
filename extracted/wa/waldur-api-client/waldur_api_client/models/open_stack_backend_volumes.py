from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackBackendVolumes")


@_attrs_define
class OpenStackBackendVolumes:
    """
    Attributes:
        name (str):
        size (int): Size in MiB
        type_ (str):
        state (str):
        availability_zone (str):
        description (Union[Unset, str]):
        metadata (Union[Unset, str]): Arbitrary key-value pairs associated with the volume
        backend_id (Union[None, Unset, str]): Volume ID in the OpenStack backend
        bootable (Union[Unset, bool]): Indicates if this volume can be used to boot an instance
        runtime_state (Union[Unset, str]):
    """

    name: str
    size: int
    type_: str
    state: str
    availability_zone: str
    description: Union[Unset, str] = UNSET
    metadata: Union[Unset, str] = UNSET
    backend_id: Union[None, Unset, str] = UNSET
    bootable: Union[Unset, bool] = UNSET
    runtime_state: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        size = self.size

        type_ = self.type_

        state = self.state

        availability_zone = self.availability_zone

        description = self.description

        metadata = self.metadata

        backend_id: Union[None, Unset, str]
        if isinstance(self.backend_id, Unset):
            backend_id = UNSET
        else:
            backend_id = self.backend_id

        bootable = self.bootable

        runtime_state = self.runtime_state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "size": size,
                "type": type_,
                "state": state,
                "availability_zone": availability_zone,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if bootable is not UNSET:
            field_dict["bootable"] = bootable
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        size = d.pop("size")

        type_ = d.pop("type")

        state = d.pop("state")

        availability_zone = d.pop("availability_zone")

        description = d.pop("description", UNSET)

        metadata = d.pop("metadata", UNSET)

        def _parse_backend_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        backend_id = _parse_backend_id(d.pop("backend_id", UNSET))

        bootable = d.pop("bootable", UNSET)

        runtime_state = d.pop("runtime_state", UNSET)

        open_stack_backend_volumes = cls(
            name=name,
            size=size,
            type_=type_,
            state=state,
            availability_zone=availability_zone,
            description=description,
            metadata=metadata,
            backend_id=backend_id,
            bootable=bootable,
            runtime_state=runtime_state,
        )

        open_stack_backend_volumes.additional_properties = d
        return open_stack_backend_volumes

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
