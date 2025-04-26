from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.new_websocket_trigger_initial_messages_item_type_1_runnable_result_args import (
        NewWebsocketTriggerInitialMessagesItemType1RunnableResultArgs,
    )


T = TypeVar("T", bound="NewWebsocketTriggerInitialMessagesItemType1RunnableResult")


@_attrs_define
class NewWebsocketTriggerInitialMessagesItemType1RunnableResult:
    """
    Attributes:
        path (str):
        args (NewWebsocketTriggerInitialMessagesItemType1RunnableResultArgs):
        is_flow (bool):
    """

    path: str
    args: "NewWebsocketTriggerInitialMessagesItemType1RunnableResultArgs"
    is_flow: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        args = self.args.to_dict()

        is_flow = self.is_flow

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "args": args,
                "is_flow": is_flow,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_websocket_trigger_initial_messages_item_type_1_runnable_result_args import (
            NewWebsocketTriggerInitialMessagesItemType1RunnableResultArgs,
        )

        d = src_dict.copy()
        path = d.pop("path")

        args = NewWebsocketTriggerInitialMessagesItemType1RunnableResultArgs.from_dict(d.pop("args"))

        is_flow = d.pop("is_flow")

        new_websocket_trigger_initial_messages_item_type_1_runnable_result = cls(
            path=path,
            args=args,
            is_flow=is_flow,
        )

        new_websocket_trigger_initial_messages_item_type_1_runnable_result.additional_properties = d
        return new_websocket_trigger_initial_messages_item_type_1_runnable_result

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
