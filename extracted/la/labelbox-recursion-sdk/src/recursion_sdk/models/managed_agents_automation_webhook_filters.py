from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_automation_webhook_field_condition import ManagedAgentsAutomationWebhookFieldCondition





T = TypeVar("T", bound="ManagedAgentsAutomationWebhookFilters")



@_attrs_define
class ManagedAgentsAutomationWebhookFilters:
    """ Optional conditions on the custom webhook body.

        Example:
            {'fieldEquals': [{'path': 'example', 'value': 'example'}]}

        Attributes:
            field_equals (list[ManagedAgentsAutomationWebhookFieldCondition]): Conditions that must all hold.
     """

    field_equals: list[ManagedAgentsAutomationWebhookFieldCondition]





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_webhook_field_condition import ManagedAgentsAutomationWebhookFieldCondition # noqa: PLC0415
        field_equals = []
        for field_equals_item_data in self.field_equals:
            field_equals_item = field_equals_item_data.to_dict()
            field_equals.append(field_equals_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "fieldEquals": field_equals,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_webhook_field_condition import ManagedAgentsAutomationWebhookFieldCondition # noqa: PLC0415
        d = dict(src_dict)
        field_equals = []
        _field_equals = d.pop("fieldEquals")
        for field_equals_item_data in (_field_equals):
            field_equals_item = ManagedAgentsAutomationWebhookFieldCondition.from_dict(field_equals_item_data)



            field_equals.append(field_equals_item)


        managed_agents_automation_webhook_filters = cls(
            field_equals=field_equals,
        )

        return managed_agents_automation_webhook_filters

