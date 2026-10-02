from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.job_executions_response_dto_executions_item_job_type import JobExecutionsResponseDtoExecutionsItemJobType
from ..models.job_executions_response_dto_executions_item_status import JobExecutionsResponseDtoExecutionsItemStatus
from ..types import UNSET, Unset






T = TypeVar("T", bound="JobExecutionsResponseDtoExecutionsItem")



@_attrs_define
class JobExecutionsResponseDtoExecutionsItem:
    """ A single Cloud Run job execution with resolved status.

        Attributes:
            name (str): Full resource name of the execution (projects/…/executions/…).
            job_type (JobExecutionsResponseDtoExecutionsItemJobType): Whether this execution belongs to the import or export
                job.
            status (JobExecutionsResponseDtoExecutionsItemStatus): Resolved status of a Cloud Run job execution.
            create_time (str): When the execution was created (ISO-8601 UTC).
            start_time (str | Unset): When the execution started running (ISO-8601 UTC).
            completion_time (str | Unset): When the execution finished (ISO-8601 UTC).
     """

    name: str
    job_type: JobExecutionsResponseDtoExecutionsItemJobType
    status: JobExecutionsResponseDtoExecutionsItemStatus
    create_time: str
    start_time: str | Unset = UNSET
    completion_time: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        job_type = self.job_type.value

        status = self.status.value

        create_time = self.create_time

        start_time = self.start_time

        completion_time = self.completion_time


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
            "jobType": job_type,
            "status": status,
            "createTime": create_time,
        })
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if completion_time is not UNSET:
            field_dict["completionTime"] = completion_time

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        job_type = JobExecutionsResponseDtoExecutionsItemJobType(d.pop("jobType"))




        status = JobExecutionsResponseDtoExecutionsItemStatus(d.pop("status"))




        create_time = d.pop("createTime")

        start_time = d.pop("startTime", UNSET)

        completion_time = d.pop("completionTime", UNSET)

        job_executions_response_dto_executions_item = cls(
            name=name,
            job_type=job_type,
            status=status,
            create_time=create_time,
            start_time=start_time,
            completion_time=completion_time,
        )

        return job_executions_response_dto_executions_item

