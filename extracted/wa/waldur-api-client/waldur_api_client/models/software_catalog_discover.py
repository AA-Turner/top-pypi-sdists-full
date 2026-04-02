from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SoftwareCatalogDiscover")


@_attrs_define
class SoftwareCatalogDiscover:
    """
    Attributes:
        name (str):
        catalog_type (str):
        latest_version (str):
        existing (bool):
        existing_version (Union[None, str]):
        update_available (bool):
    """

    name: str
    catalog_type: str
    latest_version: str
    existing: bool
    existing_version: Union[None, str]
    update_available: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        catalog_type = self.catalog_type

        latest_version = self.latest_version

        existing = self.existing

        existing_version: Union[None, str]
        existing_version = self.existing_version

        update_available = self.update_available

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "catalog_type": catalog_type,
                "latest_version": latest_version,
                "existing": existing,
                "existing_version": existing_version,
                "update_available": update_available,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        catalog_type = d.pop("catalog_type")

        latest_version = d.pop("latest_version")

        existing = d.pop("existing")

        def _parse_existing_version(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        existing_version = _parse_existing_version(d.pop("existing_version"))

        update_available = d.pop("update_available")

        software_catalog_discover = cls(
            name=name,
            catalog_type=catalog_type,
            latest_version=latest_version,
            existing=existing,
            existing_version=existing_version,
            update_available=update_available,
        )

        software_catalog_discover.additional_properties = d
        return software_catalog_discover

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
