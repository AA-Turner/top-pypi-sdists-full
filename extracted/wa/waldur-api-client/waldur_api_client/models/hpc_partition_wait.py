from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HpcPartitionWait")


@_attrs_define
class HpcPartitionWait:
    """
    Attributes:
        partition (str):
        jobs (int):
        median_wait_seconds (int):
        p90_wait_seconds (int):
    """

    partition: str
    jobs: int
    median_wait_seconds: int
    p90_wait_seconds: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        partition = self.partition

        jobs = self.jobs

        median_wait_seconds = self.median_wait_seconds

        p90_wait_seconds = self.p90_wait_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "partition": partition,
                "jobs": jobs,
                "median_wait_seconds": median_wait_seconds,
                "p90_wait_seconds": p90_wait_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        partition = d.pop("partition")

        jobs = d.pop("jobs")

        median_wait_seconds = d.pop("median_wait_seconds")

        p90_wait_seconds = d.pop("p90_wait_seconds")

        hpc_partition_wait = cls(
            partition=partition,
            jobs=jobs,
            median_wait_seconds=median_wait_seconds,
            p90_wait_seconds=p90_wait_seconds,
        )

        hpc_partition_wait.additional_properties = d
        return hpc_partition_wait

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
