import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.email_trigger_mode import EmailTriggerMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.email_trigger_error_handler_args import EmailTriggerErrorHandlerArgs
    from ..models.email_trigger_extra_perms import EmailTriggerExtraPerms
    from ..models.email_trigger_retry import EmailTriggerRetry


T = TypeVar("T", bound="EmailTrigger")


@_attrs_define
class EmailTrigger:
    """
    Attributes:
        local_part (str):
        path (str): The unique Windmill path for this trigger. Must be of the form `u/<user>/<path>` or
            `f/<folder>/<path>`. This is the trigger object path, not the HTTP route path.
        script_path (str): Path to the script or flow to execute when triggered
        permissioned_as (str): The user or group this trigger runs as (permissioned_as)
        extra_perms (EmailTriggerExtraPerms): Additional permissions for this trigger
        workspace_id (str): The workspace this trigger belongs to
        edited_by (str): Username of the last person who edited this trigger
        edited_at (datetime.datetime): Timestamp of the last edit
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        mode (EmailTriggerMode): job trigger mode
        workspaced_local_part (Union[Unset, bool]):
        error_handler_path (Union[Unset, str]):
        error_handler_args (Union[Unset, EmailTriggerErrorHandlerArgs]): The arguments to pass to the script or flow
        retry (Union[Unset, EmailTriggerRetry]): Retry configuration for failed module executions
        labels (Union[Unset, List[str]]):
        draft_only (Union[Unset, bool]): True when this row is a per-user draft with no deployed
            trigger at the same path. Set by list endpoints when
            `include_draft_only=true` synthesizes the row from the
            draft. Frontend renders a "Draft" badge.
        is_draft (Union[Unset, bool]): True when the authed user has a per-user draft at this path
            (over a deployed row or a synthesized draft-only row).
            Frontend appends a `*` to the displayed name.
    """

    local_part: str
    path: str
    script_path: str
    permissioned_as: str
    extra_perms: "EmailTriggerExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    mode: EmailTriggerMode
    workspaced_local_part: Union[Unset, bool] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "EmailTriggerErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "EmailTriggerRetry"] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    draft_only: Union[Unset, bool] = UNSET
    is_draft: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        local_part = self.local_part
        path = self.path
        script_path = self.script_path
        permissioned_as = self.permissioned_as
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
        mode = self.mode.value

        workspaced_local_part = self.workspaced_local_part
        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        draft_only = self.draft_only
        is_draft = self.is_draft

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "local_part": local_part,
                "path": path,
                "script_path": script_path,
                "permissioned_as": permissioned_as,
                "extra_perms": extra_perms,
                "workspace_id": workspace_id,
                "edited_by": edited_by,
                "edited_at": edited_at,
                "is_flow": is_flow,
                "mode": mode,
            }
        )
        if workspaced_local_part is not UNSET:
            field_dict["workspaced_local_part"] = workspaced_local_part
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry
        if labels is not UNSET:
            field_dict["labels"] = labels
        if draft_only is not UNSET:
            field_dict["draft_only"] = draft_only
        if is_draft is not UNSET:
            field_dict["is_draft"] = is_draft

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.email_trigger_error_handler_args import EmailTriggerErrorHandlerArgs
        from ..models.email_trigger_extra_perms import EmailTriggerExtraPerms
        from ..models.email_trigger_retry import EmailTriggerRetry

        d = src_dict.copy()
        local_part = d.pop("local_part")

        path = d.pop("path")

        script_path = d.pop("script_path")

        permissioned_as = d.pop("permissioned_as")

        extra_perms = EmailTriggerExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        mode = EmailTriggerMode(d.pop("mode"))

        workspaced_local_part = d.pop("workspaced_local_part", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, EmailTriggerErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = EmailTriggerErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, EmailTriggerRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = EmailTriggerRetry.from_dict(_retry)

        labels = cast(List[str], d.pop("labels", UNSET))

        draft_only = d.pop("draft_only", UNSET)

        is_draft = d.pop("is_draft", UNSET)

        email_trigger = cls(
            local_part=local_part,
            path=path,
            script_path=script_path,
            permissioned_as=permissioned_as,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            mode=mode,
            workspaced_local_part=workspaced_local_part,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            labels=labels,
            draft_only=draft_only,
            is_draft=is_draft,
        )

        email_trigger.additional_properties = d
        return email_trigger

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
