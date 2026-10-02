from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="IssueCommentPageDtoItemsItem")



@_attrs_define
class IssueCommentPageDtoItemsItem:
    """ A comment posted on an issue thread.

        Attributes:
            id (UUID): Stable issue-comment identifier (UUID).
            issue_id (UUID): Issue this comment belongs to.
            author_id (UUID): User who wrote the comment.
            content (str): Comment body, as authored.
            created_at (datetime.datetime): Timestamp when the comment was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the comment was last edited (ISO-8601, UTC).
     """

    id: UUID
    issue_id: UUID
    author_id: UUID
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        issue_id = str(self.issue_id)

        author_id = str(self.author_id)

        content = self.content

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "issueId": issue_id,
            "authorId": author_id,
            "content": content,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        issue_id = UUID(d.pop("issueId"))




        author_id = UUID(d.pop("authorId"))




        content = d.pop("content")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        issue_comment_page_dto_items_item = cls(
            id=id,
            issue_id=issue_id,
            author_id=author_id,
            content=content,
            created_at=created_at,
            updated_at=updated_at,
        )

        return issue_comment_page_dto_items_item

