import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RancherWorkload")


@_attrs_define
class RancherWorkload:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        cluster_uuid (UUID):
        cluster_name (str):
        project_uuid (UUID):
        project_name (str):
        namespace_uuid (UUID):
        namespace_name (str):
        scale (int):
        runtime_state (Union[Unset, str]):
        cluster (Union[None, Unset, str]):
        project (Union[None, Unset, str]):
        namespace (Union[None, Unset, str]):
    """

    url: str
    uuid: UUID
    name: str
    created: datetime.datetime
    modified: datetime.datetime
    cluster_uuid: UUID
    cluster_name: str
    project_uuid: UUID
    project_name: str
    namespace_uuid: UUID
    namespace_name: str
    scale: int
    runtime_state: Union[Unset, str] = UNSET
    cluster: Union[None, Unset, str] = UNSET
    project: Union[None, Unset, str] = UNSET
    namespace: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        cluster_uuid = str(self.cluster_uuid)

        cluster_name = self.cluster_name

        project_uuid = str(self.project_uuid)

        project_name = self.project_name

        namespace_uuid = str(self.namespace_uuid)

        namespace_name = self.namespace_name

        scale = self.scale

        runtime_state = self.runtime_state

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

        namespace: Union[None, Unset, str]
        if isinstance(self.namespace, Unset):
            namespace = UNSET
        else:
            namespace = self.namespace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "created": created,
                "modified": modified,
                "cluster_uuid": cluster_uuid,
                "cluster_name": cluster_name,
                "project_uuid": project_uuid,
                "project_name": project_name,
                "namespace_uuid": namespace_uuid,
                "namespace_name": namespace_name,
                "scale": scale,
            }
        )
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state
        if cluster is not UNSET:
            field_dict["cluster"] = cluster
        if project is not UNSET:
            field_dict["project"] = project
        if namespace is not UNSET:
            field_dict["namespace"] = namespace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        cluster_uuid = UUID(d.pop("cluster_uuid"))

        cluster_name = d.pop("cluster_name")

        project_uuid = UUID(d.pop("project_uuid"))

        project_name = d.pop("project_name")

        namespace_uuid = UUID(d.pop("namespace_uuid"))

        namespace_name = d.pop("namespace_name")

        scale = d.pop("scale")

        runtime_state = d.pop("runtime_state", UNSET)

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

        def _parse_namespace(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        namespace = _parse_namespace(d.pop("namespace", UNSET))

        rancher_workload = cls(
            url=url,
            uuid=uuid,
            name=name,
            created=created,
            modified=modified,
            cluster_uuid=cluster_uuid,
            cluster_name=cluster_name,
            project_uuid=project_uuid,
            project_name=project_name,
            namespace_uuid=namespace_uuid,
            namespace_name=namespace_name,
            scale=scale,
            runtime_state=runtime_state,
            cluster=cluster,
            project=project,
            namespace=namespace,
        )

        rancher_workload.additional_properties = d
        return rancher_workload

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
