from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_deploy_outcome import JobDeployOutcome
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_response import JobResponse
    from ..models.job_version_response import JobVersionResponse


T = TypeVar("T", bound="DeployedJob")


@_attrs_define
class DeployedJob:
    """
    Attributes:
        job (JobResponse): The job as it stands after the deploy.
        outcome (JobDeployOutcome): What the deploy did to the job.
        previous_version (JobVersionResponse | None | Unset): The version an updated job had before the deploy.
    """

    job: JobResponse
    outcome: JobDeployOutcome
    previous_version: JobVersionResponse | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.job_version_response import JobVersionResponse

        job = self.job.to_dict()

        outcome = self.outcome.value

        previous_version: dict[str, Any] | None | Unset
        if isinstance(self.previous_version, Unset):
            previous_version = UNSET
        elif isinstance(self.previous_version, JobVersionResponse):
            previous_version = self.previous_version.to_dict()
        else:
            previous_version = self.previous_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job": job,
                "outcome": outcome,
            }
        )
        if previous_version is not UNSET:
            field_dict["previous_version"] = previous_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_response import JobResponse
        from ..models.job_version_response import JobVersionResponse

        d = dict(src_dict)
        job = JobResponse.from_dict(d.pop("job"))

        outcome = JobDeployOutcome(d.pop("outcome"))

        def _parse_previous_version(data: object) -> JobVersionResponse | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                previous_version_type_0 = JobVersionResponse.from_dict(data)

                return previous_version_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobVersionResponse | None | Unset, data)

        previous_version = _parse_previous_version(d.pop("previous_version", UNSET))

        deployed_job = cls(
            job=job,
            outcome=outcome,
            previous_version=previous_version,
        )

        deployed_job.additional_properties = d
        return deployed_job

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
