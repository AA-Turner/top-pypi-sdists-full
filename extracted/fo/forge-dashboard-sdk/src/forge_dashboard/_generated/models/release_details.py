from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.details_body import DetailsBody





T = TypeVar("T", bound="ReleaseDetails")



@_attrs_define
class ReleaseDetails:
    """ What the release dialog shows for a published release.

        Attributes:
            tag (str):
            name (str): The release's title. Empty when the forge has none, and then the tag is the title.
            url (str): The release's page on the forge.
            published_at (str): When it was published, RFC 3339. Always set, since a release with no publish date is a 404
                instead.
            notes (DetailsBody): A pull request's description, or the release notes of a release pull request.
     """

    tag: str
    name: str
    url: str
    published_at: str
    notes: DetailsBody
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.details_body import DetailsBody # noqa: PLC0415
        tag = self.tag

        name = self.name

        url = self.url

        published_at = self.published_at

        notes = self.notes.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "tag": tag,
            "name": name,
            "url": url,
            "publishedAt": published_at,
            "notes": notes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.details_body import DetailsBody # noqa: PLC0415
        d = dict(src_dict)
        tag = d.pop("tag")

        name = d.pop("name")

        url = d.pop("url")

        published_at = d.pop("publishedAt")

        notes = DetailsBody.from_dict(d.pop("notes"))




        release_details = cls(
            tag=tag,
            name=name,
            url=url,
            published_at=published_at,
            notes=notes,
        )


        release_details.additional_properties = d
        return release_details

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
