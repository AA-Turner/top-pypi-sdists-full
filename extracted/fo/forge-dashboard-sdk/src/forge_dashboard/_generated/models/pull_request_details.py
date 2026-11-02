from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.details_body import DetailsBody
  from ..models.details_comment import DetailsComment





T = TypeVar("T", bound="PullRequestDetails")



@_attrs_define
class PullRequestDetails:
    """ What the pull request dialog shows.

        Attributes:
            description (DetailsBody): A pull request's description, or the release notes of a release pull request.
            comments (list[DetailsComment]): The conversation, oldest first, at most the first 50.
            comment_count (int): How many comments the forge has on the pull request.
            comments_truncated (bool): True when `commentCount` is more than the comments returned.
            release_notes (DetailsBody | None): For a release pull request, the release notes it will publish (a
                release-please pull request's description is its changelog). Null
                for any other pull request, and for a release pull request this
                app can't identify. Never an empty string.
     """

    description: DetailsBody
    comments: list[DetailsComment]
    comment_count: int
    comments_truncated: bool
    release_notes: DetailsBody | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.details_body import DetailsBody # noqa: PLC0415
        from ..models.details_comment import DetailsComment # noqa: PLC0415
        description = self.description.to_dict()

        comments = []
        for comments_item_data in self.comments:
            comments_item = comments_item_data.to_dict()
            comments.append(comments_item)



        comment_count = self.comment_count

        comments_truncated = self.comments_truncated

        release_notes: dict[str, Any] | None
        if isinstance(self.release_notes, DetailsBody):
            release_notes = self.release_notes.to_dict()
        else:
            release_notes = self.release_notes


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "description": description,
            "comments": comments,
            "commentCount": comment_count,
            "commentsTruncated": comments_truncated,
            "releaseNotes": release_notes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.details_body import DetailsBody # noqa: PLC0415
        from ..models.details_comment import DetailsComment # noqa: PLC0415
        d = dict(src_dict)
        description = DetailsBody.from_dict(d.pop("description"))




        comments = []
        _comments = d.pop("comments")
        for comments_item_data in (_comments):
            comments_item = DetailsComment.from_dict(comments_item_data)



            comments.append(comments_item)


        comment_count = d.pop("commentCount")

        comments_truncated = d.pop("commentsTruncated")

        def _parse_release_notes(data: object) -> DetailsBody | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                release_notes_type_1 = DetailsBody.from_dict(data)



                return release_notes_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DetailsBody | None, data)

        release_notes = _parse_release_notes(d.pop("releaseNotes"))


        pull_request_details = cls(
            description=description,
            comments=comments,
            comment_count=comment_count,
            comments_truncated=comments_truncated,
            release_notes=release_notes,
        )


        pull_request_details.additional_properties = d
        return pull_request_details

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
