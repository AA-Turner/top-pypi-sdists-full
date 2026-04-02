from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="OrderConsumerInfoRequest")


@_attrs_define
class OrderConsumerInfoRequest:
    """
    Attributes:
        consumer_message (Union[Unset, str]):
        consumer_message_attachment (Union[Unset, File]):
    """

    consumer_message: Union[Unset, str] = UNSET
    consumer_message_attachment: Union[Unset, File] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        consumer_message = self.consumer_message

        consumer_message_attachment: Union[Unset, types.FileTypes] = UNSET
        if not isinstance(self.consumer_message_attachment, Unset):
            consumer_message_attachment = self.consumer_message_attachment.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if consumer_message is not UNSET:
            field_dict["consumer_message"] = consumer_message
        if consumer_message_attachment is not UNSET:
            field_dict["consumer_message_attachment"] = consumer_message_attachment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        consumer_message = d.pop("consumer_message", UNSET)

        _consumer_message_attachment = d.pop("consumer_message_attachment", UNSET)
        consumer_message_attachment: Union[Unset, File]
        if isinstance(_consumer_message_attachment, Unset):
            consumer_message_attachment = UNSET
        else:
            consumer_message_attachment = File(payload=BytesIO(_consumer_message_attachment))

        order_consumer_info_request = cls(
            consumer_message=consumer_message,
            consumer_message_attachment=consumer_message_attachment,
        )

        order_consumer_info_request.additional_properties = d
        return order_consumer_info_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
