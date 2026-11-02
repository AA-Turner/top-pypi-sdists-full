from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListProtectionRulesResponse200ItemForkRoleMapping")


@_attrs_define
class ListProtectionRulesResponse200ItemForkRoleMapping:
    """Role a member of this workspace gets in a fork of it, keyed by the role it holds here. Unmapped roles carry over
    unchanged; where two rulesets map the same role, the first by name wins. On update, omitting it leaves the stored
    mapping unchanged.

    """

    additional_properties: Dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        list_protection_rules_response_200_item_fork_role_mapping = cls()

        list_protection_rules_response_200_item_fork_role_mapping.additional_properties = d
        return list_protection_rules_response_200_item_fork_role_mapping

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
