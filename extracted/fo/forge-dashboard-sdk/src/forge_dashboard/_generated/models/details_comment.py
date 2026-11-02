from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.details_comment_format import DetailsCommentFormat
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.person import Person
  from ..models.reactions import Reactions





T = TypeVar("T", bound="DetailsComment")



@_attrs_define
class DetailsComment:
    """ One comment on the pull request's conversation.

        Attributes:
            id (str): The forge's own identifier for the comment.
            author (None | Person): Null for a deleted account; a client shows it as "ghost".
            created_at (datetime.datetime):
            updated_at (datetime.datetime | None): When the comment was last edited, or null if it never was.
            edited (bool):
            text (str): Markdown, cut at 20,000 characters, not converted or sanitised.
            format_ (DetailsCommentFormat):
            truncated (bool):
            reactions (Reactions): The two reactions the dialog shows, `+1` and `-1` on both forges.
     """

    id: str
    author: None | Person
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    edited: bool
    text: str
    format_: DetailsCommentFormat
    truncated: bool
    reactions: Reactions
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.person import Person # noqa: PLC0415
        from ..models.reactions import Reactions # noqa: PLC0415
        id = self.id

        author: dict[str, Any] | None
        if isinstance(self.author, Person):
            author = self.author.to_dict()
        else:
            author = self.author

        created_at = self.created_at.isoformat()

        updated_at: None | str
        if isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        edited = self.edited

        text = self.text

        format_ = self.format_.value

        truncated = self.truncated

        reactions = self.reactions.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "author": author,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "edited": edited,
            "text": text,
            "format": format_,
            "truncated": truncated,
            "reactions": reactions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.person import Person # noqa: PLC0415
        from ..models.reactions import Reactions # noqa: PLC0415
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_author(data: object) -> None | Person:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                author_type_1 = Person.from_dict(data)



                return author_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Person, data)

        author = _parse_author(d.pop("author"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        def _parse_updated_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_1 = datetime.datetime.fromisoformat(data)



                return updated_at_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        updated_at = _parse_updated_at(d.pop("updatedAt"))


        edited = d.pop("edited")

        text = d.pop("text")

        format_ = DetailsCommentFormat(d.pop("format"))




        truncated = d.pop("truncated")

        reactions = Reactions.from_dict(d.pop("reactions"))




        details_comment = cls(
            id=id,
            author=author,
            created_at=created_at,
            updated_at=updated_at,
            edited=edited,
            text=text,
            format_=format_,
            truncated=truncated,
            reactions=reactions,
        )


        details_comment.additional_properties = d
        return details_comment

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
