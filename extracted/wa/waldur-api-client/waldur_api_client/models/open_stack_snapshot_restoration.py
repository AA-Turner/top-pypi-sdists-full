import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackSnapshotRestoration")


@_attrs_define
class OpenStackSnapshotRestoration:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]): New volume description.
        volume (Union[Unset, str]): Volume that is being restored from the snapshot
        volume_name (Union[Unset, str]):
        volume_state (Union[Unset, str]):
        volume_runtime_state (Union[Unset, str]):
        volume_size (Union[Unset, int]): Size in MiB
        volume_device (Union[Unset, str]): Name of volume as instance device e.g. /dev/vdb.
    """

    uuid: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    description: Union[Unset, str] = UNSET
    volume: Union[Unset, str] = UNSET
    volume_name: Union[Unset, str] = UNSET
    volume_state: Union[Unset, str] = UNSET
    volume_runtime_state: Union[Unset, str] = UNSET
    volume_size: Union[Unset, int] = UNSET
    volume_device: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        description = self.description

        volume = self.volume

        volume_name = self.volume_name

        volume_state = self.volume_state

        volume_runtime_state = self.volume_runtime_state

        volume_size = self.volume_size

        volume_device = self.volume_device

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if created is not UNSET:
            field_dict["created"] = created
        if description is not UNSET:
            field_dict["description"] = description
        if volume is not UNSET:
            field_dict["volume"] = volume
        if volume_name is not UNSET:
            field_dict["volume_name"] = volume_name
        if volume_state is not UNSET:
            field_dict["volume_state"] = volume_state
        if volume_runtime_state is not UNSET:
            field_dict["volume_runtime_state"] = volume_runtime_state
        if volume_size is not UNSET:
            field_dict["volume_size"] = volume_size
        if volume_device is not UNSET:
            field_dict["volume_device"] = volume_device

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        description = d.pop("description", UNSET)

        volume = d.pop("volume", UNSET)

        volume_name = d.pop("volume_name", UNSET)

        volume_state = d.pop("volume_state", UNSET)

        volume_runtime_state = d.pop("volume_runtime_state", UNSET)

        volume_size = d.pop("volume_size", UNSET)

        volume_device = d.pop("volume_device", UNSET)

        open_stack_snapshot_restoration = cls(
            uuid=uuid,
            created=created,
            description=description,
            volume=volume,
            volume_name=volume_name,
            volume_state=volume_state,
            volume_runtime_state=volume_runtime_state,
            volume_size=volume_size,
            volume_device=volume_device,
        )

        open_stack_snapshot_restoration.additional_properties = d
        return open_stack_snapshot_restoration

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
