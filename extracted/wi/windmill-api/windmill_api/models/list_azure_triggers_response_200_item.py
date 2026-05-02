import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_azure_triggers_response_200_item_azure_mode import ListAzureTriggersResponse200ItemAzureMode
from ..models.list_azure_triggers_response_200_item_mode import ListAzureTriggersResponse200ItemMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_azure_triggers_response_200_item_error_handler_args import (
        ListAzureTriggersResponse200ItemErrorHandlerArgs,
    )
    from ..models.list_azure_triggers_response_200_item_extra_perms import ListAzureTriggersResponse200ItemExtraPerms
    from ..models.list_azure_triggers_response_200_item_retry import ListAzureTriggersResponse200ItemRetry


T = TypeVar("T", bound="ListAzureTriggersResponse200Item")


@_attrs_define
class ListAzureTriggersResponse200Item:
    """An Azure Event Grid trigger that executes a script or flow when events arrive.

    Attributes:
        azure_resource_path (str):
        azure_mode (ListAzureTriggersResponse200ItemAzureMode): Azure Event Grid trigger mode.
        scope_resource_id (str): ARM resource ID of the topic (basic) or namespace (namespace modes).
        subscription_name (str):
        path (str): The unique Windmill path for this trigger. Must be of the form `u/<user>/<path>` or
            `f/<folder>/<path>`. This is the trigger object path, not the HTTP route path.
        script_path (str): Path to the script or flow to execute when triggered
        permissioned_as (str): The user or group this trigger runs as (permissioned_as)
        extra_perms (ListAzureTriggersResponse200ItemExtraPerms): Additional permissions for this trigger
        workspace_id (str): The workspace this trigger belongs to
        edited_by (str): Username of the last person who edited this trigger
        edited_at (datetime.datetime): Timestamp of the last edit
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        mode (ListAzureTriggersResponse200ItemMode): job trigger mode
        topic_name (Union[Unset, None, str]): Topic name within the namespace (namespace modes only).
        event_type_filters (Union[Unset, None, List[str]]):
        server_id (Union[Unset, str]):
        last_server_ping (Union[Unset, datetime.datetime]):
        error (Union[Unset, str]):
        error_handler_path (Union[Unset, str]):
        error_handler_args (Union[Unset, ListAzureTriggersResponse200ItemErrorHandlerArgs]): The arguments to pass to
            the script or flow
        retry (Union[Unset, ListAzureTriggersResponse200ItemRetry]): Retry configuration for failed module executions
        labels (Union[Unset, List[str]]):
    """

    azure_resource_path: str
    azure_mode: ListAzureTriggersResponse200ItemAzureMode
    scope_resource_id: str
    subscription_name: str
    path: str
    script_path: str
    permissioned_as: str
    extra_perms: "ListAzureTriggersResponse200ItemExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    mode: ListAzureTriggersResponse200ItemMode
    topic_name: Union[Unset, None, str] = UNSET
    event_type_filters: Union[Unset, None, List[str]] = UNSET
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "ListAzureTriggersResponse200ItemErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "ListAzureTriggersResponse200ItemRetry"] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        azure_resource_path = self.azure_resource_path
        azure_mode = self.azure_mode.value

        scope_resource_id = self.scope_resource_id
        subscription_name = self.subscription_name
        path = self.path
        script_path = self.script_path
        permissioned_as = self.permissioned_as
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
        mode = self.mode.value

        topic_name = self.topic_name
        event_type_filters: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.event_type_filters, Unset):
            if self.event_type_filters is None:
                event_type_filters = None
            else:
                event_type_filters = self.event_type_filters

        server_id = self.server_id
        last_server_ping: Union[Unset, str] = UNSET
        if not isinstance(self.last_server_ping, Unset):
            last_server_ping = self.last_server_ping.isoformat()

        error = self.error
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

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "azure_resource_path": azure_resource_path,
                "azure_mode": azure_mode,
                "scope_resource_id": scope_resource_id,
                "subscription_name": subscription_name,
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
        if topic_name is not UNSET:
            field_dict["topic_name"] = topic_name
        if event_type_filters is not UNSET:
            field_dict["event_type_filters"] = event_type_filters
        if server_id is not UNSET:
            field_dict["server_id"] = server_id
        if last_server_ping is not UNSET:
            field_dict["last_server_ping"] = last_server_ping
        if error is not UNSET:
            field_dict["error"] = error
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry
        if labels is not UNSET:
            field_dict["labels"] = labels

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_azure_triggers_response_200_item_error_handler_args import (
            ListAzureTriggersResponse200ItemErrorHandlerArgs,
        )
        from ..models.list_azure_triggers_response_200_item_extra_perms import (
            ListAzureTriggersResponse200ItemExtraPerms,
        )
        from ..models.list_azure_triggers_response_200_item_retry import ListAzureTriggersResponse200ItemRetry

        d = src_dict.copy()
        azure_resource_path = d.pop("azure_resource_path")

        azure_mode = ListAzureTriggersResponse200ItemAzureMode(d.pop("azure_mode"))

        scope_resource_id = d.pop("scope_resource_id")

        subscription_name = d.pop("subscription_name")

        path = d.pop("path")

        script_path = d.pop("script_path")

        permissioned_as = d.pop("permissioned_as")

        extra_perms = ListAzureTriggersResponse200ItemExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        mode = ListAzureTriggersResponse200ItemMode(d.pop("mode"))

        topic_name = d.pop("topic_name", UNSET)

        event_type_filters = cast(List[str], d.pop("event_type_filters", UNSET))

        server_id = d.pop("server_id", UNSET)

        _last_server_ping = d.pop("last_server_ping", UNSET)
        last_server_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_server_ping, Unset):
            last_server_ping = UNSET
        else:
            last_server_ping = isoparse(_last_server_ping)

        error = d.pop("error", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, ListAzureTriggersResponse200ItemErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = ListAzureTriggersResponse200ItemErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, ListAzureTriggersResponse200ItemRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = ListAzureTriggersResponse200ItemRetry.from_dict(_retry)

        labels = cast(List[str], d.pop("labels", UNSET))

        list_azure_triggers_response_200_item = cls(
            azure_resource_path=azure_resource_path,
            azure_mode=azure_mode,
            scope_resource_id=scope_resource_id,
            subscription_name=subscription_name,
            path=path,
            script_path=script_path,
            permissioned_as=permissioned_as,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            mode=mode,
            topic_name=topic_name,
            event_type_filters=event_type_filters,
            server_id=server_id,
            last_server_ping=last_server_ping,
            error=error,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            labels=labels,
        )

        list_azure_triggers_response_200_item.additional_properties = d
        return list_azure_triggers_response_200_item

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
