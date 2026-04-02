from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingUserStateTransitionRequest")


@_attrs_define
class OfferingUserStateTransitionRequest:
    """
    Attributes:
        comment (Union[Unset, str]): Comment explaining the state transition
        comment_url (Union[Unset, str]): URL reference related to the state transition comment
    """

    comment: Union[Unset, str] = UNSET
    comment_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        comment = self.comment

        comment_url = self.comment_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if comment is not UNSET:
            field_dict["comment"] = comment
        if comment_url is not UNSET:
            field_dict["comment_url"] = comment_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        comment = d.pop("comment", UNSET)

        comment_url = d.pop("comment_url", UNSET)

        offering_user_state_transition_request = cls(
            comment=comment,
            comment_url=comment_url,
        )

        offering_user_state_transition_request.additional_properties = d
        return offering_user_state_transition_request

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
