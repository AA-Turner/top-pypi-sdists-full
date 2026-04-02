from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackNestedVolume")


@_attrs_define
class OpenStackNestedVolume:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        image_name (Union[Unset, str]): Name of the image this volume was created from
        state (Union[Unset, str]):
        bootable (Union[Unset, bool]): Indicates if this volume can be used to boot an instance
        size (Union[Unset, int]): Size in MiB
        device (Union[Unset, str]): Name of volume as instance device e.g. /dev/vdb.
        resource_type (Union[Unset, str]):
        type_ (Union[None, Unset, str]): Type of the volume (e.g. SSD, HDD)
        type_name (Union[Unset, str]):
        marketplace_resource_uuid (Union[None, Unset, str]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    image_name: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    bootable: Union[Unset, bool] = UNSET
    size: Union[Unset, int] = UNSET
    device: Union[Unset, str] = UNSET
    resource_type: Union[Unset, str] = UNSET
    type_: Union[None, Unset, str] = UNSET
    type_name: Union[Unset, str] = UNSET
    marketplace_resource_uuid: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        image_name = self.image_name

        state = self.state

        bootable = self.bootable

        size = self.size

        device = self.device

        resource_type = self.resource_type

        type_: Union[None, Unset, str]
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

        type_name = self.type_name

        marketplace_resource_uuid: Union[None, Unset, str]
        if isinstance(self.marketplace_resource_uuid, Unset):
            marketplace_resource_uuid = UNSET
        else:
            marketplace_resource_uuid = self.marketplace_resource_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if image_name is not UNSET:
            field_dict["image_name"] = image_name
        if state is not UNSET:
            field_dict["state"] = state
        if bootable is not UNSET:
            field_dict["bootable"] = bootable
        if size is not UNSET:
            field_dict["size"] = size
        if device is not UNSET:
            field_dict["device"] = device
        if resource_type is not UNSET:
            field_dict["resource_type"] = resource_type
        if type_ is not UNSET:
            field_dict["type"] = type_
        if type_name is not UNSET:
            field_dict["type_name"] = type_name
        if marketplace_resource_uuid is not UNSET:
            field_dict["marketplace_resource_uuid"] = marketplace_resource_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        name = d.pop("name", UNSET)

        image_name = d.pop("image_name", UNSET)

        state = d.pop("state", UNSET)

        bootable = d.pop("bootable", UNSET)

        size = d.pop("size", UNSET)

        device = d.pop("device", UNSET)

        resource_type = d.pop("resource_type", UNSET)

        def _parse_type_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        type_ = _parse_type_(d.pop("type", UNSET))

        type_name = d.pop("type_name", UNSET)

        def _parse_marketplace_resource_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        marketplace_resource_uuid = _parse_marketplace_resource_uuid(d.pop("marketplace_resource_uuid", UNSET))

        open_stack_nested_volume = cls(
            url=url,
            uuid=uuid,
            name=name,
            image_name=image_name,
            state=state,
            bootable=bootable,
            size=size,
            device=device,
            resource_type=resource_type,
            type_=type_,
            type_name=type_name,
            marketplace_resource_uuid=marketplace_resource_uuid,
        )

        open_stack_nested_volume.additional_properties = d
        return open_stack_nested_volume

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
