from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HpcJobPerformanceSummary")


@_attrs_define
class HpcJobPerformanceSummary:
    """
    Attributes:
        nodes (int):
        gpus (Union[None, int]):
        gpu_hours_observed (Union[None, float]): GPU samples x sample interval
        gpu_use_percent (Union[None, float]): Mean over the job's GPUs and samples
        idle_share_percent (Union[None, float]): Samples where every GPU of the job is under 5%
        gpu_memory_percent (Union[None, float]):
        gpu_memory_peak_gib (Union[None, float]): Highest reading of one GPU
        gpu_memory_total_gib (Union[None, float]): Memory of one GPU
        gpu_power_watts (Union[None, float]): Mean per GPU
        cpu_cores_mean (Union[None, float]): Summed over the job's nodes
        host_memory_peak_gib (Union[None, float]):
        host_memory_mean_gib (Union[None, float]):
        samples (int):
        coverage_percent (Union[None, float]): Sample times seen out of those expected
        first_sample (Union[None, int]): Epoch seconds
        last_sample (Union[None, int]): Epoch seconds
    """

    nodes: int
    gpus: Union[None, int]
    gpu_hours_observed: Union[None, float]
    gpu_use_percent: Union[None, float]
    idle_share_percent: Union[None, float]
    gpu_memory_percent: Union[None, float]
    gpu_memory_peak_gib: Union[None, float]
    gpu_memory_total_gib: Union[None, float]
    gpu_power_watts: Union[None, float]
    cpu_cores_mean: Union[None, float]
    host_memory_peak_gib: Union[None, float]
    host_memory_mean_gib: Union[None, float]
    samples: int
    coverage_percent: Union[None, float]
    first_sample: Union[None, int]
    last_sample: Union[None, int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        nodes = self.nodes

        gpus: Union[None, int]
        gpus = self.gpus

        gpu_hours_observed: Union[None, float]
        gpu_hours_observed = self.gpu_hours_observed

        gpu_use_percent: Union[None, float]
        gpu_use_percent = self.gpu_use_percent

        idle_share_percent: Union[None, float]
        idle_share_percent = self.idle_share_percent

        gpu_memory_percent: Union[None, float]
        gpu_memory_percent = self.gpu_memory_percent

        gpu_memory_peak_gib: Union[None, float]
        gpu_memory_peak_gib = self.gpu_memory_peak_gib

        gpu_memory_total_gib: Union[None, float]
        gpu_memory_total_gib = self.gpu_memory_total_gib

        gpu_power_watts: Union[None, float]
        gpu_power_watts = self.gpu_power_watts

        cpu_cores_mean: Union[None, float]
        cpu_cores_mean = self.cpu_cores_mean

        host_memory_peak_gib: Union[None, float]
        host_memory_peak_gib = self.host_memory_peak_gib

        host_memory_mean_gib: Union[None, float]
        host_memory_mean_gib = self.host_memory_mean_gib

        samples = self.samples

        coverage_percent: Union[None, float]
        coverage_percent = self.coverage_percent

        first_sample: Union[None, int]
        first_sample = self.first_sample

        last_sample: Union[None, int]
        last_sample = self.last_sample

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "nodes": nodes,
                "gpus": gpus,
                "gpu_hours_observed": gpu_hours_observed,
                "gpu_use_percent": gpu_use_percent,
                "idle_share_percent": idle_share_percent,
                "gpu_memory_percent": gpu_memory_percent,
                "gpu_memory_peak_gib": gpu_memory_peak_gib,
                "gpu_memory_total_gib": gpu_memory_total_gib,
                "gpu_power_watts": gpu_power_watts,
                "cpu_cores_mean": cpu_cores_mean,
                "host_memory_peak_gib": host_memory_peak_gib,
                "host_memory_mean_gib": host_memory_mean_gib,
                "samples": samples,
                "coverage_percent": coverage_percent,
                "first_sample": first_sample,
                "last_sample": last_sample,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        nodes = d.pop("nodes")

        def _parse_gpus(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        gpus = _parse_gpus(d.pop("gpus"))

        def _parse_gpu_hours_observed(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        gpu_hours_observed = _parse_gpu_hours_observed(d.pop("gpu_hours_observed"))

        def _parse_gpu_use_percent(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        gpu_use_percent = _parse_gpu_use_percent(d.pop("gpu_use_percent"))

        def _parse_idle_share_percent(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        idle_share_percent = _parse_idle_share_percent(d.pop("idle_share_percent"))

        def _parse_gpu_memory_percent(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        gpu_memory_percent = _parse_gpu_memory_percent(d.pop("gpu_memory_percent"))

        def _parse_gpu_memory_peak_gib(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        gpu_memory_peak_gib = _parse_gpu_memory_peak_gib(d.pop("gpu_memory_peak_gib"))

        def _parse_gpu_memory_total_gib(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        gpu_memory_total_gib = _parse_gpu_memory_total_gib(d.pop("gpu_memory_total_gib"))

        def _parse_gpu_power_watts(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        gpu_power_watts = _parse_gpu_power_watts(d.pop("gpu_power_watts"))

        def _parse_cpu_cores_mean(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        cpu_cores_mean = _parse_cpu_cores_mean(d.pop("cpu_cores_mean"))

        def _parse_host_memory_peak_gib(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        host_memory_peak_gib = _parse_host_memory_peak_gib(d.pop("host_memory_peak_gib"))

        def _parse_host_memory_mean_gib(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        host_memory_mean_gib = _parse_host_memory_mean_gib(d.pop("host_memory_mean_gib"))

        samples = d.pop("samples")

        def _parse_coverage_percent(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        coverage_percent = _parse_coverage_percent(d.pop("coverage_percent"))

        def _parse_first_sample(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        first_sample = _parse_first_sample(d.pop("first_sample"))

        def _parse_last_sample(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        last_sample = _parse_last_sample(d.pop("last_sample"))

        hpc_job_performance_summary = cls(
            nodes=nodes,
            gpus=gpus,
            gpu_hours_observed=gpu_hours_observed,
            gpu_use_percent=gpu_use_percent,
            idle_share_percent=idle_share_percent,
            gpu_memory_percent=gpu_memory_percent,
            gpu_memory_peak_gib=gpu_memory_peak_gib,
            gpu_memory_total_gib=gpu_memory_total_gib,
            gpu_power_watts=gpu_power_watts,
            cpu_cores_mean=cpu_cores_mean,
            host_memory_peak_gib=host_memory_peak_gib,
            host_memory_mean_gib=host_memory_mean_gib,
            samples=samples,
            coverage_percent=coverage_percent,
            first_sample=first_sample,
            last_sample=last_sample,
        )

        hpc_job_performance_summary.additional_properties = d
        return hpc_job_performance_summary

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
