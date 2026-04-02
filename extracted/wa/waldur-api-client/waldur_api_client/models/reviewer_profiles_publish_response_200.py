import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewerProfilesPublishResponse200")


@_attrs_define
class ReviewerProfilesPublishResponse200:
    """
    Attributes:
        is_published (Union[Unset, bool]):
        published_at (Union[Unset, datetime.datetime]):
        warning (Union[Unset, str]):
    """

    is_published: Union[Unset, bool] = UNSET
    published_at: Union[Unset, datetime.datetime] = UNSET
    warning: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_published = self.is_published

        published_at: Union[Unset, str] = UNSET
        if not isinstance(self.published_at, Unset):
            published_at = self.published_at.isoformat()

        warning = self.warning

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_published is not UNSET:
            field_dict["is_published"] = is_published
        if published_at is not UNSET:
            field_dict["published_at"] = published_at
        if warning is not UNSET:
            field_dict["warning"] = warning

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_published = d.pop("is_published", UNSET)

        _published_at = d.pop("published_at", UNSET)
        published_at: Union[Unset, datetime.datetime]
        if isinstance(_published_at, Unset):
            published_at = UNSET
        else:
            published_at = isoparse(_published_at)

        warning = d.pop("warning", UNSET)

        reviewer_profiles_publish_response_200 = cls(
            is_published=is_published,
            published_at=published_at,
            warning=warning,
        )

        reviewer_profiles_publish_response_200.additional_properties = d
        return reviewer_profiles_publish_response_200

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
