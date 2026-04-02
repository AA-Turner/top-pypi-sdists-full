import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.rancher_node_role_enum import RancherNodeRoleEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="RancherNestedNode")


@_attrs_define
class RancherNestedNode:
    """
    Attributes:
        url (Union[Unset, str]):
        role (Union[Unset, RancherNodeRoleEnum]):
        instance (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        uuid (Union[Unset, UUID]):
        error_message (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
        backend_id (Union[Unset, str]):
        initial_data (Union[Unset, Any]): Initial data for instance creating.
        runtime_state (Union[Unset, str]):
        k8s_version (Union[Unset, str]):
        docker_version (Union[Unset, str]):
        cpu_allocated (Union[None, Unset, float]):
        cpu_total (Union[None, Unset, int]):
        ram_allocated (Union[None, Unset, int]): Allocated RAM in Mi.
        ram_total (Union[None, Unset, int]): Total RAM in Mi.
        pods_allocated (Union[None, Unset, int]):
        pods_total (Union[None, Unset, int]):
        labels (Union[Unset, Any]):
        annotations (Union[Unset, Any]):
    """

    url: Union[Unset, str] = UNSET
    role: Union[Unset, RancherNodeRoleEnum] = UNSET
    instance: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    error_message: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    backend_id: Union[Unset, str] = UNSET
    initial_data: Union[Unset, Any] = UNSET
    runtime_state: Union[Unset, str] = UNSET
    k8s_version: Union[Unset, str] = UNSET
    docker_version: Union[Unset, str] = UNSET
    cpu_allocated: Union[None, Unset, float] = UNSET
    cpu_total: Union[None, Unset, int] = UNSET
    ram_allocated: Union[None, Unset, int] = UNSET
    ram_total: Union[None, Unset, int] = UNSET
    pods_allocated: Union[None, Unset, int] = UNSET
    pods_total: Union[None, Unset, int] = UNSET
    labels: Union[Unset, Any] = UNSET
    annotations: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        instance = self.instance

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        error_message = self.error_message

        error_traceback = self.error_traceback

        backend_id = self.backend_id

        initial_data = self.initial_data

        runtime_state = self.runtime_state

        k8s_version = self.k8s_version

        docker_version = self.docker_version

        cpu_allocated: Union[None, Unset, float]
        if isinstance(self.cpu_allocated, Unset):
            cpu_allocated = UNSET
        else:
            cpu_allocated = self.cpu_allocated

        cpu_total: Union[None, Unset, int]
        if isinstance(self.cpu_total, Unset):
            cpu_total = UNSET
        else:
            cpu_total = self.cpu_total

        ram_allocated: Union[None, Unset, int]
        if isinstance(self.ram_allocated, Unset):
            ram_allocated = UNSET
        else:
            ram_allocated = self.ram_allocated

        ram_total: Union[None, Unset, int]
        if isinstance(self.ram_total, Unset):
            ram_total = UNSET
        else:
            ram_total = self.ram_total

        pods_allocated: Union[None, Unset, int]
        if isinstance(self.pods_allocated, Unset):
            pods_allocated = UNSET
        else:
            pods_allocated = self.pods_allocated

        pods_total: Union[None, Unset, int]
        if isinstance(self.pods_total, Unset):
            pods_total = UNSET
        else:
            pods_total = self.pods_total

        labels = self.labels

        annotations = self.annotations

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if role is not UNSET:
            field_dict["role"] = role
        if instance is not UNSET:
            field_dict["instance"] = instance
        if created is not UNSET:
            field_dict["created"] = created
        if modified is not UNSET:
            field_dict["modified"] = modified
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if initial_data is not UNSET:
            field_dict["initial_data"] = initial_data
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state
        if k8s_version is not UNSET:
            field_dict["k8s_version"] = k8s_version
        if docker_version is not UNSET:
            field_dict["docker_version"] = docker_version
        if cpu_allocated is not UNSET:
            field_dict["cpu_allocated"] = cpu_allocated
        if cpu_total is not UNSET:
            field_dict["cpu_total"] = cpu_total
        if ram_allocated is not UNSET:
            field_dict["ram_allocated"] = ram_allocated
        if ram_total is not UNSET:
            field_dict["ram_total"] = ram_total
        if pods_allocated is not UNSET:
            field_dict["pods_allocated"] = pods_allocated
        if pods_total is not UNSET:
            field_dict["pods_total"] = pods_total
        if labels is not UNSET:
            field_dict["labels"] = labels
        if annotations is not UNSET:
            field_dict["annotations"] = annotations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _role = d.pop("role", UNSET)
        role: Union[Unset, RancherNodeRoleEnum]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = RancherNodeRoleEnum(_role)

        instance = d.pop("instance", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        error_message = d.pop("error_message", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        backend_id = d.pop("backend_id", UNSET)

        initial_data = d.pop("initial_data", UNSET)

        runtime_state = d.pop("runtime_state", UNSET)

        k8s_version = d.pop("k8s_version", UNSET)

        docker_version = d.pop("docker_version", UNSET)

        def _parse_cpu_allocated(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        cpu_allocated = _parse_cpu_allocated(d.pop("cpu_allocated", UNSET))

        def _parse_cpu_total(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        cpu_total = _parse_cpu_total(d.pop("cpu_total", UNSET))

        def _parse_ram_allocated(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        ram_allocated = _parse_ram_allocated(d.pop("ram_allocated", UNSET))

        def _parse_ram_total(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        ram_total = _parse_ram_total(d.pop("ram_total", UNSET))

        def _parse_pods_allocated(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        pods_allocated = _parse_pods_allocated(d.pop("pods_allocated", UNSET))

        def _parse_pods_total(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        pods_total = _parse_pods_total(d.pop("pods_total", UNSET))

        labels = d.pop("labels", UNSET)

        annotations = d.pop("annotations", UNSET)

        rancher_nested_node = cls(
            url=url,
            role=role,
            instance=instance,
            created=created,
            modified=modified,
            uuid=uuid,
            error_message=error_message,
            error_traceback=error_traceback,
            backend_id=backend_id,
            initial_data=initial_data,
            runtime_state=runtime_state,
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
        )

        rancher_nested_node.additional_properties = d
        return rancher_nested_node

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
