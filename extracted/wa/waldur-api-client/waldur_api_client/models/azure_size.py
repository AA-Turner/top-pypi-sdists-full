from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AzureSize")


@_attrs_define
class AzureSize:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        max_data_disk_count (int):
        memory_in_mb (int):
        number_of_cores (int):
        os_disk_size_in_mb (int):
        resource_disk_size_in_mb (int):
    """

    url: str
    uuid: UUID
    name: str
    max_data_disk_count: int
    memory_in_mb: int
    number_of_cores: int
    os_disk_size_in_mb: int
    resource_disk_size_in_mb: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        max_data_disk_count = self.max_data_disk_count

        memory_in_mb = self.memory_in_mb

        number_of_cores = self.number_of_cores

        os_disk_size_in_mb = self.os_disk_size_in_mb

        resource_disk_size_in_mb = self.resource_disk_size_in_mb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "max_data_disk_count": max_data_disk_count,
                "memory_in_mb": memory_in_mb,
                "number_of_cores": number_of_cores,
                "os_disk_size_in_mb": os_disk_size_in_mb,
                "resource_disk_size_in_mb": resource_disk_size_in_mb,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        max_data_disk_count = d.pop("max_data_disk_count")

        memory_in_mb = d.pop("memory_in_mb")

        number_of_cores = d.pop("number_of_cores")

        os_disk_size_in_mb = d.pop("os_disk_size_in_mb")

        resource_disk_size_in_mb = d.pop("resource_disk_size_in_mb")

        azure_size = cls(
            url=url,
            uuid=uuid,
            name=name,
            max_data_disk_count=max_data_disk_count,
            memory_in_mb=memory_in_mb,
            number_of_cores=number_of_cores,
            os_disk_size_in_mb=os_disk_size_in_mb,
            resource_disk_size_in_mb=resource_disk_size_in_mb,
        )

        azure_size.additional_properties = d
        return azure_size

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
