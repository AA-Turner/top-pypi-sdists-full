from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedAssignmentItemRequest")


@_attrs_define
class PatchedAssignmentItemRequest:
    """
    Attributes:
        decline_reason (Union[Unset, str]): Reason provided by reviewer for declining.
    """

    decline_reason: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        decline_reason = self.decline_reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if decline_reason is not UNSET:
            field_dict["decline_reason"] = decline_reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        decline_reason = d.pop("decline_reason", UNSET)

        patched_assignment_item_request = cls(
            decline_reason=decline_reason,
        )

        patched_assignment_item_request.additional_properties = d
        return patched_assignment_item_request

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
