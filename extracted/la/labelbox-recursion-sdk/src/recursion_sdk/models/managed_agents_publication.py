from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsPublication")



@_attrs_define
class ManagedAgentsPublication:
    """ The GitHub-side outcome of one repository automation. Publication is idempotent: a retry finds the review this
    session already posted and returns it rather than duplicating comments.

        Example:
            {'published': True, 'review_id': 1, 'url': 'https://example.com'}

        Attributes:
            published (bool): Whether a GitHub review was posted. False when the run's output policy disabled publication.
            review_id (int | Unset): GitHub pull request review id. Present only when published is true.
            url (str | Unset): Web URL of the published GitHub review. Present only when published is true.
     """

    published: bool
    review_id: int | Unset = UNSET
    url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        published = self.published

        review_id = self.review_id

        url = self.url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "published": published,
        })
        if review_id is not UNSET:
            field_dict["review_id"] = review_id
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        published = d.pop("published")

        review_id = d.pop("review_id", UNSET)

        url = d.pop("url", UNSET)

        managed_agents_publication = cls(
            published=published,
            review_id=review_id,
            url=url,
        )


        managed_agents_publication.additional_properties = d
        return managed_agents_publication

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
