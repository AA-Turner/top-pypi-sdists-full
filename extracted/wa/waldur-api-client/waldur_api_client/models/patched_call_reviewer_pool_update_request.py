from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedCallReviewerPoolUpdateRequest")


@_attrs_define
class PatchedCallReviewerPoolUpdateRequest:
    """
    Attributes:
        max_assignments (Union[Unset, int]): Maximum number of proposals that can be assigned to this reviewer
    """

    max_assignments: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_assignments = self.max_assignments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_assignments is not UNSET:
            field_dict["max_assignments"] = max_assignments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_assignments = d.pop("max_assignments", UNSET)

        patched_call_reviewer_pool_update_request = cls(
            max_assignments=max_assignments,
        )

        patched_call_reviewer_pool_update_request.additional_properties = d
        return patched_call_reviewer_pool_update_request

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
