from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_webhook_event_source_delivery_summary_kind import ManagedAgentsWebhookEventSourceDeliverySummaryKind






T = TypeVar("T", bound="ManagedAgentsWebhookEventSourceDeliverySummary")



@_attrs_define
class ManagedAgentsWebhookEventSourceDeliverySummary:
    """ Customer webhook delivery without verification configuration.

        Example:
            {'kind': 'webhook', 'webhookUrl': 'example'}

        Attributes:
            kind (ManagedAgentsWebhookEventSourceDeliverySummaryKind): Customer-configured webhook delivery.
            webhook_url (str): Relative public endpoint to configure at the event provider.
     """

    kind: ManagedAgentsWebhookEventSourceDeliverySummaryKind
    webhook_url: str





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        webhook_url = self.webhook_url


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "webhookUrl": webhook_url,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = ManagedAgentsWebhookEventSourceDeliverySummaryKind(d.pop("kind"))




        webhook_url = d.pop("webhookUrl")

        managed_agents_webhook_event_source_delivery_summary = cls(
            kind=kind,
            webhook_url=webhook_url,
        )

        return managed_agents_webhook_event_source_delivery_summary

