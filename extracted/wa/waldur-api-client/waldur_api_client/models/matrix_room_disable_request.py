from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MatrixRoomDisableRequest")


@_attrs_define
class MatrixRoomDisableRequest:
    """
    Attributes:
        delete_history (Union[Unset, bool]):  Default: False.
    """

    delete_history: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        delete_history = self.delete_history

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if delete_history is not UNSET:
            field_dict["delete_history"] = delete_history

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        delete_history = d.pop("delete_history", UNSET)

        matrix_room_disable_request = cls(
            delete_history=delete_history,
        )

        matrix_room_disable_request.additional_properties = d
        return matrix_room_disable_request

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
