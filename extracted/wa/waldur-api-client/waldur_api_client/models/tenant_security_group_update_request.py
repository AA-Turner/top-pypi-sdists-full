from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_stack_security_group_rule_update_by_name_request import (
        OpenStackSecurityGroupRuleUpdateByNameRequest,
    )


T = TypeVar("T", bound="TenantSecurityGroupUpdateRequest")


@_attrs_define
class TenantSecurityGroupUpdateRequest:
    """
    Attributes:
        name (str):
        uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        rules (Union[Unset, list['OpenStackSecurityGroupRuleUpdateByNameRequest']]):
    """

    name: str
    uuid: Union[Unset, UUID] = UNSET
    description: Union[Unset, str] = UNSET
    rules: Union[Unset, list["OpenStackSecurityGroupRuleUpdateByNameRequest"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        description = self.description

        rules: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.rules, Unset):
            rules = []
            for rules_item_data in self.rules:
                rules_item = rules_item_data.to_dict()
                rules.append(rules_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if description is not UNSET:
            field_dict["description"] = description
        if rules is not UNSET:
            field_dict["rules"] = rules

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_stack_security_group_rule_update_by_name_request import (
            OpenStackSecurityGroupRuleUpdateByNameRequest,
        )

        d = dict(src_dict)
        name = d.pop("name")

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        description = d.pop("description", UNSET)

        rules = []
        _rules = d.pop("rules", UNSET)
        for rules_item_data in _rules or []:
            rules_item = OpenStackSecurityGroupRuleUpdateByNameRequest.from_dict(rules_item_data)

            rules.append(rules_item)

        tenant_security_group_update_request = cls(
            name=name,
            uuid=uuid,
            description=description,
            rules=rules,
        )

        tenant_security_group_update_request.additional_properties = d
        return tenant_security_group_update_request

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
