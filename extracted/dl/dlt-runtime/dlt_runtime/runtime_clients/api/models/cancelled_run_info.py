from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.run_status import RunStatus

T = TypeVar("T", bound="CancelledRunInfo")


@_attrs_define
class CancelledRunInfo:
    """
    Attributes:
        job_ref (str): Job reference of the cancelled run.
        previous_status (RunStatus): The status of the run
        run_id (UUID): ID of the cancelled run.
        run_number (int): Run number.
    """

    job_ref: str
    previous_status: RunStatus
    run_id: UUID
    run_number: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_ref = self.job_ref

        previous_status = self.previous_status.value

        run_id = str(self.run_id)

        run_number = self.run_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_ref": job_ref,
                "previous_status": previous_status,
                "run_id": run_id,
                "run_number": run_number,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_ref = d.pop("job_ref")

        previous_status = RunStatus(d.pop("previous_status"))

        run_id = UUID(d.pop("run_id"))

        run_number = d.pop("run_number")

        cancelled_run_info = cls(
            job_ref=job_ref,
            previous_status=previous_status,
            run_id=run_id,
            run_number=run_number,
        )

        cancelled_run_info.additional_properties = d
        return cancelled_run_info

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
