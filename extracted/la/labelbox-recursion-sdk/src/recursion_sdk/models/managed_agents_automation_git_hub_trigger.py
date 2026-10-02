from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_git_hub_trigger_type import ManagedAgentsAutomationGitHubTriggerType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.managed_agents_automation_git_hub_filters import ManagedAgentsAutomationGitHubFilters





T = TypeVar("T", bound="ManagedAgentsAutomationGitHubTrigger")



@_attrs_define
class ManagedAgentsAutomationGitHubTrigger:
    """ Closed GitHub webhook trigger configuration.

        Example:
            {'enabled': True, 'eventSourceId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'events': ['example'], 'filters':
                {'actions': ['example'], 'addedLabels': ['example'], 'baseBranches': ['example'], 'branches': ['example'],
                'commentOn': 'pull_request', 'conclusions': ['example'], 'excludeDrafts': True, 'ignoreBots': True, 'labelsAny':
                ['example'], 'labelsNone': ['example'], 'merged': True, 'repositories': ['example'], 'reviewStates':
                ['example'], 'senders': ['example'], 'textContains': ['example'], 'textExcludes': ['example'], 'textMatches':
                'example'}, 'triggerId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'github'}

        Attributes:
            enabled (bool): Whether this trigger may admit runs while the automation is active.
            event_source_id (UUID): Compatible GitHub webhook source.
            events (list[str]): GitHub webhook event names that may match this trigger.
            trigger_id (UUID): Caller-generated stable trigger identifier.
            type_ (ManagedAgentsAutomationGitHubTriggerType): GitHub trigger discriminant.
            filters (ManagedAgentsAutomationGitHubFilters | Unset): Optional conditions on the verified GitHub delivery
                body. Every present condition must match; empty lists accept any value. Example: {'actions': ['example'],
                'addedLabels': ['example'], 'baseBranches': ['example'], 'branches': ['example'], 'commentOn': 'pull_request',
                'conclusions': ['example'], 'excludeDrafts': True, 'ignoreBots': True, 'labelsAny': ['example'], 'labelsNone':
                ['example'], 'merged': True, 'repositories': ['example'], 'reviewStates': ['example'], 'senders': ['example'],
                'textContains': ['example'], 'textExcludes': ['example'], 'textMatches': 'example'}.
     """

    enabled: bool
    event_source_id: UUID
    events: list[str]
    trigger_id: UUID
    type_: ManagedAgentsAutomationGitHubTriggerType
    filters: ManagedAgentsAutomationGitHubFilters | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_git_hub_filters import ManagedAgentsAutomationGitHubFilters # noqa: PLC0415
        enabled = self.enabled

        event_source_id = str(self.event_source_id)

        events = self.events



        trigger_id = str(self.trigger_id)

        type_ = self.type_.value

        filters: dict[str, Any] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "enabled": enabled,
            "eventSourceId": event_source_id,
            "events": events,
            "triggerId": trigger_id,
            "type": type_,
        })
        if filters is not UNSET:
            field_dict["filters"] = filters

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_git_hub_filters import ManagedAgentsAutomationGitHubFilters # noqa: PLC0415
        d = dict(src_dict)
        enabled = d.pop("enabled")

        event_source_id = UUID(d.pop("eventSourceId"))




        events = cast(list[str], d.pop("events"))


        trigger_id = UUID(d.pop("triggerId"))




        type_ = ManagedAgentsAutomationGitHubTriggerType(d.pop("type"))




        _filters = d.pop("filters", UNSET)
        filters: ManagedAgentsAutomationGitHubFilters | Unset
        if isinstance(_filters,  Unset):
            filters = UNSET
        else:
            filters = ManagedAgentsAutomationGitHubFilters.from_dict(_filters)




        managed_agents_automation_git_hub_trigger = cls(
            enabled=enabled,
            event_source_id=event_source_id,
            events=events,
            trigger_id=trigger_id,
            type_=type_,
            filters=filters,
        )

        return managed_agents_automation_git_hub_trigger

