from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HpcPartition")


@_attrs_define
class HpcPartition:
    """
    Attributes:
        name (str):
        published (bool): The provider publishes this partition in Waldur.
        live (bool): The cluster reports this partition.
        total_nodes (Union[None, int]):
        idle_nodes (Union[None, int]):
        cpus (Union[None, int]):
        max_time (Union[None, int]): Minutes
        default_time (Union[None, int]): Minutes
        max_nodes (Union[None, int]):
        max_cpus_per_node (Union[None, int]):
        max_mem_per_node (Union[None, int]): MB
        cpu_arch (str):
        gpu_arch (str):
        qos (list[str]):
        default_qos (str):
    """

    name: str
    published: bool
    live: bool
    total_nodes: Union[None, int]
    idle_nodes: Union[None, int]
    cpus: Union[None, int]
    max_time: Union[None, int]
    default_time: Union[None, int]
    max_nodes: Union[None, int]
    max_cpus_per_node: Union[None, int]
    max_mem_per_node: Union[None, int]
    cpu_arch: str
    gpu_arch: str
    qos: list[str]
    default_qos: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        published = self.published

        live = self.live

        total_nodes: Union[None, int]
        total_nodes = self.total_nodes

        idle_nodes: Union[None, int]
        idle_nodes = self.idle_nodes

        cpus: Union[None, int]
        cpus = self.cpus

        max_time: Union[None, int]
        max_time = self.max_time

        default_time: Union[None, int]
        default_time = self.default_time

        max_nodes: Union[None, int]
        max_nodes = self.max_nodes

        max_cpus_per_node: Union[None, int]
        max_cpus_per_node = self.max_cpus_per_node

        max_mem_per_node: Union[None, int]
        max_mem_per_node = self.max_mem_per_node

        cpu_arch = self.cpu_arch

        gpu_arch = self.gpu_arch

        qos = self.qos

        default_qos = self.default_qos

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "published": published,
                "live": live,
                "total_nodes": total_nodes,
                "idle_nodes": idle_nodes,
                "cpus": cpus,
                "max_time": max_time,
                "default_time": default_time,
                "max_nodes": max_nodes,
                "max_cpus_per_node": max_cpus_per_node,
                "max_mem_per_node": max_mem_per_node,
                "cpu_arch": cpu_arch,
                "gpu_arch": gpu_arch,
                "qos": qos,
                "default_qos": default_qos,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        published = d.pop("published")

        live = d.pop("live")

        def _parse_total_nodes(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        total_nodes = _parse_total_nodes(d.pop("total_nodes"))

        def _parse_idle_nodes(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        idle_nodes = _parse_idle_nodes(d.pop("idle_nodes"))

        def _parse_cpus(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        cpus = _parse_cpus(d.pop("cpus"))

        def _parse_max_time(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_time = _parse_max_time(d.pop("max_time"))

        def _parse_default_time(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        default_time = _parse_default_time(d.pop("default_time"))

        def _parse_max_nodes(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_nodes = _parse_max_nodes(d.pop("max_nodes"))

        def _parse_max_cpus_per_node(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_cpus_per_node = _parse_max_cpus_per_node(d.pop("max_cpus_per_node"))

        def _parse_max_mem_per_node(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_mem_per_node = _parse_max_mem_per_node(d.pop("max_mem_per_node"))

        cpu_arch = d.pop("cpu_arch")

        gpu_arch = d.pop("gpu_arch")

        qos = cast(list[str], d.pop("qos"))

        default_qos = d.pop("default_qos")

        hpc_partition = cls(
            name=name,
            published=published,
            live=live,
            total_nodes=total_nodes,
            idle_nodes=idle_nodes,
            cpus=cpus,
            max_time=max_time,
            default_time=default_time,
            max_nodes=max_nodes,
            max_cpus_per_node=max_cpus_per_node,
            max_mem_per_node=max_mem_per_node,
            cpu_arch=cpu_arch,
            gpu_arch=gpu_arch,
            qos=qos,
            default_qos=default_qos,
        )

        hpc_partition.additional_properties = d
        return hpc_partition

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
