from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_webhook_match_condition_operator import ManagedAgentsWebhookMatchConditionOperator
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_webhook_value_selector import ManagedAgentsWebhookValueSelector





T = TypeVar("T", bound="ManagedAgentsWebhookMatchCondition")



@_attrs_define
class ManagedAgentsWebhookMatchCondition:
    """ One provider-neutral condition evaluated against a verified webhook delivery.

        Example:
            {'operator': 'equals', 'selector': {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value':
                'example', 'values': ['example']}

        Attributes:
            operator (ManagedAgentsWebhookMatchConditionOperator): Comparison applied to the selected value.
            selector (ManagedAgentsWebhookValueSelector): Selects one value from a verified webhook delivery body or
                headers. Example: {'body_pointer': 'example', 'header': 'example', 'source': 'body'}.
            value (str | Unset): Expected value for the equals operator.
            values (list[str] | Unset): Accepted values for the one_of operator.
     """

    operator: ManagedAgentsWebhookMatchConditionOperator
    selector: ManagedAgentsWebhookValueSelector
    value: str | Unset = UNSET
    values: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_webhook_value_selector import ManagedAgentsWebhookValueSelector # noqa: PLC0415
        operator = self.operator.value

        selector = self.selector.to_dict()

        value = self.value

        values: list[str] | Unset = UNSET
        if not isinstance(self.values, Unset):
            values = self.values




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "operator": operator,
            "selector": selector,
        })
        if value is not UNSET:
            field_dict["value"] = value
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_webhook_value_selector import ManagedAgentsWebhookValueSelector # noqa: PLC0415
        d = dict(src_dict)
        operator = ManagedAgentsWebhookMatchConditionOperator(d.pop("operator"))




        selector = ManagedAgentsWebhookValueSelector.from_dict(d.pop("selector"))




        value = d.pop("value", UNSET)

        values = cast(list[str], d.pop("values", UNSET))


        managed_agents_webhook_match_condition = cls(
            operator=operator,
            selector=selector,
            value=value,
            values=values,
        )


        managed_agents_webhook_match_condition.additional_properties = d
        return managed_agents_webhook_match_condition

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
