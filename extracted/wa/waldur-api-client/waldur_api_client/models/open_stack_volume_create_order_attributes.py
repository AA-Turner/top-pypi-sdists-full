from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackVolumeCreateOrderAttributes")


@_attrs_define
class OpenStackVolumeCreateOrderAttributes:
    """
    Attributes:
        name (str):
        description (Union[Unset, str]):
        image (Union[None, Unset, str]): Image that this volume was created from, if any
        size (Union[None, Unset, int]): Size in MiB
        availability_zone (Union[None, Unset, str]): Availability zone where this volume is located
        type_ (Union[None, Unset, str]): Type of the volume (e.g. SSD, HDD)
    """

    name: str
    description: Union[Unset, str] = UNSET
    image: Union[None, Unset, str] = UNSET
    size: Union[None, Unset, int] = UNSET
    availability_zone: Union[None, Unset, str] = UNSET
    type_: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        size: Union[None, Unset, int]
        if isinstance(self.size, Unset):
            size = UNSET
        else:
            size = self.size

        availability_zone: Union[None, Unset, str]
        if isinstance(self.availability_zone, Unset):
            availability_zone = UNSET
        else:
            availability_zone = self.availability_zone

        type_: Union[None, Unset, str]
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if image is not UNSET:
            field_dict["image"] = image
        if size is not UNSET:
            field_dict["size"] = size
        if availability_zone is not UNSET:
            field_dict["availability_zone"] = availability_zone
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        def _parse_size(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        size = _parse_size(d.pop("size", UNSET))

        def _parse_availability_zone(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        availability_zone = _parse_availability_zone(d.pop("availability_zone", UNSET))

        def _parse_type_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        type_ = _parse_type_(d.pop("type", UNSET))

        open_stack_volume_create_order_attributes = cls(
            name=name,
            description=description,
            image=image,
            size=size,
            availability_zone=availability_zone,
            type_=type_,
        )

        open_stack_volume_create_order_attributes.additional_properties = d
        return open_stack_volume_create_order_attributes

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
