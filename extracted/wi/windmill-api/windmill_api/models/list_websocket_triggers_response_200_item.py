import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_websocket_triggers_response_200_item_extra_perms import (
        ListWebsocketTriggersResponse200ItemExtraPerms,
    )
    from ..models.list_websocket_triggers_response_200_item_filters_item import (
        ListWebsocketTriggersResponse200ItemFiltersItem,
    )
    from ..models.list_websocket_triggers_response_200_item_initial_messages_item_type_0 import (
        ListWebsocketTriggersResponse200ItemInitialMessagesItemType0,
    )
    from ..models.list_websocket_triggers_response_200_item_initial_messages_item_type_1 import (
        ListWebsocketTriggersResponse200ItemInitialMessagesItemType1,
    )
    from ..models.list_websocket_triggers_response_200_item_url_runnable_args import (
        ListWebsocketTriggersResponse200ItemUrlRunnableArgs,
    )


T = TypeVar("T", bound="ListWebsocketTriggersResponse200Item")


@_attrs_define
class ListWebsocketTriggersResponse200Item:
    """
    Attributes:
        url (str):
        enabled (bool):
        filters (List['ListWebsocketTriggersResponse200ItemFiltersItem']):
        can_return_message (bool):
        path (str):
        script_path (str):
        email (str):
        extra_perms (ListWebsocketTriggersResponse200ItemExtraPerms):
        workspace_id (str):
        edited_by (str):
        edited_at (datetime.datetime):
        is_flow (bool):
        server_id (Union[Unset, str]):
        last_server_ping (Union[Unset, datetime.datetime]):
        error (Union[Unset, str]):
        initial_messages (Union[Unset, List[Union['ListWebsocketTriggersResponse200ItemInitialMessagesItemType0',
            'ListWebsocketTriggersResponse200ItemInitialMessagesItemType1']]]):
        url_runnable_args (Union[Unset, ListWebsocketTriggersResponse200ItemUrlRunnableArgs]):
    """

    url: str
    enabled: bool
    filters: List["ListWebsocketTriggersResponse200ItemFiltersItem"]
    can_return_message: bool
    path: str
    script_path: str
    email: str
    extra_perms: "ListWebsocketTriggersResponse200ItemExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    initial_messages: Union[
        Unset,
        List[
            Union[
                "ListWebsocketTriggersResponse200ItemInitialMessagesItemType0",
                "ListWebsocketTriggersResponse200ItemInitialMessagesItemType1",
            ]
        ],
    ] = UNSET
    url_runnable_args: Union[Unset, "ListWebsocketTriggersResponse200ItemUrlRunnableArgs"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_websocket_triggers_response_200_item_initial_messages_item_type_0 import (
            ListWebsocketTriggersResponse200ItemInitialMessagesItemType0,
        )

        url = self.url
        enabled = self.enabled
        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()

            filters.append(filters_item)

        can_return_message = self.can_return_message
        path = self.path
        script_path = self.script_path
        email = self.email
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
        server_id = self.server_id
        last_server_ping: Union[Unset, str] = UNSET
        if not isinstance(self.last_server_ping, Unset):
            last_server_ping = self.last_server_ping.isoformat()

        error = self.error
        initial_messages: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.initial_messages, Unset):
            initial_messages = []
            for initial_messages_item_data in self.initial_messages:
                initial_messages_item: Dict[str, Any]

                if isinstance(initial_messages_item_data, ListWebsocketTriggersResponse200ItemInitialMessagesItemType0):
                    initial_messages_item = initial_messages_item_data.to_dict()

                else:
                    initial_messages_item = initial_messages_item_data.to_dict()

                initial_messages.append(initial_messages_item)

        url_runnable_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.url_runnable_args, Unset):
            url_runnable_args = self.url_runnable_args.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "enabled": enabled,
                "filters": filters,
                "can_return_message": can_return_message,
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
        if server_id is not UNSET:
            field_dict["server_id"] = server_id
        if last_server_ping is not UNSET:
            field_dict["last_server_ping"] = last_server_ping
        if error is not UNSET:
            field_dict["error"] = error
        if initial_messages is not UNSET:
            field_dict["initial_messages"] = initial_messages
        if url_runnable_args is not UNSET:
            field_dict["url_runnable_args"] = url_runnable_args

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_websocket_triggers_response_200_item_extra_perms import (
            ListWebsocketTriggersResponse200ItemExtraPerms,
        )
        from ..models.list_websocket_triggers_response_200_item_filters_item import (
            ListWebsocketTriggersResponse200ItemFiltersItem,
        )
        from ..models.list_websocket_triggers_response_200_item_initial_messages_item_type_0 import (
            ListWebsocketTriggersResponse200ItemInitialMessagesItemType0,
        )
        from ..models.list_websocket_triggers_response_200_item_initial_messages_item_type_1 import (
            ListWebsocketTriggersResponse200ItemInitialMessagesItemType1,
        )
        from ..models.list_websocket_triggers_response_200_item_url_runnable_args import (
            ListWebsocketTriggersResponse200ItemUrlRunnableArgs,
        )

        d = src_dict.copy()
        url = d.pop("url")

        enabled = d.pop("enabled")

        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = ListWebsocketTriggersResponse200ItemFiltersItem.from_dict(filters_item_data)

            filters.append(filters_item)

        can_return_message = d.pop("can_return_message")

        path = d.pop("path")

        script_path = d.pop("script_path")

        email = d.pop("email")

        extra_perms = ListWebsocketTriggersResponse200ItemExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        server_id = d.pop("server_id", UNSET)

        _last_server_ping = d.pop("last_server_ping", UNSET)
        last_server_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_server_ping, Unset):
            last_server_ping = UNSET
        else:
            last_server_ping = isoparse(_last_server_ping)

        error = d.pop("error", UNSET)

        initial_messages = []
        _initial_messages = d.pop("initial_messages", UNSET)
        for initial_messages_item_data in _initial_messages or []:

            def _parse_initial_messages_item(
                data: object,
            ) -> Union[
                "ListWebsocketTriggersResponse200ItemInitialMessagesItemType0",
                "ListWebsocketTriggersResponse200ItemInitialMessagesItemType1",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    initial_messages_item_type_0 = (
                        ListWebsocketTriggersResponse200ItemInitialMessagesItemType0.from_dict(data)
                    )

                    return initial_messages_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                initial_messages_item_type_1 = ListWebsocketTriggersResponse200ItemInitialMessagesItemType1.from_dict(
                    data
                )

                return initial_messages_item_type_1

            initial_messages_item = _parse_initial_messages_item(initial_messages_item_data)

            initial_messages.append(initial_messages_item)

        _url_runnable_args = d.pop("url_runnable_args", UNSET)
        url_runnable_args: Union[Unset, ListWebsocketTriggersResponse200ItemUrlRunnableArgs]
        if isinstance(_url_runnable_args, Unset):
            url_runnable_args = UNSET
        else:
            url_runnable_args = ListWebsocketTriggersResponse200ItemUrlRunnableArgs.from_dict(_url_runnable_args)

        list_websocket_triggers_response_200_item = cls(
            url=url,
            enabled=enabled,
            filters=filters,
            can_return_message=can_return_message,
            path=path,
            script_path=script_path,
            email=email,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            server_id=server_id,
            last_server_ping=last_server_ping,
            error=error,
            initial_messages=initial_messages,
            url_runnable_args=url_runnable_args,
        )

        list_websocket_triggers_response_200_item.additional_properties = d
        return list_websocket_triggers_response_200_item

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
