from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_websocket_trigger_filters_item import EditWebsocketTriggerFiltersItem
    from ..models.edit_websocket_trigger_initial_messages_item_type_0 import (
        EditWebsocketTriggerInitialMessagesItemType0,
    )
    from ..models.edit_websocket_trigger_initial_messages_item_type_1 import (
        EditWebsocketTriggerInitialMessagesItemType1,
    )
    from ..models.edit_websocket_trigger_url_runnable_args import EditWebsocketTriggerUrlRunnableArgs


T = TypeVar("T", bound="EditWebsocketTrigger")


@_attrs_define
class EditWebsocketTrigger:
    """
    Attributes:
        url (str):
        path (str):
        script_path (str):
        is_flow (bool):
        filters (List['EditWebsocketTriggerFiltersItem']):
        can_return_message (bool):
        initial_messages (Union[Unset, List[Union['EditWebsocketTriggerInitialMessagesItemType0',
            'EditWebsocketTriggerInitialMessagesItemType1']]]):
        url_runnable_args (Union[Unset, EditWebsocketTriggerUrlRunnableArgs]):
    """

    url: str
    path: str
    script_path: str
    is_flow: bool
    filters: List["EditWebsocketTriggerFiltersItem"]
    can_return_message: bool
    initial_messages: Union[
        Unset,
        List[Union["EditWebsocketTriggerInitialMessagesItemType0", "EditWebsocketTriggerInitialMessagesItemType1"]],
    ] = UNSET
    url_runnable_args: Union[Unset, "EditWebsocketTriggerUrlRunnableArgs"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.edit_websocket_trigger_initial_messages_item_type_0 import (
            EditWebsocketTriggerInitialMessagesItemType0,
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
        initial_messages: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.initial_messages, Unset):
            initial_messages = []
            for initial_messages_item_data in self.initial_messages:
                initial_messages_item: Dict[str, Any]

                if isinstance(initial_messages_item_data, EditWebsocketTriggerInitialMessagesItemType0):
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
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
                "filters": filters,
                "can_return_message": can_return_message,
            }
        )
        if initial_messages is not UNSET:
            field_dict["initial_messages"] = initial_messages
        if url_runnable_args is not UNSET:
            field_dict["url_runnable_args"] = url_runnable_args

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_websocket_trigger_filters_item import EditWebsocketTriggerFiltersItem
        from ..models.edit_websocket_trigger_initial_messages_item_type_0 import (
            EditWebsocketTriggerInitialMessagesItemType0,
        )
        from ..models.edit_websocket_trigger_initial_messages_item_type_1 import (
            EditWebsocketTriggerInitialMessagesItemType1,
        )
        from ..models.edit_websocket_trigger_url_runnable_args import EditWebsocketTriggerUrlRunnableArgs

        d = src_dict.copy()
        url = d.pop("url")

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = EditWebsocketTriggerFiltersItem.from_dict(filters_item_data)

            filters.append(filters_item)

        can_return_message = d.pop("can_return_message")

        initial_messages = []
        _initial_messages = d.pop("initial_messages", UNSET)
        for initial_messages_item_data in _initial_messages or []:

            def _parse_initial_messages_item(
                data: object,
            ) -> Union["EditWebsocketTriggerInitialMessagesItemType0", "EditWebsocketTriggerInitialMessagesItemType1"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    initial_messages_item_type_0 = EditWebsocketTriggerInitialMessagesItemType0.from_dict(data)

                    return initial_messages_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                initial_messages_item_type_1 = EditWebsocketTriggerInitialMessagesItemType1.from_dict(data)

                return initial_messages_item_type_1

            initial_messages_item = _parse_initial_messages_item(initial_messages_item_data)

            initial_messages.append(initial_messages_item)

        _url_runnable_args = d.pop("url_runnable_args", UNSET)
        url_runnable_args: Union[Unset, EditWebsocketTriggerUrlRunnableArgs]
        if isinstance(_url_runnable_args, Unset):
            url_runnable_args = UNSET
        else:
            url_runnable_args = EditWebsocketTriggerUrlRunnableArgs.from_dict(_url_runnable_args)

        edit_websocket_trigger = cls(
            url=url,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            filters=filters,
            can_return_message=can_return_message,
            initial_messages=initial_messages,
            url_runnable_args=url_runnable_args,
        )

        edit_websocket_trigger.additional_properties = d
        return edit_websocket_trigger

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
