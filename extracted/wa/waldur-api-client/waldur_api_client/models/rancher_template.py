import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RancherTemplate")


@_attrs_define
class RancherTemplate:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        default_version (str):
        catalog_name (str):
        versions (list[str]):
        description (Union[Unset, str]):
        runtime_state (Union[Unset, str]):
        catalog (Union[None, Unset, str]):
        cluster (Union[None, Unset, str]):
        project (Union[None, Unset, str]):
        icon (Union[None, Unset, str]):
        project_url (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    name: str
    created: datetime.datetime
    modified: datetime.datetime
    default_version: str
    catalog_name: str
    versions: list[str]
    description: Union[Unset, str] = UNSET
    runtime_state: Union[Unset, str] = UNSET
    catalog: Union[None, Unset, str] = UNSET
    cluster: Union[None, Unset, str] = UNSET
    project: Union[None, Unset, str] = UNSET
    icon: Union[None, Unset, str] = UNSET
    project_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        default_version = self.default_version

        catalog_name = self.catalog_name

        versions = self.versions

        description = self.description

        runtime_state = self.runtime_state

        catalog: Union[None, Unset, str]
        if isinstance(self.catalog, Unset):
            catalog = UNSET
        else:
            catalog = self.catalog

        cluster: Union[None, Unset, str]
        if isinstance(self.cluster, Unset):
            cluster = UNSET
        else:
            cluster = self.cluster

        project: Union[None, Unset, str]
        if isinstance(self.project, Unset):
            project = UNSET
        else:
            project = self.project

        icon: Union[None, Unset, str]
        if isinstance(self.icon, Unset):
            icon = UNSET
        else:
            icon = self.icon

        project_url = self.project_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "created": created,
                "modified": modified,
                "default_version": default_version,
                "catalog_name": catalog_name,
                "versions": versions,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state
        if catalog is not UNSET:
            field_dict["catalog"] = catalog
        if cluster is not UNSET:
            field_dict["cluster"] = cluster
        if project is not UNSET:
            field_dict["project"] = project
        if icon is not UNSET:
            field_dict["icon"] = icon
        if project_url is not UNSET:
            field_dict["project_url"] = project_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        default_version = d.pop("default_version")

        catalog_name = d.pop("catalog_name")

        versions = cast(list[str], d.pop("versions"))

        description = d.pop("description", UNSET)

        runtime_state = d.pop("runtime_state", UNSET)

        def _parse_catalog(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        catalog = _parse_catalog(d.pop("catalog", UNSET))

        def _parse_cluster(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cluster = _parse_cluster(d.pop("cluster", UNSET))

        def _parse_project(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project = _parse_project(d.pop("project", UNSET))

        def _parse_icon(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        icon = _parse_icon(d.pop("icon", UNSET))

        project_url = d.pop("project_url", UNSET)

        rancher_template = cls(
            url=url,
            uuid=uuid,
            name=name,
            created=created,
            modified=modified,
            default_version=default_version,
            catalog_name=catalog_name,
            versions=versions,
            description=description,
            runtime_state=runtime_state,
            catalog=catalog,
            cluster=cluster,
            project=project,
            icon=icon,
            project_url=project_url,
        )

        rancher_template.additional_properties = d
        return rancher_template

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
