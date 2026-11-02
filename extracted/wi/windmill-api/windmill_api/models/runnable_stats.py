from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RunnableStats")


@_attrs_define
class RunnableStats:
    """Resource usage of the jobs of one runnable on one worker group. Memory and CPU are only known for jobs run as a
    subprocess; memory is the peak of the job's main process.

        Attributes:
            workspace_id (str):
            runnable_path (str): path of the script or flow step; `<adhoc>` gathers previews and other runs without a stable
                path
            worker_group (str):
            job_count (int):
            total_duration_ms (int):
            max_memory_peak (int): highest peak memory of a job, in kB
            sum_memory_peak (int): sum of the peak memory of the jobs that have one, in kB
            memory_sample_count (int): number of jobs that have a peak memory reading
            total_cpu_ms (int):
    """

    workspace_id: str
    runnable_path: str
    worker_group: str
    job_count: int
    total_duration_ms: int
    max_memory_peak: int
    sum_memory_peak: int
    memory_sample_count: int
    total_cpu_ms: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        runnable_path = self.runnable_path
        worker_group = self.worker_group
        job_count = self.job_count
        total_duration_ms = self.total_duration_ms
        max_memory_peak = self.max_memory_peak
        sum_memory_peak = self.sum_memory_peak
        memory_sample_count = self.memory_sample_count
        total_cpu_ms = self.total_cpu_ms

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_id": workspace_id,
                "runnable_path": runnable_path,
                "worker_group": worker_group,
                "job_count": job_count,
                "total_duration_ms": total_duration_ms,
                "max_memory_peak": max_memory_peak,
                "sum_memory_peak": sum_memory_peak,
                "memory_sample_count": memory_sample_count,
                "total_cpu_ms": total_cpu_ms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        runnable_path = d.pop("runnable_path")

        worker_group = d.pop("worker_group")

        job_count = d.pop("job_count")

        total_duration_ms = d.pop("total_duration_ms")

        max_memory_peak = d.pop("max_memory_peak")

        sum_memory_peak = d.pop("sum_memory_peak")

        memory_sample_count = d.pop("memory_sample_count")

        total_cpu_ms = d.pop("total_cpu_ms")

        runnable_stats = cls(
            workspace_id=workspace_id,
            runnable_path=runnable_path,
            worker_group=worker_group,
            job_count=job_count,
            total_duration_ms=total_duration_ms,
            max_memory_peak=max_memory_peak,
            sum_memory_peak=sum_memory_peak,
            memory_sample_count=memory_sample_count,
            total_cpu_ms=total_cpu_ms,
        )

        runnable_stats.additional_properties = d
        return runnable_stats

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
