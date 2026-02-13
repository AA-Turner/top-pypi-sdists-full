from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_protection_rules_response_200_item_rules_item import ListProtectionRulesResponse200ItemRulesItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListProtectionRulesResponse200Item")


@_attrs_define
class ListProtectionRulesResponse200Item:
    """A workspace protection rule defining restrictions and bypass permissions

    Attributes:
        name (str): Unique name for the protection rule Example: Production Protection.
        rules (List[ListProtectionRulesResponse200ItemRulesItem]): Configuration of protection restrictions
        bypass_groups (List[str]): Groups that can bypass this ruleset
        bypass_users (List[str]): Users that can bypass this ruleset
        workspace_id (Union[Unset, str]):
    """

    name: str
    rules: List[ListProtectionRulesResponse200ItemRulesItem]
    bypass_groups: List[str]
    bypass_users: List[str]
    workspace_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        rules = []
        for rules_item_data in self.rules:
            rules_item = rules_item_data.value

            rules.append(rules_item)

        bypass_groups = self.bypass_groups

        bypass_users = self.bypass_users

        workspace_id = self.workspace_id

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
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        rules = []
        _rules = d.pop("rules")
        for rules_item_data in _rules:
            rules_item = ListProtectionRulesResponse200ItemRulesItem(rules_item_data)

            rules.append(rules_item)

        bypass_groups = cast(List[str], d.pop("bypass_groups"))

        bypass_users = cast(List[str], d.pop("bypass_users"))

        workspace_id = d.pop("workspace_id", UNSET)

        list_protection_rules_response_200_item = cls(
            name=name,
            rules=rules,
            bypass_groups=bypass_groups,
            bypass_users=bypass_users,
            workspace_id=workspace_id,
        )

        list_protection_rules_response_200_item.additional_properties = d
        return list_protection_rules_response_200_item

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
