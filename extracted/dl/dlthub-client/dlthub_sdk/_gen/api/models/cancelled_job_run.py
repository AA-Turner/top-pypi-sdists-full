from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.run_status import RunStatus

T = TypeVar("T", bound="CancelledJobRun")


@_attrs_define
class CancelledJobRun:
    """
    Attributes:
        job_ref (str): Job reference of the cancelled run.
        job_run_id (UUID): ID of the cancelled run.
        job_run_number (int): Run number.
        previous_status (RunStatus | str): Status of the run when the cancel request arrived.
    """

    job_ref: str
    job_run_id: UUID
    job_run_number: int
    previous_status: RunStatus | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_ref = self.job_ref

        job_run_id = str(self.job_run_id)

        job_run_number = self.job_run_number

        previous_status: str
        if isinstance(self.previous_status, RunStatus):
            previous_status = self.previous_status.value
        else:
            previous_status = self.previous_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_ref": job_ref,
                "job_run_id": job_run_id,
                "job_run_number": job_run_number,
                "previous_status": previous_status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_ref = d.pop("job_ref")

        job_run_id = UUID(d.pop("job_run_id"))

        job_run_number = d.pop("job_run_number")

        def _parse_previous_status(data: object) -> RunStatus | str:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                previous_status_type_0 = RunStatus(data)

                return previous_status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(RunStatus | str, data)

        previous_status = _parse_previous_status(d.pop("previous_status"))

        cancelled_job_run = cls(
            job_ref=job_ref,
            job_run_id=job_run_id,
            job_run_number=job_run_number,
            previous_status=previous_status,
        )

        cancelled_job_run.additional_properties = d
        return cancelled_job_run

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
