from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackNestedVolumeRequest")


@_attrs_define
class OpenStackNestedVolumeRequest:
    """
    Attributes:
        size (int): Size in MiB
        image_name (Union[Unset, str]): Name of the image this volume was created from
        bootable (Union[Unset, bool]): Indicates if this volume can be used to boot an instance
        device (Union[Unset, str]): Name of volume as instance device e.g. /dev/vdb.
        type_ (Union[None, Unset, str]): Type of the volume (e.g. SSD, HDD)
    """

    size: int
    image_name: Union[Unset, str] = UNSET
    bootable: Union[Unset, bool] = UNSET
    device: Union[Unset, str] = UNSET
    type_: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        size = self.size

        image_name = self.image_name

        bootable = self.bootable

        device = self.device

        type_: Union[None, Unset, str]
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "size": size,
            }
        )
        if image_name is not UNSET:
            field_dict["image_name"] = image_name
        if bootable is not UNSET:
            field_dict["bootable"] = bootable
        if device is not UNSET:
            field_dict["device"] = device
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        size = d.pop("size")

        image_name = d.pop("image_name", UNSET)

        bootable = d.pop("bootable", UNSET)

        device = d.pop("device", UNSET)

        def _parse_type_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        type_ = _parse_type_(d.pop("type", UNSET))

        open_stack_nested_volume_request = cls(
            size=size,
            image_name=image_name,
            bootable=bootable,
            device=device,
            type_=type_,
        )

        open_stack_nested_volume_request.additional_properties = d
        return open_stack_nested_volume_request

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
