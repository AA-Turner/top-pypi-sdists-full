from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CancelJobRunsRequest")


@_attrs_define
class CancelJobRunsRequest:
    """
    Attributes:
        job_run_ids (list[UUID]): Runs to cancel; a run already in a terminal state is skipped.
        dry_run (bool | Unset): If true, return runs that would be cancelled without cancelling them. Default: False.
    """

    job_run_ids: list[UUID]
    dry_run: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_run_ids = []
        for job_run_ids_item_data in self.job_run_ids:
            job_run_ids_item = str(job_run_ids_item_data)
            job_run_ids.append(job_run_ids_item)

        dry_run = self.dry_run

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_run_ids": job_run_ids,
            }
        )
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_run_ids = []
        _job_run_ids = d.pop("job_run_ids")
        for job_run_ids_item_data in _job_run_ids:
            job_run_ids_item = UUID(job_run_ids_item_data)

            job_run_ids.append(job_run_ids_item)

        dry_run = d.pop("dry_run", UNSET)

        cancel_job_runs_request = cls(
            job_run_ids=job_run_ids,
            dry_run=dry_run,
        )

        cancel_job_runs_request.additional_properties = d
        return cancel_job_runs_request

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
