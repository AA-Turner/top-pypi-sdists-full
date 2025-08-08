from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_websocket_connection_json_body_url_runnable_args import (
        TestWebsocketConnectionJsonBodyUrlRunnableArgs,
    )


T = TypeVar("T", bound="TestWebsocketConnectionJsonBody")


@_attrs_define
class TestWebsocketConnectionJsonBody:
    """
    Attributes:
        url (str):
        can_return_message (bool):
        url_runnable_args (Union[Unset, TestWebsocketConnectionJsonBodyUrlRunnableArgs]): The arguments to pass to the
            script or flow
    """

    url: str
    can_return_message: bool
    url_runnable_args: Union[Unset, "TestWebsocketConnectionJsonBodyUrlRunnableArgs"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        can_return_message = self.can_return_message
        url_runnable_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.url_runnable_args, Unset):
            url_runnable_args = self.url_runnable_args.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "can_return_message": can_return_message,
            }
        )
        if url_runnable_args is not UNSET:
            field_dict["url_runnable_args"] = url_runnable_args

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_websocket_connection_json_body_url_runnable_args import (
            TestWebsocketConnectionJsonBodyUrlRunnableArgs,
        )

        d = src_dict.copy()
        url = d.pop("url")

        can_return_message = d.pop("can_return_message")

        _url_runnable_args = d.pop("url_runnable_args", UNSET)
        url_runnable_args: Union[Unset, TestWebsocketConnectionJsonBodyUrlRunnableArgs]
        if isinstance(_url_runnable_args, Unset):
            url_runnable_args = UNSET
        else:
            url_runnable_args = TestWebsocketConnectionJsonBodyUrlRunnableArgs.from_dict(_url_runnable_args)

        test_websocket_connection_json_body = cls(
            url=url,
            can_return_message=can_return_message,
            url_runnable_args=url_runnable_args,
        )

        test_websocket_connection_json_body.additional_properties = d
        return test_websocket_connection_json_body

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
