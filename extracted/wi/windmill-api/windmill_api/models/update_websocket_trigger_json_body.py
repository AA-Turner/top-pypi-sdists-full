from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_websocket_trigger_json_body_filter_logic import UpdateWebsocketTriggerJsonBodyFilterLogic
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_websocket_trigger_json_body_error_handler_args import (
        UpdateWebsocketTriggerJsonBodyErrorHandlerArgs,
    )
    from ..models.update_websocket_trigger_json_body_filters_item import UpdateWebsocketTriggerJsonBodyFiltersItem
    from ..models.update_websocket_trigger_json_body_heartbeat import UpdateWebsocketTriggerJsonBodyHeartbeat
    from ..models.update_websocket_trigger_json_body_initial_messages_item_type_0 import (
        UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0,
    )
    from ..models.update_websocket_trigger_json_body_initial_messages_item_type_1 import (
        UpdateWebsocketTriggerJsonBodyInitialMessagesItemType1,
    )
    from ..models.update_websocket_trigger_json_body_retry import UpdateWebsocketTriggerJsonBodyRetry
    from ..models.update_websocket_trigger_json_body_url_runnable_args import (
        UpdateWebsocketTriggerJsonBodyUrlRunnableArgs,
    )


T = TypeVar("T", bound="UpdateWebsocketTriggerJsonBody")


