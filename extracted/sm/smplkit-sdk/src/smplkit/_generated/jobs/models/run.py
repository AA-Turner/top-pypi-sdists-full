from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_failure_reason_type_0 import check_run_failure_reason_type_0
from ..models.run_failure_reason_type_0 import RunFailureReasonType0
from ..models.run_status import check_run_status
from ..models.run_status import RunStatus
from ..models.run_trigger import check_run_trigger
from ..models.run_trigger import RunTrigger
from dateutil.parser import isoparse
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
    from ..models.run_request_type_0 import RunRequestType0
    from ..models.run_result_type_0 import RunResultType0


T = TypeVar("T", bound="Run")


@_attrs_define
class Run:
    """One occurrence of a job executing.

    Attributes:
        job (str): The id of the job this run belongs to.
        trigger (RunTrigger): Why the run exists: `SCHEDULE`, `MANUAL` (Run now), or `RERUN`.
        status (RunStatus): Lifecycle state of the run.
        job_version (int | None | Unset): The job's version at the time the run executed.
        rerun_of (None | Unset | UUID): The source run's id; set only when `trigger` is `RERUN`.
        scheduled_for (datetime.datetime | None | Unset): The intended fire time for a scheduled run; `null` for manual
            / rerun runs.
        started_at (datetime.datetime | None | Unset): When execution started.
        finished_at (datetime.datetime | None | Unset): When execution finished.
        pending_duration_ms (int | None | Unset): Milliseconds the run waited as `PENDING` before starting.
        run_duration_ms (int | None | Unset): Milliseconds the run spent executing.
        total_duration_ms (int | None | Unset): Milliseconds from enqueue to finish.
        failure_reason (None | RunFailureReasonType0 | Unset): Why a `FAILED` run failed; `null` otherwise.
        error (None | str | Unset): Free-text failure detail, if any.
        request (None | RunRequestType0 | Unset): Snapshot of the request that was sent (header values redacted).
            Forensics only.
        result (None | RunResultType0 | Unset): Outcome of the call. For `http`: `status`, `headers`, `body` (capped at
            64 KiB), `body_truncated`, and the original `body_bytes`.
        created_at (datetime.datetime | None | Unset): When the run was enqueued (became `PENDING`).
    """

    job: str
    trigger: RunTrigger
    status: RunStatus
    job_version: int | None | Unset = UNSET
    rerun_of: None | Unset | UUID = UNSET
    scheduled_for: datetime.datetime | None | Unset = UNSET
    started_at: datetime.datetime | None | Unset = UNSET
    finished_at: datetime.datetime | None | Unset = UNSET
    pending_duration_ms: int | None | Unset = UNSET
    run_duration_ms: int | None | Unset = UNSET
    total_duration_ms: int | None | Unset = UNSET
    failure_reason: None | RunFailureReasonType0 | Unset = UNSET
    error: None | str | Unset = UNSET
    request: None | RunRequestType0 | Unset = UNSET
    result: None | RunResultType0 | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.run_request_type_0 import RunRequestType0
        from ..models.run_result_type_0 import RunResultType0

        job = self.job

        trigger: str = self.trigger

        status: str = self.status

        job_version: int | None | Unset
        if isinstance(self.job_version, Unset):
            job_version = UNSET
        else:
            job_version = self.job_version

        rerun_of: None | str | Unset
        if isinstance(self.rerun_of, Unset):
            rerun_of = UNSET
        elif isinstance(self.rerun_of, UUID):
            rerun_of = str(self.rerun_of)
        else:
            rerun_of = self.rerun_of

        scheduled_for: None | str | Unset
        if isinstance(self.scheduled_for, Unset):
            scheduled_for = UNSET
        elif isinstance(self.scheduled_for, datetime.datetime):
            scheduled_for = self.scheduled_for.isoformat()
        else:
            scheduled_for = self.scheduled_for

        started_at: None | str | Unset
        if isinstance(self.started_at, Unset):
            started_at = UNSET
        elif isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        finished_at: None | str | Unset
        if isinstance(self.finished_at, Unset):
            finished_at = UNSET
        elif isinstance(self.finished_at, datetime.datetime):
            finished_at = self.finished_at.isoformat()
        else:
            finished_at = self.finished_at

        pending_duration_ms: int | None | Unset
        if isinstance(self.pending_duration_ms, Unset):
            pending_duration_ms = UNSET
        else:
            pending_duration_ms = self.pending_duration_ms

        run_duration_ms: int | None | Unset
        if isinstance(self.run_duration_ms, Unset):
            run_duration_ms = UNSET
        else:
            run_duration_ms = self.run_duration_ms

        total_duration_ms: int | None | Unset
        if isinstance(self.total_duration_ms, Unset):
            total_duration_ms = UNSET
        else:
            total_duration_ms = self.total_duration_ms

        failure_reason: None | str | Unset
        if isinstance(self.failure_reason, Unset):
            failure_reason = UNSET
        elif isinstance(self.failure_reason, str):
            failure_reason = self.failure_reason
        else:
            failure_reason = self.failure_reason

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        request: dict[str, Any] | None | Unset
        if isinstance(self.request, Unset):
            request = UNSET
        elif isinstance(self.request, RunRequestType0):
            request = self.request.to_dict()
        else:
            request = self.request

        result: dict[str, Any] | None | Unset
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, RunResultType0):
            result = self.result.to_dict()
        else:
            result = self.result

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job": job,
                "trigger": trigger,
                "status": status,
            }
        )
        if job_version is not UNSET:
            field_dict["job_version"] = job_version
        if rerun_of is not UNSET:
            field_dict["rerun_of"] = rerun_of
        if scheduled_for is not UNSET:
            field_dict["scheduled_for"] = scheduled_for
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if finished_at is not UNSET:
            field_dict["finished_at"] = finished_at
        if pending_duration_ms is not UNSET:
            field_dict["pending_duration_ms"] = pending_duration_ms
        if run_duration_ms is not UNSET:
            field_dict["run_duration_ms"] = run_duration_ms
        if total_duration_ms is not UNSET:
            field_dict["total_duration_ms"] = total_duration_ms
        if failure_reason is not UNSET:
            field_dict["failure_reason"] = failure_reason
        if error is not UNSET:
            field_dict["error"] = error
        if request is not UNSET:
            field_dict["request"] = request
        if result is not UNSET:
            field_dict["result"] = result
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_request_type_0 import RunRequestType0
        from ..models.run_result_type_0 import RunResultType0

        d = dict(src_dict)
        job = d.pop("job")

        trigger = check_run_trigger(d.pop("trigger"))

        status = check_run_status(d.pop("status"))

        def _parse_job_version(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        job_version = _parse_job_version(d.pop("job_version", UNSET))

        def _parse_rerun_of(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                rerun_of_type_0 = UUID(data)

                return rerun_of_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        rerun_of = _parse_rerun_of(d.pop("rerun_of", UNSET))

        def _parse_scheduled_for(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scheduled_for_type_0 = isoparse(data)

                return scheduled_for_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        scheduled_for = _parse_scheduled_for(d.pop("scheduled_for", UNSET))

        def _parse_started_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = isoparse(data)

                return started_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        started_at = _parse_started_at(d.pop("started_at", UNSET))

        def _parse_finished_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finished_at_type_0 = isoparse(data)

                return finished_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        finished_at = _parse_finished_at(d.pop("finished_at", UNSET))

        def _parse_pending_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        pending_duration_ms = _parse_pending_duration_ms(d.pop("pending_duration_ms", UNSET))

        def _parse_run_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        run_duration_ms = _parse_run_duration_ms(d.pop("run_duration_ms", UNSET))

        def _parse_total_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_duration_ms = _parse_total_duration_ms(d.pop("total_duration_ms", UNSET))

        def _parse_failure_reason(data: object) -> None | RunFailureReasonType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                failure_reason_type_0 = check_run_failure_reason_type_0(data)

                return failure_reason_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunFailureReasonType0 | Unset, data)

        failure_reason = _parse_failure_reason(d.pop("failure_reason", UNSET))

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        def _parse_request(data: object) -> None | RunRequestType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                request_type_0 = RunRequestType0.from_dict(data)

                return request_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunRequestType0 | Unset, data)

        request = _parse_request(d.pop("request", UNSET))

        def _parse_result(data: object) -> None | RunResultType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = RunResultType0.from_dict(data)

                return result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunResultType0 | Unset, data)

        result = _parse_result(d.pop("result", UNSET))

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        run = cls(
            job=job,
            trigger=trigger,
            status=status,
            job_version=job_version,
            rerun_of=rerun_of,
            scheduled_for=scheduled_for,
            started_at=started_at,
            finished_at=finished_at,
            pending_duration_ms=pending_duration_ms,
            run_duration_ms=run_duration_ms,
            total_duration_ms=total_duration_ms,
            failure_reason=failure_reason,
            error=error,
            request=request,
            result=result,
            created_at=created_at,
        )

        run.additional_properties = d
        return run

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
