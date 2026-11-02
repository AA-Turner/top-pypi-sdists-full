from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.issue_details_state import IssueDetailsState
from typing import cast

if TYPE_CHECKING:
  from ..models.details_body import DetailsBody
  from ..models.details_comment import DetailsComment





T = TypeVar("T", bound="IssueDetails")



@_attrs_define
class IssueDetails:
    """ What the issue dialog shows.

        Attributes:
            state (IssueDetailsState): Whether the forge has the issue open or closed right now. The
                dialog draws its status from this, so an issue closed or reopened
                while the dialog is open shows the change.
            description (DetailsBody): A pull request's description, or the release notes of a release pull request.
            comments (list[DetailsComment]): The conversation, oldest first, at most the first 50.
            comment_count (int): How many comments the forge has on the issue.
            comments_truncated (bool): True when `commentCount` is more than the comments returned.
     """

    state: IssueDetailsState
    description: DetailsBody
    comments: list[DetailsComment]
    comment_count: int
    comments_truncated: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.details_body import DetailsBody # noqa: PLC0415
        from ..models.details_comment import DetailsComment # noqa: PLC0415
        state = self.state.value

        description = self.description.to_dict()

        comments = []
        for comments_item_data in self.comments:
            comments_item = comments_item_data.to_dict()
            comments.append(comments_item)



        comment_count = self.comment_count

        comments_truncated = self.comments_truncated


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "state": state,
            "description": description,
            "comments": comments,
            "commentCount": comment_count,
            "commentsTruncated": comments_truncated,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.details_body import DetailsBody # noqa: PLC0415
        from ..models.details_comment import DetailsComment # noqa: PLC0415
        d = dict(src_dict)
        state = IssueDetailsState(d.pop("state"))




        description = DetailsBody.from_dict(d.pop("description"))




        comments = []
        _comments = d.pop("comments")
        for comments_item_data in (_comments):
            comments_item = DetailsComment.from_dict(comments_item_data)



            comments.append(comments_item)


        comment_count = d.pop("commentCount")

        comments_truncated = d.pop("commentsTruncated")

        issue_details = cls(
            state=state,
            description=description,
            comments=comments,
            comment_count=comment_count,
            comments_truncated=comments_truncated,
        )


        issue_details.additional_properties = d
        return issue_details

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
