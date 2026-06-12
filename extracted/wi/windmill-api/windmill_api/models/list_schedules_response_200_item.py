import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_schedules_response_200_item_args import ListSchedulesResponse200ItemArgs
    from ..models.list_schedules_response_200_item_extra_perms import ListSchedulesResponse200ItemExtraPerms
    from ..models.list_schedules_response_200_item_on_failure_extra_args import (
        ListSchedulesResponse200ItemOnFailureExtraArgs,
    )
    from ..models.list_schedules_response_200_item_on_recovery_extra_args import (
        ListSchedulesResponse200ItemOnRecoveryExtraArgs,
    )
    from ..models.list_schedules_response_200_item_on_success_extra_args import (
        ListSchedulesResponse200ItemOnSuccessExtraArgs,
    )
    from ..models.list_schedules_response_200_item_retry import ListSchedulesResponse200ItemRetry


T = TypeVar("T", bound="ListSchedulesResponse200Item")


@_attrs_define
class ListSchedulesResponse200Item:
    """
    Attributes:
        path (str): The unique Windmill path for this schedule. Must be of the form `u/<user>/<path>` or
            `f/<folder>/<path>`.
        edited_by (str): Username of the last person who edited this schedule
        edited_at (datetime.datetime): Timestamp of the last edit
        schedule (str): Cron expression with 6 fields (seconds, minutes, hours, day of month, month, day of week).
            Example '0 0 12 * * *' for daily at noon
        timezone (str): IANA timezone for the schedule (e.g., 'UTC', 'Europe/Paris', 'America/New_York')
        enabled (bool): Whether the schedule is currently active and will trigger jobs
        script_path (str): Path to the script or flow to execute when triggered
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        extra_perms (ListSchedulesResponse200ItemExtraPerms): Additional permissions for this schedule
        email (str): Email of the user who owns this schedule, used for permissioned_as
        permissioned_as (str): The user or group this schedule runs as (e.g., 'u/admin' or 'g/mygroup')
        args (Union[Unset, None, ListSchedulesResponse200ItemArgs]): The arguments to pass to the script or flow
        error (Union[Unset, None, str]): Last error message if the schedule failed to trigger
        on_failure (Union[Unset, None, str]): Path to a script or flow to run when the scheduled job fails
        on_failure_times (Union[Unset, None, float]): Number of consecutive failures before the on_failure handler is
            triggered (default 1)
        on_failure_exact (Union[Unset, None, bool]): If true, trigger on_failure handler only on exactly N failures, not
            on every failure after N
        on_failure_extra_args (Union[Unset, None, ListSchedulesResponse200ItemOnFailureExtraArgs]): The arguments to
            pass to the script or flow
        on_recovery (Union[Unset, None, str]): Path to a script or flow to run when the schedule recovers after failures
        on_recovery_times (Union[Unset, None, float]): Number of consecutive successes before the on_recovery handler is
            triggered (default 1)
        on_recovery_extra_args (Union[Unset, None, ListSchedulesResponse200ItemOnRecoveryExtraArgs]): The arguments to
            pass to the script or flow
        on_success (Union[Unset, None, str]): Path to a script or flow to run after each successful execution
        on_success_extra_args (Union[Unset, None, ListSchedulesResponse200ItemOnSuccessExtraArgs]): The arguments to
            pass to the script or flow
        ws_error_handler_muted (Union[Unset, bool]): If true, the workspace-level error handler will not be triggered
            for this schedule's failures
        retry (Union[Unset, None, ListSchedulesResponse200ItemRetry]): Retry configuration for failed module executions
        summary (Union[Unset, None, str]): Short summary describing the purpose of this schedule
        description (Union[Unset, None, str]): Detailed description of what this schedule does
        no_flow_overlap (Union[Unset, bool]): If true, skip this schedule's execution if the previous run is still in
            progress (prevents concurrent runs)
        tag (Union[Unset, None, str]): Worker tag to route jobs to specific worker groups
        paused_until (Union[Unset, None, datetime.datetime]): ISO 8601 datetime until which the schedule is paused.
            Schedule resumes automatically after this time
        cron_version (Union[Unset, None, str]): Cron parser version. Use 'v2' for extended syntax with additional
            features
        dynamic_skip (Union[Unset, None, str]): Path to a script that validates scheduled datetimes. Receives
            scheduled_for datetime and returns boolean to skip (true) or run (false)
        labels (Union[Unset, List[str]]):
        inherited_labels (Union[Unset, List[str]]): Labels inherited from the parent folder, computed at read time.
            Read-only — edit them on the folder.
    """

    path: str
    edited_by: str
    edited_at: datetime.datetime
    schedule: str
    timezone: str
    enabled: bool
    script_path: str
    is_flow: bool
    extra_perms: "ListSchedulesResponse200ItemExtraPerms"
    email: str
    permissioned_as: str
    args: Union[Unset, None, "ListSchedulesResponse200ItemArgs"] = UNSET
    error: Union[Unset, None, str] = UNSET
    on_failure: Union[Unset, None, str] = UNSET
    on_failure_times: Union[Unset, None, float] = UNSET
    on_failure_exact: Union[Unset, None, bool] = UNSET
    on_failure_extra_args: Union[Unset, None, "ListSchedulesResponse200ItemOnFailureExtraArgs"] = UNSET
    on_recovery: Union[Unset, None, str] = UNSET
    on_recovery_times: Union[Unset, None, float] = UNSET
    on_recovery_extra_args: Union[Unset, None, "ListSchedulesResponse200ItemOnRecoveryExtraArgs"] = UNSET
    on_success: Union[Unset, None, str] = UNSET
    on_success_extra_args: Union[Unset, None, "ListSchedulesResponse200ItemOnSuccessExtraArgs"] = UNSET
    ws_error_handler_muted: Union[Unset, bool] = UNSET
    retry: Union[Unset, None, "ListSchedulesResponse200ItemRetry"] = UNSET
    summary: Union[Unset, None, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    no_flow_overlap: Union[Unset, bool] = UNSET
    tag: Union[Unset, None, str] = UNSET
    paused_until: Union[Unset, None, datetime.datetime] = UNSET
    cron_version: Union[Unset, None, str] = UNSET
    dynamic_skip: Union[Unset, None, str] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    inherited_labels: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        schedule = self.schedule
        timezone = self.timezone
        enabled = self.enabled
        script_path = self.script_path
        is_flow = self.is_flow
        extra_perms = self.extra_perms.to_dict()

        email = self.email
        permissioned_as = self.permissioned_as
        args: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args.to_dict() if self.args else None

        error = self.error
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

        summary = self.summary
        description = self.description
        no_flow_overlap = self.no_flow_overlap
        tag = self.tag
        paused_until: Union[Unset, None, str] = UNSET
        if not isinstance(self.paused_until, Unset):
            paused_until = self.paused_until.isoformat() if self.paused_until else None

        cron_version = self.cron_version
        dynamic_skip = self.dynamic_skip
        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        inherited_labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.inherited_labels, Unset):
            inherited_labels = self.inherited_labels

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "edited_by": edited_by,
                "edited_at": edited_at,
                "schedule": schedule,
                "timezone": timezone,
                "enabled": enabled,
                "script_path": script_path,
                "is_flow": is_flow,
                "extra_perms": extra_perms,
                "email": email,
                "permissioned_as": permissioned_as,
            }
        )
        if args is not UNSET:
            field_dict["args"] = args
        if error is not UNSET:
            field_dict["error"] = error
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
        if summary is not UNSET:
            field_dict["summary"] = summary
        if description is not UNSET:
            field_dict["description"] = description
        if no_flow_overlap is not UNSET:
            field_dict["no_flow_overlap"] = no_flow_overlap
        if tag is not UNSET:
            field_dict["tag"] = tag
        if paused_until is not UNSET:
            field_dict["paused_until"] = paused_until
        if cron_version is not UNSET:
            field_dict["cron_version"] = cron_version
        if dynamic_skip is not UNSET:
            field_dict["dynamic_skip"] = dynamic_skip
        if labels is not UNSET:
            field_dict["labels"] = labels
        if inherited_labels is not UNSET:
            field_dict["inherited_labels"] = inherited_labels

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_schedules_response_200_item_args import ListSchedulesResponse200ItemArgs
        from ..models.list_schedules_response_200_item_extra_perms import ListSchedulesResponse200ItemExtraPerms
        from ..models.list_schedules_response_200_item_on_failure_extra_args import (
            ListSchedulesResponse200ItemOnFailureExtraArgs,
        )
        from ..models.list_schedules_response_200_item_on_recovery_extra_args import (
            ListSchedulesResponse200ItemOnRecoveryExtraArgs,
        )
        from ..models.list_schedules_response_200_item_on_success_extra_args import (
            ListSchedulesResponse200ItemOnSuccessExtraArgs,
        )
        from ..models.list_schedules_response_200_item_retry import ListSchedulesResponse200ItemRetry

        d = src_dict.copy()
        path = d.pop("path")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        schedule = d.pop("schedule")

        timezone = d.pop("timezone")

        enabled = d.pop("enabled")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        extra_perms = ListSchedulesResponse200ItemExtraPerms.from_dict(d.pop("extra_perms"))

        email = d.pop("email")

        permissioned_as = d.pop("permissioned_as")

        _args = d.pop("args", UNSET)
        args: Union[Unset, None, ListSchedulesResponse200ItemArgs]
        if _args is None:
            args = None
        elif isinstance(_args, Unset):
            args = UNSET
        else:
            args = ListSchedulesResponse200ItemArgs.from_dict(_args)

        error = d.pop("error", UNSET)

        on_failure = d.pop("on_failure", UNSET)

        on_failure_times = d.pop("on_failure_times", UNSET)

        on_failure_exact = d.pop("on_failure_exact", UNSET)

        _on_failure_extra_args = d.pop("on_failure_extra_args", UNSET)
        on_failure_extra_args: Union[Unset, None, ListSchedulesResponse200ItemOnFailureExtraArgs]
        if _on_failure_extra_args is None:
            on_failure_extra_args = None
        elif isinstance(_on_failure_extra_args, Unset):
            on_failure_extra_args = UNSET
        else:
            on_failure_extra_args = ListSchedulesResponse200ItemOnFailureExtraArgs.from_dict(_on_failure_extra_args)

        on_recovery = d.pop("on_recovery", UNSET)

        on_recovery_times = d.pop("on_recovery_times", UNSET)

        _on_recovery_extra_args = d.pop("on_recovery_extra_args", UNSET)
        on_recovery_extra_args: Union[Unset, None, ListSchedulesResponse200ItemOnRecoveryExtraArgs]
        if _on_recovery_extra_args is None:
            on_recovery_extra_args = None
        elif isinstance(_on_recovery_extra_args, Unset):
            on_recovery_extra_args = UNSET
        else:
            on_recovery_extra_args = ListSchedulesResponse200ItemOnRecoveryExtraArgs.from_dict(_on_recovery_extra_args)

        on_success = d.pop("on_success", UNSET)

        _on_success_extra_args = d.pop("on_success_extra_args", UNSET)
        on_success_extra_args: Union[Unset, None, ListSchedulesResponse200ItemOnSuccessExtraArgs]
        if _on_success_extra_args is None:
            on_success_extra_args = None
        elif isinstance(_on_success_extra_args, Unset):
            on_success_extra_args = UNSET
        else:
            on_success_extra_args = ListSchedulesResponse200ItemOnSuccessExtraArgs.from_dict(_on_success_extra_args)

        ws_error_handler_muted = d.pop("ws_error_handler_muted", UNSET)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, None, ListSchedulesResponse200ItemRetry]
        if _retry is None:
            retry = None
        elif isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = ListSchedulesResponse200ItemRetry.from_dict(_retry)

        summary = d.pop("summary", UNSET)

        description = d.pop("description", UNSET)

        no_flow_overlap = d.pop("no_flow_overlap", UNSET)

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

        labels = cast(List[str], d.pop("labels", UNSET))

        inherited_labels = cast(List[str], d.pop("inherited_labels", UNSET))

        list_schedules_response_200_item = cls(
            path=path,
            edited_by=edited_by,
            edited_at=edited_at,
            schedule=schedule,
            timezone=timezone,
            enabled=enabled,
            script_path=script_path,
            is_flow=is_flow,
            extra_perms=extra_perms,
            email=email,
            permissioned_as=permissioned_as,
            args=args,
            error=error,
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
            summary=summary,
            description=description,
            no_flow_overlap=no_flow_overlap,
            tag=tag,
            paused_until=paused_until,
            cron_version=cron_version,
            dynamic_skip=dynamic_skip,
            labels=labels,
            inherited_labels=inherited_labels,
        )

        list_schedules_response_200_item.additional_properties = d
        return list_schedules_response_200_item

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
