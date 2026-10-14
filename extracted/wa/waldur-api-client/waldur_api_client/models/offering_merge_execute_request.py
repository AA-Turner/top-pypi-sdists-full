from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingMergeExecuteRequest")


@_attrs_define
class OfferingMergeExecuteRequest:
    """
    Attributes:
        acknowledged_warnings (Union[Unset, list[str]]): Codes of every warning in the stored preview.
    """

    acknowledged_warnings: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        acknowledged_warnings: Union[Unset, list[str]] = UNSET
        if not isinstance(self.acknowledged_warnings, Unset):
            acknowledged_warnings = self.acknowledged_warnings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if acknowledged_warnings is not UNSET:
            field_dict["acknowledged_warnings"] = acknowledged_warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        acknowledged_warnings = cast(list[str], d.pop("acknowledged_warnings", UNSET))

        offering_merge_execute_request = cls(
            acknowledged_warnings=acknowledged_warnings,
        )

        offering_merge_execute_request.additional_properties = d
        return offering_merge_execute_request

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
