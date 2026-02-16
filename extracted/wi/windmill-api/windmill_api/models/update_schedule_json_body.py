import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_schedule_json_body_args import UpdateScheduleJsonBodyArgs
    from ..models.update_schedule_json_body_on_failure_extra_args import UpdateScheduleJsonBodyOnFailureExtraArgs
    from ..models.update_schedule_json_body_on_recovery_extra_args import UpdateScheduleJsonBodyOnRecoveryExtraArgs
    from ..models.update_schedule_json_body_on_success_extra_args import UpdateScheduleJsonBodyOnSuccessExtraArgs
    from ..models.update_schedule_json_body_retry import UpdateScheduleJsonBodyRetry


T = TypeVar("T", bound="UpdateScheduleJsonBody")


@_attrs_define
class UpdateScheduleJsonBody:
    """
    Attributes:
        schedule (str): Cron expression with 6 fields (seconds, minutes, hours, day of month, month, day of week).
            Example '0 0 12 * * *' for daily at noon
        timezone (str): IANA timezone for the schedule (e.g., 'UTC', 'Europe/Paris', 'America/New_York')
        args (Optional[UpdateScheduleJsonBodyArgs]): The arguments to pass to the script or flow
        on_failure (Union[Unset, None, str]): Path to a script or flow to run when the scheduled job fails
        on_failure_times (Union[Unset, None, float]): Number of consecutive failures before the on_failure handler is
            triggered (default 1)
        on_failure_exact (Union[Unset, None, bool]): If true, trigger on_failure handler only on exactly N failures, not
            on every failure after N
        on_failure_extra_args (Union[Unset, None, UpdateScheduleJsonBodyOnFailureExtraArgs]): The arguments to pass to
            the script or flow
        on_recovery (Union[Unset, None, str]): Path to a script or flow to run when the schedule recovers after failures
        on_recovery_times (Union[Unset, None, float]): Number of consecutive successes before the on_recovery handler is
            triggered (default 1)
        on_recovery_extra_args (Union[Unset, None, UpdateScheduleJsonBodyOnRecoveryExtraArgs]): The arguments to pass to
            the script or flow
        on_success (Union[Unset, None, str]): Path to a script or flow to run after each successful execution
        on_success_extra_args (Union[Unset, None, UpdateScheduleJsonBodyOnSuccessExtraArgs]): The arguments to pass to
            the script or flow
        ws_error_handler_muted (Union[Unset, bool]): If true, the workspace-level error handler will not be triggered
            for this schedule's failures
        retry (Union[Unset, None, UpdateScheduleJsonBodyRetry]): Retry configuration for failed module executions
        no_flow_overlap (Union[Unset, bool]): If true, skip this schedule's execution if the previous run is still in
            progress (prevents concurrent runs)
        summary (Union[Unset, None, str]): Short summary describing the purpose of this schedule
        description (Union[Unset, None, str]): Detailed description of what this schedule does
        tag (Union[Unset, None, str]): Worker tag to route jobs to specific worker groups
        paused_until (Union[Unset, None, datetime.datetime]): ISO 8601 datetime until which the schedule is paused.
            Schedule resumes automatically after this time
        cron_version (Union[Unset, None, str]): Cron parser version. Use 'v2' for extended syntax with additional
            features
        dynamic_skip (Union[Unset, None, str]): Path to a script that validates scheduled datetimes. Receives
            scheduled_for datetime and returns boolean to skip (true) or run (false)
    """

    schedule: str
    timezone: str
    args: Optional["UpdateScheduleJsonBodyArgs"]
    on_failure: Union[Unset, None, str] = UNSET
    on_failure_times: Union[Unset, None, float] = UNSET
    on_failure_exact: Union[Unset, None, bool] = UNSET
    on_failure_extra_args: Union[Unset, None, "UpdateScheduleJsonBodyOnFailureExtraArgs"] = UNSET
    on_recovery: Union[Unset, None, str] = UNSET
    on_recovery_times: Union[Unset, None, float] = UNSET
    on_recovery_extra_args: Union[Unset, None, "UpdateScheduleJsonBodyOnRecoveryExtraArgs"] = UNSET
    on_success: Union[Unset, None, str] = UNSET
    on_success_extra_args: Union[Unset, None, "UpdateScheduleJsonBodyOnSuccessExtraArgs"] = UNSET
    ws_error_handler_muted: Union[Unset, bool] = UNSET
    retry: Union[Unset, None, "UpdateScheduleJsonBodyRetry"] = UNSET
    no_flow_overlap: Union[Unset, bool] = UNSET
    summary: Union[Unset, None, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    tag: Union[Unset, None, str] = UNSET
    paused_until: Union[Unset, None, datetime.datetime] = UNSET
    cron_version: Union[Unset, None, str] = UNSET
    dynamic_skip: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        schedule = self.schedule
        timezone = self.timezone
        args = self.args.to_dict() if self.args else None

        on_failure = self.on_failure
        on_failure_times = self.on_failure_times
        on_failure_exact = self.on_failure_exact
        on_failure_extra_args: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.on_failure_extra_args, Unset):
            on_failure_extra_args = self.on_failure_extra_args.to_dict() if self.on_failure_extra_args else None

        on_recovery = self.on_recovery
        on_recovery_times = self.on_recovery_times
        on_recovery_extra_args: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.on_recovery_extra_args, Unset):
            on_recovery_extra_args = self.on_recovery_extra_args.to_dict() if self.on_recovery_extra_args else None

        on_success = self.on_success
        on_success_extra_args: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.on_success_extra_args, Unset):
            on_success_extra_args = self.on_success_extra_args.to_dict() if self.on_success_extra_args else None

        ws_error_handler_muted = self.ws_error_handler_muted
        retry: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict() if self.retry else None

        no_flow_overlap = self.no_flow_overlap
        summary = self.summary
        description = self.description
        tag = self.tag
        paused_until: Union[Unset, None, str] = UNSET
        if not isinstance(self.paused_until, Unset):
            paused_until = self.paused_until.isoformat() if self.paused_until else None

        cron_version = self.cron_version
        dynamic_skip = self.dynamic_skip

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schedule": schedule,
                "timezone": timezone,
                "args": args,
            }
        )
        if on_failure is not UNSET:
            field_dict["on_failure"] = on_failure
        if on_failure_times is not UNSET:
            field_dict["on_failure_times"] = on_failure_times
        if on_failure_exact is not UNSET:
            field_dict["on_failure_exact"] = on_failure_exact
        if on_failure_extra_args is not UNSET:
            field_dict["on_failure_extra_args"] = on_failure_extra_args
        if on_recovery is not UNSET:
            field_dict["on_recovery"] = on_recovery
        if on_recovery_times is not UNSET:
            field_dict["on_recovery_times"] = on_recovery_times
        if on_recovery_extra_args is not UNSET:
            field_dict["on_recovery_extra_args"] = on_recovery_extra_args
        if on_success is not UNSET:
            field_dict["on_success"] = on_success
        if on_success_extra_args is not UNSET:
            field_dict["on_success_extra_args"] = on_success_extra_args
        if ws_error_handler_muted is not UNSET:
            field_dict["ws_error_handler_muted"] = ws_error_handler_muted
        if retry is not UNSET:
            field_dict["retry"] = retry
        if no_flow_overlap is not UNSET:
            field_dict["no_flow_overlap"] = no_flow_overlap
        if summary is not UNSET:
            field_dict["summary"] = summary
        if description is not UNSET:
            field_dict["description"] = description
        if tag is not UNSET:
            field_dict["tag"] = tag
        if paused_until is not UNSET:
            field_dict["paused_until"] = paused_until
        if cron_version is not UNSET:
            field_dict["cron_version"] = cron_version
        if dynamic_skip is not UNSET:
            field_dict["dynamic_skip"] = dynamic_skip

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_schedule_json_body_args import UpdateScheduleJsonBodyArgs
        from ..models.update_schedule_json_body_on_failure_extra_args import UpdateScheduleJsonBodyOnFailureExtraArgs
        from ..models.update_schedule_json_body_on_recovery_extra_args import UpdateScheduleJsonBodyOnRecoveryExtraArgs
        from ..models.update_schedule_json_body_on_success_extra_args import UpdateScheduleJsonBodyOnSuccessExtraArgs
        from ..models.update_schedule_json_body_retry import UpdateScheduleJsonBodyRetry

        d = src_dict.copy()
        schedule = d.pop("schedule")

        timezone = d.pop("timezone")

        _args = d.pop("args")
        args: Optional[UpdateScheduleJsonBodyArgs]
        if _args is None:
            args = None
        else:
            args = UpdateScheduleJsonBodyArgs.from_dict(_args)

        on_failure = d.pop("on_failure", UNSET)

        on_failure_times = d.pop("on_failure_times", UNSET)

        on_failure_exact = d.pop("on_failure_exact", UNSET)

        _on_failure_extra_args = d.pop("on_failure_extra_args", UNSET)
        on_failure_extra_args: Union[Unset, None, UpdateScheduleJsonBodyOnFailureExtraArgs]
        if _on_failure_extra_args is None:
            on_failure_extra_args = None
        elif isinstance(_on_failure_extra_args, Unset):
            on_failure_extra_args = UNSET
        else:
            on_failure_extra_args = UpdateScheduleJsonBodyOnFailureExtraArgs.from_dict(_on_failure_extra_args)

        on_recovery = d.pop("on_recovery", UNSET)

        on_recovery_times = d.pop("on_recovery_times", UNSET)

        _on_recovery_extra_args = d.pop("on_recovery_extra_args", UNSET)
        on_recovery_extra_args: Union[Unset, None, UpdateScheduleJsonBodyOnRecoveryExtraArgs]
        if _on_recovery_extra_args is None:
            on_recovery_extra_args = None
        elif isinstance(_on_recovery_extra_args, Unset):
            on_recovery_extra_args = UNSET
        else:
            on_recovery_extra_args = UpdateScheduleJsonBodyOnRecoveryExtraArgs.from_dict(_on_recovery_extra_args)

        on_success = d.pop("on_success", UNSET)

        _on_success_extra_args = d.pop("on_success_extra_args", UNSET)
        on_success_extra_args: Union[Unset, None, UpdateScheduleJsonBodyOnSuccessExtraArgs]
        if _on_success_extra_args is None:
            on_success_extra_args = None
        elif isinstance(_on_success_extra_args, Unset):
            on_success_extra_args = UNSET
        else:
            on_success_extra_args = UpdateScheduleJsonBodyOnSuccessExtraArgs.from_dict(_on_success_extra_args)

        ws_error_handler_muted = d.pop("ws_error_handler_muted", UNSET)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, None, UpdateScheduleJsonBodyRetry]
        if _retry is None:
            retry = None
        elif isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = UpdateScheduleJsonBodyRetry.from_dict(_retry)

        no_flow_overlap = d.pop("no_flow_overlap", UNSET)

        summary = d.pop("summary", UNSET)

        description = d.pop("description", UNSET)

        tag = d.pop("tag", UNSET)

        _paused_until = d.pop("paused_until", UNSET)
        paused_until: Union[Unset, None, datetime.datetime]
        if _paused_until is None:
            paused_until = None
        elif isinstance(_paused_until, Unset):
            paused_until = UNSET
        else:
            paused_until = isoparse(_paused_until)

        cron_version = d.pop("cron_version", UNSET)

        dynamic_skip = d.pop("dynamic_skip", UNSET)

        update_schedule_json_body = cls(
            schedule=schedule,
            timezone=timezone,
            args=args,
            on_failure=on_failure,
            on_failure_times=on_failure_times,
            on_failure_exact=on_failure_exact,
            on_failure_extra_args=on_failure_extra_args,
            on_recovery=on_recovery,
            on_recovery_times=on_recovery_times,
            on_recovery_extra_args=on_recovery_extra_args,
            on_success=on_success,
            on_success_extra_args=on_success_extra_args,
            ws_error_handler_muted=ws_error_handler_muted,
            retry=retry,
            no_flow_overlap=no_flow_overlap,
            summary=summary,
            description=description,
            tag=tag,
            paused_until=paused_until,
            cron_version=cron_version,
            dynamic_skip=dynamic_skip,
        )

        update_schedule_json_body.additional_properties = d
        return update_schedule_json_body

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
