import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_schedule_response_200_args import GetScheduleResponse200Args
    from ..models.get_schedule_response_200_extra_perms import GetScheduleResponse200ExtraPerms
    from ..models.get_schedule_response_200_on_failure_extra_args import GetScheduleResponse200OnFailureExtraArgs
    from ..models.get_schedule_response_200_on_recovery_extra_args import GetScheduleResponse200OnRecoveryExtraArgs
    from ..models.get_schedule_response_200_on_success_extra_args import GetScheduleResponse200OnSuccessExtraArgs
    from ..models.get_schedule_response_200_retry import GetScheduleResponse200Retry


T = TypeVar("T", bound="GetScheduleResponse200")


@_attrs_define
class GetScheduleResponse200:
    """
    Attributes:
        path (str):
        edited_by (str):
        edited_at (datetime.datetime):
        schedule (str):
        timezone (str):
        enabled (bool):
        script_path (str):
        is_flow (bool):
        extra_perms (GetScheduleResponse200ExtraPerms):
        email (str):
        args (Union[Unset, GetScheduleResponse200Args]):
        error (Union[Unset, str]):
        on_failure (Union[Unset, str]):
        on_failure_times (Union[Unset, float]):
        on_failure_exact (Union[Unset, bool]):
        on_failure_extra_args (Union[Unset, GetScheduleResponse200OnFailureExtraArgs]):
        on_recovery (Union[Unset, str]):
        on_recovery_times (Union[Unset, float]):
        on_recovery_extra_args (Union[Unset, GetScheduleResponse200OnRecoveryExtraArgs]):
        on_success (Union[Unset, str]):
        on_success_extra_args (Union[Unset, GetScheduleResponse200OnSuccessExtraArgs]):
        ws_error_handler_muted (Union[Unset, bool]):
        retry (Union[Unset, GetScheduleResponse200Retry]):
        summary (Union[Unset, str]):
        description (Union[Unset, str]):
        no_flow_overlap (Union[Unset, bool]):
        tag (Union[Unset, str]):
        paused_until (Union[Unset, datetime.datetime]):
        cron_version (Union[Unset, str]):
    """

    path: str
    edited_by: str
    edited_at: datetime.datetime
    schedule: str
    timezone: str
    enabled: bool
    script_path: str
    is_flow: bool
    extra_perms: "GetScheduleResponse200ExtraPerms"
    email: str
    args: Union[Unset, "GetScheduleResponse200Args"] = UNSET
    error: Union[Unset, str] = UNSET
    on_failure: Union[Unset, str] = UNSET
    on_failure_times: Union[Unset, float] = UNSET
    on_failure_exact: Union[Unset, bool] = UNSET
    on_failure_extra_args: Union[Unset, "GetScheduleResponse200OnFailureExtraArgs"] = UNSET
    on_recovery: Union[Unset, str] = UNSET
    on_recovery_times: Union[Unset, float] = UNSET
    on_recovery_extra_args: Union[Unset, "GetScheduleResponse200OnRecoveryExtraArgs"] = UNSET
    on_success: Union[Unset, str] = UNSET
    on_success_extra_args: Union[Unset, "GetScheduleResponse200OnSuccessExtraArgs"] = UNSET
    ws_error_handler_muted: Union[Unset, bool] = UNSET
    retry: Union[Unset, "GetScheduleResponse200Retry"] = UNSET
    summary: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    no_flow_overlap: Union[Unset, bool] = UNSET
    tag: Union[Unset, str] = UNSET
    paused_until: Union[Unset, datetime.datetime] = UNSET
    cron_version: Union[Unset, str] = UNSET
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
        args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args.to_dict()

        error = self.error
        on_failure = self.on_failure
        on_failure_times = self.on_failure_times
        on_failure_exact = self.on_failure_exact
        on_failure_extra_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.on_failure_extra_args, Unset):
            on_failure_extra_args = self.on_failure_extra_args.to_dict()

        on_recovery = self.on_recovery
        on_recovery_times = self.on_recovery_times
        on_recovery_extra_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.on_recovery_extra_args, Unset):
            on_recovery_extra_args = self.on_recovery_extra_args.to_dict()

        on_success = self.on_success
        on_success_extra_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.on_success_extra_args, Unset):
            on_success_extra_args = self.on_success_extra_args.to_dict()

        ws_error_handler_muted = self.ws_error_handler_muted
        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        summary = self.summary
        description = self.description
        no_flow_overlap = self.no_flow_overlap
        tag = self.tag
        paused_until: Union[Unset, str] = UNSET
        if not isinstance(self.paused_until, Unset):
            paused_until = self.paused_until.isoformat()

        cron_version = self.cron_version

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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_schedule_response_200_args import GetScheduleResponse200Args
        from ..models.get_schedule_response_200_extra_perms import GetScheduleResponse200ExtraPerms
        from ..models.get_schedule_response_200_on_failure_extra_args import GetScheduleResponse200OnFailureExtraArgs
        from ..models.get_schedule_response_200_on_recovery_extra_args import GetScheduleResponse200OnRecoveryExtraArgs
        from ..models.get_schedule_response_200_on_success_extra_args import GetScheduleResponse200OnSuccessExtraArgs
        from ..models.get_schedule_response_200_retry import GetScheduleResponse200Retry

        d = src_dict.copy()
        path = d.pop("path")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        schedule = d.pop("schedule")

        timezone = d.pop("timezone")

        enabled = d.pop("enabled")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        extra_perms = GetScheduleResponse200ExtraPerms.from_dict(d.pop("extra_perms"))

        email = d.pop("email")

        _args = d.pop("args", UNSET)
        args: Union[Unset, GetScheduleResponse200Args]
        if isinstance(_args, Unset):
            args = UNSET
        else:
            args = GetScheduleResponse200Args.from_dict(_args)

        error = d.pop("error", UNSET)

        on_failure = d.pop("on_failure", UNSET)

        on_failure_times = d.pop("on_failure_times", UNSET)

        on_failure_exact = d.pop("on_failure_exact", UNSET)

        _on_failure_extra_args = d.pop("on_failure_extra_args", UNSET)
        on_failure_extra_args: Union[Unset, GetScheduleResponse200OnFailureExtraArgs]
        if isinstance(_on_failure_extra_args, Unset):
            on_failure_extra_args = UNSET
        else:
            on_failure_extra_args = GetScheduleResponse200OnFailureExtraArgs.from_dict(_on_failure_extra_args)

        on_recovery = d.pop("on_recovery", UNSET)

        on_recovery_times = d.pop("on_recovery_times", UNSET)

        _on_recovery_extra_args = d.pop("on_recovery_extra_args", UNSET)
        on_recovery_extra_args: Union[Unset, GetScheduleResponse200OnRecoveryExtraArgs]
        if isinstance(_on_recovery_extra_args, Unset):
            on_recovery_extra_args = UNSET
        else:
            on_recovery_extra_args = GetScheduleResponse200OnRecoveryExtraArgs.from_dict(_on_recovery_extra_args)

        on_success = d.pop("on_success", UNSET)

        _on_success_extra_args = d.pop("on_success_extra_args", UNSET)
        on_success_extra_args: Union[Unset, GetScheduleResponse200OnSuccessExtraArgs]
        if isinstance(_on_success_extra_args, Unset):
            on_success_extra_args = UNSET
        else:
            on_success_extra_args = GetScheduleResponse200OnSuccessExtraArgs.from_dict(_on_success_extra_args)

        ws_error_handler_muted = d.pop("ws_error_handler_muted", UNSET)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, GetScheduleResponse200Retry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = GetScheduleResponse200Retry.from_dict(_retry)

        summary = d.pop("summary", UNSET)

        description = d.pop("description", UNSET)

        no_flow_overlap = d.pop("no_flow_overlap", UNSET)

        tag = d.pop("tag", UNSET)

        _paused_until = d.pop("paused_until", UNSET)
        paused_until: Union[Unset, datetime.datetime]
        if isinstance(_paused_until, Unset):
            paused_until = UNSET
        else:
            paused_until = isoparse(_paused_until)

        cron_version = d.pop("cron_version", UNSET)

        get_schedule_response_200 = cls(
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
        )

        get_schedule_response_200.additional_properties = d
        return get_schedule_response_200

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