@_attrs_define
class UpdateWebsocketTriggerJsonBody:
    """
    Attributes:
        url (str): The WebSocket URL to connect to (can be a static URL or computed by a runnable)
        path (str): The unique Windmill path for this trigger. Must be of the form `u/<user>/<path>` or
            `f/<folder>/<path>`. This is the trigger object path, not the HTTP route path.
        script_path (str): Path to the script or flow to execute when a message is received
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        filters (List['UpdateWebsocketTriggerJsonBodyFiltersItem']): Array of key-value filters to match incoming
            messages (only matching messages trigger the script)
        can_return_message (bool): If true, the script can return a message to send back through the WebSocket
        can_return_error_result (bool): If true, error results are sent back through the WebSocket
        filter_logic (Union[Unset, UpdateWebsocketTriggerJsonBodyFilterLogic]): Logic to apply when evaluating filters.
            'and' requires all filters to match, 'or' requires any filter to match. Default:
            UpdateWebsocketTriggerJsonBodyFilterLogic.AND.
        initial_messages (Union[Unset, None, List[Union['UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0',
            'UpdateWebsocketTriggerJsonBodyInitialMessagesItemType1']]]): Messages to send immediately after connecting (can
            be raw strings or computed by runnables)
        url_runnable_args (Union[Unset, None, UpdateWebsocketTriggerJsonBodyUrlRunnableArgs]): The arguments to pass to
            the script or flow
        heartbeat (Union[Unset, None, UpdateWebsocketTriggerJsonBodyHeartbeat]): Optional periodic heartbeat message
            configuration
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails
        error_handler_args (Union[Unset, UpdateWebsocketTriggerJsonBodyErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, UpdateWebsocketTriggerJsonBodyRetry]): Retry configuration for failed module executions
        permissioned_as (Union[Unset, str]): The user or group this trigger runs as. Used during deployment to preserve
            the original trigger owner.
        preserve_permissioned_as (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group,
            preserves the original permissioned_as value instead of overwriting it.
        labels (Union[Unset, List[str]]):
    """

    url: str
    path: str
    script_path: str
    is_flow: bool
    filters: List["UpdateWebsocketTriggerJsonBodyFiltersItem"]
    can_return_message: bool
    can_return_error_result: bool
    filter_logic: Union[
        Unset, UpdateWebsocketTriggerJsonBodyFilterLogic
    ] = UpdateWebsocketTriggerJsonBodyFilterLogic.AND
    initial_messages: Union[
        Unset,
        None,
        List[
            Union[
                "UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0",
                "UpdateWebsocketTriggerJsonBodyInitialMessagesItemType1",
            ]
        ],
    ] = UNSET
    url_runnable_args: Union[Unset, None, "UpdateWebsocketTriggerJsonBodyUrlRunnableArgs"] = UNSET
    heartbeat: Union[Unset, None, "UpdateWebsocketTriggerJsonBodyHeartbeat"] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "UpdateWebsocketTriggerJsonBodyErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "UpdateWebsocketTriggerJsonBodyRetry"] = UNSET
    permissioned_as: Union[Unset, str] = UNSET
    preserve_permissioned_as: Union[Unset, bool] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.update_websocket_trigger_json_body_initial_messages_item_type_0 import (
            UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0,
        )

        url = self.url
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()

            filters.append(filters_item)

        can_return_message = self.can_return_message
        can_return_error_result = self.can_return_error_result
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

                    if isinstance(initial_messages_item_data, UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0):
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

        permissioned_as = self.permissioned_as
        preserve_permissioned_as = self.preserve_permissioned_as
        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
                "filters": filters,
                "can_return_message": can_return_message,
                "can_return_error_result": can_return_error_result,
            }
        )
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
        if permissioned_as is not UNSET:
            field_dict["permissioned_as"] = permissioned_as
        if preserve_permissioned_as is not UNSET:
            field_dict["preserve_permissioned_as"] = preserve_permissioned_as
        if labels is not UNSET:
            field_dict["labels"] = labels

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_websocket_trigger_json_body_error_handler_args import (
            UpdateWebsocketTriggerJsonBodyErrorHandlerArgs,
        )
        from ..models.update_websocket_trigger_json_body_filters_item import UpdateWebsocketTriggerJsonBodyFiltersItem
        from ..models.update_websocket_trigger_json_body_heartbeat import UpdateWebsocketTriggerJsonBodyHeartbeat
        from ..models.update_websocket_trigger_json_body_initial_messages_item_type_0 import (
            UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0,
        )
        from ..models.update_websocket_trigger_json_body_initial_messages_item_type_1 import (
            UpdateWebsocketTriggerJsonBodyInitialMessagesItemType1,
        )
        from ..models.update_websocket_trigger_json_body_retry import UpdateWebsocketTriggerJsonBodyRetry
        from ..models.update_websocket_trigger_json_body_url_runnable_args import (
            UpdateWebsocketTriggerJsonBodyUrlRunnableArgs,
        )

        d = src_dict.copy()
        url = d.pop("url")

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = UpdateWebsocketTriggerJsonBodyFiltersItem.from_dict(filters_item_data)

            filters.append(filters_item)

        can_return_message = d.pop("can_return_message")

        can_return_error_result = d.pop("can_return_error_result")

        _filter_logic = d.pop("filter_logic", UNSET)
        filter_logic: Union[Unset, UpdateWebsocketTriggerJsonBodyFilterLogic]
        if isinstance(_filter_logic, Unset):
            filter_logic = UNSET
        else:
            filter_logic = UpdateWebsocketTriggerJsonBodyFilterLogic(_filter_logic)

        initial_messages = []
        _initial_messages = d.pop("initial_messages", UNSET)
        for initial_messages_item_data in _initial_messages or []:

            def _parse_initial_messages_item(
                data: object,
            ) -> Union[
                "UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0",
                "UpdateWebsocketTriggerJsonBodyInitialMessagesItemType1",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    initial_messages_item_type_0 = UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0.from_dict(
                        data
                    )

                    return initial_messages_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                initial_messages_item_type_1 = UpdateWebsocketTriggerJsonBodyInitialMessagesItemType1.from_dict(data)

                return initial_messages_item_type_1

            initial_messages_item = _parse_initial_messages_item(initial_messages_item_data)

            initial_messages.append(initial_messages_item)

        _url_runnable_args = d.pop("url_runnable_args", UNSET)
        url_runnable_args: Union[Unset, None, UpdateWebsocketTriggerJsonBodyUrlRunnableArgs]
        if _url_runnable_args is None:
            url_runnable_args = None
        elif isinstance(_url_runnable_args, Unset):
            url_runnable_args = UNSET
        else:
            url_runnable_args = UpdateWebsocketTriggerJsonBodyUrlRunnableArgs.from_dict(_url_runnable_args)

        _heartbeat = d.pop("heartbeat", UNSET)
        heartbeat: Union[Unset, None, UpdateWebsocketTriggerJsonBodyHeartbeat]
        if _heartbeat is None:
            heartbeat = None
        elif isinstance(_heartbeat, Unset):
            heartbeat = UNSET
        else:
            heartbeat = UpdateWebsocketTriggerJsonBodyHeartbeat.from_dict(_heartbeat)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, UpdateWebsocketTriggerJsonBodyErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = UpdateWebsocketTriggerJsonBodyErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, UpdateWebsocketTriggerJsonBodyRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = UpdateWebsocketTriggerJsonBodyRetry.from_dict(_retry)

        permissioned_as = d.pop("permissioned_as", UNSET)

        preserve_permissioned_as = d.pop("preserve_permissioned_as", UNSET)

        labels = cast(List[str], d.pop("labels", UNSET))

        update_websocket_trigger_json_body = cls(
            url=url,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            filters=filters,
            can_return_message=can_return_message,
            can_return_error_result=can_return_error_result,
            filter_logic=filter_logic,
            initial_messages=initial_messages,
            url_runnable_args=url_runnable_args,
            heartbeat=heartbeat,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            permissioned_as=permissioned_as,
            preserve_permissioned_as=preserve_permissioned_as,
            labels=labels,
        )

        update_websocket_trigger_json_body.additional_properties = d
        return update_websocket_trigger_json_body

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
