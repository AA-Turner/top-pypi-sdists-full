from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_slack_bot_events_mode import ManagedAgentsAutomationSlackBotEventsMode






T = TypeVar("T", bound="ManagedAgentsAutomationSlackBotEvents")



@_attrs_define
class ManagedAgentsAutomationSlackBotEvents:
    """ Trigger-local handling for messages authored by external Slack apps.

        Example:
            {'mode': 'ignore'}

        Attributes:
            mode (ManagedAgentsAutomationSlackBotEventsMode): Whether events authored by a provably different Slack app may
                match.
     """

    mode: ManagedAgentsAutomationSlackBotEventsMode





    def to_dict(self) -> dict[str, Any]:
        mode = self.mode.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "mode": mode,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = ManagedAgentsAutomationSlackBotEventsMode(d.pop("mode"))




        managed_agents_automation_slack_bot_events = cls(
            mode=mode,
        )

        return managed_agents_automation_slack_bot_events

