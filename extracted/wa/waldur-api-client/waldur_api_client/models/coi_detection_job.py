import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.coi_detection_job_job_type_enum import COIDetectionJobJobTypeEnum
from ..models.coi_detection_job_state_enum import COIDetectionJobStateEnum

T = TypeVar("T", bound="COIDetectionJob")


@_attrs_define
class COIDetectionJob:
    """
    Attributes:
        url (str): Return URL for the job detail endpoint.
        uuid (UUID):
        call (str):
        call_uuid (UUID):
        call_name (str):
        job_type (COIDetectionJobJobTypeEnum):
        state (COIDetectionJobStateEnum):
        total_pairs (int):
        processed_pairs (int):
        progress_percentage (float):
        conflicts_found (int):
        started_at (Union[None, datetime.datetime]):
        completed_at (Union[None, datetime.datetime]):
        error_message (str):
        created (datetime.datetime):
    """

    url: str
    uuid: UUID
    call: str
    call_uuid: UUID
    call_name: str
    job_type: COIDetectionJobJobTypeEnum
    state: COIDetectionJobStateEnum
    total_pairs: int
    processed_pairs: int
    progress_percentage: float
    conflicts_found: int
    started_at: Union[None, datetime.datetime]
    completed_at: Union[None, datetime.datetime]
    error_message: str
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        call = self.call

        call_uuid = str(self.call_uuid)

        call_name = self.call_name

        job_type = self.job_type.value

        state = self.state.value

        total_pairs = self.total_pairs

        processed_pairs = self.processed_pairs

        progress_percentage = self.progress_percentage

        conflicts_found = self.conflicts_found

        started_at: Union[None, str]
        if isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        completed_at: Union[None, str]
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        error_message = self.error_message

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "call": call,
                "call_uuid": call_uuid,
                "call_name": call_name,
                "job_type": job_type,
                "state": state,
                "total_pairs": total_pairs,
                "processed_pairs": processed_pairs,
                "progress_percentage": progress_percentage,
                "conflicts_found": conflicts_found,
                "started_at": started_at,
                "completed_at": completed_at,
                "error_message": error_message,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        call = d.pop("call")

        call_uuid = UUID(d.pop("call_uuid"))

        call_name = d.pop("call_name")

        job_type = COIDetectionJobJobTypeEnum(d.pop("job_type"))

        state = COIDetectionJobStateEnum(d.pop("state"))

        total_pairs = d.pop("total_pairs")

        processed_pairs = d.pop("processed_pairs")

        progress_percentage = d.pop("progress_percentage")

        conflicts_found = d.pop("conflicts_found")

        def _parse_started_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = isoparse(data)

                return started_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        started_at = _parse_started_at(d.pop("started_at"))

        def _parse_completed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)

                return completed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        completed_at = _parse_completed_at(d.pop("completed_at"))

        error_message = d.pop("error_message")

        created = isoparse(d.pop("created"))

        coi_detection_job = cls(
            url=url,
            uuid=uuid,
            call=call,
            call_uuid=call_uuid,
            call_name=call_name,
            job_type=job_type,
            state=state,
            total_pairs=total_pairs,
            processed_pairs=processed_pairs,
            progress_percentage=progress_percentage,
            conflicts_found=conflicts_found,
            started_at=started_at,
            completed_at=completed_at,
            error_message=error_message,
            created=created,
        )

        coi_detection_job.additional_properties = d
        return coi_detection_job

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
