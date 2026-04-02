import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_parent_software import NestedParentSoftware
    from ..models.nested_software_version import NestedSoftwareVersion


T = TypeVar("T", bound="SoftwarePackage")


@_attrs_define
class SoftwarePackage:
    """
    Attributes:
        url (str):
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        catalog (str):
        name (str):
        parent_softwares (list['NestedParentSoftware']):
        catalog_name (str):
        catalog_version (str):
        catalog_type (str):
        catalog_type_display (str):
        version_count (int):
        extension_count (int):
        versions (list['NestedSoftwareVersion']):
        description (Union[Unset, str]):
        homepage (Union[None, Unset, str]):
        categories (Union[Unset, Any]): Package categories (e.g., ['bio', 'hpc', 'build-tools'])
        licenses (Union[Unset, Any]): Software licenses (e.g., ['GPL-3.0', 'MIT'])
        maintainers (Union[Unset, Any]): Package maintainers
        is_extension (Union[Unset, bool]): Whether this package is an extension of another package
    """

    url: str
    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    catalog: str
    name: str
    parent_softwares: list["NestedParentSoftware"]
    catalog_name: str
    catalog_version: str
    catalog_type: str
    catalog_type_display: str
    version_count: int
    extension_count: int
    versions: list["NestedSoftwareVersion"]
    description: Union[Unset, str] = UNSET
    homepage: Union[None, Unset, str] = UNSET
    categories: Union[Unset, Any] = UNSET
    licenses: Union[Unset, Any] = UNSET
    maintainers: Union[Unset, Any] = UNSET
    is_extension: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        catalog = self.catalog

        name = self.name

        parent_softwares = []
        for parent_softwares_item_data in self.parent_softwares:
            parent_softwares_item = parent_softwares_item_data.to_dict()
            parent_softwares.append(parent_softwares_item)

        catalog_name = self.catalog_name

        catalog_version = self.catalog_version

        catalog_type = self.catalog_type

        catalog_type_display = self.catalog_type_display

        version_count = self.version_count

        extension_count = self.extension_count

        versions = []
        for versions_item_data in self.versions:
            versions_item = versions_item_data.to_dict()
            versions.append(versions_item)

        description = self.description

        homepage: Union[None, Unset, str]
        if isinstance(self.homepage, Unset):
            homepage = UNSET
        else:
            homepage = self.homepage

        categories = self.categories

        licenses = self.licenses

        maintainers = self.maintainers

        is_extension = self.is_extension

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "catalog": catalog,
                "name": name,
                "parent_softwares": parent_softwares,
                "catalog_name": catalog_name,
                "catalog_version": catalog_version,
                "catalog_type": catalog_type,
                "catalog_type_display": catalog_type_display,
                "version_count": version_count,
                "extension_count": extension_count,
                "versions": versions,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if homepage is not UNSET:
            field_dict["homepage"] = homepage
        if categories is not UNSET:
            field_dict["categories"] = categories
        if licenses is not UNSET:
            field_dict["licenses"] = licenses
        if maintainers is not UNSET:
            field_dict["maintainers"] = maintainers
        if is_extension is not UNSET:
            field_dict["is_extension"] = is_extension

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_parent_software import NestedParentSoftware
        from ..models.nested_software_version import NestedSoftwareVersion

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        catalog = d.pop("catalog")

        name = d.pop("name")

        parent_softwares = []
        _parent_softwares = d.pop("parent_softwares")
        for parent_softwares_item_data in _parent_softwares:
            parent_softwares_item = NestedParentSoftware.from_dict(parent_softwares_item_data)

            parent_softwares.append(parent_softwares_item)

        catalog_name = d.pop("catalog_name")

        catalog_version = d.pop("catalog_version")

        catalog_type = d.pop("catalog_type")

        catalog_type_display = d.pop("catalog_type_display")

        version_count = d.pop("version_count")

        extension_count = d.pop("extension_count")

        versions = []
        _versions = d.pop("versions")
        for versions_item_data in _versions:
            versions_item = NestedSoftwareVersion.from_dict(versions_item_data)

            versions.append(versions_item)

        description = d.pop("description", UNSET)

        def _parse_homepage(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        homepage = _parse_homepage(d.pop("homepage", UNSET))

        categories = d.pop("categories", UNSET)

        licenses = d.pop("licenses", UNSET)

        maintainers = d.pop("maintainers", UNSET)

        is_extension = d.pop("is_extension", UNSET)

        software_package = cls(
            url=url,
            uuid=uuid,
            created=created,
            modified=modified,
            catalog=catalog,
            name=name,
            parent_softwares=parent_softwares,
            catalog_name=catalog_name,
            catalog_version=catalog_version,
            catalog_type=catalog_type,
            catalog_type_display=catalog_type_display,
            version_count=version_count,
            extension_count=extension_count,
            versions=versions,
            description=description,
            homepage=homepage,
            categories=categories,
            licenses=licenses,
            maintainers=maintainers,
            is_extension=is_extension,
        )

        software_package.additional_properties = d
        return software_package

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
