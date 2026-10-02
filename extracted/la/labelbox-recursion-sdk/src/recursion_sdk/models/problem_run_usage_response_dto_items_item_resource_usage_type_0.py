from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0_cpu import ProblemRunUsageResponseDtoItemsItemResourceUsageType0Cpu
  from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0_disk_type_0 import ProblemRunUsageResponseDtoItemsItemResourceUsageType0DiskType0
  from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0_gpu_type_0 import ProblemRunUsageResponseDtoItemsItemResourceUsageType0GpuType0
  from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0_memory import ProblemRunUsageResponseDtoItemsItemResourceUsageType0Memory





T = TypeVar("T", bound="ProblemRunUsageResponseDtoItemsItemResourceUsageType0")



@_attrs_define
class ProblemRunUsageResponseDtoItemsItemResourceUsageType0:
    """ What the run's container actually consumed, summarised by the agent-service runner over the workload phase.
    Capacities are the cgroup limits the run was granted, so peak/avg against capacity reads as consumed vs requested.

        Attributes:
            scope (str): Sampling scope reported by the runner, e.g. 'cgroup' for the run's own container.
            sample_count (float): Number of samples folded into this summary.
            sampled_seconds (float): Wall-clock seconds the samples cover — the workload phase, not queueing.
            cpu (ProblemRunUsageResponseDtoItemsItemResourceUsageType0Cpu): CPU consumed against what was requested.
            memory (ProblemRunUsageResponseDtoItemsItemResourceUsageType0Memory): Memory consumed against what was
                requested.
            gpu (None | ProblemRunUsageResponseDtoItemsItemResourceUsageType0GpuType0): GPU utilization and memory. Null
                when the run had no GPU.
            disk (None | ProblemRunUsageResponseDtoItemsItemResourceUsageType0DiskType0): Workspace disk usage. Null when
                the runner could not read the filesystem.
     """

    scope: str
    sample_count: float
    sampled_seconds: float
    cpu: ProblemRunUsageResponseDtoItemsItemResourceUsageType0Cpu
    memory: ProblemRunUsageResponseDtoItemsItemResourceUsageType0Memory
    gpu: None | ProblemRunUsageResponseDtoItemsItemResourceUsageType0GpuType0
    disk: None | ProblemRunUsageResponseDtoItemsItemResourceUsageType0DiskType0





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0_cpu import ProblemRunUsageResponseDtoItemsItemResourceUsageType0Cpu # noqa: PLC0415
        from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0_disk_type_0 import ProblemRunUsageResponseDtoItemsItemResourceUsageType0DiskType0 # noqa: PLC0415
        from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0_gpu_type_0 import ProblemRunUsageResponseDtoItemsItemResourceUsageType0GpuType0 # noqa: PLC0415
        from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0_memory import ProblemRunUsageResponseDtoItemsItemResourceUsageType0Memory # noqa: PLC0415
        scope = self.scope

        sample_count = self.sample_count

        sampled_seconds = self.sampled_seconds

        cpu = self.cpu.to_dict()

        memory = self.memory.to_dict()

        gpu: dict[str, Any] | None
        if isinstance(self.gpu, ProblemRunUsageResponseDtoItemsItemResourceUsageType0GpuType0):
            gpu = self.gpu.to_dict()
        else:
            gpu = self.gpu

        disk: dict[str, Any] | None
        if isinstance(self.disk, ProblemRunUsageResponseDtoItemsItemResourceUsageType0DiskType0):
            disk = self.disk.to_dict()
        else:
            disk = self.disk


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "scope": scope,
            "sampleCount": sample_count,
            "sampledSeconds": sampled_seconds,
            "cpu": cpu,
            "memory": memory,
            "gpu": gpu,
            "disk": disk,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0_cpu import ProblemRunUsageResponseDtoItemsItemResourceUsageType0Cpu # noqa: PLC0415
        from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0_disk_type_0 import ProblemRunUsageResponseDtoItemsItemResourceUsageType0DiskType0 # noqa: PLC0415
        from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0_gpu_type_0 import ProblemRunUsageResponseDtoItemsItemResourceUsageType0GpuType0 # noqa: PLC0415
        from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0_memory import ProblemRunUsageResponseDtoItemsItemResourceUsageType0Memory # noqa: PLC0415
        d = dict(src_dict)
        scope = d.pop("scope")

        sample_count = d.pop("sampleCount")

        sampled_seconds = d.pop("sampledSeconds")

        cpu = ProblemRunUsageResponseDtoItemsItemResourceUsageType0Cpu.from_dict(d.pop("cpu"))




        memory = ProblemRunUsageResponseDtoItemsItemResourceUsageType0Memory.from_dict(d.pop("memory"))




        def _parse_gpu(data: object) -> None | ProblemRunUsageResponseDtoItemsItemResourceUsageType0GpuType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                gpu_type_0 = ProblemRunUsageResponseDtoItemsItemResourceUsageType0GpuType0.from_dict(data)



                return gpu_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProblemRunUsageResponseDtoItemsItemResourceUsageType0GpuType0, data)

        gpu = _parse_gpu(d.pop("gpu"))


        def _parse_disk(data: object) -> None | ProblemRunUsageResponseDtoItemsItemResourceUsageType0DiskType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                disk_type_0 = ProblemRunUsageResponseDtoItemsItemResourceUsageType0DiskType0.from_dict(data)



                return disk_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProblemRunUsageResponseDtoItemsItemResourceUsageType0DiskType0, data)

        disk = _parse_disk(d.pop("disk"))


        problem_run_usage_response_dto_items_item_resource_usage_type_0 = cls(
            scope=scope,
            sample_count=sample_count,
            sampled_seconds=sampled_seconds,
            cpu=cpu,
            memory=memory,
            gpu=gpu,
            disk=disk,
        )

        return problem_run_usage_response_dto_items_item_resource_usage_type_0

