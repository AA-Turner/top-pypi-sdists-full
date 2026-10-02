from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackVolumeAvailabilityZone")


@_attrs_define
class OpenStackVolumeAvailabilityZone:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        settings (Union[None, Unset, str]):
        available (Union[Unset, bool]):
    """

    url: str
    uuid: UUID
    name: str
    settings: Union[None, Unset, str] = UNSET
    available: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        settings: Union[None, Unset, str]
        if isinstance(self.settings, Unset):
            settings = UNSET
        else:
            settings = self.settings

        available = self.available

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
            }
        )
        if settings is not UNSET:
            field_dict["settings"] = settings
        if available is not UNSET:
            field_dict["available"] = available

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        def _parse_settings(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        settings = _parse_settings(d.pop("settings", UNSET))

        available = d.pop("available", UNSET)

        open_stack_volume_availability_zone = cls(
            url=url,
            uuid=uuid,
            name=name,
            settings=settings,
            available=available,
        )

        open_stack_volume_availability_zone.additional_properties = d
        return open_stack_volume_availability_zone

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
