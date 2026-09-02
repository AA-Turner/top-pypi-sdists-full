import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_websocket_trigger_response_200_filter_logic import GetWebsocketTriggerResponse200FilterLogic
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_websocket_trigger_response_200_draft import GetWebsocketTriggerResponse200Draft
    from ..models.get_websocket_trigger_response_200_error_handler_args import (
        GetWebsocketTriggerResponse200ErrorHandlerArgs,
    )
    from ..models.get_websocket_trigger_response_200_heartbeat import GetWebsocketTriggerResponse200Heartbeat
    from ..models.get_websocket_trigger_response_200_initial_messages_item_type_0 import (
        GetWebsocketTriggerResponse200InitialMessagesItemType0,
    )
    from ..models.get_websocket_trigger_response_200_initial_messages_item_type_1 import (
        GetWebsocketTriggerResponse200InitialMessagesItemType1,
    )
    from ..models.get_websocket_trigger_response_200_other_drafts_users_item import (
        GetWebsocketTriggerResponse200OtherDraftsUsersItem,
    )
    from ..models.get_websocket_trigger_response_200_retry import GetWebsocketTriggerResponse200Retry
    from ..models.get_websocket_trigger_response_200_url_runnable_args import (
        GetWebsocketTriggerResponse200UrlRunnableArgs,
    )


T = TypeVar("T", bound="GetWebsocketTriggerResponse200")


