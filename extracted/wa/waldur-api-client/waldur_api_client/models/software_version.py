import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.software_version_module import SoftwareVersionModule
    from ..models.software_version_toolchain import SoftwareVersionToolchain


T = TypeVar("T", bound="SoftwareVersion")


@_attrs_define
class SoftwareVersion:
    """
    Attributes:
        url (str):
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        version (str):
        release_date (Union[None, datetime.date]):
        dependencies (Any): Package dependencies (format varies by catalog type)
        metadata (Any): Version-specific metadata (toolchains, build info, modules, etc.)
        package_name (str):
        catalog_type (str):
        target_count (int):
        module (SoftwareVersionModule):
        required_modules (list[Any]):
        extensions (list[Any]):
        toolchain (SoftwareVersionToolchain):
        toolchain_families_compatibility (list[Any]):
    """

    url: str
    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    version: str
    release_date: Union[None, datetime.date]
    dependencies: Any
    metadata: Any
    package_name: str
    catalog_type: str
    target_count: int
    module: "SoftwareVersionModule"
    required_modules: list[Any]
    extensions: list[Any]
    toolchain: "SoftwareVersionToolchain"
    toolchain_families_compatibility: list[Any]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        version = self.version

        release_date: Union[None, str]
        if isinstance(self.release_date, datetime.date):
            release_date = self.release_date.isoformat()
        else:
            release_date = self.release_date

        dependencies = self.dependencies

        metadata = self.metadata

        package_name = self.package_name

        catalog_type = self.catalog_type

        target_count = self.target_count

        module = self.module.to_dict()

        required_modules = self.required_modules

        extensions = self.extensions

        toolchain = self.toolchain.to_dict()

        toolchain_families_compatibility = self.toolchain_families_compatibility

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "version": version,
                "release_date": release_date,
                "dependencies": dependencies,
                "metadata": metadata,
                "package_name": package_name,
                "catalog_type": catalog_type,
                "target_count": target_count,
                "module": module,
                "required_modules": required_modules,
                "extensions": extensions,
                "toolchain": toolchain,
                "toolchain_families_compatibility": toolchain_families_compatibility,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.software_version_module import SoftwareVersionModule
        from ..models.software_version_toolchain import SoftwareVersionToolchain

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        version = d.pop("version")

        def _parse_release_date(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                release_date_type_0 = isoparse(data).date()

                return release_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        release_date = _parse_release_date(d.pop("release_date"))

        dependencies = d.pop("dependencies")

        metadata = d.pop("metadata")

        package_name = d.pop("package_name")

        catalog_type = d.pop("catalog_type")

        target_count = d.pop("target_count")

        module = SoftwareVersionModule.from_dict(d.pop("module"))

        required_modules = cast(list[Any], d.pop("required_modules"))

        extensions = cast(list[Any], d.pop("extensions"))

        toolchain = SoftwareVersionToolchain.from_dict(d.pop("toolchain"))

        toolchain_families_compatibility = cast(list[Any], d.pop("toolchain_families_compatibility"))

        software_version = cls(
            url=url,
            uuid=uuid,
            created=created,
            modified=modified,
            version=version,
            release_date=release_date,
            dependencies=dependencies,
            metadata=metadata,
            package_name=package_name,
            catalog_type=catalog_type,
            target_count=target_count,
            module=module,
            required_modules=required_modules,
            extensions=extensions,
            toolchain=toolchain,
            toolchain_families_compatibility=toolchain_families_compatibility,
        )

        software_version.additional_properties = d
        return software_version

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
