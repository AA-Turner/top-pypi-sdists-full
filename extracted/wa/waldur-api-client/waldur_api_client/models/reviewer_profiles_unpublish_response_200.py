from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewerProfilesUnpublishResponse200")


@_attrs_define
class ReviewerProfilesUnpublishResponse200:
    """
    Attributes:
        is_published (Union[Unset, bool]):
        detail (Union[Unset, str]):
    """

    is_published: Union[Unset, bool] = UNSET
    detail: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_published = self.is_published

        detail = self.detail

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_published is not UNSET:
            field_dict["is_published"] = is_published
        if detail is not UNSET:
            field_dict["detail"] = detail

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_published = d.pop("is_published", UNSET)

        detail = d.pop("detail", UNSET)

        reviewer_profiles_unpublish_response_200 = cls(
            is_published=is_published,
            detail=detail,
        )

        reviewer_profiles_unpublish_response_200.additional_properties = d
        return reviewer_profiles_unpublish_response_200

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
