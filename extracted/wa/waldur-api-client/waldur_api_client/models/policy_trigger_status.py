from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.policy_gate_enum import PolicyGateEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PolicyTriggerStatus")


@_attrs_define
class PolicyTriggerStatus:
    """
    Attributes:
        gate (Union[Unset, PolicyGateEnum]):
        triggered (Union[Unset, bool]): Whether the policy fires on the current figures. This is the evaluation now;
            has_fired is the stored state of the last evaluation that ran its actions, and the two can differ until the next
            one.
        credit_value_compared (Union[None, Unset, str]): Deprecated: always null. The policy no longer compares the
            credit balance with limit_cost.
    """

    gate: Union[Unset, PolicyGateEnum] = UNSET
    triggered: Union[Unset, bool] = UNSET
    credit_value_compared: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        gate: Union[Unset, str] = UNSET
        if not isinstance(self.gate, Unset):
            gate = self.gate.value

        triggered = self.triggered

        credit_value_compared: Union[None, Unset, str]
        if isinstance(self.credit_value_compared, Unset):
            credit_value_compared = UNSET
        else:
            credit_value_compared = self.credit_value_compared

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if gate is not UNSET:
            field_dict["gate"] = gate
        if triggered is not UNSET:
            field_dict["triggered"] = triggered
        if credit_value_compared is not UNSET:
            field_dict["credit_value_compared"] = credit_value_compared

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _gate = d.pop("gate", UNSET)
        gate: Union[Unset, PolicyGateEnum]
        if isinstance(_gate, Unset):
            gate = UNSET
        else:
            gate = PolicyGateEnum(_gate)

        triggered = d.pop("triggered", UNSET)

        def _parse_credit_value_compared(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        credit_value_compared = _parse_credit_value_compared(d.pop("credit_value_compared", UNSET))

        policy_trigger_status = cls(
            gate=gate,
            triggered=triggered,
            credit_value_compared=credit_value_compared,
        )

        policy_trigger_status.additional_properties = d
        return policy_trigger_status

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
