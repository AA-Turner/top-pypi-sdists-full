from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.catalog_type_enum import CatalogTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedSoftwareCatalogRequest")


@_attrs_define
class PatchedSoftwareCatalogRequest:
    """
    Attributes:
        name (Union[Unset, str]): Catalog name (e.g., EESSI, Spack)
        version (Union[Unset, str]): Catalog version (e.g., 2023.06, 0.21.0)
        catalog_type (Union[Unset, CatalogTypeEnum]):  Default: CatalogTypeEnum.BINARY_RUNTIME.
        source_url (Union[Unset, str]): Catalog source URL
        description (Union[Unset, str]):
        metadata (Union[Unset, Any]): Catalog-specific metadata (architecture maps, API endpoints, etc.)
        auto_update_enabled (Union[Unset, bool]): Whether to automatically update this catalog via scheduled tasks
        update_errors (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    catalog_type: Union[Unset, CatalogTypeEnum] = CatalogTypeEnum.BINARY_RUNTIME
    source_url: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    metadata: Union[Unset, Any] = UNSET
    auto_update_enabled: Union[Unset, bool] = UNSET
    update_errors: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        version = self.version

        catalog_type: Union[Unset, str] = UNSET
        if not isinstance(self.catalog_type, Unset):
            catalog_type = self.catalog_type.value

        source_url = self.source_url

        description = self.description

        metadata = self.metadata

        auto_update_enabled = self.auto_update_enabled

        update_errors = self.update_errors

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if version is not UNSET:
            field_dict["version"] = version
        if catalog_type is not UNSET:
            field_dict["catalog_type"] = catalog_type
        if source_url is not UNSET:
            field_dict["source_url"] = source_url
        if description is not UNSET:
            field_dict["description"] = description
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if auto_update_enabled is not UNSET:
            field_dict["auto_update_enabled"] = auto_update_enabled
        if update_errors is not UNSET:
            field_dict["update_errors"] = update_errors

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        version = d.pop("version", UNSET)

        _catalog_type = d.pop("catalog_type", UNSET)
        catalog_type: Union[Unset, CatalogTypeEnum]
        if isinstance(_catalog_type, Unset):
            catalog_type = UNSET
        else:
            catalog_type = CatalogTypeEnum(_catalog_type)

        source_url = d.pop("source_url", UNSET)

        description = d.pop("description", UNSET)

        metadata = d.pop("metadata", UNSET)

        auto_update_enabled = d.pop("auto_update_enabled", UNSET)

        update_errors = d.pop("update_errors", UNSET)

        patched_software_catalog_request = cls(
            name=name,
            version=version,
            catalog_type=catalog_type,
            source_url=source_url,
            description=description,
            metadata=metadata,
            auto_update_enabled=auto_update_enabled,
            update_errors=update_errors,
        )

        patched_software_catalog_request.additional_properties = d
        return patched_software_catalog_request

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
