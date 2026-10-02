from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_slack_trigger_request_events_item import ManagedAgentsAutomationSlackTriggerRequestEventsItem
from ..models.managed_agents_automation_slack_trigger_request_type import ManagedAgentsAutomationSlackTriggerRequestType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.managed_agents_automation_slack_bot_events import ManagedAgentsAutomationSlackBotEvents
  from ..models.managed_agents_automation_slack_filters_request import ManagedAgentsAutomationSlackFiltersRequest
  from ..models.managed_agents_automation_slack_routing import ManagedAgentsAutomationSlackRouting





T = TypeVar("T", bound="ManagedAgentsAutomationSlackTriggerRequest")



@_attrs_define
class ManagedAgentsAutomationSlackTriggerRequest:
    """ Closed Slack Events API trigger configuration.

        Example:
            {'allowSharedChannels': True, 'botEvents': {'mode': 'ignore'}, 'enabled': True, 'eventSourceId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'events': ['message'], 'filters': {'ignoreThreadReplies': True,
                'textContains': ['example'], 'textExcludes': ['example'], 'textMatches': 'example'}, 'routing': {'channelIds':
                ['example'], 'workspaceIds': ['example']}, 'triggerId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'slack'}

        Attributes:
            bot_events (ManagedAgentsAutomationSlackBotEvents): Trigger-local handling for messages authored by external
                Slack apps. Example: {'mode': 'ignore'}.
            enabled (bool): Whether this trigger may admit runs while the automation is active.
            event_source_id (UUID): Compatible Slack Events API source.
            events (list[ManagedAgentsAutomationSlackTriggerRequestEventsItem]): Slack event types that may match this
                trigger.
            routing (ManagedAgentsAutomationSlackRouting): Workspace and channel routing constraints for a Slack trigger.
                Example: {'channelIds': ['example'], 'workspaceIds': ['example']}.
            trigger_id (UUID): Caller-generated stable trigger identifier.
            type_ (ManagedAgentsAutomationSlackTriggerRequestType): Slack trigger discriminant.
            allow_shared_channels (bool | Unset): Explicitly allow events from Slack Connect channels shared with other
                organizations. Defaults to false. Default: False.
            filters (ManagedAgentsAutomationSlackFiltersRequest | Unset): Optional conditions on the Slack message text and
                threading. Example: {'ignoreThreadReplies': True, 'textContains': ['example'], 'textExcludes': ['example'],
                'textMatches': 'example'}.
     """

    bot_events: ManagedAgentsAutomationSlackBotEvents
    enabled: bool
    event_source_id: UUID
    events: list[ManagedAgentsAutomationSlackTriggerRequestEventsItem]
    routing: ManagedAgentsAutomationSlackRouting
    trigger_id: UUID
    type_: ManagedAgentsAutomationSlackTriggerRequestType
    allow_shared_channels: bool | Unset = False
    filters: ManagedAgentsAutomationSlackFiltersRequest | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_slack_bot_events import ManagedAgentsAutomationSlackBotEvents # noqa: PLC0415
        from ..models.managed_agents_automation_slack_filters_request import ManagedAgentsAutomationSlackFiltersRequest # noqa: PLC0415
        from ..models.managed_agents_automation_slack_routing import ManagedAgentsAutomationSlackRouting # noqa: PLC0415
        bot_events = self.bot_events.to_dict()

        enabled = self.enabled

        event_source_id = str(self.event_source_id)

        events = []
        for events_item_data in self.events:
            events_item = events_item_data.value
            events.append(events_item)



        routing = self.routing.to_dict()

        trigger_id = str(self.trigger_id)

        type_ = self.type_.value

        allow_shared_channels = self.allow_shared_channels

        filters: dict[str, Any] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "botEvents": bot_events,
            "enabled": enabled,
            "eventSourceId": event_source_id,
            "events": events,
            "routing": routing,
            "triggerId": trigger_id,
            "type": type_,
        })
        if allow_shared_channels is not UNSET:
            field_dict["allowSharedChannels"] = allow_shared_channels
        if filters is not UNSET:
            field_dict["filters"] = filters

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_slack_bot_events import ManagedAgentsAutomationSlackBotEvents # noqa: PLC0415
        from ..models.managed_agents_automation_slack_filters_request import ManagedAgentsAutomationSlackFiltersRequest # noqa: PLC0415
        from ..models.managed_agents_automation_slack_routing import ManagedAgentsAutomationSlackRouting # noqa: PLC0415
        d = dict(src_dict)
        bot_events = ManagedAgentsAutomationSlackBotEvents.from_dict(d.pop("botEvents"))




        enabled = d.pop("enabled")

        event_source_id = UUID(d.pop("eventSourceId"))




        events = []
        _events = d.pop("events")
        for events_item_data in (_events):
            events_item = ManagedAgentsAutomationSlackTriggerRequestEventsItem(events_item_data)



            events.append(events_item)


        routing = ManagedAgentsAutomationSlackRouting.from_dict(d.pop("routing"))




        trigger_id = UUID(d.pop("triggerId"))




        type_ = ManagedAgentsAutomationSlackTriggerRequestType(d.pop("type"))




        allow_shared_channels = d.pop("allowSharedChannels", UNSET)

        _filters = d.pop("filters", UNSET)
        filters: ManagedAgentsAutomationSlackFiltersRequest | Unset
        if isinstance(_filters,  Unset):
            filters = UNSET
        else:
            filters = ManagedAgentsAutomationSlackFiltersRequest.from_dict(_filters)




        managed_agents_automation_slack_trigger_request = cls(
            bot_events=bot_events,
            enabled=enabled,
            event_source_id=event_source_id,
            events=events,
            routing=routing,
            trigger_id=trigger_id,
            type_=type_,
            allow_shared_channels=allow_shared_channels,
            filters=filters,
        )

        return managed_agents_automation_slack_trigger_request

