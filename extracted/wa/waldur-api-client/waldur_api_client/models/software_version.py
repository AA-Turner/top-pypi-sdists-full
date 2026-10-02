import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.software_module import SoftwareModule
    from ..models.software_toolchain import SoftwareToolchain
    from ..models.software_version_dependencies import SoftwareVersionDependencies
    from ..models.software_version_metadata import SoftwareVersionMetadata


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
        module_version (str): EESSI EasyBuild module version
        release_date (Union[None, datetime.date]):
        dependencies (SoftwareVersionDependencies): Package dependencies (format varies by catalog type)
        metadata (SoftwareVersionMetadata): Version-specific metadata (toolchains, build info, modules, etc.)
        package_name (str):
        catalog_type (str):
        target_count (int):
        module (Union['SoftwareModule', None]):
        required_modules (list[Any]):
        extensions (list[Any]):
        toolchain (Union['SoftwareToolchain', None]):
        toolchain_families_compatibility (list[Any]):
    """

    url: str
    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    version: str
    module_version: str
    release_date: Union[None, datetime.date]
    dependencies: "SoftwareVersionDependencies"
    metadata: "SoftwareVersionMetadata"
    package_name: str
    catalog_type: str
    target_count: int
    module: Union["SoftwareModule", None]
    required_modules: list[Any]
    extensions: list[Any]
    toolchain: Union["SoftwareToolchain", None]
    toolchain_families_compatibility: list[Any]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.software_module import SoftwareModule
        from ..models.software_toolchain import SoftwareToolchain

        url = self.url

        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        version = self.version

        module_version = self.module_version

        release_date: Union[None, str]
        if isinstance(self.release_date, datetime.date):
            release_date = self.release_date.isoformat()
        else:
            release_date = self.release_date

        dependencies = self.dependencies.to_dict()

        metadata = self.metadata.to_dict()

        package_name = self.package_name

        catalog_type = self.catalog_type

        target_count = self.target_count

        module: Union[None, dict[str, Any]]
        if isinstance(self.module, SoftwareModule):
            module = self.module.to_dict()
        else:
            module = self.module

        required_modules = self.required_modules

        extensions = self.extensions

        toolchain: Union[None, dict[str, Any]]
        if isinstance(self.toolchain, SoftwareToolchain):
            toolchain = self.toolchain.to_dict()
        else:
            toolchain = self.toolchain

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
                "module_version": module_version,
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
        from ..models.software_module import SoftwareModule
        from ..models.software_toolchain import SoftwareToolchain
        from ..models.software_version_dependencies import SoftwareVersionDependencies
        from ..models.software_version_metadata import SoftwareVersionMetadata

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        version = d.pop("version")

        module_version = d.pop("module_version")

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

        dependencies = SoftwareVersionDependencies.from_dict(d.pop("dependencies"))

        metadata = SoftwareVersionMetadata.from_dict(d.pop("metadata"))

        package_name = d.pop("package_name")

        catalog_type = d.pop("catalog_type")

        target_count = d.pop("target_count")

        def _parse_module(data: object) -> Union["SoftwareModule", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                module_type_1 = SoftwareModule.from_dict(data)

                return module_type_1
            except:  # noqa: E722
                pass
            return cast(Union["SoftwareModule", None], data)

        module = _parse_module(d.pop("module"))

        required_modules = cast(list[Any], d.pop("required_modules"))

        extensions = cast(list[Any], d.pop("extensions"))

        def _parse_toolchain(data: object) -> Union["SoftwareToolchain", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                toolchain_type_1 = SoftwareToolchain.from_dict(data)

                return toolchain_type_1
            except:  # noqa: E722
                pass
            return cast(Union["SoftwareToolchain", None], data)

        toolchain = _parse_toolchain(d.pop("toolchain"))

        toolchain_families_compatibility = cast(list[Any], d.pop("toolchain_families_compatibility"))

        software_version = cls(
            url=url,
            uuid=uuid,
            created=created,
            modified=modified,
            version=version,
            module_version=module_version,
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
