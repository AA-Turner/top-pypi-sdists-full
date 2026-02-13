from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_protection_rule_json_body_rules_item import UpdateProtectionRuleJsonBodyRulesItem

T = TypeVar("T", bound="UpdateProtectionRuleJsonBody")


@_attrs_define
class UpdateProtectionRuleJsonBody:
    """
    Attributes:
        rules (List[UpdateProtectionRuleJsonBodyRulesItem]): Configuration of protection restrictions
        bypass_groups (List[str]): Groups that can bypass this ruleset
        bypass_users (List[str]): Users that can bypass this ruleset
    """

    rules: List[UpdateProtectionRuleJsonBodyRulesItem]
    bypass_groups: List[str]
    bypass_users: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        rules = []
        for rules_item_data in self.rules:
            rules_item = rules_item_data.value

            rules.append(rules_item)

        bypass_groups = self.bypass_groups

        bypass_users = self.bypass_users

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rules": rules,
                "bypass_groups": bypass_groups,
                "bypass_users": bypass_users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        rules = []
        _rules = d.pop("rules")
        for rules_item_data in _rules:
            rules_item = UpdateProtectionRuleJsonBodyRulesItem(rules_item_data)

            rules.append(rules_item)

        bypass_groups = cast(List[str], d.pop("bypass_groups"))

        bypass_users = cast(List[str], d.pop("bypass_users"))

        update_protection_rule_json_body = cls(
            rules=rules,
            bypass_groups=bypass_groups,
            bypass_users=bypass_users,
        )

        update_protection_rule_json_body.additional_properties = d
        return update_protection_rule_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
