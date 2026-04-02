from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedSoftwareTargetRequest")


@_attrs_define
class NestedSoftwareTargetRequest:
    """
    Attributes:
        target_type (Union[Unset, str]): Type of target (architecture, platform, variant, etc.)
        target_name (Union[Unset, str]): Target identifier (x86_64/generic, linux, variant_name, etc.)
        target_subtype (Union[Unset, str]): Target subtype (microarchitecture, distribution, etc.)
        location (Union[Unset, str]): Target location (CVMFS path, download URL, etc.)
        metadata (Union[Unset, Any]): Target-specific metadata (build options, system requirements, etc.)
        gpu_architectures (Union[Unset, Any]): List of GPU architectures this target supports (e.g., ['nvidia/cc70',
            'nvidia/cc90'])
    """

    target_type: Union[Unset, str] = UNSET
    target_name: Union[Unset, str] = UNSET
    target_subtype: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    metadata: Union[Unset, Any] = UNSET
    gpu_architectures: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target_type = self.target_type

        target_name = self.target_name

        target_subtype = self.target_subtype

        location = self.location

        metadata = self.metadata

        gpu_architectures = self.gpu_architectures

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if target_type is not UNSET:
            field_dict["target_type"] = target_type
        if target_name is not UNSET:
            field_dict["target_name"] = target_name
        if target_subtype is not UNSET:
            field_dict["target_subtype"] = target_subtype
        if location is not UNSET:
            field_dict["location"] = location
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if gpu_architectures is not UNSET:
            field_dict["gpu_architectures"] = gpu_architectures

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target_type = d.pop("target_type", UNSET)

        target_name = d.pop("target_name", UNSET)

        target_subtype = d.pop("target_subtype", UNSET)

        location = d.pop("location", UNSET)

        metadata = d.pop("metadata", UNSET)

        gpu_architectures = d.pop("gpu_architectures", UNSET)

        nested_software_target_request = cls(
            target_type=target_type,
            target_name=target_name,
            target_subtype=target_subtype,
            location=location,
            metadata=metadata,
            gpu_architectures=gpu_architectures,
        )

        nested_software_target_request.additional_properties = d
        return nested_software_target_request

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
