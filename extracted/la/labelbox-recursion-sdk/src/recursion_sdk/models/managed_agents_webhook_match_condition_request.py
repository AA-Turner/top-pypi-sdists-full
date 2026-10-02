from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_webhook_match_condition_request_operator import ManagedAgentsWebhookMatchConditionRequestOperator
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_webhook_value_selector_request import ManagedAgentsWebhookValueSelectorRequest





T = TypeVar("T", bound="ManagedAgentsWebhookMatchConditionRequest")



@_attrs_define
class ManagedAgentsWebhookMatchConditionRequest:
    """ One provider-neutral condition evaluated against a verified webhook delivery.

        Example:
            {'operator': 'equals', 'selector': {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value':
                'example', 'values': ['example']}

        Attributes:
            operator (ManagedAgentsWebhookMatchConditionRequestOperator | Unset): Comparison applied to the selected value.
            selector (ManagedAgentsWebhookValueSelectorRequest | Unset): Selects one value from a verified webhook delivery
                body or headers. Example: {'body_pointer': 'example', 'header': 'example', 'source': 'body'}.
            value (str | Unset): Expected value for the equals operator.
            values (list[str] | Unset): Accepted values for the one_of operator.
     """

    operator: ManagedAgentsWebhookMatchConditionRequestOperator | Unset = UNSET
    selector: ManagedAgentsWebhookValueSelectorRequest | Unset = UNSET
    value: str | Unset = UNSET
    values: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_webhook_value_selector_request import ManagedAgentsWebhookValueSelectorRequest # noqa: PLC0415
        operator: str | Unset = UNSET
        if not isinstance(self.operator, Unset):
            operator = self.operator.value


        selector: dict[str, Any] | Unset = UNSET
        if not isinstance(self.selector, Unset):
            selector = self.selector.to_dict()

        value = self.value

        values: list[str] | Unset = UNSET
        if not isinstance(self.values, Unset):
            values = self.values




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if operator is not UNSET:
            field_dict["operator"] = operator
        if selector is not UNSET:
            field_dict["selector"] = selector
        if value is not UNSET:
            field_dict["value"] = value
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_webhook_value_selector_request import ManagedAgentsWebhookValueSelectorRequest # noqa: PLC0415
        d = dict(src_dict)
        _operator = d.pop("operator", UNSET)
        operator: ManagedAgentsWebhookMatchConditionRequestOperator | Unset
        if isinstance(_operator,  Unset):
            operator = UNSET
        else:
            operator = ManagedAgentsWebhookMatchConditionRequestOperator(_operator)




        _selector = d.pop("selector", UNSET)
        selector: ManagedAgentsWebhookValueSelectorRequest | Unset
        if isinstance(_selector,  Unset):
            selector = UNSET
        else:
            selector = ManagedAgentsWebhookValueSelectorRequest.from_dict(_selector)




        value = d.pop("value", UNSET)

        values = cast(list[str], d.pop("values", UNSET))


        managed_agents_webhook_match_condition_request = cls(
            operator=operator,
            selector=selector,
            value=value,
            values=values,
        )


        managed_agents_webhook_match_condition_request.additional_properties = d
        return managed_agents_webhook_match_condition_request

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
