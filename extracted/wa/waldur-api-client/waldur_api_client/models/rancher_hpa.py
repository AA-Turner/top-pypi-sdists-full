import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RancherHPA")


@_attrs_define
class RancherHPA:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        runtime_state (str):
        cluster (Union[None, str]):
        cluster_uuid (UUID):
        cluster_name (str):
        project (Union[None, str]):
        project_uuid (UUID):
        project_name (str):
        namespace (Union[None, str]):
        namespace_uuid (UUID):
        namespace_name (str):
        workload_uuid (UUID):
        workload_name (str):
        current_replicas (int):
        desired_replicas (int):
        metrics (Any):
        description (Union[Unset, str]):
        workload (Union[None, Unset, str]):
        min_replicas (Union[Unset, int]):
        max_replicas (Union[Unset, int]):
    """

    url: str
    uuid: UUID
    name: str
    created: datetime.datetime
    modified: datetime.datetime
    runtime_state: str
    cluster: Union[None, str]
    cluster_uuid: UUID
    cluster_name: str
    project: Union[None, str]
    project_uuid: UUID
    project_name: str
    namespace: Union[None, str]
    namespace_uuid: UUID
    namespace_name: str
    workload_uuid: UUID
    workload_name: str
    current_replicas: int
    desired_replicas: int
    metrics: Any
    description: Union[Unset, str] = UNSET
    workload: Union[None, Unset, str] = UNSET
    min_replicas: Union[Unset, int] = UNSET
    max_replicas: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        runtime_state = self.runtime_state

        cluster: Union[None, str]
        cluster = self.cluster

        cluster_uuid = str(self.cluster_uuid)

        cluster_name = self.cluster_name

        project: Union[None, str]
        project = self.project

        project_uuid = str(self.project_uuid)

        project_name = self.project_name

        namespace: Union[None, str]
        namespace = self.namespace

        namespace_uuid = str(self.namespace_uuid)

        namespace_name = self.namespace_name

        workload_uuid = str(self.workload_uuid)

        workload_name = self.workload_name

        current_replicas = self.current_replicas

        desired_replicas = self.desired_replicas

        metrics = self.metrics

        description = self.description

        workload: Union[None, Unset, str]
        if isinstance(self.workload, Unset):
            workload = UNSET
        else:
            workload = self.workload

        min_replicas = self.min_replicas

        max_replicas = self.max_replicas

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "created": created,
                "modified": modified,
                "runtime_state": runtime_state,
                "cluster": cluster,
                "cluster_uuid": cluster_uuid,
                "cluster_name": cluster_name,
                "project": project,
                "project_uuid": project_uuid,
                "project_name": project_name,
                "namespace": namespace,
                "namespace_uuid": namespace_uuid,
                "namespace_name": namespace_name,
                "workload_uuid": workload_uuid,
                "workload_name": workload_name,
                "current_replicas": current_replicas,
                "desired_replicas": desired_replicas,
                "metrics": metrics,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if workload is not UNSET:
            field_dict["workload"] = workload
        if min_replicas is not UNSET:
            field_dict["min_replicas"] = min_replicas
        if max_replicas is not UNSET:
            field_dict["max_replicas"] = max_replicas

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        runtime_state = d.pop("runtime_state")

        def _parse_cluster(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        cluster = _parse_cluster(d.pop("cluster"))

        cluster_uuid = UUID(d.pop("cluster_uuid"))

        cluster_name = d.pop("cluster_name")

        def _parse_project(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        project = _parse_project(d.pop("project"))

        project_uuid = UUID(d.pop("project_uuid"))

        project_name = d.pop("project_name")

        def _parse_namespace(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        namespace = _parse_namespace(d.pop("namespace"))

        namespace_uuid = UUID(d.pop("namespace_uuid"))

        namespace_name = d.pop("namespace_name")

        workload_uuid = UUID(d.pop("workload_uuid"))

        workload_name = d.pop("workload_name")

        current_replicas = d.pop("current_replicas")

        desired_replicas = d.pop("desired_replicas")

        metrics = d.pop("metrics")

        description = d.pop("description", UNSET)

        def _parse_workload(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        workload = _parse_workload(d.pop("workload", UNSET))

        min_replicas = d.pop("min_replicas", UNSET)

        max_replicas = d.pop("max_replicas", UNSET)

        rancher_hpa = cls(
            url=url,
            uuid=uuid,
            name=name,
            created=created,
            modified=modified,
            runtime_state=runtime_state,
            cluster=cluster,
            cluster_uuid=cluster_uuid,
            cluster_name=cluster_name,
            project=project,
            project_uuid=project_uuid,
            project_name=project_name,
            namespace=namespace,
            namespace_uuid=namespace_uuid,
            namespace_name=namespace_name,
            workload_uuid=workload_uuid,
            workload_name=workload_name,
            current_replicas=current_replicas,
            desired_replicas=desired_replicas,
            metrics=metrics,
            description=description,
            workload=workload,
            min_replicas=min_replicas,
            max_replicas=max_replicas,
        )

        rancher_hpa.additional_properties = d
        return rancher_hpa

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
