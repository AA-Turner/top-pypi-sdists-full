from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.flag_rule_logic import FlagRuleLogic


T = TypeVar("T", bound="FlagRule")


@_attrs_define
class FlagRule:
    """A targeting rule that overrides the default within an environment.

    Attributes:
        logic (FlagRuleLogic): JSON Logic expression evaluated against the evaluation context. The rule fires when the
            expression is truthy.
        value (Any): Value returned when the rule fires. Must reference a value from the flag's `values` array
            (constrained flags) or match the flag's `type` (unconstrained flags).
        description (None | str | Unset): Human-readable description of the rule.
    """

    logic: FlagRuleLogic
    value: Any
    description: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        logic = self.logic.to_dict()

        value = self.value

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "logic": logic,
                "value": value,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.flag_rule_logic import FlagRuleLogic

        d = dict(src_dict)
        logic = FlagRuleLogic.from_dict(d.pop("logic"))

        value = d.pop("value")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        flag_rule = cls(
            logic=logic,
            value=value,
            description=description,
        )

        flag_rule.additional_properties = d
        return flag_rule

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
