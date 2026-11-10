from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patched_rancher_ingress_request_rules import PatchedRancherIngressRequestRules


T = TypeVar("T", bound="PatchedRancherIngressRequest")


@_attrs_define
class PatchedRancherIngressRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        rules (Union[Unset, PatchedRancherIngressRequestRules]):
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    rules: Union[Unset, "PatchedRancherIngressRequestRules"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        rules: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.rules, Unset):
            rules = self.rules.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if rules is not UNSET:
            field_dict["rules"] = rules

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.patched_rancher_ingress_request_rules import PatchedRancherIngressRequestRules

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _rules = d.pop("rules", UNSET)
        rules: Union[Unset, PatchedRancherIngressRequestRules]
        if isinstance(_rules, Unset):
            rules = UNSET
        else:
            rules = PatchedRancherIngressRequestRules.from_dict(_rules)

        patched_rancher_ingress_request = cls(
            name=name,
            description=description,
            rules=rules,
        )

        patched_rancher_ingress_request.additional_properties = d
        return patched_rancher_ingress_request

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
