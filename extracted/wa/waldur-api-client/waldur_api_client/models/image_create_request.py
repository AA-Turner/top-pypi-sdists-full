from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.container_format_enum import ContainerFormatEnum
from ..models.disk_format_enum import DiskFormatEnum
from ..models.visibility_enum import VisibilityEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ImageCreateRequest")


@_attrs_define
class ImageCreateRequest:
    """
    Attributes:
        name (str):
        min_ram (Union[Unset, int]):  Default: 0.
        min_disk (Union[Unset, int]):  Default: 0.
        disk_format (Union[Unset, DiskFormatEnum]):  Default: DiskFormatEnum.QCOW2.
        container_format (Union[Unset, ContainerFormatEnum]):  Default: ContainerFormatEnum.BARE.
        visibility (Union[Unset, VisibilityEnum]):  Default: VisibilityEnum.PRIVATE.
    """

    name: str
    min_ram: Union[Unset, int] = 0
    min_disk: Union[Unset, int] = 0
    disk_format: Union[Unset, DiskFormatEnum] = DiskFormatEnum.QCOW2
    container_format: Union[Unset, ContainerFormatEnum] = ContainerFormatEnum.BARE
    visibility: Union[Unset, VisibilityEnum] = VisibilityEnum.PRIVATE
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        min_ram = self.min_ram

        min_disk = self.min_disk

        disk_format: Union[Unset, str] = UNSET
        if not isinstance(self.disk_format, Unset):
            disk_format = self.disk_format.value

        container_format: Union[Unset, str] = UNSET
        if not isinstance(self.container_format, Unset):
            container_format = self.container_format.value

        visibility: Union[Unset, str] = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if min_ram is not UNSET:
            field_dict["min_ram"] = min_ram
        if min_disk is not UNSET:
            field_dict["min_disk"] = min_disk
        if disk_format is not UNSET:
            field_dict["disk_format"] = disk_format
        if container_format is not UNSET:
            field_dict["container_format"] = container_format
        if visibility is not UNSET:
            field_dict["visibility"] = visibility

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        min_ram = d.pop("min_ram", UNSET)

        min_disk = d.pop("min_disk", UNSET)

        _disk_format = d.pop("disk_format", UNSET)
        disk_format: Union[Unset, DiskFormatEnum]
        if isinstance(_disk_format, Unset):
            disk_format = UNSET
        else:
            disk_format = DiskFormatEnum(_disk_format)

        _container_format = d.pop("container_format", UNSET)
        container_format: Union[Unset, ContainerFormatEnum]
        if isinstance(_container_format, Unset):
            container_format = UNSET
        else:
            container_format = ContainerFormatEnum(_container_format)

        _visibility = d.pop("visibility", UNSET)
        visibility: Union[Unset, VisibilityEnum]
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = VisibilityEnum(_visibility)

        image_create_request = cls(
            name=name,
            min_ram=min_ram,
            min_disk=min_disk,
            disk_format=disk_format,
            container_format=container_format,
            visibility=visibility,
        )

        image_create_request.additional_properties = d
        return image_create_request

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
