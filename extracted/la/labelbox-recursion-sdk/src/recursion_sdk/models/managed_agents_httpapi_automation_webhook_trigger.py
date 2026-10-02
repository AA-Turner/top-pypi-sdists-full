from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_httpapi_automation_webhook_trigger_type import ManagedAgentsHttpapiAutomationWebhookTriggerType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.managed_agents_automation_webhook_filters import ManagedAgentsAutomationWebhookFilters





T = TypeVar("T", bound="ManagedAgentsHttpapiAutomationWebhookTrigger")



@_attrs_define
class ManagedAgentsHttpapiAutomationWebhookTrigger:
    """ Closed custom-webhook trigger configuration.

        Example:
            {'enabled': True, 'eventSourceId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'filters': {'fieldEquals': [{'path':
                'example', 'value': 'example'}]}, 'triggerId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'webhook'}

        Attributes:
            enabled (bool): Whether this trigger may admit runs while the automation is active.
            event_source_id (UUID): Compatible custom webhook source.
            trigger_id (UUID): Caller-generated stable trigger identifier.
            type_ (ManagedAgentsHttpapiAutomationWebhookTriggerType): Custom-webhook trigger discriminant.
            filters (ManagedAgentsAutomationWebhookFilters | Unset): Optional conditions on the custom webhook body.
                Example: {'fieldEquals': [{'path': 'example', 'value': 'example'}]}.
     """

    enabled: bool
    event_source_id: UUID
    trigger_id: UUID
    type_: ManagedAgentsHttpapiAutomationWebhookTriggerType
    filters: ManagedAgentsAutomationWebhookFilters | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_webhook_filters import ManagedAgentsAutomationWebhookFilters # noqa: PLC0415
        enabled = self.enabled

        event_source_id = str(self.event_source_id)

        trigger_id = str(self.trigger_id)

        type_ = self.type_.value

        filters: dict[str, Any] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "enabled": enabled,
            "eventSourceId": event_source_id,
            "triggerId": trigger_id,
            "type": type_,
        })
        if filters is not UNSET:
            field_dict["filters"] = filters

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_webhook_filters import ManagedAgentsAutomationWebhookFilters # noqa: PLC0415
        d = dict(src_dict)
        enabled = d.pop("enabled")

        event_source_id = UUID(d.pop("eventSourceId"))




        trigger_id = UUID(d.pop("triggerId"))




        type_ = ManagedAgentsHttpapiAutomationWebhookTriggerType(d.pop("type"))




        _filters = d.pop("filters", UNSET)
        filters: ManagedAgentsAutomationWebhookFilters | Unset
        if isinstance(_filters,  Unset):
            filters = UNSET
        else:
            filters = ManagedAgentsAutomationWebhookFilters.from_dict(_filters)




        managed_agents_httpapi_automation_webhook_trigger = cls(
            enabled=enabled,
            event_source_id=event_source_id,
            trigger_id=trigger_id,
            type_=type_,
            filters=filters,
        )

        return managed_agents_httpapi_automation_webhook_trigger

