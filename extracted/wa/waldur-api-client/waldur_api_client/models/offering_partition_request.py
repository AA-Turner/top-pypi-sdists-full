from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingPartitionRequest")


@_attrs_define
class OfferingPartitionRequest:
    """
    Attributes:
        offering (UUID):
        partition_name (str): Name of the SLURM partition
        cpu_arch (Union[Unset, str]): CPU architecture of the partition (e.g., x86_64/amd/zen3)
        gpu_arch (Union[Unset, str]): GPU architecture of the partition (e.g., nvidia/cc90, amd/gfx90a)
        cpu_bind (Union[None, Unset, int]): Default task binding policy (SLURM cpu_bind)
        def_cpu_per_gpu (Union[None, Unset, int]): Default CPUs allocated per GPU
        max_cpus_per_node (Union[None, Unset, int]): Maximum allocated CPUs per node
        max_cpus_per_socket (Union[None, Unset, int]): Maximum allocated CPUs per socket
        def_mem_per_cpu (Union[None, Unset, int]): Default memory per CPU in MB
        def_mem_per_gpu (Union[None, Unset, int]): Default memory per GPU in MB
        def_mem_per_node (Union[None, Unset, int]): Default memory per node in MB
        max_mem_per_cpu (Union[None, Unset, int]): Maximum memory per CPU in MB
        max_mem_per_node (Union[None, Unset, int]): Maximum memory per node in MB
        default_time (Union[None, Unset, int]): Default time limit in minutes
        max_time (Union[None, Unset, int]): Maximum time limit in minutes
        grace_time (Union[None, Unset, int]): Preemption grace time in seconds
        max_nodes (Union[None, Unset, int]): Maximum nodes per job
        min_nodes (Union[None, Unset, int]): Minimum nodes per job
        exclusive_topo (Union[Unset, bool]): Exclusive topology access required
        exclusive_user (Union[Unset, bool]): Exclusive user access required
        priority_tier (Union[None, Unset, int]): Priority tier for scheduling and preemption
        qos (Union[Unset, str]): Quality of Service (QOS) name
        req_resv (Union[Unset, bool]): Require reservation for job allocation
    """

    offering: UUID
    partition_name: str
    cpu_arch: Union[Unset, str] = UNSET
    gpu_arch: Union[Unset, str] = UNSET
    cpu_bind: Union[None, Unset, int] = UNSET
    def_cpu_per_gpu: Union[None, Unset, int] = UNSET
    max_cpus_per_node: Union[None, Unset, int] = UNSET
    max_cpus_per_socket: Union[None, Unset, int] = UNSET
    def_mem_per_cpu: Union[None, Unset, int] = UNSET
    def_mem_per_gpu: Union[None, Unset, int] = UNSET
    def_mem_per_node: Union[None, Unset, int] = UNSET
    max_mem_per_cpu: Union[None, Unset, int] = UNSET
    max_mem_per_node: Union[None, Unset, int] = UNSET
    default_time: Union[None, Unset, int] = UNSET
    max_time: Union[None, Unset, int] = UNSET
    grace_time: Union[None, Unset, int] = UNSET
    max_nodes: Union[None, Unset, int] = UNSET
    min_nodes: Union[None, Unset, int] = UNSET
    exclusive_topo: Union[Unset, bool] = UNSET
    exclusive_user: Union[Unset, bool] = UNSET
    priority_tier: Union[None, Unset, int] = UNSET
    qos: Union[Unset, str] = UNSET
    req_resv: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering = str(self.offering)

        partition_name = self.partition_name

        cpu_arch = self.cpu_arch

        gpu_arch = self.gpu_arch

        cpu_bind: Union[None, Unset, int]
        if isinstance(self.cpu_bind, Unset):
            cpu_bind = UNSET
        else:
            cpu_bind = self.cpu_bind

        def_cpu_per_gpu: Union[None, Unset, int]
        if isinstance(self.def_cpu_per_gpu, Unset):
            def_cpu_per_gpu = UNSET
        else:
            def_cpu_per_gpu = self.def_cpu_per_gpu

        max_cpus_per_node: Union[None, Unset, int]
        if isinstance(self.max_cpus_per_node, Unset):
            max_cpus_per_node = UNSET
        else:
            max_cpus_per_node = self.max_cpus_per_node

        max_cpus_per_socket: Union[None, Unset, int]
        if isinstance(self.max_cpus_per_socket, Unset):
            max_cpus_per_socket = UNSET
        else:
            max_cpus_per_socket = self.max_cpus_per_socket

        def_mem_per_cpu: Union[None, Unset, int]
        if isinstance(self.def_mem_per_cpu, Unset):
            def_mem_per_cpu = UNSET
        else:
            def_mem_per_cpu = self.def_mem_per_cpu

        def_mem_per_gpu: Union[None, Unset, int]
        if isinstance(self.def_mem_per_gpu, Unset):
            def_mem_per_gpu = UNSET
        else:
            def_mem_per_gpu = self.def_mem_per_gpu

        def_mem_per_node: Union[None, Unset, int]
        if isinstance(self.def_mem_per_node, Unset):
            def_mem_per_node = UNSET
        else:
            def_mem_per_node = self.def_mem_per_node

        max_mem_per_cpu: Union[None, Unset, int]
        if isinstance(self.max_mem_per_cpu, Unset):
            max_mem_per_cpu = UNSET
        else:
            max_mem_per_cpu = self.max_mem_per_cpu

        max_mem_per_node: Union[None, Unset, int]
        if isinstance(self.max_mem_per_node, Unset):
            max_mem_per_node = UNSET
        else:
            max_mem_per_node = self.max_mem_per_node

        default_time: Union[None, Unset, int]
        if isinstance(self.default_time, Unset):
            default_time = UNSET
        else:
            default_time = self.default_time

        max_time: Union[None, Unset, int]
        if isinstance(self.max_time, Unset):
            max_time = UNSET
        else:
            max_time = self.max_time

        grace_time: Union[None, Unset, int]
        if isinstance(self.grace_time, Unset):
            grace_time = UNSET
        else:
            grace_time = self.grace_time

        max_nodes: Union[None, Unset, int]
        if isinstance(self.max_nodes, Unset):
            max_nodes = UNSET
        else:
            max_nodes = self.max_nodes

        min_nodes: Union[None, Unset, int]
        if isinstance(self.min_nodes, Unset):
            min_nodes = UNSET
        else:
            min_nodes = self.min_nodes

        exclusive_topo = self.exclusive_topo

        exclusive_user = self.exclusive_user

        priority_tier: Union[None, Unset, int]
        if isinstance(self.priority_tier, Unset):
            priority_tier = UNSET
        else:
            priority_tier = self.priority_tier

        qos = self.qos

        req_resv = self.req_resv

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering": offering,
                "partition_name": partition_name,
            }
        )
        if cpu_arch is not UNSET:
            field_dict["cpu_arch"] = cpu_arch
        if gpu_arch is not UNSET:
            field_dict["gpu_arch"] = gpu_arch
        if cpu_bind is not UNSET:
            field_dict["cpu_bind"] = cpu_bind
        if def_cpu_per_gpu is not UNSET:
            field_dict["def_cpu_per_gpu"] = def_cpu_per_gpu
        if max_cpus_per_node is not UNSET:
            field_dict["max_cpus_per_node"] = max_cpus_per_node
        if max_cpus_per_socket is not UNSET:
            field_dict["max_cpus_per_socket"] = max_cpus_per_socket
        if def_mem_per_cpu is not UNSET:
            field_dict["def_mem_per_cpu"] = def_mem_per_cpu
        if def_mem_per_gpu is not UNSET:
            field_dict["def_mem_per_gpu"] = def_mem_per_gpu
        if def_mem_per_node is not UNSET:
            field_dict["def_mem_per_node"] = def_mem_per_node
        if max_mem_per_cpu is not UNSET:
            field_dict["max_mem_per_cpu"] = max_mem_per_cpu
        if max_mem_per_node is not UNSET:
            field_dict["max_mem_per_node"] = max_mem_per_node
        if default_time is not UNSET:
            field_dict["default_time"] = default_time
        if max_time is not UNSET:
            field_dict["max_time"] = max_time
        if grace_time is not UNSET:
            field_dict["grace_time"] = grace_time
        if max_nodes is not UNSET:
            field_dict["max_nodes"] = max_nodes
        if min_nodes is not UNSET:
            field_dict["min_nodes"] = min_nodes
        if exclusive_topo is not UNSET:
            field_dict["exclusive_topo"] = exclusive_topo
        if exclusive_user is not UNSET:
            field_dict["exclusive_user"] = exclusive_user
        if priority_tier is not UNSET:
            field_dict["priority_tier"] = priority_tier
        if qos is not UNSET:
            field_dict["qos"] = qos
        if req_resv is not UNSET:
            field_dict["req_resv"] = req_resv

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering = UUID(d.pop("offering"))

        partition_name = d.pop("partition_name")

        cpu_arch = d.pop("cpu_arch", UNSET)

        gpu_arch = d.pop("gpu_arch", UNSET)

        def _parse_cpu_bind(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        cpu_bind = _parse_cpu_bind(d.pop("cpu_bind", UNSET))

        def _parse_def_cpu_per_gpu(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        def_cpu_per_gpu = _parse_def_cpu_per_gpu(d.pop("def_cpu_per_gpu", UNSET))

        def _parse_max_cpus_per_node(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_cpus_per_node = _parse_max_cpus_per_node(d.pop("max_cpus_per_node", UNSET))

        def _parse_max_cpus_per_socket(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_cpus_per_socket = _parse_max_cpus_per_socket(d.pop("max_cpus_per_socket", UNSET))

        def _parse_def_mem_per_cpu(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        def_mem_per_cpu = _parse_def_mem_per_cpu(d.pop("def_mem_per_cpu", UNSET))

        def _parse_def_mem_per_gpu(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        def_mem_per_gpu = _parse_def_mem_per_gpu(d.pop("def_mem_per_gpu", UNSET))

        def _parse_def_mem_per_node(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        def_mem_per_node = _parse_def_mem_per_node(d.pop("def_mem_per_node", UNSET))

        def _parse_max_mem_per_cpu(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_mem_per_cpu = _parse_max_mem_per_cpu(d.pop("max_mem_per_cpu", UNSET))

        def _parse_max_mem_per_node(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_mem_per_node = _parse_max_mem_per_node(d.pop("max_mem_per_node", UNSET))

        def _parse_default_time(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        default_time = _parse_default_time(d.pop("default_time", UNSET))

        def _parse_max_time(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_time = _parse_max_time(d.pop("max_time", UNSET))

        def _parse_grace_time(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        grace_time = _parse_grace_time(d.pop("grace_time", UNSET))

        def _parse_max_nodes(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_nodes = _parse_max_nodes(d.pop("max_nodes", UNSET))

        def _parse_min_nodes(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        min_nodes = _parse_min_nodes(d.pop("min_nodes", UNSET))

        exclusive_topo = d.pop("exclusive_topo", UNSET)

        exclusive_user = d.pop("exclusive_user", UNSET)

        def _parse_priority_tier(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        priority_tier = _parse_priority_tier(d.pop("priority_tier", UNSET))

        qos = d.pop("qos", UNSET)

        req_resv = d.pop("req_resv", UNSET)

        offering_partition_request = cls(
            offering=offering,
            partition_name=partition_name,
            cpu_arch=cpu_arch,
            gpu_arch=gpu_arch,
            cpu_bind=cpu_bind,
            def_cpu_per_gpu=def_cpu_per_gpu,
            max_cpus_per_node=max_cpus_per_node,
            max_cpus_per_socket=max_cpus_per_socket,
            def_mem_per_cpu=def_mem_per_cpu,
            def_mem_per_gpu=def_mem_per_gpu,
            def_mem_per_node=def_mem_per_node,
            max_mem_per_cpu=max_mem_per_cpu,
            max_mem_per_node=max_mem_per_node,
            default_time=default_time,
            max_time=max_time,
            grace_time=grace_time,
            max_nodes=max_nodes,
            min_nodes=min_nodes,
            exclusive_topo=exclusive_topo,
            exclusive_user=exclusive_user,
            priority_tier=priority_tier,
            qos=qos,
            req_resv=req_resv,
        )

        offering_partition_request.additional_properties = d
        return offering_partition_request

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
