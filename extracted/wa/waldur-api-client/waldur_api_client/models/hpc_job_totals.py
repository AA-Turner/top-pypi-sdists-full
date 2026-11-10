from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HpcJobTotals")


@_attrs_define
class HpcJobTotals:
    """
    Attributes:
        completed (int):
        failed (int):
        timeout (int):
        cancelled (int):
        running (int):
        pending (int):
    """

    completed: int
    failed: int
    timeout: int
    cancelled: int
    running: int
    pending: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        completed = self.completed

        failed = self.failed

        timeout = self.timeout

        cancelled = self.cancelled

        running = self.running

        pending = self.pending

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "completed": completed,
                "failed": failed,
                "timeout": timeout,
                "cancelled": cancelled,
                "running": running,
                "pending": pending,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        completed = d.pop("completed")

        failed = d.pop("failed")

        timeout = d.pop("timeout")

        cancelled = d.pop("cancelled")

        running = d.pop("running")

        pending = d.pop("pending")

        hpc_job_totals = cls(
            completed=completed,
            failed=failed,
            timeout=timeout,
            cancelled=cancelled,
            running=running,
            pending=pending,
        )

        hpc_job_totals.additional_properties = d
        return hpc_job_totals

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
