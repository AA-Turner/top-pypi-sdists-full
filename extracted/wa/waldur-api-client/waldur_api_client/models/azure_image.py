from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AzureImage")


@_attrs_define
class AzureImage:
    """
    Attributes:
        url (str):
        uuid (UUID):
        publisher (str):
        name (str):
        sku (str):
        version (str):
    """

    url: str
    uuid: UUID
    publisher: str
    name: str
    sku: str
    version: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        publisher = self.publisher

        name = self.name

        sku = self.sku

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "publisher": publisher,
                "name": name,
                "sku": sku,
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        publisher = d.pop("publisher")

        name = d.pop("name")

        sku = d.pop("sku")

        version = d.pop("version")

        azure_image = cls(
            url=url,
            uuid=uuid,
            publisher=publisher,
            name=name,
            sku=sku,
            version=version,
        )

        azure_image.additional_properties = d
        return azure_image

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
