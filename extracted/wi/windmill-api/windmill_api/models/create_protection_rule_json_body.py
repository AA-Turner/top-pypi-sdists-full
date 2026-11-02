from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_protection_rule_json_body_rules_item import CreateProtectionRuleJsonBodyRulesItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_protection_rule_json_body_fork_role_mapping import CreateProtectionRuleJsonBodyForkRoleMapping


T = TypeVar("T", bound="CreateProtectionRuleJsonBody")


@_attrs_define
class CreateProtectionRuleJsonBody:
    """
    Attributes:
        name (str): Unique name for the protection rule Example: Production Protection.
        rules (List[CreateProtectionRuleJsonBodyRulesItem]): Configuration of protection restrictions
        bypass_groups (List[str]): Groups that can bypass this ruleset
        bypass_users (List[str]): Users that can bypass this ruleset
        fork_role_mapping (Union[Unset, CreateProtectionRuleJsonBodyForkRoleMapping]): Role a member of this workspace
            gets in a fork of it, keyed by the role it holds here. Unmapped roles carry over unchanged; where two rulesets
            map the same role, the first by name wins. On update, omitting it leaves the stored mapping unchanged.
    """

    name: str
    rules: List[CreateProtectionRuleJsonBodyRulesItem]
    bypass_groups: List[str]
    bypass_users: List[str]
    fork_role_mapping: Union[Unset, "CreateProtectionRuleJsonBodyForkRoleMapping"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        rules = []
        for rules_item_data in self.rules:
            rules_item = rules_item_data.value

            rules.append(rules_item)

        bypass_groups = self.bypass_groups

        bypass_users = self.bypass_users

        fork_role_mapping: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fork_role_mapping, Unset):
            fork_role_mapping = self.fork_role_mapping.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "rules": rules,
                "bypass_groups": bypass_groups,
                "bypass_users": bypass_users,
            }
        )
        if fork_role_mapping is not UNSET:
            field_dict["fork_role_mapping"] = fork_role_mapping

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_protection_rule_json_body_fork_role_mapping import (
            CreateProtectionRuleJsonBodyForkRoleMapping,
        )

        d = src_dict.copy()
        name = d.pop("name")

        rules = []
        _rules = d.pop("rules")
        for rules_item_data in _rules:
            rules_item = CreateProtectionRuleJsonBodyRulesItem(rules_item_data)

            rules.append(rules_item)

        bypass_groups = cast(List[str], d.pop("bypass_groups"))

        bypass_users = cast(List[str], d.pop("bypass_users"))

        _fork_role_mapping = d.pop("fork_role_mapping", UNSET)
        fork_role_mapping: Union[Unset, CreateProtectionRuleJsonBodyForkRoleMapping]
        if isinstance(_fork_role_mapping, Unset):
            fork_role_mapping = UNSET
        else:
            fork_role_mapping = CreateProtectionRuleJsonBodyForkRoleMapping.from_dict(_fork_role_mapping)

        create_protection_rule_json_body = cls(
            name=name,
            rules=rules,
            bypass_groups=bypass_groups,
            bypass_users=bypass_users,
            fork_role_mapping=fork_role_mapping,
        )

        create_protection_rule_json_body.additional_properties = d
        return create_protection_rule_json_body

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
