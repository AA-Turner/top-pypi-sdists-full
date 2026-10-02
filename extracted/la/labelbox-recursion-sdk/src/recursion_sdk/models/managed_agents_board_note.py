from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsBoardNote")



@_attrs_define
class ManagedAgentsBoardNote:
    """ Prose attached to a board task by a member or by the harness: review verdicts, blockers, handover details. Notes are
    appended, never edited, so they read as the task's history.

        Example:
            {'at': '2026-02-18T09:30:00Z', 'by': 'example', 'text': 'example'}

        Attributes:
            at (datetime.datetime): When the note was added.
            by (str): Session id of the author, or "system" for a note the harness wrote (for example a released claim).
            text (str): The note's text. A reviewer's verdict on a proposal, a blocker, or a handover detail.
     """

    at: datetime.datetime
    by: str
    text: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        at = self.at.isoformat()

        by = self.by

        text = self.text


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "at": at,
            "by": by,
            "text": text,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        at = datetime.datetime.fromisoformat(d.pop("at"))




        by = d.pop("by")

        text = d.pop("text")

        managed_agents_board_note = cls(
            at=at,
            by=by,
            text=text,
        )


        managed_agents_board_note.additional_properties = d
        return managed_agents_board_note

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
