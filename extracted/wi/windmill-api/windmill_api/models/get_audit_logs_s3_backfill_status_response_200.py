import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAuditLogsS3BackfillStatusResponse200")


@_attrs_define
class GetAuditLogsS3BackfillStatusResponse200:
    """
    Attributes:
        running (bool):
        started_at (datetime.datetime):
        phase (str):
        from_ (datetime.datetime):
        to (datetime.datetime):
        rows_written (int):
        objects_written (int):
        errors (int):
        finished_at (Union[Unset, None, datetime.datetime]):
        last_ts (Union[Unset, None, datetime.datetime]):
        last_error (Union[Unset, None, str]):
    """

    running: bool
    started_at: datetime.datetime
    phase: str
    from_: datetime.datetime
    to: datetime.datetime
    rows_written: int
    objects_written: int
    errors: int
    finished_at: Union[Unset, None, datetime.datetime] = UNSET
    last_ts: Union[Unset, None, datetime.datetime] = UNSET
    last_error: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        running = self.running
        started_at = self.started_at.isoformat()

        phase = self.phase
        from_ = self.from_.isoformat()

        to = self.to.isoformat()

        rows_written = self.rows_written
        objects_written = self.objects_written
        errors = self.errors
        finished_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat() if self.finished_at else None

        last_ts: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_ts, Unset):
            last_ts = self.last_ts.isoformat() if self.last_ts else None

        last_error = self.last_error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "running": running,
                "started_at": started_at,
                "phase": phase,
                "from": from_,
                "to": to,
                "rows_written": rows_written,
                "objects_written": objects_written,
                "errors": errors,
            }
        )
        if finished_at is not UNSET:
            field_dict["finished_at"] = finished_at
        if last_ts is not UNSET:
            field_dict["last_ts"] = last_ts
        if last_error is not UNSET:
            field_dict["last_error"] = last_error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        running = d.pop("running")

        started_at = isoparse(d.pop("started_at"))

        phase = d.pop("phase")

        from_ = isoparse(d.pop("from"))

        to = isoparse(d.pop("to"))

        rows_written = d.pop("rows_written")

        objects_written = d.pop("objects_written")

        errors = d.pop("errors")

        _finished_at = d.pop("finished_at", UNSET)
        finished_at: Union[Unset, None, datetime.datetime]
        if _finished_at is None:
            finished_at = None
        elif isinstance(_finished_at, Unset):
            finished_at = UNSET
        else:
            finished_at = isoparse(_finished_at)

        _last_ts = d.pop("last_ts", UNSET)
        last_ts: Union[Unset, None, datetime.datetime]
        if _last_ts is None:
            last_ts = None
        elif isinstance(_last_ts, Unset):
            last_ts = UNSET
        else:
            last_ts = isoparse(_last_ts)

        last_error = d.pop("last_error", UNSET)

        get_audit_logs_s3_backfill_status_response_200 = cls(
            running=running,
            started_at=started_at,
            phase=phase,
            from_=from_,
            to=to,
            rows_written=rows_written,
            objects_written=objects_written,
            errors=errors,
            finished_at=finished_at,
            last_ts=last_ts,
            last_error=last_error,
        )

        get_audit_logs_s3_backfill_status_response_200.additional_properties = d
        return get_audit_logs_s3_backfill_status_response_200

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
