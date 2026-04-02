from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackFlavor")


@_attrs_define
class OpenStackFlavor:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        settings (Union[Unset, str]):
        cores (Union[Unset, int]): Number of cores in a VM
        ram (Union[Unset, int]): Memory size in MiB
        disk (Union[Unset, int]): Root disk size in MiB
        backend_id (Union[Unset, str]):
        display_name (Union[Unset, str]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    settings: Union[Unset, str] = UNSET
    cores: Union[Unset, int] = UNSET
    ram: Union[Unset, int] = UNSET
    disk: Union[Unset, int] = UNSET
    backend_id: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        settings = self.settings

        cores = self.cores

        ram = self.ram

        disk = self.disk

        backend_id = self.backend_id

        display_name = self.display_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if settings is not UNSET:
            field_dict["settings"] = settings
        if cores is not UNSET:
            field_dict["cores"] = cores
        if ram is not UNSET:
            field_dict["ram"] = ram
        if disk is not UNSET:
            field_dict["disk"] = disk
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if display_name is not UNSET:
            field_dict["display_name"] = display_name

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

        settings = d.pop("settings", UNSET)

        cores = d.pop("cores", UNSET)

        ram = d.pop("ram", UNSET)

        disk = d.pop("disk", UNSET)

        backend_id = d.pop("backend_id", UNSET)

        display_name = d.pop("display_name", UNSET)

        open_stack_flavor = cls(
            url=url,
            uuid=uuid,
            name=name,
            settings=settings,
            cores=cores,
            ram=ram,
            disk=disk,
            backend_id=backend_id,
            display_name=display_name,
        )

        open_stack_flavor.additional_properties = d
        return open_stack_flavor

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
