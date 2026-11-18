from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.issue_pull_request_state import IssuePullRequestState
from typing import cast

if TYPE_CHECKING:
  from ..models.person import Person





T = TypeVar("T", bound="IssuePullRequest")



@_attrs_define
class IssuePullRequest:
    """ Present only when `kind` is `pullRequest`: what the header of a pull
    request needs when the board has no row for it, because it is closed,
    merged or in a repository the board doesn't track. The dialog words it.

        Attributes:
            title (str): The pull request's title, as the forge has it now.
            state (IssuePullRequestState): Where the pull request stands. `closed` means closed without merging.
            author (None | Person): Who opened it. Null for a deleted account.
     """

    title: str
    state: IssuePullRequestState
    author: None | Person
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.person import Person # noqa: PLC0415
        title = self.title

        state = self.state.value

        author: dict[str, Any] | None
        if isinstance(self.author, Person):
            author = self.author.to_dict()
        else:
            author = self.author


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "title": title,
            "state": state,
            "author": author,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.person import Person # noqa: PLC0415
        d = dict(src_dict)
        title = d.pop("title")

        state = IssuePullRequestState(d.pop("state"))




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


        issue_pull_request = cls(
            title=title,
            state=state,
            author=author,
        )


        issue_pull_request.additional_properties = d
        return issue_pull_request

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
