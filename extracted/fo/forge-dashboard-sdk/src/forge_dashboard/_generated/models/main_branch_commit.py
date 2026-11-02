from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="MainBranchCommit")



@_attrs_define
class MainBranchCommit:
    """ The newest commit on the default branch.

        Attributes:
            sha (str): The commit id, shortened to seven characters.
            subject (str): The first line of the commit message.
            author (str): The commit author's login where the forge knows it, else the name
                on the commit. Empty when the forge didn't say.
            committed_at (datetime.datetime | None): When the commit was made, or null when the forge didn't say.
     """

    sha: str
    subject: str
    author: str
    committed_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        sha = self.sha

        subject = self.subject

        author = self.author

        committed_at: None | str
        if isinstance(self.committed_at, datetime.datetime):
            committed_at = self.committed_at.isoformat()
        else:
            committed_at = self.committed_at


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "sha": sha,
            "subject": subject,
            "author": author,
            "committedAt": committed_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sha = d.pop("sha")

        subject = d.pop("subject")

        author = d.pop("author")

        def _parse_committed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                committed_at_type_0 = datetime.datetime.fromisoformat(data)



                return committed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        committed_at = _parse_committed_at(d.pop("committedAt"))


        main_branch_commit = cls(
            sha=sha,
            subject=subject,
            author=author,
            committed_at=committed_at,
        )


        main_branch_commit.additional_properties = d
        return main_branch_commit

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
