from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsAutomationSlackFilters")



@_attrs_define
class ManagedAgentsAutomationSlackFilters:
    """ Optional conditions on the Slack message text and threading.

        Example:
            {'ignoreThreadReplies': True, 'textContains': ['example'], 'textExcludes': ['example'], 'textMatches':
                'example'}

        Attributes:
            ignore_thread_replies (bool | Unset): Reject replies inside a thread; only top-level messages match.
            text_contains (list[str] | Unset): The message must contain at least one of these phrases, ignoring case.
            text_excludes (list[str] | Unset): The message must contain none of these phrases, ignoring case.
            text_matches (str | Unset): An RE2 regular expression the message must match, ignoring case.
     """

    ignore_thread_replies: bool | Unset = UNSET
    text_contains: list[str] | Unset = UNSET
    text_excludes: list[str] | Unset = UNSET
    text_matches: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        ignore_thread_replies = self.ignore_thread_replies

        text_contains: list[str] | Unset = UNSET
        if not isinstance(self.text_contains, Unset):
            text_contains = self.text_contains



        text_excludes: list[str] | Unset = UNSET
        if not isinstance(self.text_excludes, Unset):
            text_excludes = self.text_excludes



        text_matches = self.text_matches


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if ignore_thread_replies is not UNSET:
            field_dict["ignoreThreadReplies"] = ignore_thread_replies
        if text_contains is not UNSET:
            field_dict["textContains"] = text_contains
        if text_excludes is not UNSET:
            field_dict["textExcludes"] = text_excludes
        if text_matches is not UNSET:
            field_dict["textMatches"] = text_matches

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ignore_thread_replies = d.pop("ignoreThreadReplies", UNSET)

        text_contains = cast(list[str], d.pop("textContains", UNSET))


        text_excludes = cast(list[str], d.pop("textExcludes", UNSET))


        text_matches = d.pop("textMatches", UNSET)

        managed_agents_automation_slack_filters = cls(
            ignore_thread_replies=ignore_thread_replies,
            text_contains=text_contains,
            text_excludes=text_excludes,
            text_matches=text_matches,
        )

        return managed_agents_automation_slack_filters

