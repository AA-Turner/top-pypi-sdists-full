from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsAutomationWebhookFieldCondition")



@_attrs_define
class ManagedAgentsAutomationWebhookFieldCondition:
    """ One equality condition on a custom webhook body.

        Example:
            {'path': 'example', 'value': 'example'}

        Attributes:
            path (str): Dot-separated path into the JSON body, such as data.level. Decimal segments index arrays.
            value (str): Expected scalar written as JSON text without quotes: a string as-is, a number, true, false, or
                null.
     """

    path: str
    value: str





    def to_dict(self) -> dict[str, Any]:
        path = self.path

        value = self.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "path": path,
            "value": value,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        value = d.pop("value")

        managed_agents_automation_webhook_field_condition = cls(
            path=path,
            value=value,
        )

        return managed_agents_automation_webhook_field_condition

