import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.core_states import CoreStates
from ..models.rancher_node_role_enum import RancherNodeRoleEnum

T = TypeVar("T", bound="RancherNode")


@_attrs_define
class RancherNode:
    """
    Attributes:
        uuid (UUID):
        url (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        name (str):
        backend_id (str):
        project_uuid (UUID):
        service_settings_name (str):
        service_settings_uuid (UUID):
        resource_type (str):
        state (CoreStates):
        cluster (str):
        cluster_name (str):
        cluster_uuid (UUID):
        instance (str):
        instance_name (str):
        instance_uuid (UUID):
        instance_marketplace_uuid (UUID):
        role (RancherNodeRoleEnum):
        k8s_version (str):
        docker_version (str):
        cpu_allocated (Union[None, float]):
        cpu_total (Union[None, int]):
        ram_allocated (Union[None, int]): Allocated RAM in Mi.
        ram_total (Union[None, int]): Total RAM in Mi.
        pods_allocated (Union[None, int]):
        pods_total (Union[None, int]):
        labels (Any):
        annotations (Any):
        runtime_state (str):
    """

    uuid: UUID
    url: str
    created: datetime.datetime
    modified: datetime.datetime
    name: str
    backend_id: str
    project_uuid: UUID
    service_settings_name: str
    service_settings_uuid: UUID
    resource_type: str
    state: CoreStates
    cluster: str
    cluster_name: str
    cluster_uuid: UUID
    instance: str
    instance_name: str
    instance_uuid: UUID
    instance_marketplace_uuid: UUID
    role: RancherNodeRoleEnum
    k8s_version: str
    docker_version: str
    cpu_allocated: Union[None, float]
    cpu_total: Union[None, int]
    ram_allocated: Union[None, int]
    ram_total: Union[None, int]
    pods_allocated: Union[None, int]
    pods_total: Union[None, int]
    labels: Any
    annotations: Any
    runtime_state: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        name = self.name

        backend_id = self.backend_id

        project_uuid = str(self.project_uuid)

        service_settings_name = self.service_settings_name

        service_settings_uuid = str(self.service_settings_uuid)

        resource_type = self.resource_type

        state = self.state.value

        cluster = self.cluster

        cluster_name = self.cluster_name

        cluster_uuid = str(self.cluster_uuid)

        instance = self.instance

        instance_name = self.instance_name

        instance_uuid = str(self.instance_uuid)

        instance_marketplace_uuid = str(self.instance_marketplace_uuid)

        role = self.role.value

        k8s_version = self.k8s_version

        docker_version = self.docker_version

        cpu_allocated: Union[None, float]
        cpu_allocated = self.cpu_allocated

        cpu_total: Union[None, int]
        cpu_total = self.cpu_total

        ram_allocated: Union[None, int]
        ram_allocated = self.ram_allocated

        ram_total: Union[None, int]
        ram_total = self.ram_total

        pods_allocated: Union[None, int]
        pods_allocated = self.pods_allocated

        pods_total: Union[None, int]
        pods_total = self.pods_total

        labels = self.labels

        annotations = self.annotations

        runtime_state = self.runtime_state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "created": created,
                "modified": modified,
                "name": name,
                "backend_id": backend_id,
                "project_uuid": project_uuid,
                "service_settings_name": service_settings_name,
                "service_settings_uuid": service_settings_uuid,
                "resource_type": resource_type,
                "state": state,
                "cluster": cluster,
                "cluster_name": cluster_name,
                "cluster_uuid": cluster_uuid,
                "instance": instance,
                "instance_name": instance_name,
                "instance_uuid": instance_uuid,
                "instance_marketplace_uuid": instance_marketplace_uuid,
                "role": role,
                "k8s_version": k8s_version,
                "docker_version": docker_version,
                "cpu_allocated": cpu_allocated,
                "cpu_total": cpu_total,
                "ram_allocated": ram_allocated,
                "ram_total": ram_total,
                "pods_allocated": pods_allocated,
                "pods_total": pods_total,
                "labels": labels,
                "annotations": annotations,
                "runtime_state": runtime_state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        name = d.pop("name")

        backend_id = d.pop("backend_id")

        project_uuid = UUID(d.pop("project_uuid"))

        service_settings_name = d.pop("service_settings_name")

        service_settings_uuid = UUID(d.pop("service_settings_uuid"))

        resource_type = d.pop("resource_type")

        state = CoreStates(d.pop("state"))

        cluster = d.pop("cluster")

        cluster_name = d.pop("cluster_name")

        cluster_uuid = UUID(d.pop("cluster_uuid"))

        instance = d.pop("instance")

        instance_name = d.pop("instance_name")

        instance_uuid = UUID(d.pop("instance_uuid"))

        instance_marketplace_uuid = UUID(d.pop("instance_marketplace_uuid"))

        role = RancherNodeRoleEnum(d.pop("role"))

        k8s_version = d.pop("k8s_version")

        docker_version = d.pop("docker_version")

        def _parse_cpu_allocated(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        cpu_allocated = _parse_cpu_allocated(d.pop("cpu_allocated"))

        def _parse_cpu_total(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        cpu_total = _parse_cpu_total(d.pop("cpu_total"))

        def _parse_ram_allocated(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        ram_allocated = _parse_ram_allocated(d.pop("ram_allocated"))

        def _parse_ram_total(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        ram_total = _parse_ram_total(d.pop("ram_total"))

        def _parse_pods_allocated(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        pods_allocated = _parse_pods_allocated(d.pop("pods_allocated"))

        def _parse_pods_total(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        pods_total = _parse_pods_total(d.pop("pods_total"))

        labels = d.pop("labels")

        annotations = d.pop("annotations")

        runtime_state = d.pop("runtime_state")

        rancher_node = cls(
            uuid=uuid,
            url=url,
            created=created,
            modified=modified,
            name=name,
            backend_id=backend_id,
            project_uuid=project_uuid,
            service_settings_name=service_settings_name,
            service_settings_uuid=service_settings_uuid,
            resource_type=resource_type,
            state=state,
            cluster=cluster,
            cluster_name=cluster_name,
            cluster_uuid=cluster_uuid,
            instance=instance,
            instance_name=instance_name,
            instance_uuid=instance_uuid,
            instance_marketplace_uuid=instance_marketplace_uuid,
            role=role,
            k8s_version=k8s_version,
            docker_version=docker_version,
            cpu_allocated=cpu_allocated,
            cpu_total=cpu_total,
            ram_allocated=ram_allocated,
            ram_total=ram_total,
            pods_allocated=pods_allocated,
            pods_total=pods_total,
            labels=labels,
            annotations=annotations,
            runtime_state=runtime_state,
        )

        rancher_node.additional_properties = d
        return rancher_node

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
