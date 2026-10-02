from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_slack_channel import ManagedAgentsSlackChannel





T = TypeVar("T", bound="ManagedAgentsSlackChannels")



@_attrs_define
class ManagedAgentsSlackChannels:
    """ The channels a Slack connection's bot is a member of, read live from Slack with a short cache. Returned to populate
    the channel picker when creating or editing a Slack trigger binding; the binding itself still stores the channel id.

        Example:
            {'channels': [{'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'isExtShared': True, 'isPrivate': True, 'name':
                'example-name'}], 'fetchedAt': '2026-02-18T09:30:00Z', 'retryAfterSeconds': 1, 'stale': True, 'truncated': True}

        Attributes:
            channels (list[ManagedAgentsSlackChannel]): Bounded channel-selection catalog, sorted by name. A channel the bot
                has not been invited to is never listed; invite it in Slack first. Check truncated before treating absence as
                meaningful.
            fetched_at (datetime.datetime): When this list was read from Slack (RFC 3339). Lists are cached briefly, so a
                channel joined a moment ago may not appear yet.
            stale (bool): True when Slack could not be asked and an expired cached list was served instead. Check
                retryAfterSeconds before retrying.
            truncated (bool): True when the listing stopped at a size budget while Slack still had more channels; channels
                past the budget are absent, so a missing channel does not mean the bot is not a member.
            retry_after_seconds (int | Unset): How long to wait before asking again, when the list is stale because Slack
                throttled the read.
     """

    channels: list[ManagedAgentsSlackChannel]
    fetched_at: datetime.datetime
    stale: bool
    truncated: bool
    retry_after_seconds: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_slack_channel import ManagedAgentsSlackChannel # noqa: PLC0415
        channels = []
        for channels_item_data in self.channels:
            channels_item = channels_item_data.to_dict()
            channels.append(channels_item)



        fetched_at = self.fetched_at.isoformat()

        stale = self.stale

        truncated = self.truncated

        retry_after_seconds = self.retry_after_seconds


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "channels": channels,
            "fetchedAt": fetched_at,
            "stale": stale,
            "truncated": truncated,
        })
        if retry_after_seconds is not UNSET:
            field_dict["retryAfterSeconds"] = retry_after_seconds

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_slack_channel import ManagedAgentsSlackChannel # noqa: PLC0415
        d = dict(src_dict)
        channels = []
        _channels = d.pop("channels")
        for channels_item_data in (_channels):
            channels_item = ManagedAgentsSlackChannel.from_dict(channels_item_data)



            channels.append(channels_item)


        fetched_at = datetime.datetime.fromisoformat(d.pop("fetchedAt"))




        stale = d.pop("stale")

        truncated = d.pop("truncated")

        retry_after_seconds = d.pop("retryAfterSeconds", UNSET)

        managed_agents_slack_channels = cls(
            channels=channels,
            fetched_at=fetched_at,
            stale=stale,
            truncated=truncated,
            retry_after_seconds=retry_after_seconds,
        )


        managed_agents_slack_channels.additional_properties = d
        return managed_agents_slack_channels

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
