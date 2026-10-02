from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.job_executions_response_dto_time_range import JobExecutionsResponseDtoTimeRange
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.job_executions_response_dto_executions_item import JobExecutionsResponseDtoExecutionsItem





T = TypeVar("T", bound="JobExecutionsResponseDto")



@_attrs_define
class JobExecutionsResponseDto:
    """ Cloud Run job executions for import and export jobs over a chosen time range.

        Attributes:
            time_range (JobExecutionsResponseDtoTimeRange): Lookback window for monitoring queries.
            import_job_configured (bool): Whether an import job is configured on this platform.
            export_job_configured (bool): Whether an export job is configured on this platform.
            executions (list[JobExecutionsResponseDtoExecutionsItem]): Job executions within the requested time range,
                newest first.
            truncated (bool | Unset): True if the Cloud Run API returned more executions than the page size; some results
                may be missing.
     """

    time_range: JobExecutionsResponseDtoTimeRange
    import_job_configured: bool
    export_job_configured: bool
    executions: list[JobExecutionsResponseDtoExecutionsItem]
    truncated: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.job_executions_response_dto_executions_item import JobExecutionsResponseDtoExecutionsItem # noqa: PLC0415
        time_range = self.time_range.value

        import_job_configured = self.import_job_configured

        export_job_configured = self.export_job_configured

        executions = []
        for executions_item_data in self.executions:
            executions_item = executions_item_data.to_dict()
            executions.append(executions_item)



        truncated = self.truncated


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "timeRange": time_range,
            "importJobConfigured": import_job_configured,
            "exportJobConfigured": export_job_configured,
            "executions": executions,
        })
        if truncated is not UNSET:
            field_dict["truncated"] = truncated

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_executions_response_dto_executions_item import JobExecutionsResponseDtoExecutionsItem # noqa: PLC0415
        d = dict(src_dict)
        time_range = JobExecutionsResponseDtoTimeRange(d.pop("timeRange"))




        import_job_configured = d.pop("importJobConfigured")

        export_job_configured = d.pop("exportJobConfigured")

        executions = []
        _executions = d.pop("executions")
        for executions_item_data in (_executions):
            executions_item = JobExecutionsResponseDtoExecutionsItem.from_dict(executions_item_data)



            executions.append(executions_item)


        truncated = d.pop("truncated", UNSET)

        job_executions_response_dto = cls(
            time_range=time_range,
            import_job_configured=import_job_configured,
            export_job_configured=export_job_configured,
            executions=executions,
            truncated=truncated,
        )

        return job_executions_response_dto