@_attrs_define
class GetWebsocketTriggerResponse200:
    """
    Attributes:
        url (str): The WebSocket URL to connect to (can be a static URL or computed by a runnable)
        filters (List[Any]): Filters to match incoming messages (only matching messages trigger the script). Each entry
            is either a leaf `{key, value}` (top-level field) or `{path, value}` (dotted path into nested objects), or a
            group `{any_of: [...]}` / `{all_of: [...]}` / `{none_of: [...]}` nesting more entries. Entries at the top level
            are combined with `filter_logic`.
        can_return_message (bool): If true, the script can return a message to send back through the WebSocket
        can_return_error_result (bool): If true, error results are sent back through the WebSocket
        is_draft (bool):
        server_id (Union[Unset, str]): ID of the server currently handling this trigger (internal)
        last_server_ping (Union[Unset, datetime.datetime]): Timestamp of last server heartbeat (internal)
        error (Union[Unset, str]): Last error message if the trigger failed
        filter_logic (Union[Unset, GetWebsocketTriggerResponse200FilterLogic]): Logic to apply when evaluating the top-
            level filters. 'and' requires all of them to match, 'or' requires any of them to match. Nested
            `any_of`/`all_of`/`none_of` groups carry their own logic. Default:
            GetWebsocketTriggerResponse200FilterLogic.AND.
        initial_messages (Union[Unset, None, List[Union['GetWebsocketTriggerResponse200InitialMessagesItemType0',
            'GetWebsocketTriggerResponse200InitialMessagesItemType1']]]): Messages to send immediately after connecting (can
            be raw strings or computed by runnables)
        url_runnable_args (Union[Unset, None, GetWebsocketTriggerResponse200UrlRunnableArgs]): The arguments to pass to
            the script or flow
        heartbeat (Union[Unset, None, GetWebsocketTriggerResponse200Heartbeat]): Optional periodic heartbeat message
            configuration
        error_handler_path (Union[Unset, str]): Path to a script to run when the triggered job fails. A bare path,
            without the script/ or flow/ prefix a schedule error handler takes; it cannot be a flow.
        error_handler_args (Union[Unset, GetWebsocketTriggerResponse200ErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, GetWebsocketTriggerResponse200Retry]): Retry configuration for failed module executions
        draft_saved_at (Union[Unset, datetime.datetime]):
        no_deployed (Union[Unset, bool]):
        draft (Union[Unset, GetWebsocketTriggerResponse200Draft]):
        other_drafts_users (Union[Unset, List['GetWebsocketTriggerResponse200OtherDraftsUsersItem']]): Other workspace
            users (and the legacy NULL-email row, if any)
            with a saved draft at the same path. Populated only on the
            authed user's "get by path" responses for kinds the editor
            surfaces a fork banner for (script, flow, app, raw_app).
            Empty / omitted for kinds without that UI.
    """

    url: str
    filters: List[Any]
    can_return_message: bool
    can_return_error_result: bool
    is_draft: bool
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    filter_logic: Union[
        Unset, GetWebsocketTriggerResponse200FilterLogic
    ] = GetWebsocketTriggerResponse200FilterLogic.AND
    initial_messages: Union[
        Unset,
        None,
        List[
            Union[
                "GetWebsocketTriggerResponse200InitialMessagesItemType0",
                "GetWebsocketTriggerResponse200InitialMessagesItemType1",
            ]
        ],
    ] = UNSET
    url_runnable_args: Union[Unset, None, "GetWebsocketTriggerResponse200UrlRunnableArgs"] = UNSET
    heartbeat: Union[Unset, None, "GetWebsocketTriggerResponse200Heartbeat"] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "GetWebsocketTriggerResponse200ErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "GetWebsocketTriggerResponse200Retry"] = UNSET
    draft_saved_at: Union[Unset, datetime.datetime] = UNSET
    no_deployed: Union[Unset, bool] = UNSET
    draft: Union[Unset, "GetWebsocketTriggerResponse200Draft"] = UNSET
    other_drafts_users: Union[Unset, List["GetWebsocketTriggerResponse200OtherDraftsUsersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.get_websocket_trigger_response_200_initial_messages_item_type_0 import (
            GetWebsocketTriggerResponse200InitialMessagesItemType0,
        )

        url = self.url
        filters = self.filters

        can_return_message = self.can_return_message
        can_return_error_result = self.can_return_error_result
        is_draft = self.is_draft
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

                    if isinstance(initial_messages_item_data, GetWebsocketTriggerResponse200InitialMessagesItemType0):
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

        draft_saved_at: Union[Unset, str] = UNSET
        if not isinstance(self.draft_saved_at, Unset):
            draft_saved_at = self.draft_saved_at.isoformat()

        no_deployed = self.no_deployed
        draft: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.draft, Unset):
            draft = self.draft.to_dict()

        other_drafts_users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.other_drafts_users, Unset):
            other_drafts_users = []
            for other_drafts_users_item_data in self.other_drafts_users:
                other_drafts_users_item = other_drafts_users_item_data.to_dict()

                other_drafts_users.append(other_drafts_users_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "filters": filters,
                "can_return_message": can_return_message,
                "can_return_error_result": can_return_error_result,
                "is_draft": is_draft,
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
        if draft_saved_at is not UNSET:
            field_dict["draft_saved_at"] = draft_saved_at
        if no_deployed is not UNSET:
            field_dict["no_deployed"] = no_deployed
        if draft is not UNSET:
            field_dict["draft"] = draft
        if other_drafts_users is not UNSET:
            field_dict["other_drafts_users"] = other_drafts_users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_websocket_trigger_response_200_draft import GetWebsocketTriggerResponse200Draft
        from ..models.get_websocket_trigger_response_200_error_handler_args import (
            GetWebsocketTriggerResponse200ErrorHandlerArgs,
        )
        from ..models.get_websocket_trigger_response_200_heartbeat import GetWebsocketTriggerResponse200Heartbeat
        from ..models.get_websocket_trigger_response_200_initial_messages_item_type_0 import (
            GetWebsocketTriggerResponse200InitialMessagesItemType0,
        )
        from ..models.get_websocket_trigger_response_200_initial_messages_item_type_1 import (
            GetWebsocketTriggerResponse200InitialMessagesItemType1,
        )
        from ..models.get_websocket_trigger_response_200_other_drafts_users_item import (
            GetWebsocketTriggerResponse200OtherDraftsUsersItem,
        )
        from ..models.get_websocket_trigger_response_200_retry import GetWebsocketTriggerResponse200Retry
        from ..models.get_websocket_trigger_response_200_url_runnable_args import (
            GetWebsocketTriggerResponse200UrlRunnableArgs,
        )

        d = src_dict.copy()
        url = d.pop("url")

        filters = cast(List[Any], d.pop("filters"))

        can_return_message = d.pop("can_return_message")

        can_return_error_result = d.pop("can_return_error_result")

        is_draft = d.pop("is_draft")

        server_id = d.pop("server_id", UNSET)

        _last_server_ping = d.pop("last_server_ping", UNSET)
        last_server_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_server_ping, Unset):
            last_server_ping = UNSET
        else:
            last_server_ping = isoparse(_last_server_ping)

        error = d.pop("error", UNSET)

        _filter_logic = d.pop("filter_logic", UNSET)
        filter_logic: Union[Unset, GetWebsocketTriggerResponse200FilterLogic]
        if isinstance(_filter_logic, Unset):
            filter_logic = UNSET
        else:
            filter_logic = GetWebsocketTriggerResponse200FilterLogic(_filter_logic)

        initial_messages = []
        _initial_messages = d.pop("initial_messages", UNSET)
        for initial_messages_item_data in _initial_messages or []:

            def _parse_initial_messages_item(
                data: object,
            ) -> Union[
                "GetWebsocketTriggerResponse200InitialMessagesItemType0",
                "GetWebsocketTriggerResponse200InitialMessagesItemType1",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    initial_messages_item_type_0 = GetWebsocketTriggerResponse200InitialMessagesItemType0.from_dict(
                        data
                    )

                    return initial_messages_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                initial_messages_item_type_1 = GetWebsocketTriggerResponse200InitialMessagesItemType1.from_dict(data)

                return initial_messages_item_type_1

            initial_messages_item = _parse_initial_messages_item(initial_messages_item_data)

            initial_messages.append(initial_messages_item)

        _url_runnable_args = d.pop("url_runnable_args", UNSET)
        url_runnable_args: Union[Unset, None, GetWebsocketTriggerResponse200UrlRunnableArgs]
        if _url_runnable_args is None:
            url_runnable_args = None
        elif isinstance(_url_runnable_args, Unset):
            url_runnable_args = UNSET
        else:
            url_runnable_args = GetWebsocketTriggerResponse200UrlRunnableArgs.from_dict(_url_runnable_args)

        _heartbeat = d.pop("heartbeat", UNSET)
        heartbeat: Union[Unset, None, GetWebsocketTriggerResponse200Heartbeat]
        if _heartbeat is None:
            heartbeat = None
        elif isinstance(_heartbeat, Unset):
            heartbeat = UNSET
        else:
            heartbeat = GetWebsocketTriggerResponse200Heartbeat.from_dict(_heartbeat)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, GetWebsocketTriggerResponse200ErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = GetWebsocketTriggerResponse200ErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, GetWebsocketTriggerResponse200Retry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = GetWebsocketTriggerResponse200Retry.from_dict(_retry)

        _draft_saved_at = d.pop("draft_saved_at", UNSET)
        draft_saved_at: Union[Unset, datetime.datetime]
        if isinstance(_draft_saved_at, Unset):
            draft_saved_at = UNSET
        else:
            draft_saved_at = isoparse(_draft_saved_at)

        no_deployed = d.pop("no_deployed", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, GetWebsocketTriggerResponse200Draft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = GetWebsocketTriggerResponse200Draft.from_dict(_draft)

        other_drafts_users = []
        _other_drafts_users = d.pop("other_drafts_users", UNSET)
        for other_drafts_users_item_data in _other_drafts_users or []:
            other_drafts_users_item = GetWebsocketTriggerResponse200OtherDraftsUsersItem.from_dict(
                other_drafts_users_item_data
            )

            other_drafts_users.append(other_drafts_users_item)

        get_websocket_trigger_response_200 = cls(
            url=url,
            filters=filters,
            can_return_message=can_return_message,
            can_return_error_result=can_return_error_result,
            is_draft=is_draft,
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
            draft_saved_at=draft_saved_at,
            no_deployed=no_deployed,
            draft=draft,
            other_drafts_users=other_drafts_users,
        )

        get_websocket_trigger_response_200.additional_properties = d
        return get_websocket_trigger_response_200

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
