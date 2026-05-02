import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetLogCleanupStatusResponse200")


@_attrs_define
class GetLogCleanupStatusResponse200:
    """
    Attributes:
        running (bool):
        started_at (datetime.datetime):
        phase (str):
        total_service (int):
        processed_service (int):
        total_jobs (int):
        processed_jobs (int):
        s3_deleted (int):
        orphans_scanned (int):
        orphans_deleted (int):
        errors (int):
        finished_at (Union[Unset, None, datetime.datetime]):
        last_error (Union[Unset, None, str]):
    """

    running: bool
    started_at: datetime.datetime
    phase: str
    total_service: int
    processed_service: int
    total_jobs: int
    processed_jobs: int
    s3_deleted: int
    orphans_scanned: int
    orphans_deleted: int
    errors: int
    finished_at: Union[Unset, None, datetime.datetime] = UNSET
    last_error: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        running = self.running
        started_at = self.started_at.isoformat()

        phase = self.phase
        total_service = self.total_service
        processed_service = self.processed_service
        total_jobs = self.total_jobs
        processed_jobs = self.processed_jobs
        s3_deleted = self.s3_deleted
        orphans_scanned = self.orphans_scanned
        orphans_deleted = self.orphans_deleted
        errors = self.errors
        finished_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat() if self.finished_at else None

        last_error = self.last_error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "running": running,
                "started_at": started_at,
                "phase": phase,
                "total_service": total_service,
                "processed_service": processed_service,
                "total_jobs": total_jobs,
                "processed_jobs": processed_jobs,
                "s3_deleted": s3_deleted,
                "orphans_scanned": orphans_scanned,
                "orphans_deleted": orphans_deleted,
                "errors": errors,
            }
        )
        if finished_at is not UNSET:
            field_dict["finished_at"] = finished_at
        if last_error is not UNSET:
            field_dict["last_error"] = last_error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        running = d.pop("running")

        started_at = isoparse(d.pop("started_at"))

        phase = d.pop("phase")

        total_service = d.pop("total_service")

        processed_service = d.pop("processed_service")

        total_jobs = d.pop("total_jobs")

        processed_jobs = d.pop("processed_jobs")

        s3_deleted = d.pop("s3_deleted")

        orphans_scanned = d.pop("orphans_scanned")

        orphans_deleted = d.pop("orphans_deleted")

        errors = d.pop("errors")

        _finished_at = d.pop("finished_at", UNSET)
        finished_at: Union[Unset, None, datetime.datetime]
        if _finished_at is None:
            finished_at = None
        elif isinstance(_finished_at, Unset):
            finished_at = UNSET
        else:
            finished_at = isoparse(_finished_at)

        last_error = d.pop("last_error", UNSET)

        get_log_cleanup_status_response_200 = cls(
            running=running,
            started_at=started_at,
            phase=phase,
            total_service=total_service,
            processed_service=processed_service,
            total_jobs=total_jobs,
            processed_jobs=processed_jobs,
            s3_deleted=s3_deleted,
            orphans_scanned=orphans_scanned,
            orphans_deleted=orphans_deleted,
            errors=errors,
            finished_at=finished_at,
            last_error=last_error,
        )

        get_log_cleanup_status_response_200.additional_properties = d
        return get_log_cleanup_status_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
