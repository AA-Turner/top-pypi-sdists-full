import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_email_triggers_response_200_item_error_handler_args import (
        ListEmailTriggersResponse200ItemErrorHandlerArgs,
    )
    from ..models.list_email_triggers_response_200_item_extra_perms import ListEmailTriggersResponse200ItemExtraPerms
    from ..models.list_email_triggers_response_200_item_retry import ListEmailTriggersResponse200ItemRetry


T = TypeVar("T", bound="ListEmailTriggersResponse200Item")


@_attrs_define
class ListEmailTriggersResponse200Item:
    """
    Attributes:
        local_part (str):
        path (str):
        script_path (str):
        email (str):
        extra_perms (ListEmailTriggersResponse200ItemExtraPerms):
        workspace_id (str):
        edited_by (str):
        edited_at (datetime.datetime):
        is_flow (bool):
        workspaced_local_part (Union[Unset, bool]):
        error_handler_path (Union[Unset, str]):
        error_handler_args (Union[Unset, ListEmailTriggersResponse200ItemErrorHandlerArgs]): The arguments to pass to
            the script or flow
        retry (Union[Unset, ListEmailTriggersResponse200ItemRetry]):
    """

    local_part: str
    path: str
    script_path: str
    email: str
    extra_perms: "ListEmailTriggersResponse200ItemExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    workspaced_local_part: Union[Unset, bool] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "ListEmailTriggersResponse200ItemErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "ListEmailTriggersResponse200ItemRetry"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        local_part = self.local_part
        path = self.path
        script_path = self.script_path
        email = self.email
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
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
                "local_part": local_part,
                "path": path,
                "script_path": script_path,
                "email": email,
                "extra_perms": extra_perms,
                "workspace_id": workspace_id,
                "edited_by": edited_by,
                "edited_at": edited_at,
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_email_triggers_response_200_item_error_handler_args import (
            ListEmailTriggersResponse200ItemErrorHandlerArgs,
        )
        from ..models.list_email_triggers_response_200_item_extra_perms import (
            ListEmailTriggersResponse200ItemExtraPerms,
        )
        from ..models.list_email_triggers_response_200_item_retry import ListEmailTriggersResponse200ItemRetry

        d = src_dict.copy()
        local_part = d.pop("local_part")

        path = d.pop("path")

        script_path = d.pop("script_path")

        email = d.pop("email")

        extra_perms = ListEmailTriggersResponse200ItemExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        workspaced_local_part = d.pop("workspaced_local_part", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, ListEmailTriggersResponse200ItemErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = ListEmailTriggersResponse200ItemErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, ListEmailTriggersResponse200ItemRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = ListEmailTriggersResponse200ItemRetry.from_dict(_retry)

        list_email_triggers_response_200_item = cls(
            local_part=local_part,
            path=path,
            script_path=script_path,
            email=email,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            workspaced_local_part=workspaced_local_part,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
        )

        list_email_triggers_response_200_item.additional_properties = d
        return list_email_triggers_response_200_item

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
