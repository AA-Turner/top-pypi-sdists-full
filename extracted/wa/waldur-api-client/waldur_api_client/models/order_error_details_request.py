from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderErrorDetailsRequest")


@_attrs_define
class OrderErrorDetailsRequest:
    """
    Attributes:
        error_message (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
        consumer_rejection_comment (Union[Unset, str]):
    """

    error_message: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    consumer_rejection_comment: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error_message = self.error_message

        error_traceback = self.error_traceback

        consumer_rejection_comment = self.consumer_rejection_comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback
        if consumer_rejection_comment is not UNSET:
            field_dict["consumer_rejection_comment"] = consumer_rejection_comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error_message = d.pop("error_message", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        consumer_rejection_comment = d.pop("consumer_rejection_comment", UNSET)

        order_error_details_request = cls(
            error_message=error_message,
            error_traceback=error_traceback,
            consumer_rejection_comment=consumer_rejection_comment,
        )

        order_error_details_request.additional_properties = d
        return order_error_details_request

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
