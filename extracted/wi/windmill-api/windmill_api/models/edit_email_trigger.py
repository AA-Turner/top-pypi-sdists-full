from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_email_trigger_error_handler_args import EditEmailTriggerErrorHandlerArgs
    from ..models.edit_email_trigger_retry import EditEmailTriggerRetry


T = TypeVar("T", bound="EditEmailTrigger")


@_attrs_define
class EditEmailTrigger:
    """
    Attributes:
        path (str):
        script_path (str):
        is_flow (bool):
        local_part (Union[Unset, str]):
        workspaced_local_part (Union[Unset, bool]):
        error_handler_path (Union[Unset, str]):
        error_handler_args (Union[Unset, EditEmailTriggerErrorHandlerArgs]): The arguments to pass to the script or flow
        retry (Union[Unset, EditEmailTriggerRetry]):
    """

    path: str
    script_path: str
    is_flow: bool
    local_part: Union[Unset, str] = UNSET
    workspaced_local_part: Union[Unset, bool] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "EditEmailTriggerErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "EditEmailTriggerRetry"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        local_part = self.local_part
        workspaced_local_part = self.workspaced_local_part
        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
            }
        )
        if local_part is not UNSET:
            field_dict["local_part"] = local_part
        if workspaced_local_part is not UNSET:
            field_dict["workspaced_local_part"] = workspaced_local_part
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_email_trigger_error_handler_args import EditEmailTriggerErrorHandlerArgs
        from ..models.edit_email_trigger_retry import EditEmailTriggerRetry

        d = src_dict.copy()
        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        local_part = d.pop("local_part", UNSET)

        workspaced_local_part = d.pop("workspaced_local_part", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, EditEmailTriggerErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = EditEmailTriggerErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, EditEmailTriggerRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = EditEmailTriggerRetry.from_dict(_retry)

        edit_email_trigger = cls(
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            local_part=local_part,
            workspaced_local_part=workspaced_local_part,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
        )

        edit_email_trigger.additional_properties = d
        return edit_email_trigger

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
