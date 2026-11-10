from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HpcJobProcess")


@_attrs_define
class HpcJobProcess:
    """
    Attributes:
        command (str):
        nodes (int):
        samples (int):
        mean_cpu_percent (Union[None, float]):
        max_cpu_percent (Union[None, float]):
        peak_rss_gib (float):
    """

    command: str
    nodes: int
    samples: int
    mean_cpu_percent: Union[None, float]
    max_cpu_percent: Union[None, float]
    peak_rss_gib: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        command = self.command

        nodes = self.nodes

        samples = self.samples

        mean_cpu_percent: Union[None, float]
        mean_cpu_percent = self.mean_cpu_percent

        max_cpu_percent: Union[None, float]
        max_cpu_percent = self.max_cpu_percent

        peak_rss_gib = self.peak_rss_gib

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "command": command,
                "nodes": nodes,
                "samples": samples,
                "mean_cpu_percent": mean_cpu_percent,
                "max_cpu_percent": max_cpu_percent,
                "peak_rss_gib": peak_rss_gib,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        command = d.pop("command")

        nodes = d.pop("nodes")

        samples = d.pop("samples")

        def _parse_mean_cpu_percent(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        mean_cpu_percent = _parse_mean_cpu_percent(d.pop("mean_cpu_percent"))

        def _parse_max_cpu_percent(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        max_cpu_percent = _parse_max_cpu_percent(d.pop("max_cpu_percent"))

        peak_rss_gib = d.pop("peak_rss_gib")

        hpc_job_process = cls(
            command=command,
            nodes=nodes,
            samples=samples,
            mean_cpu_percent=mean_cpu_percent,
            max_cpu_percent=max_cpu_percent,
            peak_rss_gib=peak_rss_gib,
        )

        hpc_job_process.additional_properties = d
        return hpc_job_process

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
