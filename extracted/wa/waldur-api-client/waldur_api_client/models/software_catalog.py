import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.catalog_type_enum import CatalogTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="SoftwareCatalog")


@_attrs_define
class SoftwareCatalog:
    """
    Attributes:
        url (str):
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        name (str): Catalog name (e.g., EESSI, Spack)
        version (str): Catalog version (e.g., 2023.06, 0.21.0)
        catalog_type_display (str):
        last_update_attempt (Union[None, datetime.datetime]):
        last_successful_update (Union[None, datetime.datetime]):
        package_count (int):
        version_count (int):
        target_count (int):
        catalog_type (Union[Unset, CatalogTypeEnum]):  Default: CatalogTypeEnum.BINARY_RUNTIME.
        source_url (Union[Unset, str]): Catalog source URL
        description (Union[Unset, str]):
        metadata (Union[Unset, Any]): Catalog-specific metadata (architecture maps, API endpoints, etc.)
        auto_update_enabled (Union[Unset, bool]): Whether to automatically update this catalog via scheduled tasks
        update_errors (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    name: str
    version: str
    catalog_type_display: str
    last_update_attempt: Union[None, datetime.datetime]
    last_successful_update: Union[None, datetime.datetime]
    package_count: int
    version_count: int
    target_count: int
    catalog_type: Union[Unset, CatalogTypeEnum] = CatalogTypeEnum.BINARY_RUNTIME
    source_url: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    metadata: Union[Unset, Any] = UNSET
    auto_update_enabled: Union[Unset, bool] = UNSET
    update_errors: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        name = self.name

        version = self.version

        catalog_type_display = self.catalog_type_display

        last_update_attempt: Union[None, str]
        if isinstance(self.last_update_attempt, datetime.datetime):
            last_update_attempt = self.last_update_attempt.isoformat()
        else:
            last_update_attempt = self.last_update_attempt

        last_successful_update: Union[None, str]
        if isinstance(self.last_successful_update, datetime.datetime):
            last_successful_update = self.last_successful_update.isoformat()
        else:
            last_successful_update = self.last_successful_update

        package_count = self.package_count

        version_count = self.version_count

        target_count = self.target_count

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
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "name": name,
                "version": version,
                "catalog_type_display": catalog_type_display,
                "last_update_attempt": last_update_attempt,
                "last_successful_update": last_successful_update,
                "package_count": package_count,
                "version_count": version_count,
                "target_count": target_count,
            }
        )
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
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        name = d.pop("name")

        version = d.pop("version")

        catalog_type_display = d.pop("catalog_type_display")

        def _parse_last_update_attempt(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_update_attempt_type_0 = isoparse(data)

                return last_update_attempt_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_update_attempt = _parse_last_update_attempt(d.pop("last_update_attempt"))

        def _parse_last_successful_update(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_successful_update_type_0 = isoparse(data)

                return last_successful_update_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_successful_update = _parse_last_successful_update(d.pop("last_successful_update"))

        package_count = d.pop("package_count")

        version_count = d.pop("version_count")

        target_count = d.pop("target_count")

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

        software_catalog = cls(
            url=url,
            uuid=uuid,
            created=created,
            modified=modified,
            name=name,
            version=version,
            catalog_type_display=catalog_type_display,
            last_update_attempt=last_update_attempt,
            last_successful_update=last_successful_update,
            package_count=package_count,
            version_count=version_count,
            target_count=target_count,
            catalog_type=catalog_type,
            source_url=source_url,
            description=description,
            metadata=metadata,
            auto_update_enabled=auto_update_enabled,
            update_errors=update_errors,
        )

        software_catalog.additional_properties = d
        return software_catalog

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
