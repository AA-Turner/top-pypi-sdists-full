import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.websocket_trigger_filter_logic import WebsocketTriggerFilterLogic
from ..models.websocket_trigger_mode import WebsocketTriggerMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.websocket_trigger_error_handler_args import WebsocketTriggerErrorHandlerArgs
    from ..models.websocket_trigger_extra_perms import WebsocketTriggerExtraPerms
    from ..models.websocket_trigger_filters_item import WebsocketTriggerFiltersItem
    from ..models.websocket_trigger_heartbeat import WebsocketTriggerHeartbeat
    from ..models.websocket_trigger_initial_messages_item_type_0 import WebsocketTriggerInitialMessagesItemType0
    from ..models.websocket_trigger_initial_messages_item_type_1 import WebsocketTriggerInitialMessagesItemType1
    from ..models.websocket_trigger_retry import WebsocketTriggerRetry
    from ..models.websocket_trigger_url_runnable_args import WebsocketTriggerUrlRunnableArgs


T = TypeVar("T", bound="WebsocketTrigger")


@_attrs_define
class WebsocketTrigger:
    """
    Attributes:
        url (str): The WebSocket URL to connect to (can be a static URL or computed by a runnable)
        filters (List['WebsocketTriggerFiltersItem']): Array of key-value filters to match incoming messages (only
            matching messages trigger the script)
        can_return_message (bool): If true, the script can return a message to send back through the WebSocket
        can_return_error_result (bool): If true, error results are sent back through the WebSocket
        path (str): The unique Windmill path for this trigger. Must be of the form `u/<user>/<path>` or
            `f/<folder>/<path>`. This is the trigger object path, not the HTTP route path.
        script_path (str): Path to the script or flow to execute when triggered
        permissioned_as (str): The user or group this trigger runs as (permissioned_as)
        extra_perms (WebsocketTriggerExtraPerms): Additional permissions for this trigger
        workspace_id (str): The workspace this trigger belongs to
        edited_by (str): Username of the last person who edited this trigger
        edited_at (datetime.datetime): Timestamp of the last edit
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        mode (WebsocketTriggerMode): job trigger mode
        server_id (Union[Unset, str]): ID of the server currently handling this trigger (internal)
        last_server_ping (Union[Unset, datetime.datetime]): Timestamp of last server heartbeat (internal)
        error (Union[Unset, str]): Last error message if the trigger failed
        filter_logic (Union[Unset, WebsocketTriggerFilterLogic]): Logic to apply when evaluating filters. 'and' requires
            all filters to match, 'or' requires any filter to match. Default: WebsocketTriggerFilterLogic.AND.
        initial_messages (Union[Unset, None, List[Union['WebsocketTriggerInitialMessagesItemType0',
            'WebsocketTriggerInitialMessagesItemType1']]]): Messages to send immediately after connecting (can be raw
            strings or computed by runnables)
        url_runnable_args (Union[Unset, None, WebsocketTriggerUrlRunnableArgs]): The arguments to pass to the script or
            flow
        heartbeat (Union[Unset, None, WebsocketTriggerHeartbeat]): Optional periodic heartbeat message configuration
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails
        error_handler_args (Union[Unset, WebsocketTriggerErrorHandlerArgs]): The arguments to pass to the script or flow
        retry (Union[Unset, WebsocketTriggerRetry]): Retry configuration for failed module executions
        labels (Union[Unset, List[str]]):
    """

    url: str
    filters: List["WebsocketTriggerFiltersItem"]
    can_return_message: bool
    can_return_error_result: bool
    path: str
    script_path: str
    permissioned_as: str
    extra_perms: "WebsocketTriggerExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    mode: WebsocketTriggerMode
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    filter_logic: Union[Unset, WebsocketTriggerFilterLogic] = WebsocketTriggerFilterLogic.AND
    initial_messages: Union[
        Unset, None, List[Union["WebsocketTriggerInitialMessagesItemType0", "WebsocketTriggerInitialMessagesItemType1"]]
    ] = UNSET
    url_runnable_args: Union[Unset, None, "WebsocketTriggerUrlRunnableArgs"] = UNSET
    heartbeat: Union[Unset, None, "WebsocketTriggerHeartbeat"] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "WebsocketTriggerErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "WebsocketTriggerRetry"] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.websocket_trigger_initial_messages_item_type_0 import WebsocketTriggerInitialMessagesItemType0

        url = self.url
        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()

            filters.append(filters_item)

        can_return_message = self.can_return_message
        can_return_error_result = self.can_return_error_result
        path = self.path
        script_path = self.script_path
        permissioned_as = self.permissioned_as
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
        mode = self.mode.value

        server_id = self.server_id
        last_server_ping: Union[Unset, str] = UNSET
        if not isinstance(self.last_server_ping, Unset):
            last_server_ping = self.last_server_ping.isoformat()

        error = self.error
        filter_logic: Union[Unset, str] = UNSET
        if not isinstance(self.filter_logic, Unset):
            filter_logic = self.filter_logic.value

        initial_messages: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.initial_messages, Unset):
            if self.initial_messages is None:
                initial_messages = None
            else:
                initial_messages = []
                for initial_messages_item_data in self.initial_messages:
                    initial_messages_item: Dict[str, Any]

                    if isinstance(initial_messages_item_data, WebsocketTriggerInitialMessagesItemType0):
                        initial_messages_item = initial_messages_item_data.to_dict()

                    else:
                        initial_messages_item = initial_messages_item_data.to_dict()

                    initial_messages.append(initial_messages_item)

        url_runnable_args: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.url_runnable_args, Unset):
            url_runnable_args = self.url_runnable_args.to_dict() if self.url_runnable_args else None

        heartbeat: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.heartbeat, Unset):
            heartbeat = self.heartbeat.to_dict() if self.heartbeat else None

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
                "url": url,
                "filters": filters,
                "can_return_message": can_return_message,
                "can_return_error_result": can_return_error_result,
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
        if server_id is not UNSET:
            field_dict["server_id"] = server_id
        if last_server_ping is not UNSET:
            field_dict["last_server_ping"] = last_server_ping
        if error is not UNSET:
            field_dict["error"] = error
        if filter_logic is not UNSET:
            field_dict["filter_logic"] = filter_logic
        if initial_messages is not UNSET:
            field_dict["initial_messages"] = initial_messages
        if url_runnable_args is not UNSET:
            field_dict["url_runnable_args"] = url_runnable_args
        if heartbeat is not UNSET:
            field_dict["heartbeat"] = heartbeat
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
        from ..models.websocket_trigger_error_handler_args import WebsocketTriggerErrorHandlerArgs
        from ..models.websocket_trigger_extra_perms import WebsocketTriggerExtraPerms
        from ..models.websocket_trigger_filters_item import WebsocketTriggerFiltersItem
        from ..models.websocket_trigger_heartbeat import WebsocketTriggerHeartbeat
        from ..models.websocket_trigger_initial_messages_item_type_0 import WebsocketTriggerInitialMessagesItemType0
        from ..models.websocket_trigger_initial_messages_item_type_1 import WebsocketTriggerInitialMessagesItemType1
        from ..models.websocket_trigger_retry import WebsocketTriggerRetry
        from ..models.websocket_trigger_url_runnable_args import WebsocketTriggerUrlRunnableArgs

        d = src_dict.copy()
        url = d.pop("url")

        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = WebsocketTriggerFiltersItem.from_dict(filters_item_data)

            filters.append(filters_item)

        can_return_message = d.pop("can_return_message")

        can_return_error_result = d.pop("can_return_error_result")

        path = d.pop("path")

        script_path = d.pop("script_path")

        permissioned_as = d.pop("permissioned_as")

        extra_perms = WebsocketTriggerExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        mode = WebsocketTriggerMode(d.pop("mode"))

        server_id = d.pop("server_id", UNSET)

        _last_server_ping = d.pop("last_server_ping", UNSET)
        last_server_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_server_ping, Unset):
            last_server_ping = UNSET
        else:
            last_server_ping = isoparse(_last_server_ping)

        error = d.pop("error", UNSET)

        _filter_logic = d.pop("filter_logic", UNSET)
        filter_logic: Union[Unset, WebsocketTriggerFilterLogic]
        if isinstance(_filter_logic, Unset):
            filter_logic = UNSET
        else:
            filter_logic = WebsocketTriggerFilterLogic(_filter_logic)

        initial_messages = []
        _initial_messages = d.pop("initial_messages", UNSET)
        for initial_messages_item_data in _initial_messages or []:

            def _parse_initial_messages_item(
                data: object,
            ) -> Union["WebsocketTriggerInitialMessagesItemType0", "WebsocketTriggerInitialMessagesItemType1"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    initial_messages_item_type_0 = WebsocketTriggerInitialMessagesItemType0.from_dict(data)

                    return initial_messages_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                initial_messages_item_type_1 = WebsocketTriggerInitialMessagesItemType1.from_dict(data)

                return initial_messages_item_type_1

            initial_messages_item = _parse_initial_messages_item(initial_messages_item_data)

            initial_messages.append(initial_messages_item)

        _url_runnable_args = d.pop("url_runnable_args", UNSET)
        url_runnable_args: Union[Unset, None, WebsocketTriggerUrlRunnableArgs]
        if _url_runnable_args is None:
            url_runnable_args = None
        elif isinstance(_url_runnable_args, Unset):
            url_runnable_args = UNSET
        else:
            url_runnable_args = WebsocketTriggerUrlRunnableArgs.from_dict(_url_runnable_args)

        _heartbeat = d.pop("heartbeat", UNSET)
        heartbeat: Union[Unset, None, WebsocketTriggerHeartbeat]
        if _heartbeat is None:
            heartbeat = None
        elif isinstance(_heartbeat, Unset):
            heartbeat = UNSET
        else:
            heartbeat = WebsocketTriggerHeartbeat.from_dict(_heartbeat)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, WebsocketTriggerErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = WebsocketTriggerErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, WebsocketTriggerRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = WebsocketTriggerRetry.from_dict(_retry)

        labels = cast(List[str], d.pop("labels", UNSET))

        websocket_trigger = cls(
            url=url,
            filters=filters,
            can_return_message=can_return_message,
            can_return_error_result=can_return_error_result,
            path=path,
            script_path=script_path,
            permissioned_as=permissioned_as,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            mode=mode,
            server_id=server_id,
            last_server_ping=last_server_ping,
            error=error,
            filter_logic=filter_logic,
            initial_messages=initial_messages,
            url_runnable_args=url_runnable_args,
            heartbeat=heartbeat,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            labels=labels,
        )

        websocket_trigger.additional_properties = d
        return websocket_trigger

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
