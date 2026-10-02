from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="ManagedAgentsAutomationSlackRouting")



@_attrs_define
class ManagedAgentsAutomationSlackRouting:
    """ Workspace and channel routing constraints for a Slack trigger.

        Example:
            {'channelIds': ['example'], 'workspaceIds': ['example']}

        Attributes:
            channel_ids (list[str]): Slack channel ids accepted by this trigger; an empty list accepts every channel.
            workspace_ids (list[str]): Slack workspace ids accepted by this trigger; an empty list accepts every workspace
                received by the source.
     """

    channel_ids: list[str]
    workspace_ids: list[str]





    def to_dict(self) -> dict[str, Any]:
        channel_ids = self.channel_ids



        workspace_ids = self.workspace_ids




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "channelIds": channel_ids,
            "workspaceIds": workspace_ids,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        channel_ids = cast(list[str], d.pop("channelIds"))


        workspace_ids = cast(list[str], d.pop("workspaceIds"))


        managed_agents_automation_slack_routing = cls(
            channel_ids=channel_ids,
            workspace_ids=workspace_ids,
        )

        return managed_agents_automation_slack_routing

