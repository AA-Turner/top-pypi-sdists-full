from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.issue_details_kind import IssueDetailsKind
from ..models.issue_details_state import IssueDetailsState
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.details_body import DetailsBody
  from ..models.details_comment import DetailsComment
  from ..models.issue_pull_request import IssuePullRequest
  from ..models.item_reference import ItemReference





T = TypeVar("T", bound="IssueDetails")



@_attrs_define
class IssueDetails:
    """ What the issue dialog shows.

        Attributes:
            kind (IssueDetailsKind): What the number turned out to be. A forge shares one number space
                between issues and pull requests, so a bare number in a description
                can name either, and this endpoint answers for both. The
                client decides which dialog to open; a pull request's `state` is
                `closed` once it is merged as well as when it is closed unmerged.
            state (IssueDetailsState): Whether the forge has the issue open or closed right now. The
                dialog draws its status from this, so an issue closed or reopened
                while the dialog is open shows the change.
            description (DetailsBody): A pull request's description, or the release notes of a release pull request.
            comments (list[DetailsComment]): The conversation, oldest first, at most the first 50.
            comment_count (int): How many comments the forge has on the issue.
            comments_truncated (bool): True when `commentCount` is more than the comments returned.
            references (list[ItemReference]): The items that refer to this one, as the forge's own timeline
                records them, newest first, at most the first 50. They are read
                from the forge, so a closed or merged item shows them as well as an
                open one: the board's own pills list open pull requests only. An
                empty array means nothing refers to it. Only the entries whose
                `direction` is `incoming` are returned for now; `outgoing` is part
                of the contract so a later release can add what this item refers
                to without another change.
            pull_request (IssuePullRequest | Unset): Present only when `kind` is `pullRequest`: what the header of a pull
                request needs when the board has no row for it, because it is closed,
                merged or in a repository the board doesn't track. The dialog words it.
     """

    kind: IssueDetailsKind
    state: IssueDetailsState
    description: DetailsBody
    comments: list[DetailsComment]
    comment_count: int
    comments_truncated: bool
    references: list[ItemReference]
    pull_request: IssuePullRequest | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.details_body import DetailsBody # noqa: PLC0415
        from ..models.details_comment import DetailsComment # noqa: PLC0415
        from ..models.issue_pull_request import IssuePullRequest # noqa: PLC0415
        from ..models.item_reference import ItemReference # noqa: PLC0415
        kind = self.kind.value

        state = self.state.value

        description = self.description.to_dict()

        comments = []
        for comments_item_data in self.comments:
            comments_item = comments_item_data.to_dict()
            comments.append(comments_item)



        comment_count = self.comment_count

        comments_truncated = self.comments_truncated

        references = []
        for references_item_data in self.references:
            references_item = references_item_data.to_dict()
            references.append(references_item)



        pull_request: dict[str, Any] | Unset = UNSET
        if not isinstance(self.pull_request, Unset):
            pull_request = self.pull_request.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "kind": kind,
            "state": state,
            "description": description,
            "comments": comments,
            "commentCount": comment_count,
            "commentsTruncated": comments_truncated,
            "references": references,
        })
        if pull_request is not UNSET:
            field_dict["pullRequest"] = pull_request

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.details_body import DetailsBody # noqa: PLC0415
        from ..models.details_comment import DetailsComment # noqa: PLC0415
        from ..models.issue_pull_request import IssuePullRequest # noqa: PLC0415
        from ..models.item_reference import ItemReference # noqa: PLC0415
        d = dict(src_dict)
        kind = IssueDetailsKind(d.pop("kind"))




        state = IssueDetailsState(d.pop("state"))




        description = DetailsBody.from_dict(d.pop("description"))




        comments = []
        _comments = d.pop("comments")
        for comments_item_data in (_comments):
            comments_item = DetailsComment.from_dict(comments_item_data)



            comments.append(comments_item)


        comment_count = d.pop("commentCount")

        comments_truncated = d.pop("commentsTruncated")

        references = []
        _references = d.pop("references")
        for references_item_data in (_references):
            references_item = ItemReference.from_dict(references_item_data)



            references.append(references_item)


        _pull_request = d.pop("pullRequest", UNSET)
        pull_request: IssuePullRequest | Unset
        if isinstance(_pull_request,  Unset):
            pull_request = UNSET
        else:
            pull_request = IssuePullRequest.from_dict(_pull_request)




        issue_details = cls(
            kind=kind,
            state=state,
            description=description,
            comments=comments,
            comment_count=comment_count,
            comments_truncated=comments_truncated,
            references=references,
            pull_request=pull_request,
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
