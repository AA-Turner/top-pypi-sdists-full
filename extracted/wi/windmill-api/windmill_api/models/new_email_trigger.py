from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.new_email_trigger_mode import NewEmailTriggerMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_email_trigger_error_handler_args import NewEmailTriggerErrorHandlerArgs
    from ..models.new_email_trigger_retry import NewEmailTriggerRetry


T = TypeVar("T", bound="NewEmailTrigger")


@_attrs_define
class NewEmailTrigger:
    """
    Attributes:
        path (str):
        script_path (str):
        local_part (str):
        is_flow (bool):
        workspaced_local_part (Union[Unset, bool]):
        error_handler_path (Union[Unset, str]):
        error_handler_args (Union[Unset, NewEmailTriggerErrorHandlerArgs]): The arguments to pass to the script or flow
        retry (Union[Unset, NewEmailTriggerRetry]): Retry configuration for failed module executions
        mode (Union[Unset, NewEmailTriggerMode]): job trigger mode
        permissioned_as (Union[Unset, str]): The user or group this trigger runs as. Used during deployment to preserve
            the original trigger owner.
        preserve_permissioned_as (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group,
            preserves the original permissioned_as value instead of overwriting it.
        labels (Union[Unset, List[str]]):
    """

    path: str
    script_path: str
    local_part: str
    is_flow: bool
    workspaced_local_part: Union[Unset, bool] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "NewEmailTriggerErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "NewEmailTriggerRetry"] = UNSET
    mode: Union[Unset, NewEmailTriggerMode] = UNSET
    permissioned_as: Union[Unset, str] = UNSET
    preserve_permissioned_as: Union[Unset, bool] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        script_path = self.script_path
        local_part = self.local_part
        is_flow = self.is_flow
        workspaced_local_part = self.workspaced_local_part
        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        mode: Union[Unset, str] = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        permissioned_as = self.permissioned_as
        preserve_permissioned_as = self.preserve_permissioned_as
        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "script_path": script_path,
                "local_part": local_part,
                "is_flow": is_flow,
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
        if mode is not UNSET:
            field_dict["mode"] = mode
        if permissioned_as is not UNSET:
            field_dict["permissioned_as"] = permissioned_as
        if preserve_permissioned_as is not UNSET:
            field_dict["preserve_permissioned_as"] = preserve_permissioned_as
        if labels is not UNSET:
            field_dict["labels"] = labels

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_email_trigger_error_handler_args import NewEmailTriggerErrorHandlerArgs
        from ..models.new_email_trigger_retry import NewEmailTriggerRetry

        d = src_dict.copy()
        path = d.pop("path")

        script_path = d.pop("script_path")

        local_part = d.pop("local_part")

        is_flow = d.pop("is_flow")

        workspaced_local_part = d.pop("workspaced_local_part", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, NewEmailTriggerErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = NewEmailTriggerErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, NewEmailTriggerRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = NewEmailTriggerRetry.from_dict(_retry)

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, NewEmailTriggerMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = NewEmailTriggerMode(_mode)

        permissioned_as = d.pop("permissioned_as", UNSET)

        preserve_permissioned_as = d.pop("preserve_permissioned_as", UNSET)

        labels = cast(List[str], d.pop("labels", UNSET))

        new_email_trigger = cls(
            path=path,
            script_path=script_path,
            local_part=local_part,
            is_flow=is_flow,
            workspaced_local_part=workspaced_local_part,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            mode=mode,
            permissioned_as=permissioned_as,
            preserve_permissioned_as=preserve_permissioned_as,
            labels=labels,
        )

        new_email_trigger.additional_properties = d
        return new_email_trigger

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
